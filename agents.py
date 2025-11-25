"""Agent nodes for the LangGraph workflow."""

import json
import base64
import os
from pathlib import Path
from typing import TypedDict, List, Dict, Any
from PIL import Image
import io
from dotenv import load_dotenv
import google.generativeai as genai
from config import MODEL_NAME, SYSTEM_PROMPT, CATEGORIES

# Load environment variables
load_dotenv()


class State(TypedDict):
    """State for the agent workflow."""
    image_path: str
    image_name: str
    image_data: bytes
    prediction: Dict[str, str]
    ground_truth: str
    is_correct: bool
    error: str


def encode_image(image_path: str) -> str:
    """Encode image to base64."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


class InputHandler:
    """Handles input image loading and preprocessing."""
    
    @staticmethod
    def process(state: State) -> State:
        """Load and preprocess the image."""
        try:
            image_path = state["image_path"]
            with open(image_path, "rb") as f:
                state["image_data"] = f.read()
            state["image_name"] = Path(image_path).stem
        except Exception as e:
            state["error"] = f"Input handler error: {str(e)}"
        return state


class MultimodalProcessor:
    """Processes images using multimodal LLM."""
    
    def __init__(self):
        # Configure Gemini API
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        genai.configure(api_key=api_key)
        
        # Initialize model
        self.model = genai.GenerativeModel(
            model_name=MODEL_NAME,
            generation_config={
                "temperature": 0.1,
                "top_p": 0.95,
                "top_k": 40,
                "max_output_tokens": 1024,
            }
        )
    
    def process(self, state: State) -> State:
        """Process image with multimodal LLM."""
        if state.get("error"):
            return state
        
        try:
            # Load image from bytes
            image = Image.open(io.BytesIO(state["image_data"]))
            
            # Create prompt with system instructions
            prompt = f"""{SYSTEM_PROMPT}

Analyze this dermatology image and provide your top 3 predictions in JSON format."""
            
            # Generate response
            response = self.model.generate_content([prompt, image])
            
            # Parse response
            content = response.text
            # Extract JSON from response
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()
            
            prediction = json.loads(content)
            state["prediction"] = prediction
            
        except Exception as e:
            state["error"] = f"Processor error: {str(e)}"
        
        return state


class Predictor:
    """Makes predictions using the multimodal model."""
    
    def __init__(self):
        self.processor = MultimodalProcessor()
    
    def process(self, state: State) -> State:
        """Generate prediction."""
        return self.processor.process(state)


class ResultEvaluator:
    """Evaluates predictions against ground truth."""
    
    def __init__(self, ground_truth_df):
        self.ground_truth_df = ground_truth_df
    
    def process(self, state: State) -> State:
        """Evaluate prediction accuracy."""
        if state.get("error"):
            return state
        
        try:
            image_name = state["image_name"]
            prediction = state["prediction"]
            
            # Get ground truth
            row = self.ground_truth_df[self.ground_truth_df['image'] == image_name]
            if row.empty:
                state["error"] = f"No ground truth found for {image_name}"
                return state
            
            # Find true label
            true_label = None
            for col in CATEGORIES.keys():
                if row[col].values[0] == 1.0:
                    true_label = col
                    break
            
            state["ground_truth"] = true_label
            
            # Check if prediction is correct (any of top 3 matches)
            predicted_labels = [
                prediction.get("top_1"),
                prediction.get("top_2"),
                prediction.get("top_3")
            ]
            
            state["is_correct"] = true_label in predicted_labels
            
        except Exception as e:
            state["error"] = f"Evaluator error: {str(e)}"
        
        return state


class OutputHandler:
    """Handles output and result storage."""
    
    @staticmethod
    def process(state: State) -> State:
        """Store results."""
        return state
