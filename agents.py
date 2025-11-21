"""Agent nodes for the LangGraph workflow."""

import json
import base64
from pathlib import Path
from typing import TypedDict, List, Dict, Any
from PIL import Image
import io
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from config import LMSTUDIO_BASE_URL, MODEL_NAME, SYSTEM_PROMPT, CATEGORIES


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
        self.llm = ChatOpenAI(
            base_url=LMSTUDIO_BASE_URL,
            api_key="lm-studio",
            model=MODEL_NAME,
            temperature=0.1
        )
    
    def process(self, state: State) -> State:
        """Process image with multimodal LLM."""
        if state.get("error"):
            return state
        
        try:
            # Encode image
            base64_image = base64.b64encode(state["image_data"]).decode('utf-8')
            
            # Create message with image
            messages = [
                SystemMessage(content=SYSTEM_PROMPT),
                HumanMessage(
                    content=[
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        },
                        {
                            "type": "text",
                            "text": "Analyze this dermatology image and provide your top 3 predictions in JSON format."
                        }
                    ]
                )
            ]
            
            response = self.llm.invoke(messages)
            
            # Parse response
            content = response.content
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
