from ApplicationLayer.VaccineDTO import VaccineDTO
from PersistanceLayer.ClinicDAO import _ClinicDAO
from PersistanceLayer.LogisticDAO import _LogisticDAO
from PersistanceLayer.VaccineDAO import _VaccineDAO
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
                # getting the order sent data
                location=order[0]
                amount=order[1]
                # getting the Clinic's logistic who sent the order
                clinic = self.get_clinic_logistic(location)
                clinic.demand = str(int(clinic.demand) - int(amount))
                _ClinicDAO().update(clinic)
                logistic = self.Logistics[clinic.logistic]
                # finished updating the logistic's sent amount
                logistic.count_sent= str(int(logistic.count_sent) + int(amount))
                _LogisticDAO().update_sent(logistic)
                # removing inventory
                while int(amount)>=0:
                    for vaccine in self.sorted_vaccines_by_Date():
                        if int(vaccine.quantity) >= int(amount):
                            vaccine.quantity= str(int(vaccine.quantity) - int(amount))
                            _VaccineDAO().update(vaccine)
                            amount=-1
                        else:
                            amount = str(int(amount) - int(vaccine.quantity))
                            del self.Vaccines[vaccine.id]
                            _VaccineDAO().delete(vaccine)
                # finished reducing the inventory
            elif len(order)==3:
                # getting the order received data
                sup_name=order[0]
                amount=order[1]
                date=order[2]
                # getting the supplier's id who delivered the order
                supplier = self.get_supplier_by_name(sup_name)
                # getting the next unused vaccine id
                nextID=str(self.find_id())
                vaccine = VaccineDTO(nextID,date,supplier.id, amount)
                self.Vaccines[vaccine.id]=vaccine
                _VaccineDAO().insert(vaccine)
                # finished adding new vaccine to the data base and dict
                logistic = self.Logistics[supplier.id]
                logistic.count_received = str(int(logistic.count_received)+int(amount))
                _LogisticDAO().update_received(logistic)
                # finished updating the logistic's received amount
            self.write_to_output_file()
        pass

    def get_orders_file(self, orders_file_path):
        with open(".\\" + orders_file_path, "r", encoding="utf-8") as ordersFile:
            rows = ordersFile.read().split("\n")
            for row in rows:
                data = row.split(",")
                self.Orders.append(data)
        pass


    def write_to_output_file(self):
        with open(".\\output.txt","a", encoding="utf-8") as outputFile:
            invent = self.get_total_inventory()[0]
            demand = self.get_total_demand()[0]
            received = self.get_total_received()[0]
            sent = self.get_total_sent()[0]
            out = str(invent)+","+str(demand)+","+str(received)+","+str(sent)+"\n"
            outputFile.write(out)
        pass

    def get_supplier_by_name(self,sup_name):
        for supplier in self.Suppliers.values():
            if supplier.name==sup_name:
                return supplier
        return None

    def get_clinic_logistic(self,clinic_location):
        for clinic in self.Clinics.values():
            if clinic.location == clinic_location:
                return clinic
        return None

    def sorted_vaccines_by_Date(self):
        output=[]
        index = 0
        for obj in _Repository().dates_sorted():
            output.insert(index, self.get_vaccine(obj[0]))
            index+=1
        return output

    def get_vaccine(self,vaccine_id):
        for vaccine in self.Vaccines.keys():
            if vaccine_id == int(vaccine):
                return self.Vaccines[vaccine]
        return None

    def get_total_inventory(self):
        return _Repository().total_vaccines()[0]

    def get_total_sent(self):
        return _Repository().total_sent()[0]

    def get_total_received(self):
        return _Repository().total_received()[0]

    def get_total_demand(self):
        return _Repository().total_demand()[0]
