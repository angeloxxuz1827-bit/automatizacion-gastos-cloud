from pathlib import Path

# Directory containing the prompt template files.
PROMPTS_DIR = Path(__file__).parent

# Load the system prompt used to instruct the LLM for structured
# data extraction. The prompt is read once at module import time
# and reused throughout the application's lifecycle.
with open(
    PROMPTS_DIR / "system_prompt_structure_data.txt",
    "r",
    encoding="utf-8"
) as f:
    system_prompt_structure_data = f.read()