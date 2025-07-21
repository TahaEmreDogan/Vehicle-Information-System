from dataclasses import dataclass
import psycopg2
from psycopg2 import Error


@dataclass
class Inspection():

    def __init__(self,vehicle_id,inspection_tpye,inspection_date,inspection_price,inspection_result,next_inspection_date,inspection_personnel,inspection_description):
        self.vehicle_id = vehicle_id
        self.inspection_tpye = inspection_tpye
        self.inspection_date = inspection_date
        self.inspection_price = inspection_price
        self.inspection_result = inspection_result
        self.next_inspection_date = next_inspection_date
        self.inspection_personnel = inspection_personnel
        self.inspection_description = inspection_description

    def show_inspection_details(self):
        print("Vehicle Id : {}\nInspection Type : {}\nInspection Date : {}\nInspection Price : {}\nInspection Result : {}\nNex Inspection Date : {}\nInspection Personnel : {}\nInspection Description : {}\n".format(self.vehicle_id,self.inspection_tpye,self.inspection_date,self.inspection_price,self.inspection_result,self.next_inspection_date,self.inspection_presonnel,self.inspection_description))

inspection = " "

def add_new_inspection(vehicle_id,inspection_tpye,inspection_date,inspection_price,inspection_result,next_inspection_date,inspection_personnel,inspection_description):
        connection = None
        cursor = None
        try:
            connection = psycopg2.connect(
                user="postgres",
                password="12345",
                host="localhost",
                port="5432",
                database="plakasorgu"
            )
            cursor = connection.cursor()
            insert_query = """
                INSERT INTO inspection (inspection_tpye,inspection_date,inspection_price,inspection_result,next_inspection_date,inspection_personnel,inspection_description)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            record_to_insert = (vehicle_id,inspection_tpye,inspection_date,inspection_price,inspection_result,next_inspection_date,inspection_personnel,inspection_description)
            cursor.execute(insert_query, record_to_insert)
            connection.commit()
            print("Inspection information has been added.")
            inspections = Inspection(vehicle_id,inspection_tpye,inspection_date,inspection_price,inspection_result,next_inspection_date,inspection_personnel,inspection_description)
            inspections.append(inspection)
        except (Exception, Error) as error:
            print("An error occurred in PostgreSQL:", error)
        finally:
            if cursor is not None:
                cursor.close()
            if connection is not None:
                connection.close()
                print("PostgreSQL connection closed.")

def update_inspection_details(vehicle_id,inspection_tpye,inspection_date,inspection_price,inspection_result,next_inspection_date,inspection_personnel,inspection_description):
        connection = None
        cursor = None
        try:
            connection = psycopg2.connect(
                user="postgres",
                password="12345",
                host="localhost",
                port="5432",
                database="plakasorgu"
            )
            cursor = connection.cursor()
            insert_query = """
                INSERT INTO inspections (inspection_tpye,inspection_date,inspection_price,inspection_result,next_inspection_date,inspection_personnel,inspection_description)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            record_to_insert = (vehicle_id,inspection_tpye,inspection_date,inspection_price,inspection_result,next_inspection_date,inspection_personnel,inspection_description)
            cursor.execute(insert_query, record_to_insert)
            connection.commit()
            print("Inspection information has been added.")
        except (Exception, Error) as error:
            print("An error occurred in PostgreSQL:", error)
        finally:
            if cursor is not None:
                cursor.close()
            if connection is not None:
                connection.close()
                print("PostgreSQL connection closed.")    