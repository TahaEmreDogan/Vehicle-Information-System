import tkinter as tk
from tkinter import messagebox
from db import (
    add_vehicle_to_db, check_plate_in_db, get_inspections_by_vehicle_id,
    add_inspection_to_db, update_inspection_in_db, get_insurance_by_vehicle_id,
    add_insurance_by_vehicle_id, admin_login
)
from vehicle import Vehicle
from inspection import Inspection
from insurance import Insurance

# Renk paleti
BG_COLOR = "#f4f6fb"         # Açık mavi-gri
FRAME_BG = "#e9eaf6"        # Kutular için daha koyu açık mavi
BUTTON_BG = "#4a6fa5"       # Mavi
BUTTON_FG = "#fff"
LABEL_FG = "#22223b"
RESULT_BG = "#fff"
RESULT_FG = "#2d3142"
RESULT_BORDER = "#4a6fa5"
FONT_HEADER = ("Segoe UI", 14, "bold")
FONT_LABEL = ("Segoe UI", 11)
FONT_RESULT = ("Consolas", 13, "bold")

class LoginWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Admin Giriş")
        self.geometry("300x180")
        self.resizable(False, False)
        self.configure(bg=BG_COLOR)
        tk.Label(self, text="Admin Name:", bg=BG_COLOR, fg=LABEL_FG, font=FONT_LABEL).pack(pady=5)
        self.username_entry = tk.Entry(self)
        self.username_entry.pack(pady=5)
        tk.Label(self, text="Admin Password:", bg=BG_COLOR, fg=LABEL_FG, font=FONT_LABEL).pack(pady=5)
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack(pady=5)
        tk.Button(self, text="Giriş", command=self.login, bg=BUTTON_BG, fg=BUTTON_FG, font=FONT_LABEL, activebackground="#35507a").pack(pady=10)
        self.result = False

    def login(self):
        admin_name = self.username_entry.get().strip()
        admin_password = self.password_entry.get().strip()
        if admin_login(admin_name, admin_password):
            self.result = True
            self.destroy()
        else:
            messagebox.showerror("Hata", "Admin adı veya şifre yanlış!")

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Araç Sorgulama ve Ekleme Sistemi")
        self.geometry("1300x700")
        self.resizable(False, False)
        self.configure(bg=BG_COLOR)
        self.is_admin_logged_in = False
        # İkonları yükle
        self.icon_arac = tk.PhotoImage(file="arac.png")
        self.icon_muayene = tk.PhotoImage(file="muayene.png")
        self.icon_sigorta = tk.PhotoImage(file="sigorta.png")
        try:
            self.icon_admin = tk.PhotoImage(file="admin.png")
        except Exception:
            self.icon_admin = None
        self.create_widgets()

    def create_widgets(self):
        admin_button_frame = tk.Frame(self, bg=BG_COLOR)
        admin_button_frame.place(x=1150, y=10)
        if self.icon_admin:
            admin_icon_label = tk.Label(admin_button_frame, image=self.icon_admin, bg=BG_COLOR)
            admin_icon_label.image = self.icon_admin
            admin_icon_label.pack(side=tk.LEFT, padx=(0, 4))
        self.admin_login_btn = tk.Button(admin_button_frame, text="Admin Girişi", command=self.admin_login_popup, font=("Arial", 10, "bold"), bg=BUTTON_BG, fg=BUTTON_FG, activebackground="#35507a")
        self.admin_login_btn.pack(side=tk.LEFT)

        tk.Label(self, text="Plaka Sorgula", font=FONT_HEADER, bg=BG_COLOR, fg=LABEL_FG).pack(pady=10)
        # Plaka sorgu kutusu ve büyüteç ikonunu bir frame içinde hizala
        plate_frame = tk.Frame(self, bg=BG_COLOR)
        plate_frame.pack(pady=2)
        try:
            self.icon_search = tk.PhotoImage(file="search.png")
        except Exception:
            self.icon_search = None
        self.plate_query = tk.Entry(plate_frame, width=28, font=("Segoe UI", 15, "bold"), bg="#f8fafc", fg="#22223b", bd=3, relief="solid", highlightbackground=RESULT_BORDER, highlightcolor=RESULT_BORDER, highlightthickness=2)
        self.plate_query.pack(side=tk.LEFT, ipady=6, ipadx=2, padx=(0, 0))
        if self.icon_search:
            search_btn = tk.Button(
                plate_frame, image=self.icon_search, command=self.query_plate,
                bg=BUTTON_BG, activebackground="#35507a", bd=0, highlightthickness=0
            )
        else:
            search_btn = tk.Button(
                plate_frame, text="Sorgula", command=self.query_plate,
                font=("Arial", 11, "bold"), bg=BUTTON_BG, fg=BUTTON_FG, activebackground="#35507a"
            )
        search_btn.pack(side=tk.LEFT, padx=(6, 0), ipadx=6, ipady=2)

        self.result_text = tk.Text(self, width=95, height=10, font=FONT_RESULT, state='disabled', bg=RESULT_BG, fg=RESULT_FG, bd=3, relief="solid", highlightbackground=RESULT_BORDER, highlightcolor=RESULT_BORDER, highlightthickness=2)
        self.result_text.pack(pady=7)
        self.admin_area = tk.Frame(self, bg=BG_COLOR)

    def show_admin_widgets(self):
        if hasattr(self, 'admin_widgets_created') and self.admin_widgets_created:
            self.admin_area.pack(pady=12)
            return
        self.admin_widgets_created = True

        container = tk.Frame(self.admin_area, bg=BG_COLOR)
        container.pack()

        # Araç Ekle
        vehicle_frame = tk.Frame(container, bg=FRAME_BG, bd=2, relief="groove")
        vehicle_frame.pack(side=tk.LEFT, padx=20, pady=5, fill='y')
        vehicle_header = tk.Frame(vehicle_frame, bg=FRAME_BG)
        vehicle_header.pack(anchor="w", pady=(5, 2))
        tk.Label(vehicle_header, image=self.icon_arac, bg=FRAME_BG).pack(side=tk.LEFT, padx=(0, 6))
        tk.Label(vehicle_header, text="Araç Ekle", font=("Arial", 12, "bold"), bg=FRAME_BG, fg=LABEL_FG).pack(side=tk.LEFT)

        self.entries = {}
        fields = ["id", "plate", "brand", "model", "status", "vehicle_type"]
        for field in fields:
            frame = tk.Frame(vehicle_frame, bg=FRAME_BG)
            frame.pack(pady=1, anchor="w")
            tk.Label(frame, text=field.title()+":", width=12, anchor="w", bg=FRAME_BG, fg=LABEL_FG, font=FONT_LABEL).pack(side=tk.LEFT)
            entry = tk.Entry(frame, width=18, font=FONT_LABEL)
            entry.pack(side=tk.LEFT)
            self.entries[field] = entry
        tk.Button(vehicle_frame, text="Aracı Ekle", command=self.add_vehicle, width=20, bg=BUTTON_BG, fg=BUTTON_FG, font=FONT_LABEL, activebackground="#35507a").pack(pady=7)

        # Muayene Bilgisi
        inspection_frame = tk.Frame(container, bg=FRAME_BG, bd=2, relief="groove")
        inspection_frame.pack(side=tk.LEFT, padx=20, pady=5, fill='y')
        inspection_header = tk.Frame(inspection_frame, bg=FRAME_BG)
        inspection_header.pack(anchor="w", pady=(5, 2))
        tk.Label(inspection_header, image=self.icon_muayene, bg=FRAME_BG).pack(side=tk.LEFT, padx=(0, 6))
        tk.Label(inspection_header, text="Muayene Bilgisi Ekle / Güncelle", font=("Arial", 12, "bold"), bg=FRAME_BG, fg=LABEL_FG).pack(side=tk.LEFT)

        self.inspection_entries = {}
        inspection_fields = [
            "vehicle_id", "inspection_type", "inspection_date", "inspection_price",
            "inspection_result", "next_inspection_date", "inspection_personnel", "inspection_description"
        ]
        for field in inspection_fields:
            frame = tk.Frame(inspection_frame, bg=FRAME_BG)
            frame.pack(pady=1, anchor="w")
            tk.Label(frame, text=field.replace("_", " ").title()+":", width=21, anchor="w", bg=FRAME_BG, fg=LABEL_FG, font=FONT_LABEL).pack(side=tk.LEFT)
            entry = tk.Entry(frame, width=20, font=FONT_LABEL)
            entry.pack(side=tk.LEFT)
            self.inspection_entries[field] = entry
        button_frame = tk.Frame(inspection_frame, bg=FRAME_BG)
        button_frame.pack(pady=4)
        tk.Button(button_frame, text="Muayene Ekle", command=self.add_inspection, width=15, bg=BUTTON_BG, fg=BUTTON_FG, font=FONT_LABEL, activebackground="#35507a").pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Muayene Güncelle", command=self.update_inspection, width=15, bg=BUTTON_BG, fg=BUTTON_FG, font=FONT_LABEL, activebackground="#35507a").pack(side=tk.LEFT, padx=5)

        # Sigorta
        insurance_frame = tk.Frame(container, bg=FRAME_BG, bd=2, relief="groove")
        insurance_frame.pack(side=tk.LEFT, padx=20, pady=5, fill='y')
        insurance_header = tk.Frame(insurance_frame, bg=FRAME_BG)
        insurance_header.pack(anchor="w", pady=(5, 2))
        tk.Label(insurance_header, image=self.icon_sigorta, bg=FRAME_BG).pack(side=tk.LEFT, padx=(0, 6))
        tk.Label(insurance_header, text="Sigorta Ekle", font=("Arial", 12, "bold"), bg=FRAME_BG, fg=LABEL_FG).pack(side=tk.LEFT)

        self.insurance_entries = {}
        insurance_fields = [
            "vehicle_id", "insurance_type", "insurance_company", "policy_number",
            "policy_amount", "start_date", "end_date", "status"
        ]
        for field in insurance_fields:
            frame = tk.Frame(insurance_frame, bg=FRAME_BG)
            frame.pack(pady=1, anchor="w")
            tk.Label(frame, text=field.replace("_", " ").title()+":", width=21, anchor="w", bg=FRAME_BG, fg=LABEL_FG, font=FONT_LABEL).pack(side=tk.LEFT)
            entry = tk.Entry(frame, width=20, font=FONT_LABEL)
            entry.pack(side=tk.LEFT)
            self.insurance_entries[field] = entry
        tk.Button(insurance_frame, text="Sigorta Ekle", command=self.add_insurance, width=20, bg=BUTTON_BG, fg=BUTTON_FG, font=FONT_LABEL, activebackground="#35507a").pack(pady=7)

        self.admin_area.pack(pady=12)

    def admin_login_popup(self):
        if not getattr(self, "is_admin_logged_in", False):
            login_window = LoginWindow(self)
            self.wait_window(login_window)
            if login_window.result:
                self.is_admin_logged_in = True
                self.admin_login_btn.config(state="disabled", text="Admin Giriş Yapıldı")
                self.show_admin_widgets()
            else:
                messagebox.showerror("Hata", "Admin girişi başarısız!")
        else:
            messagebox.showinfo("Bilgi", "Zaten admin girişi yaptınız.")

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
