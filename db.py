import psycopg2

def get_connection():
    return psycopg2.connect(
        host="dpg-d14akindiees73d3uvl0-a",
        user="lms_uxw7_user",
        password="yQwHBL2HHRoTtAZPc443HzHLeLwfUi0x",
        dbname="lms_uxw7",
        port=5432
    )
