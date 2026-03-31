from src.models import Bill
from src.manager import Manager
from src.models import Parameters

def test_sum_of_apartment_costs ():
    parameters = Parameters()
    manager = Manager(parameters)
    assert manager.get_apartment_costs('apart-polanka', 2025, 1) == 910.00
    assert manager.get_apartment_costs('apart-polanka', 2025, 2) == 0
    assert manager.get_apartment_costs('apart-polanka-2', 2025, 1) == 0

