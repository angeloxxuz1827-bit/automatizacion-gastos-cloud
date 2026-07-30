


from pathlib import Path

PROMPTS_DIR = Path(__file__).parent

with open(
    PROMPTS_DIR / "system_prompt_structure_data.txt",
    "r",
    encoding="utf-8"
) as f:
    system_prompt_structure_data = f.read()
