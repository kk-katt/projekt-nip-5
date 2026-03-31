from src.models import Apartment, Bill, Parameters, Tenant, Transfer, ApartmentSettlement


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
    
    def get_apartment_costs(self, apartment_key, year=None, month=None):
        if apartment_key not in self.apartments:
            return None
        total = 0
        for bill in self.bills:
            if apartment_key != bill.apartment:
                continue
            if year != bill.settlement_year and year != None:
                continue
            if month != bill.settlement_month and month != None:
                continue
            total += bill.amount_pln
        return total
    
    def get_settlement_costs(self, apartment_key, year, month):
        if apartment_key not in self.apartments:
            return None
        total = 0
        for tenant in self.tenants.values():
            if tenant.apartment == apartment_key:
                total += tenant.rent_pln
        settlement = ApartmentSettlement(
            apartment = apartment_key,
            year = year,
            month = month,
            total_bills_pln = self.get_apartment_costs(apartment_key, year, month),
            total_rent_pln = total,
            total_due_pln = self.get_apartment_costs(apartment_key, year, month) + total,
        )
        total = settlement.total_rent_pln
        return total
    
    def get_settlement_costs(self, apartment_key, year, month):
        if apartment_key not in self.apartments:
            return None
        bills = self.get_apartment_costs(apartment_key, year, month)
        if bills == 0 or bills is None:
            return 0
        total_rent = 0
        for tenant in self.tenants.values():
            if tenant.apartment == apartment_key:
                total_rent += tenant.rent_pln
        return total_rent
        
    def get_settlement_cost_for_tenent(self, apartment_key, tenant, year=None, month=None):
        total_rent = 0
        bill_sum = 0
        if apartment_key not in self.apartments:
            return None
        for tenantl in self.tenants.values():
            if tenant == tenantl.name:
                total_rent += tenantl.rent_pln
                
        for bill in self.bills:
            if  bill.apartment != apartment_key or bill.settlement_month != month or bill.settlement_year != year:
                continue
            bill_sum += bill.amount_pln
            
        bill_sum = bill_sum / len(self.tenants)
        
        return bill_sum + total_rent
        