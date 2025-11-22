"""Agent nodes for the LangGraph workflow."""

import json
import base64
from pathlib import Path
from typing import TypedDict, List, Dict, Any
from PIL import Image
import io
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from config import LMSTUDIO_BASE_URL, MODEL_NAME, SYSTEM_PROMPT, TARGET_CONDITIONS


class State(TypedDict):
    """State for the agent workflow."""
    image_path: str
    image_name: str
    image_data: bytes
    prediction: Dict[str, str]
    ground_truth: Dict[str, float]
    evaluation: Dict[str, bool]
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
            
            # Check if file exists
            if not Path(image_path).exists():
                state["error"] = f"File not found: {image_path}"
                return state
            
            with open(image_path, "rb") as f:
                state["image_data"] = f.read()
            state["image_name"] = Path(image_path).stem
        except FileNotFoundError:
            state["error"] = f"File not found: {state['image_path']}"
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
                            "text": "Analyze this chest X-ray image and determine if Pneumonia, Atelectasis, or Fracture are present. Provide your findings in JSON format."
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
            image_path = state["image_path"]
            prediction = state["prediction"]
            
            # Get ground truth - match by Path column
            row = self.ground_truth_df[self.ground_truth_df['Path'] == image_path]
            if row.empty:
                state["error"] = f"No ground truth found for {image_path}"
                return state
            
            # Extract ground truth for target conditions
            ground_truth = {}
            for condition in TARGET_CONDITIONS:
                if condition in row.columns:
                    ground_truth[condition] = row[condition].values[0]
                else:
                    ground_truth[condition] = 0.0
            
            state["ground_truth"] = ground_truth
            
            # Evaluate each condition
            evaluation = {}
            for condition in TARGET_CONDITIONS:
                pred_value = prediction.get(condition, "Absent")
                true_value = ground_truth.get(condition, 0.0)
                
                # Convert prediction to binary (Present=1, Absent=0)
                pred_binary = 1.0 if pred_value == "Present" else 0.0
                
                # Check if prediction matches ground truth
                evaluation[condition] = (pred_binary == true_value)
            
            state["evaluation"] = evaluation
            
        except Exception as e:
            state["error"] = f"Evaluator error: {str(e)}"
        
        return state


class OutputHandler:
    """Handles output and result storage."""
    
    @staticmethod
    def process(state: State) -> State:
        """Store results."""
        return state
