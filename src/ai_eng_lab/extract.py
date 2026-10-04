from openai import OpenAI
from pydantic import BaseModel, Field, ValidationError

from ai_eng_lab.llm import get_client


class JobPosting(BaseModel):
    title: str = Field(description="Chức danh công việc")
    company: str | None = Field(default=None, description="Tên công ty nếu có")
    skills: list[str] = Field(
        default_factory=list,
        description=(
            "Tất cả kỹ năng, công nghệ, công cụ được nhắc tới trong yêu cầu hoặc mô tả "
            "(ví dụ Python, Docker, RAG). Chỉ để rỗng nếu văn bản hoàn toàn không nhắc tới."
        ),
    )
    experience_years: int | None = Field(
        default=None, description="Số năm kinh nghiệm tối thiểu; null nếu không nêu"
    )


SYSTEM_PROMPT = (
    "Bạn là bộ trích xuất thông tin tuyển dụng. Trả về duy nhất JSON hợp lệ "
    "theo schema, không kèm markdown hay giải thích. title phải là tên chức danh "
    "ngắn gọn của vị trí. skills chỉ gồm các công nghệ, công cụ, framework, "
    "ngôn ngữ và nền tảng được nêu rõ trong JD; không thêm kỹ năng suy đoán. "
    "Liệt kê đầy đủ và không lặp lại. Với các trường khác, nếu văn bản không "
    "nói thì để null. Không bịa thông tin."
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
                {
                    "role": "user",
                    "content": (
                        "Trích xuất title và skills từ JD sau. Với skills, "
                        "liệt kê mỗi kỹ năng một phần tử.\n\n"
                        f"JD:\n{text}"
                    ),
                },
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
