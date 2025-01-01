import csv
import os
import traceback
import psycopg2
from psycopg2 import sql


def process_csv_file(file_path, db_connection):
    try:
        # Open the CSV file for reading
        with open(file_path, mode='r', newline='', encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                dashboard_name = row.get("Dashboard Name")
                dashboard_id = row.get("Dashboard ID")

                print("*********** ", dashboard_name, " - ", dashboard_id)
                if not dashboard_name or not dashboard_id:
                    raise ValueError("Invalid file format. Missing 'Dashboard Name' or 'Dashboard ID'")

                # SQL query to insert data
                query = """
                    INSERT INTO report_dashboard (name, dashboard_id)
                    VALUES (%s, %s)
                """

                # Create a cursor from the connection
                with db_connection.cursor() as cursor:
                    cursor.execute(query, (dashboard_name, dashboard_id))  # Execute the query with parameters

            db_connection.commit()  # Commit the transaction
    except Exception as e:
        print(traceback.format_exc())
        db_connection.rollback()  # Rollback on error
        raise e
    finally:
        os.remove(file_path)  # Clean up the temporary file
