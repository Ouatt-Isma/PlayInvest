## Launch Server

```bash
cd backend
PYTHONPATH=. uvicorn main:app --reload
--log-level debug

PYTHONPATH=. uvicorn app.main:app --reload --host :: --port 8000
```