class Insurance():
    def __init__(self,vehicle_id,insurance_type,insurance_company,policy_number,policy_amount,start_date,end_date,status):
        self.vehicle_id = vehicle_id
        self.insurance_type = insurance_type
        self.insurance_company = insurance_company
        self.policy_number = policy_number
        self.policy_amount = policy_amount
        self.start_date = start_date
        self.end_date = end_date
        self.status = status

    def show_insurance_info(self):
        return (
            f"Vehicle Id: {self.vehicle_id}\n"
            f"Insurance Type: {self.insurance_type}\n"
            f"Insurance Company: {self.insurance_company}\n"
            f"Policy Number: {self.policy_number}\n"
            f"Policy Amount: {self.policy_amount}\n"
            f"Status : {self.status}"
            f"Start Date: {self.start_date}\n"
            f"End Date: {self.end_date}\n"
        )