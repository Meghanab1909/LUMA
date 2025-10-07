# server.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mysql.connector
import logging
from typing import Optional

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
        roles_str = ",".join(user.roles)

        cursor.execute("SELECT role_id FROM role where role_name=%s", (roles_str,))
        role = cursor.fetchone()

        role_id = role[0]

        cursor.execute(
            "INSERT INTO user (username, email, password_hash, roles, role_id) VALUES (%s, %s, %s, %s, %s)",
            (user.username, user.email, user.password, roles_str, role_id)
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

class Ticket(BaseModel):
    title: str
    description: str
    priority: str 
    created_by: str 
    assigned_to: Optional[str] = None
    specialization: list[str] 
    created_at: str 
    status: str 
    updated_at: Optional[str] = None

@app.post("/tickets")
def raise_ticket(ticket: Ticket):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SET FOREIGN_KEY_CHECKS=0")

    try:
        specialization_str = ",".join(ticket.specialization)

        cursor.execute("SELECT user_id FROM user where username=%s", (ticket.created_by,))
        user = cursor.fetchone()

        if user is None:
            raise HTTPException(status_code=404, detail=f"User '{ticket.created_by}' not found in the database.")

        user_id = user[0]

        logging.info(f"user_id: {user_id}")
        logging.info(f"Ticket data: {(ticket.title, ticket.description, ticket.status, ticket.priority, user_id, None, ticket.created_at, ticket.updated_at, specialization_str)}")

        cursor.execute("INSERT INTO BUGTICKET (TITLE, DESCRIPTION, STATUS, PRIORITY, CREATED_BY, ASSIGNED_TO, CREATED_AT, UPDATED_AT, SPECIALISATION) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    (ticket.title, ticket.description, ticket.status, ticket.priority, user_id, None, ticket.created_at, None, specialization_str))
        
        
        bugticket_id = cursor.lastrowid

        cursor.execute("INSERT INTO AUDITLOG (bugtkt_id, user_id, action) VALUES (%s, %s, %s)", (bugticket_id, user_id, f"Ticket raised by USER {user_id}"))
        
        conn.commit()
        cursor.execute("SET FOREIGN_KEY_CHECKS=1")
        return {"message": "Ticket raised successfully"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@app.get("/tickets")
def show_tickets():
    conn = get_db()
    cursor = conn.cursor(dictionary = True)

    try:
        cursor.execute("select *from bugticket where assigned_to IS NULL")
        tickets = cursor.fetchall()
        return {"tickets": tickets}
    except Exception as e:
        raise HTTPException(status = 500, detail = str(e))
    finally:
        cursor.close()
        conn.close()

class AcceptTicket(BaseModel):
    ticket_id: int
    username: str

@app.post("/accept-tickets")
def accept(ticket: AcceptTicket):
    conn = get_db()
    cursor = conn.cursor()

    try:
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
        
        cursor.execute("select user_id from user where username = %s", (ticket.username,))
        user = cursor.fetchone()

        if user is None:
            raise HTTPException(status_code=404, detail=f"User '{ticket.created_by}' not found in the database.")
        
        user_id = user[0]

        cursor.execute("update bugticket set assigned_to = %s and status = %s where bugtkt_id = %s", (user_id, "IN PROGRESS", ticket.ticket_id))

        cursor.execute("INSERT INTO AUDITLOG (bugtkt_id, user_id, action) VALUES (%s, %s, %s)",
                       (ticket.ticket_id, user_id, f"Ticket {ticket.ticket_id} accepted by USER {user_id}"))
        
        conn.commit()

        cursor.execute("SET FOREIGN_KEY_CHECKS = 1")

        return {"message": "Ticket accepted successfully"}
    except Exception as e:
        raise HTTPException(status = 500, detail = str(e))
    finally:
        cursor.close()
        conn.close()

@app.get("/accept-tickets")
def display_usertickets(username: str):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
        
        cursor.execute("select user_id from user where username = %s", (username,))
        user = cursor.fetchone()

        if user is None:
            raise HTTPException(status_code=404, detail=f"User '{username}' not found in the database.")
        
        user_id = user["user_id"]

        cursor.execute("select *from bugticket where created_by = %s and STATUS <> %s", (user_id, "CLOSED",))
        created_tickets = cursor.fetchall()

        cursor.execute("select *from bugticket where assigned_to = %s and STATUS <> %s", (user_id, "CLOSED"))
        assigned_tickets = cursor.fetchall()

        cursor.execute("SET FOREIGN_KEY_CHECKS = 1")

        return {"created_tickets": created_tickets, "assigned_tickets": assigned_tickets}
    except Exception as e:
        raise HTTPException(status = 500, detail = str(e))
    finally:
        cursor.close()
        conn.close()

class Comments(BaseModel):
    bugtkt_id: int
    username: str 
    comment_text: str 

@app.post("/comments")
def write_comment(comment: Comments):
    conn = get_db()
    cursor = conn.cursor()

    try:
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0")

        cursor.execute("select user_id from user where username = %s", (comment.username,))
        user = cursor.fetchone()

        if user is None:
            raise HTTPException(status_code=404, detail=f"User '{comment.username}' not found in the database.")
        
        user_id = user[0]

        cursor.execute("select created_by, assigned_to from bugticket where bugtkt_id = %s", (comment.bugtkt_id,))

        user2 = cursor.fetchone()


        if(user_id not in (user2[0], user2[1])):
            raise HTTPException(status_code=404, detail=f"This user has neither created or been assigned to hence cannot comment")

        cursor.execute("INSERT INTO COMMENT (bug_id, user_id, comment_text) VALUES (%s, %s, %s)",
                       (comment.bugtkt_id, user_id, comment.comment_text))

        cursor.execute("INSERT INTO AUDITLOG (bugtkt_id, user_id, action) VALUES (%s, %s, %s)",
                       (comment.bugtkt_id, user_id, f"A comment was added for TICKET {comment.bugtkt_id} by USER {user_id}"))

        conn.commit()

        cursor.execute("SET FOREIGN_KEY_CHECKS = 1")

        return {"message": "Comment added successfully"}
    except Exception as e:
        raise HTTPException(status_code = 500, detail = str(e))
    finally:
        cursor.close()
        conn.close()

@app.get("/comments")
def show_comments(bugtkt_id: int):
    conn = get_db()
    cursor = conn.cursor(dictionary = True)

    try:
        cursor.execute("select *from comment where bug_id = %s", (bugtkt_id,))
        comments = cursor.fetchall()
        return {"comments": comments}
    except Exception as e:
        raise HTTPException(status = 500, detail = str(e))
    finally:
        cursor.close()
        conn.close()

class CloseTicket(BaseModel):
    ticket_id: int
    username: str

@app.post("/close-tickets")
def close_tickets(ticket: CloseTicket):
    conn = get_db()
    cursor = conn.cursor()

    try:
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0")

        cursor.execute("select user_id from user where username = %s", (ticket.username,))
        user = cursor.fetchone()

        if user is None:
            raise HTTPException(status_code=404, detail=f"User '{ticket.username}' not found in the database.")
        
        user_id = user[0]

        cursor.execute("UPDATE bugticket set STATUS = %s where bugtkt_id = %s", ("CLOSED", ticket.ticket_id))

        cursor.execute("INSERT INTO AUDITLOG (bugtkt_id, user_id, action) VALUES (%s, %s, %s)",
                       (ticket.ticket_id, user_id, f"Ticket {ticket.ticket_id} closed by USER {user_id}"))

        conn.commit()

        cursor.execute("SET FOREIGN_KEY_CHECKS = 1")

        return {"message": "Ticket closed successfully"}
    except Exception as e:
        raise HTTPException(status = 500, detail = str(e))
    finally:
        cursor.close()
        conn.close()