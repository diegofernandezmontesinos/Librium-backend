# OnlineLibrary - Backend (FastAPI)

## Quick start (dev)
```bash
python3 -m venv venv
source env/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 4000
