from fastapi import FastAPI, HTTPException

from pydantic import BaseModel
import os
import sqlite3
import json


BASE_DIR = os.path.dirname(__file__)
DB_PATH = os.path.join(BASE_DIR, "db.sqlite3")

app = FastAPI(title="Expense Tracker API")


def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                sub_category TEXT DEFAULT '',                
                date TEXT NOT NULL,
                note TEXT DEFAULT ''
            )
        ''')
        conn.commit()


init_db()


class ExpenseCreate(BaseModel):
    date: str
    amount: float
    category: str
    sub_category: str | None = ""
    note: str | None = ""


@app.post("/expenses/")
def add_expenses(payload: ExpenseCreate):
    '''
    Add Expensed in the DB

    :param date: Description
    :type date: str
    :param amount: Description
    :type amount: float
    :param category: Description
    :type category: str
    :param sub_category: Description
    :type sub_category: str
    :param note: Description
    :type note: str
    '''

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO expenses (date, amount, category, sub_category, note)
            VALUES (?, ?, ?, ?, ?)
        ''', (payload.date, payload.amount, payload.category, payload.sub_category, payload.note))
        conn.commit()
        return {"status": "ok", "id": cursor.lastrowid}


@app.get('/expenses')
def list_expenses():
    '''
    List Expenses of Yours from the DB
    '''
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id,date,amount,category,sub_category,note FROM expenses ORDER BY id ASC
        ''')
        return {'status': 'ok', 'data': cursor.fetchall()}


@app.get('/expenses/date-range/')
def list_expenses_with_date(start_date: str, end_date: str):
    '''
    list of all expenses which comes bw these dates.

    :param start_date: Description
    :type start_date: str
    :param end_date: Description
    :type end_date: str
    '''
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id,date,amount,category,sub_category,note FROM expenses WHERE date BETWEEN ? AND ? ORDER BY id ASC
        ''', (start_date, end_date))
        return {'status': 'ok', 'data': cursor.fetchall()}


@app.get('/expenses/summarize/')
def summarize(start_date: str, end_date: str, category: str | None = None):
    '''
    Summarize all expenses which comes bw these dates.

    :param start_date: Description
    :type start_date: str
    :param end_date: Description
    :type end_date: str
    '''
    with sqlite3.connect(DB_PATH) as conn:
        query = ('''
            SELECT category, SUM(amount) AS total_amount from expenses WHERE date BETWEEN ? AND ?
        ''')
        params = [start_date, end_date]
        if category:
            query += " AND category = ?"
            params.append(category)
        query += " GROUP BY category ORDER BY category ASC"
        cur = conn.execute(query, params)
        cols = [d[0] for d in cur.description]
        return {'data': [dict(zip(cols, r)) for r in cur.fetchall()]}
