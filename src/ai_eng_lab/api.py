from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from openai import OpenAI
from pydantic import BaseModel, Field

from ai_eng_lab.extract import JobPosting, extract
from ai_eng_lab.llm import get_client

app = FastAPI(
    title="AI Engineer JD Extractor",
    description="Extract structured job-posting fields from a job description.",
    version="0.1.0",
)


class ExtractRequest(BaseModel):
    text: str = Field(min_length=1, description="Nội dung JD cần trích xuất")
    model: str = Field(default="qwen3:8b", min_length=1)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/extract", response_model=JobPosting)
def extract_job_posting(
    request: ExtractRequest,
    client: Annotated[OpenAI, Depends(get_client)],
) -> JobPosting:
    try:
        return extract(
            request.text,
            JobPosting,
            model=request.model,
            client=client,
        )
    except ValueError as error:
        raise HTTPException(
            status_code=502,
            detail=f"Model không trả về JD hợp lệ: {error}",
        ) from error
