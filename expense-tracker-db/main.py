from fastmcp import FastMCP
import os
import sqlite3


DB_PATH = os.path.join(os.path.dirname(__file__), 'expenses.db')

mcp = FastMCP(name="Expense Tracker DB")


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

@mcp.tool()
def add_expenses(date: str, amount: float, category: str, sub_category: str = "", note: str = ""):
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
        ''', (date, amount, category, sub_category, note))
        conn.commit()
        return {"status": "ok", "id": cursor.lastrowid}


@mcp.tool()
def list_expenses():
    '''
    List Expenses of Yours from the DB
    '''
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id,date,amount,category,sub_category,note FROM expenses ORDER BY id ASC
        ''')
        return cursor.fetchall()


if __name__ == "__main__":    
    mcp.run()
