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

    def load_data(self):
        repo = _Repository()
        repo.load_project(self)
        self.get_orders_file("orders.txt")
    pass

    def run(self):
        # print(self.Vaccines)
        # print(self.Suppliers)
        # print(self.Clinics)
        # print(self.Logistics)
        # print(self.Orders)
        for order in self.Orders:
            if len(order)==2:
                location=order[0]
                amount=order[1]

            elif len(order)==3:
                sup_name=order[0]
                amount=order[1]
                date=order[2]
                vaccine = VaccineDTO()

        pass

    def get_orders_file(self, orders_file_path):
        with open(".\\" + orders_file_path, "r", encoding="utf-8") as ordersFile:
            rows = ordersFile.read().split("\n")
            for row in rows:
                data = row.split(",")
                self.Orders.append(data)

        pass



