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

def get_report_id_by_name(dashboard_name, db_connection):
    query = "SELECT id FROM report_dashboard WHERE name = %s"
    with db_connection.cursor() as cursor:
        cursor.execute(query, (dashboard_name,))
        print("Query :", query)
        result = cursor.fetchone()
        print("****", result)
        return result[0] if result else None


def get_role_ids_by_name(roles, db_connection):
    # Split the roles by comma and clean up the spaces
    role_names = [role.strip() for role in roles.split(',')]
    role_ids = []

    for role_name in role_names:
        query = "SELECT id FROM rbac_master WHERE role_name = %s"
        with db_connection.cursor() as cursor:
            cursor.execute(query, (role_name,))
            result = cursor.fetchone()
            if result:
                role_ids.append(result[0])
            else:
                print(f"Role '{role_name}' not found in rbac_master.")

    return role_ids


def insert_report_rbac(report_id, role_id, db_connection):
    query = """
        INSERT INTO report_rbac (report_id, role_id)
        VALUES (%s, %s)
    """
    with db_connection.cursor() as cursor:
        cursor.execute(query, (report_id, role_id))  # Execute the insert query with parameters


def process_csv_file_role_dashboard(file_path, db_connection):
    try:
        with open(file_path, mode='r', newline='', encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file)

            for row in reader:
                dashboard_name = row.get("Dashboard Name")
                print("*********", dashboard_name)
                # dashboard_name = dashboard_name.strip()
                roles = row.get("Role")
                print("*********", roles)

                if not dashboard_name or not roles:
                    raise ValueError("Invalid file format. Missing 'Dashboard Name' or 'Role'")

                # Step 1: Get the report_id (dashboard ID) for the given dashboard name
                report_id = get_report_id_by_name(dashboard_name, db_connection)
                print("******", report_id)
                if not report_id:
                    raise ValueError(f"Dashboard '{dashboard_name}' not found in report_dashboard.")

                # Step 2: Process roles and get role_id(s) for each role
                role_ids = get_role_ids_by_name(roles, db_connection)

                # Step 3: Insert data into report_rbac for each role
                for role_id in role_ids:
                    insert_report_rbac(report_id, role_id, db_connection)

            db_connection.commit()  # Commit the transaction
    except Exception as e:
        print(traceback.format_exc())
        db_connection.rollback()  # Rollback on error
        raise e
    finally:
        os.remove(file_path)  # Clean up the temporary file

