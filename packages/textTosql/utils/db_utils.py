import sqlite3
import pandas as pd
import random

class MockDB:
    def __init__(self, db_path=":memory:"):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self._setup_schema()
        self._populate_data()

    def _setup_schema(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS patients (
                id INTEGER PRIMARY KEY,
                age INTEGER,
                diagnosis TEXT,
                gender TEXT
            )
        ''')
        self.conn.commit()

    def _populate_data(self):
        # Insert 100 mock patients
        data = []
        diseases = ["Diabetes", "Hypertension", "Cancer", "Asthma"]
        genders = ["Male", "Female"]
        
        for i in range(100):
            age = random.randint(18, 90)
            diagnosis = random.choice(diseases)
            gender = random.choice(genders)
            data.append((i, age, diagnosis, gender))
            
        self.cursor.executemany('INSERT INTO patients VALUES (?, ?, ?, ?)', data)
        self.conn.commit()

    def execute_query(self, sql):
        try:
            return pd.read_sql_query(sql, self.conn)
        except Exception as e:
            # print(f"SQL Execution Error: {e}")
            return None

    def close(self):
        self.conn.close()
