import re
import unicodedata


def slugify(text: str) -> str:
    normalized_text = unicodedata.normalize("NFKD", text)
    without_accents = "".join(
        character
        for character in normalized_text
        if not unicodedata.combining(character)
    )
    return re.sub(r"[^\w]+", "-", without_accents.lower(), flags=re.UNICODE).strip("-")


def main() -> None:
    print("Hello from ai-eng-lab!")
