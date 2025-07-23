import psycopg2
from psycopg2 import Error

def db_connect():
    return psycopg2.connect(
        user="postgres",          
        password="12345",         
        host="localhost",
        port="5432",
        database="plakasorgu"     
    )

def add_vehicle_to_db(id, plate, brand, model, status, vehicle_type):
    connection = None
    cursor = None
    try:
        connection = db_connect()
        cursor = connection.cursor()
        insert_query = """
            INSERT INTO vehicles (id, plate, brand, model, status, vehicle_type)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (id, plate, brand, model, status, vehicle_type))
        connection.commit()
        return True
    except (Exception, Error) as error:
        print("Database Error:", error)
        return False
    finally:
        if cursor: cursor.close()
        if connection: connection.close()

def check_plate_in_db(plate):
    connection = None
    cursor = None
    try:
        connection = db_connect()
        cursor = connection.cursor()
        select_query = "SELECT id, plate, brand, model, status, vehicle_type FROM vehicles WHERE plate = %s"
        cursor.execute(select_query, (plate,))
        record = cursor.fetchone()
        return record
    except (Exception, Error) as error:
        print("Database Error:", error)
        return None
    finally:
        if cursor: cursor.close()
        if connection: connection.close()

def get_inspections_by_vehicle_id(vehicle_id):
    connection = None
    cursor = None
    try:
        connection = db_connect()
        cursor = connection.cursor()
        select_query = """
            SELECT inspection_type, inspection_date, inspection_price, inspection_result,
                   next_inspection_date, inspection_personnel, inspection_description
            FROM inspections
            WHERE vehicle_id = %s
        """
        cursor.execute(select_query, (vehicle_id,))
        records = cursor.fetchall()
        print(f"Muayene sorgusu sonucu: {records}")  # Kontrol için!
        return records
    except (Exception, Error) as error:
        print("Database Error:", error)
        return []
    finally:
        if cursor: cursor.close()
        if connection: connection.close()

def add_inspection_to_db(vehicle_id, inspection_type, inspection_date, inspection_price, inspection_result, next_inspection_date, inspection_personnel, inspection_description):
    connection = None
    cursor = None
    try:
        connection = db_connect()
        cursor = connection.cursor()
        insert_query = """
            INSERT INTO inspections (
                vehicle_id, inspection_type, inspection_date, inspection_price,
                inspection_result, next_inspection_date, inspection_personnel, inspection_description
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (
            vehicle_id, inspection_type, inspection_date, inspection_price,
            inspection_result, next_inspection_date, inspection_personnel, inspection_description
        ))
        connection.commit()
        return True
    except (Exception, Error) as error:
        print("Database Error:", error)
        return False
    finally:
        if cursor: cursor.close()
        if connection: connection.close()

def update_inspection_in_db(vehicle_id, inspection_type, inspection_date, inspection_price, inspection_result, next_inspection_date, inspection_personnel, inspection_description):
    connection = None
    cursor = None
    try:
        connection = db_connect()
        cursor = connection.cursor()
        update_query = """
            UPDATE inspections SET
                inspection_type = %s,
                inspection_date = %s,
                inspection_price = %s,
                inspection_result = %s,
                next_inspection_date = %s,
                inspection_personnel = %s,
                inspection_description = %s
            WHERE vehicle_id = %s
        """
        cursor.execute(update_query, (
            inspection_type, inspection_date, inspection_price, inspection_result,
            next_inspection_date, inspection_personnel, inspection_description, vehicle_id
        ))
        connection.commit()
        return True
    except (Exception, Error) as error:
        print("Database Error:", error)
        return False
    finally:
        if cursor: cursor.close()
        if connection: connection.close()

def get_insurance_by_vehicle_id(vehicle_id):
    connection = None
    cursor = None
    try:
        connection = db_connect()
        cursor = connection.cursor()
        query = """
            SELECT vehicle_id, insurance_type, insurance_company, policy_number, 
                   policy_amount, start_date, end_date, status 
            FROM insurance WHERE vehicle_id = %s
        """
        cursor.execute(query, (vehicle_id,))
        records = cursor.fetchall()
        print(f"Sigorta sorgusu sonucu: {records}")
        return records
    except (Exception, Error) as error:
        print("Database Error:", error)
        return []
    finally:
        if cursor: cursor.close()
        if connection: connection.close()

def add_insurance_by_vehicle_id(vehicle_id, insurance_type, insurance_company, policy_number, 
            policy_amount, start_date, end_date, status):
    connection = None
    cursor = None
    try:
        connection = db_connect()
        cursor = connection.cursor()
        query = """
            INSERT INTO insurance (vehicle_id, insurance_type, insurance_company, policy_number, 
            policy_amount, start_date, end_date, status ) 
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s) 
        """
        cursor.execute(query, (vehicle_id, insurance_type, insurance_company, policy_number, 
            policy_amount, start_date, end_date, status))
        connection.commit()
        return True
    except (Exception, Error) as error:
        print("Database Error:", error)
        return False
    finally:
        if cursor: cursor.close()
        if connection: connection.close()
