from pathlib import Path


PROMPT_PATH = Path(__file__).resolve().parent / "prompt.txt"


def load_prompt_template() -> str:
    return PROMPT_PATH.read_text(encoding="utf-8")


def build_prompt(
    knowledge_base: str,
    number: str,
    short_description: str,
    description: str,
    priority: int,
) -> str:
    prompt = load_prompt_template()

    replacements = {
        "{{KNOWLEDGE_BASE}}": knowledge_base,
        "{{NUMBER}}": number,
        "{{SHORT_DESCRIPTION}}": short_description,
        "{{DESCRIPTION}}": description,
        "{{PRIORITY}}": str(priority),
    }

    for placeholder, value in replacements.items():
        prompt = prompt.replace(placeholder, value)

    return prompt