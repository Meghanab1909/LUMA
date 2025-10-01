# server.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mysql.connector

app = FastAPI()

# Define input schema
class User(BaseModel):
    username: str
    email: str = None
    password: str
    roles: list[str] = []

# Database connection
def get_db():
    return mysql.connector.connect(
        host="localhost",      # change if your DB is remote
        user="root",           # your MySQL username
        password="412356",   # your MySQL password
        database="minijira"  # your DB name
    )

@app.post("/register")
def register_user(user: User):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SET FOREIGN_KEY_CHECKS=0")

    try:
        cursor.execute(
            "INSERT INTO user (username, email, password_hash, roles) VALUES (%s, %s, %s, %s)",
            (user.username, user.email, user.password, ",".join(user.roles))
        )
        conn.commit()
        cursor.execute("SET FOREIGN_KEY_CHECKS=1")
        return {"message": "User registered successfully"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conn.close()

class LoginRequest(BaseModel):
    username: str
    password: str

@app.post("/login")
def login_user(login: LoginRequest):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM user WHERE (username=%s OR email=%s) AND password_hash=%s",
        (login.username, login.username, login.password)
    )
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    if user:
        return {"message": "Login successful", "user": user}
    else:
        raise HTTPException(status_code=401, detail="Invalid username or password")