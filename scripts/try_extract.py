from ai_eng_lab.extract import JobPosting, extract

text = """Tuyển AI Engineer tại công ty ABC.
Yêu cầu: Python, FastAPI, Docker; ít nhất 2 năm kinh nghiệm; biết RAG là lợi thế."""

print(extract(text, JobPosting).model_dump_json(indent=2))
