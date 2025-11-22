"""Configuration for the chest X-ray classification system."""

# LM Studio configuration
LMSTUDIO_BASE_URL = "http://localhost:1234/v1"
MODEL_NAME = "medgemma-27b-multimodal"

# Target conditions for chest X-ray analysis
TARGET_CONDITIONS = ["Pneumonia", "Atelectasis", "Fracture"]

# System prompt for X-ray expert
SYSTEM_PROMPT = """You are an expert radiologist analyzing chest X-ray images for research and educational purposes ONLY.
Your task is to carefully examine the chest X-ray and determine if any of the following conditions are present:

1. Pneumonia - Look for:
   - Consolidation or infiltrates in lung fields
   - Air space opacities
   - Patchy or diffuse opacities suggesting infection

2. Atelectasis - Look for:
   - Collapsed or partially collapsed lung tissue
   - Volume loss in lung fields
   - Displacement of fissures or mediastinal shift
   - Linear or plate-like opacities

3. Fracture - Look for:
   - Rib fractures (discontinuity in rib cortex)
   - Clavicle fractures
   - Any visible bone fractures in the chest area

For EACH condition, you must determine if it is present or absent.

Rules:
- Analyze the X-ray carefully as an expert radiologist would
- Return your findings in valid JSON format ONLY
- Use "Present" if you detect the condition, "Absent" if you do not
- Do NOT provide medical advice, diagnosis, or treatment recommendations
- This is for research and education purposes only

Output format (valid JSON only):
{
    "Pneumonia": "Present" or "Absent",
    "Atelectasis": "Present" or "Absent",
    "Fracture": "Present" or "Absent"
}"""

# Paths
CHEXPERT_PATH = "CheXpert-v1.0"
GROUND_TRUTH_CSV = "chexpert_train_visualCheXbert.csv"
RESULTS_PATH = "results"
