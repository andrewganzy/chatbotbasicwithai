import sqlite3
import json
import logging
from contextlib import contextmanager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@contextmanager
def get_db():
    try:
        db = sqlite3.connect('knowledge_base.db')
        db.row_factory = sqlite3.Row
        yield db
    except sqlite3.Error as e:
        logger.error(f"Database connection error: {e}")
        raise
    finally:
        if 'db' in locals():
            db.close()

def init_db():
    try:
        with get_db() as db:
            cursor = db.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS knowledge_base
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 data TEXT NOT NULL,
                 created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
            ''')
            db.commit()
            logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        raise

def migrate_json_to_sqlite():
    try:
        # First, check if we already have data in SQLite
        with get_db() as db:
            cursor = db.cursor()
            cursor.execute('SELECT COUNT(*) FROM knowledge_base')
            count = cursor.fetchone()[0]
            
            if count > 0:
                logger.info("Data already exists in database, skipping migration")
                return

        # If no data exists, proceed with migration
        with open('knowledge_base.json', 'r') as f:
            data = json.load(f)
            logger.info(f"Loaded {len(data)} items from knowledge_base.json")
            
            with get_db() as db:
                cursor = db.cursor()
                # Insert each item
                for item in data:
                    cursor.execute('INSERT INTO knowledge_base (data) VALUES (?)',
                                 (json.dumps(item),))
                db.commit()
                logger.info("Migration completed successfully")
                
    except FileNotFoundError:
        logger.warning("knowledge_base.json not found, creating empty database")
    except json.JSONDecodeError as e:
        logger.error(f"Error parsing knowledge_base.json: {e}")
    except Exception as e:
        logger.error(f"Error during migration: {e}")
        raise

def get_knowledge_base():
    try:
        with get_db() as db:
            cursor = db.cursor()
            cursor.execute('SELECT data FROM knowledge_base')
            rows = cursor.fetchall()
            result = [json.loads(row[0]) for row in rows]
            logger.info(f"Retrieved {len(result)} items from knowledge base")
            return result
    except Exception as e:
        logger.error(f"Error retrieving knowledge base: {e}")
        return []  # Return empty list instead of raising to prevent app crash

def add_to_knowledge_base(data):
    try:
        with get_db() as db:
            cursor = db.cursor()
            cursor.execute('INSERT INTO knowledge_base (data) VALUES (?)',
                          (json.dumps(data),))
            db.commit()
            logger.info("Successfully added new item to knowledge base")
    except Exception as e:
        logger.error(f"Error adding to knowledge base: {e}")
        raise
