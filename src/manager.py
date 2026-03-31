from src.models import Apartment, Bill, Parameters, Tenant, Transfer


class Manager:
    def __init__(self, parameters: Parameters):
        self.parameters = parameters 

        self.apartments = {}
        self.tenants = {}
        self.transfers = []
        self.bills = []
       
        self.load_data()

    def load_data(self):
        self.apartments = Apartment.from_json_file(self.parameters.apartments_json_path)
        self.tenants = Tenant.from_json_file(self.parameters.tenants_json_path)
        self.transfers = Transfer.from_json_file(self.parameters.transfers_json_path)
        self.bills = Bill.from_json_file(self.parameters.bills_json_path)

    def check_tenants_apartment_keys(self) -> bool:
        for tenant in self.tenants.values():
            if tenant.apartment not in self.apartments:
                return False
        return True
    
    def get_apartment_costs(self, apartment_key, year, month):
        total = 0
        for bill in self.bills:
            if apartment_key != bill.apartment:
                continue
            if month != bill.settlement_month:
                continue
            total += bill.amount_pln
        return total
    
    # class Bill(BaseModel):
    # amount_pln: float
    # date_due: str
    # apartment: str
    # settlement_year: int
    # settlement_month: int
    # type: str

    # @staticmethod
    # def from_json_file(file_path: str) -> List['Bill']:
    #     data = None
    #     with open(file_path, 'r') as file:
    #         data = json.load(file)
    #     assert isinstance(data, list), "Expected a list of bills"
    #     return [Bill(**bill) for bill in data]