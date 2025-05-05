import sqlite3
from datetime import datetime
import os

DB_PATH = "clipboard.db"

def get_db_connection():
    """Create and return a database connection"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Enable column access by name
    return conn

def init_db():
    """Initialize the database with proper error handling"""
    try:
        conn = get_db_connection()
        c = conn.cursor()
        
        # Check if table exists
        c.execute("""SELECT name FROM sqlite_master 
                     WHERE type='table' AND name='clips'""")
        if not c.fetchone():
            c.execute("""CREATE TABLE clips
                        (id INTEGER PRIMARY KEY AUTOINCREMENT,
                        content TEXT NOT NULL,
                        content_type TEXT,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                        preview TEXT)""")
            conn.commit()
            print("✅ Database table created successfully")
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
    finally:
        conn.close()

def save_clip(content, content_type="text"):
    """Save content to database with error handling"""
    try:
        conn = get_db_connection()
        c = conn.cursor()
        c.execute("""INSERT INTO clips 
                    (content, content_type, preview) 
                    VALUES (?, ?, ?)""",
                 (content, content_type, str(content)[:100]))
        conn.commit()
        return True
    except Exception as e:
        print(f"❌ Failed to save clip: {e}")
        return False
    finally:
        conn.close()

# Initialize database when module loads
init_db()