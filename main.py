import tkinter as tk
from tkinter import messagebox
from db import (
    add_vehicle_to_db, check_plate_in_db, get_inspections_by_vehicle_id,
    add_inspection_to_db, update_inspection_in_db, get_insurance_by_vehicle_id,add_insurance_by_vehicle_id
)
from vehicle import Vehicle
from insurance import Insurance

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Araç Sorgulama ve Ekleme")
        self.geometry("1000x1300")
        self.resizable(False, False)
        self.create_widgets()

    def create_widgets(self):
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

        tk.Label(self, text="Plaka Sorgula", font=("Arial", 12, "bold")).pack(pady=5)
        self.plate_query = tk.Entry(self, width=20)
        self.plate_query.pack()
        tk.Button(self, text="Sorgula", command=self.query_plate).pack(pady=5)

        self.result_text = tk.Text(self, width=65, height=20, font=("Arial", 11), state='disabled')
        self.result_text.pack(pady=5)

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
        tk.Label(self, text="Sigorta Ekle", font=("Arial", 12, "bold")).pack(pady=5)
        self.insurance_entries = {}
        insurance_fields = [
            "vehicle_id", "insurance_type", "insurance_company", "policy_number",
            "policy_amount", "start_date", "end_date", "status"
        ]
        for field in insurance_fields:
            frame = tk.Frame(self)
            frame.pack(pady=1)
            tk.Label(frame, text=field.replace("_", " ").title()+":", width=20, anchor="w").pack(side=tk.LEFT)
            entry = tk.Entry(frame, width=35)
            entry.pack(side=tk.LEFT)
            self.insurance_entries[field] = entry

        tk.Button(self, text="Sigorta Ekle", command=self.add_insurance).pack(pady=6)


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

            insurance_records = get_insurance_by_vehicle_id(vehicle.id)
            if insurance_records:
                self.result_text.insert(tk.END, "\nSigorta Bilgileri:\n")
                for i, ins_record in enumerate(insurance_records, start=1):
                    insurance = Insurance(*ins_record)
                    self.result_text.insert(tk.END, insurance.show_insurance_info() + "\n")
            else:
                self.result_text.insert(tk.END, "Sigorta bilgisi bulunamadı.\n")
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
    
    def add_insurance(self):
        try:
            data = {field: entry.get() for field, entry in self.insurance_entries.items()}
            data["vehicle_id"] = int(data["vehicle_id"])
            data["policy_amount"] = float(data["policy_amount"])
            if add_insurance_by_vehicle_id(**data):
                messagebox.showinfo("Başarılı", "Sigorta bilgisi eklendi.")
                for entry in self.insurance_entries.values():
                    entry.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Hata", f"Sigorta bilgisi eklenemedi.\n{e}")


if __name__ == "__main__":
    app = MainApp()
    app.mainloop()