from openai import OpenAI
from pydantic import BaseModel, Field, ValidationError

from ai_eng_lab.llm import get_client


class JobPosting(BaseModel):
    title: str
    company: str | None = None
    skills: list[str] = Field(default_factory=list)
    experience_years: int | None = None


SYSTEM_PROMPT = (
    "Trích xuất thông tin từ văn bản theo đúng schema. "
    "Không bịa thông tin; nếu không có thì để null hoặc danh sách rỗng."
)


def extract[T: BaseModel](
    text: str,
    schema: type[T],
    model: str = "qwen3:8b",
    client: OpenAI | None = None,
    max_retries: int = 2,
) -> T:
    client = client or get_client()
    last_error: ValidationError | None = None
    for _ in range(max_retries + 1):
        resp = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": text},
            ],
            temperature=0,
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": schema.__name__,
                    "schema": schema.model_json_schema(),
                },
            },
        )
        raw = resp.choices[0].message.content or ""
        try:
            return schema.model_validate_json(raw)
        except ValidationError as err:
            last_error = err
    raise ValueError(
        f"Không parse được output sau {max_retries + 1} lần"
    ) from last_error
