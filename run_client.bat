@echo off
set SERVER_NAME=MSB
set PORT=8000

echo 🌐 Starting client to connect with server at http://%SERVER_NAME%:%PORT% ...
streamlit run main.py
pause
