import tkinter as tk
from tkinter import messagebox
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

    def details(self):
        return (f"Id: {self.id}\nPlate: {self.plate}\nBrand: {self.brand}\n"
                f"Model: {self.model}\nStatus: {self.status}\nVehicle Type: {self.vehicle_type}")

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
        record_to_insert = (id, plate, brand, model, status, vehicle_type)
        cursor.execute(insert_query, record_to_insert)
        connection.commit()
        return True
    except (Exception, Error) as error:
        messagebox.showerror("Database Error", f"Error: {error}")
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
        messagebox.showerror("Database Error", f"Error: {error}")
        return None
    finally:
        if cursor: cursor.close()
        if connection: connection.close()

# YENİ: Belirli bir aracın muayene kayıtlarını getir
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
        return records
    except (Exception, Error) as error:
        messagebox.showerror("Database Error", f"Error: {error}")
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
                vehicle_id,
                inspection_type,
                inspection_date,
                inspection_price,
                inspection_result,
                next_inspection_date,
                inspection_personnel,
                inspection_description
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (
            vehicle_id,
            inspection_type,
            inspection_date,
            inspection_price,
            inspection_result,
            next_inspection_date,
            inspection_personnel,
            inspection_description
        ))
        connection.commit()
        return True
    except (Exception, Error) as error:
        messagebox.showerror("Database Error", f"Error: {error}")
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
            inspection_type,
            inspection_date,
            inspection_price,
            inspection_result,
            next_inspection_date,
            inspection_personnel,
            inspection_description,
            vehicle_id
        ))
        connection.commit()
        return True
    except (Exception, Error) as error:
        messagebox.showerror("Database Error", f"Error: {error}")
        return False
    finally:
        if cursor: cursor.close()
        if connection: connection.close()

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Araç Sorgulama ve Ekleme")
        self.geometry("580x950")
        self.resizable(False, False)
        self.create_widgets()

    def create_widgets(self):
        # Araç Ekleme
        tk.Label(self, text="Araç Ekle", font=("Arial", 12, "bold")).pack(pady=5)
        self.entries = {}
        fields = ["id", "plate", "brand", "model", "status", "vehicle_type"]
        for field in fields:
            frame = tk.Frame(self)
            frame.pack(pady=1)
            tk.Label(frame, text=field.title()+":", width=12, anchor="w").pack(side=tk.LEFT)
            entry = tk.Entry(frame, width=28)
            entry.pack(side=tk.LEFT)
            self.entries[field] = entry

        tk.Button(self, text="Aracı Ekle", command=self.add_vehicle).pack(pady=6)

        # Plaka Sorgulama
        tk.Label(self, text="Plaka Sorgula", font=("Arial", 12, "bold")).pack(pady=5)
        self.plate_query = tk.Entry(self, width=20)
        self.plate_query.pack()
        tk.Button(self, text="Sorgula", command=self.query_plate).pack(pady=5)

        self.result_text = tk.Text(self, width=65, height=15, font=("Arial", 11), state='disabled')
        self.result_text.pack(pady=5)

        # Muayene Bilgisi Ekleme
        tk.Label(self, text="Muayene Bilgisi Ekle / Güncelle", font=("Arial", 12, "bold")).pack(pady=5)
        self.inspection_entries = {}
        inspection_fields = [
            "vehicle_id", "inspection_type", "inspection_date", "inspection_price",
            "inspection_result", "next_inspection_date", "inspection_personnel", "inspection_description"
        ]
        for field in inspection_fields:
            frame = tk.Frame(self)
            frame.pack(pady=1)
            tk.Label(frame, text=field.replace("_", " ").title()+":", width=20, anchor="w").pack(side=tk.LEFT)
            entry = tk.Entry(frame, width=35)
            entry.pack(side=tk.LEFT)
            self.inspection_entries[field] = entry

        button_frame = tk.Frame(self)
        button_frame.pack(pady=6)
        tk.Button(button_frame, text="Muayene Ekle", command=self.add_inspection).pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="Muayene Güncelle", command=self.update_inspection).pack(side=tk.LEFT, padx=10)

    def add_vehicle(self):
        try:
            id = int(self.entries["id"].get())
            plate = self.entries["plate"].get()
            brand = self.entries["brand"].get()
            model = self.entries["model"].get()
            status = self.entries["status"].get()
            vehicle_type = self.entries["vehicle_type"].get()
            if add_vehicle_to_db(id, plate, brand, model, status, vehicle_type):
                messagebox.showinfo("Başarılı", "Araç başarıyla eklendi.")
                for entry in self.entries.values():
                    entry.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Hata", f"Girilen bilgileri kontrol edin.\n{e}")

    def query_plate(self):
        plate = self.plate_query.get()
        record = check_plate_in_db(plate)
        self.result_text.config(state='normal')
        self.result_text.delete(1.0, tk.END)
        if record:
            vehicle = Vehicle(*record)
            self.result_text.insert(tk.END, vehicle.details() + "\n\n")

            # Muayene bilgilerini getir ve göster
            inspections = get_inspections_by_vehicle_id(vehicle.id)
            if inspections:
                self.result_text.insert(tk.END, "Muayene Bilgileri:\n")
                for i, inspection in enumerate(inspections, start=1):
                    (inspection_type, inspection_date, inspection_price,
                     inspection_result, next_inspection_date, inspection_personnel,
                     inspection_description) = inspection
                    self.result_text.insert(
                        tk.END,
                        f"\n--- Muayene {i} ---\n"
                        f"Tür: {inspection_type}\n"
                        f"Tarih: {inspection_date}\n"
                        f"Fiyat: {inspection_price}\n"
                        f"Sonuç: {inspection_result}\n"
                        f"Sonraki Muayene Tarihi: {next_inspection_date}\n"
                        f"Personel: {inspection_personnel}\n"
                        f"Açıklama: {inspection_description}\n"
                    )
            else:
                self.result_text.insert(tk.END, "Muayene bilgisi bulunamadı.\n")
        else:
            self.result_text.insert(tk.END, "Bu plakaya ait araç bulunamadı.")
        self.result_text.config(state='disabled')

    def add_inspection(self):
        try:
            data = {field: entry.get() for field, entry in self.inspection_entries.items()}
            data["vehicle_id"] = int(data["vehicle_id"])
            data["inspection_price"] = float(data["inspection_price"])
            if add_inspection_to_db(**data):
                messagebox.showinfo("Başarılı", "Muayene bilgisi eklendi.")
                for entry in self.inspection_entries.values():
                    entry.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Hata", f"Muayene bilgisi eklenemedi.\n{e}")

    def update_inspection(self):
        try:
            data = {field: entry.get() for field, entry in self.inspection_entries.items()}
            data["vehicle_id"] = int(data["vehicle_id"])
            data["inspection_price"] = float(data["inspection_price"])
            if update_inspection_in_db(**data):
                messagebox.showinfo("Başarılı", "Muayene bilgisi güncellendi.")
        except Exception as e:
            messagebox.showerror("Hata", f"Muayene bilgisi güncellenemedi.\n{e}")

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
