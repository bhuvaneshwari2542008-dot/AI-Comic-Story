# ComicCraft

ComicCraft is a FastAPI and Jinja2 web application that turns a prompt into a structured five-panel comic. It includes Gemini story generation, deterministic demo artwork, browser preview, JSON API, and PDF export.

## Features

- Responsive comic creation form
- Pydantic input and AI-output validation
- Optional Gemini structured story generation
- Demo mode that works without an API key
- Generated panel images and JSON storage
- PDF download
- Automated route and model tests

## Quick start

```bash
python -m venv .venv
```

Activate it:

```powershell
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
```

```bash
# macOS/Linux
source .venv/bin/activate
```

Install and configure:

```bash
python -m pip install -r requirements.txt
cp .env.example .env  # Windows: copy .env.example .env
uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000. API docs are at http://127.0.0.1:8000/docs.

## Gemini mode

Demo mode is enabled by default. To use Gemini, edit `.env`:

```env
DEMO_MODE=false
GEMINI_API_KEY=your_key
GEMINI_TEXT_MODEL=gemini-2.5-flash
```

Use a model currently available to your API account. Generated panel art remains local placeholder artwork in this starter project. Replace `ImageGenerator` with a supported cloud image model or a Diffusers pipeline when desired.

## Tests

```bash
python -m pip install -r requirements-dev.txt
pytest -v
```

## Routes

- `GET /` — form
- `POST /generate` — form generation
- `POST /api/comics` — JSON generation
- `GET /comic/{comic_id}` — preview
- `GET /comic/{comic_id}/pdf` — PDF download
- `GET /health` — health check

## Safety

Never commit `.env` or API keys. AI output is validated and Jinja escapes generated text by default.
