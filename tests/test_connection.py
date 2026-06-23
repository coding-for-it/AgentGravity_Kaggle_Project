from services.snowflake_connection import get_connection
import traceback

try:
    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("SELECT CURRENT_VERSION()")

    result = cursor.fetchone()

    print("\nSUCCESS!")
    print("Snowflake Version:", result)

    cursor.close()
    conn.close()

except Exception as e:
    print("\nERROR!")
    print(type(e))
    print(e)

    traceback.print_exc()