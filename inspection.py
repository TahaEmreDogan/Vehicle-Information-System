class Inspection:
    def __init__(self, vehicle_id, inspection_type, inspection_date, inspection_price, inspection_result, next_inspection_date, inspection_personnel, inspection_description):
        self.vehicle_id = vehicle_id
        self.inspection_type = inspection_type
        self.inspection_date = inspection_date
        self.inspection_price = inspection_price
        self.inspection_result = inspection_result
        self.next_inspection_date = next_inspection_date
        self.inspection_personnel = inspection_personnel
        self.inspection_description = inspection_description

    def details(self):
        return (
            f"Vehicle Id : {self.vehicle_id}\n"
            f"Inspection Type : {self.inspection_type}\n"
            f"Inspection Date : {self.inspection_date}\n"
            f"Inspection Price : {self.inspection_price}\n"
            f"Inspection Result : {self.inspection_result}\n"
            f"Next Inspection Date : {self.next_inspection_date}\n"
            f"Inspection Personnel : {self.inspection_personnel}\n"
            f"Inspection Description : {self.inspection_description}\n"
        )
