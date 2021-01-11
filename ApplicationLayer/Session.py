from ApplicationLayer.VaccineDTO import VaccineDTO
from PersistanceLayer.LogisticDAO import _LogisticDAO
from Repo.Repository import _Repository


class Session:
    Vaccines = {}
    Suppliers = {}
    Clinics = {}
    Logistics = {}
    Orders = []

    def __init__(self):
        self.load_data()

    def find_id(self):
        max=0
        for key in self.Vaccines.keys():
            if int(key) > int(max):
                max = int(key)
        return max+1

    def load_data(self):
        repo = _Repository()
        repo.load_project(self)
        self.get_orders_file("orders.txt")
    pass

    def run(self):
        for order in self.Orders:
            if len(order)==2:
                location=order[0]
                amount=order[1]

            elif len(order)==3:

                sup_name=order[0]
                amount=order[1]
                date=order[2]
                supplier = self.get_supplier_by_name(sup_name)
                vaccine = VaccineDTO(str(self.find_id()),date,supplier.id, amount)

                logistic = self.Logistics[supplier.id]
                logistic.count_received += amount
                _LogisticDAO().update(logistic)



        pass

    def get_orders_file(self, orders_file_path):
        with open(".\\" + orders_file_path, "r", encoding="utf-8") as ordersFile:
            rows = ordersFile.read().split("\n")
            for row in rows:
                data = row.split(",")
                self.Orders.append(data)
        pass


    def write_to_output_file(self):
        pass

    def get_supplier_by_name(self,sup_name):
        for supplier in self.Suppliers.values():
            if(supplier.name==sup_name):
                return supplier
        return None
