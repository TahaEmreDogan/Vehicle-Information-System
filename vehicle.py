class Vehicle:
    def __init__(self, id, plate, brand, model, status, vehicle_type):
        self.id = id
        self.plate = plate
        self.brand = brand
        self.model = model
        self.status = status
        self.vehicle_type = vehicle_type

    def details(self):
        return (
            f"Id: {self.id}\n"
            f"Plate: {self.plate}\n"
            f"Brand: {self.brand}\n"
            f"Model: {self.model}\n"
            f"Status: {self.status}\n"
            f"Vehicle Type: {self.vehicle_type}"
        )
