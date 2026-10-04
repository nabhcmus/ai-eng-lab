curl -X POST http://127.0.0.1:8000/extract ^
  -H "Content-Type: application/json" ^
  -d "{\"text\":\"Senior AI Engineer cần Python, PyTorch và Docker\"}"# ai-eng-lab

Một dự án Python tối giản để thực hành quy trình phát triển có kiểm tra tự động. Dự án sử dụng [uv](https://docs.astral.sh/uv/) để quản lý môi trường và phụ thuộc, [Ruff](https://docs.astral.sh/ruff/) để format/lint, và `pytest` để chạy test.

## Yêu cầu

- Python 3.14 trở lên
- `uv` phiên bản mới

Kiểm tra các công cụ đã được cài:

```bash
python --version
uv --version
```

## Bắt đầu

1. Clone repository và đi vào thư mục dự án:

	```bash
	git clone <URL_REPOSITORY>
	cd ai-eng-lab
	```

2. Đồng bộ môi trường:

	```bash
	uv sync --dev
	```

	Lệnh này tạo hoặc cập nhật môi trường ảo `.venv`, cài dự án và các phụ thuộc trong nhóm `dev` như `pytest` và `ruff`. File `uv.lock` giúp các máy cài cùng phiên bản phụ thuộc.

3. Chạy chương trình mẫu:

	```bash
	uv run ai-eng-lab
	```

## Kiểm tra chất lượng mã

Chạy format tự động, sửa lỗi lint có thể tự sửa, sau đó chạy test:

```bash
uv run ruff format .
uv run ruff check . --fix
uv run pytest
```

## Đánh giá trích xuất JD

Bộ eval đầu tiên nằm trong [`tests/data/jd_samples.json`](tests/data/jd_samples.json),
gồm 5 JD AI Engineer được gán nhãn thủ công cho `title` và `skills`. Chạy evaluator
với model cục bộ đang cấu hình:

```bash
uv run python scripts/eval_jd.py
```

Script in JSON report với tỷ lệ đúng riêng cho từng trường. `title` được so sánh
không phân biệt hoa thường và khoảng trắng; `skills` được so sánh như một tập hợp
không phân biệt hoa thường, nhưng phải khớp đầy đủ (không thiếu hoặc thừa kỹ năng).

## API

Khởi động API bằng FastAPI và Uvicorn:

```bash
uv run uvicorn ai_eng_lab.api:app --reload
```

Kiểm tra health:

```bash
curl http://127.0.0.1:8000/health
```

Trích xuất JD:

```bash
curl -X POST http://127.0.0.1:8000/extract ^
  -H "Content-Type: application/json" ^
  -d "{\"text\":\"Senior AI Engineer cần Python, PyTorch và Docker\"}"
```

API docs tương tác có sẵn tại `http://127.0.0.1:8000/docs`. Endpoint `POST /extract`
trả về `JobPosting`; request bắt buộc có `text` và tùy chọn `model`.

Trong CI, format được kiểm tra ở chế độ không sửa file:

```bash
uv run ruff format --check .
uv run ruff check .
uv run pytest
```

## GitHub Actions

Workflow tại `.github/workflows/ci.yml` tự động chạy khi có push hoặc pull request vào repository. Các bước chính:

1. Checkout mã nguồn.
2. Cài Python 3.14.
3. Cài và bật cache của `uv`.
4. Chạy `uv sync --dev` để cài đúng môi trường từ `uv.lock`.
5. Kiểm tra format bằng `ruff format --check`.
6. Kiểm tra lint bằng `ruff check`.
7. Chạy toàn bộ test bằng `pytest`.

Pull request chỉ đạt kiểm tra khi cả ba bước chất lượng mã đều thành công.

## Cấu trúc dự án

```text
ai-eng-lab/
├── src/ai_eng_lab/       # Mã nguồn chính
├── tests/                # Test tự động
├── pyproject.toml        # Cấu hình dự án và phụ thuộc
└── uv.lock               # Phiên bản phụ thuộc đã khóa
```
