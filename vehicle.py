import psycopg2
from psycopg2 import Error

class Vehicle:
    def __init__(self, id, plate, brand, model, status, vehicle_type):
        self.id = id
        self.plate = plate
        self.brand = brand
        self.model = model
        self.status = status
        self.vehicle_type = vehicle_type

    def show_details(self):
        print("Id : {}\nPlate : {}\nBrand : {}\nModel: {}\nStatus : {}\nVehicle Type : {}\n".format(
            self.id, self.plate, self.brand, self.model, self.status, self.vehicle_type
        ))

    @staticmethod
    def plate_check():
        user_plate = input("Enter your plate: ")

        connection = None
        try:
            connection = psycopg2.connect(
                user="postgres",       
                password="12345",
                host="localhost",
                port="5432",
                database="plakasorgu"
            )
            cursor = connection.cursor()

            select_query = "SELECT id, plate, brand, model, status, vehicle_type FROM vehicles WHERE plate = %s"
            cursor.execute(select_query, (user_plate,))
            record = cursor.fetchone()

            if record:
                vehicle = Vehicle(*record)
                vehicle.show_details()
            else:
                print("Bu plakaya ait araç bulunamadı.")

        except (Exception, Error) as error:
            print("PostgreSQL'den veri çekerken hata oluştu:", error)
        finally:
            if connection is not None:
                cursor.close()
                connection.close()

vehicles = []
def add_vehicle(id, plate, brand, model, status, vehicle_type):
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
            INSERT INTO vehicles (id, plate, brand, model, status, vehicle_type)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        record_to_insert = (id, plate, brand, model, status, vehicle_type)
        cursor.execute(insert_query, record_to_insert)
        connection.commit()
        print("Araç başarıyla veritabanına eklendi.")
        vehicle = Vehicle(id, plate, brand, model, status, vehicle_type)
        vehicles.append(vehicle)
    except (Exception, Error) as error:
        print("PostgreSQL'de hata oluştu:", error)
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None:
            connection.close()
            print("PostgreSQL bağlantısı kapatıldı.")

if __name__== "__main__":
    add_vehicle(
        id=4,
        plate="23HLN001",
        brand="Audi",
        model="RS7",
        status="Ready",
        vehicle_type="Sedan",
    )


if __name__ == "__main__":
    Vehicle.plate_check()
