import psycopg2
from dotenv import load_dotenv
import os
import time

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

UPDATE_QUERY = """
UPDATE client_protocol_task
SET status_id = (SELECT id FROM tag WHERE value = 'missed')
WHERE status_id = (SELECT id FROM tag WHERE value = 'todo')
  AND scheduled_time < NOW();
"""

CURRENT_TIME_QUERY = "SELECT NOW();"

def update_status():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()

        cursor.execute(CURRENT_TIME_QUERY)
        db_current_time = cursor.fetchone()[0]
        print(f"Current date and time from the database: {db_current_time}")

        cursor.execute(UPDATE_QUERY)

        conn.commit()
        print("Successfully updated status to 'missed' for overdue tasks.")
    except Exception as e:
        print(f"Error updating task statuses: {e}")
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'conn' in locals() and conn:
            conn.close()

if __name__ == "__main__":
    while True:
        update_status()
        time.sleep(30)  # Wait for 30 seconds before running again
