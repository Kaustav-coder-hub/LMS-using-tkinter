import psycopg2
import os

def get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "dpg-d14akindiees73d3uvl0-a"),
        user=os.getenv("DB_USER", "lms_uxw7_user"),
        password=os.getenv("DB_PASSWORD", "yQwHBL2HHRoTtAZPc443HzHLeLwfUi0x"),
        dbname=os.getenv("DB_NAME", "lms_uxw7"),
        port=os.getenv("DB_PORT", 5432)
    )
