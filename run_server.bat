@echo off
echo 🚀 Starting FastAPI server on host 0.0.0.0 port 8000...
uvicorn server:app --host 0.0.0.0 --port 8000 --reload
pause
