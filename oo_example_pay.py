#base class == employe all employ log hours, allowed vacation time, can take vacation time 
#two derived employees one gets payed on salary, They other is payed an hourly rate 
class employe(): 
    def __init__ (self,name, pto  ):
        self.name = name
        self.pto = pto 
        self.hours = 0 
        self.taken_pto = 0 
    def log_hours(self, hours):
        self.hours = self.hours +hours
        return f"{self.name} has logged {self.hours} hous"
    def take_pto(self, twotake):
        self.taken_pto = self.taken_pto + twotake
        if self.taken_pto > self.pto:
            return f"{self.name} has no more vacatuion time he has exceeded his time by {abs(self.pto -self.taken_pto )} days" 
        else:
            return f"{self.name} has taken {self.taken_pto} days out of his maxium of {self.pto} he has {abs(self.pto - self.taken_pto)  } days left"
    def calc_pay (self):
        pass

class hourly(employe):
    def __init__ (self, name, pto, rate ):
        super().__init__ (name,pto)
        self.rate = rate
    def calc_pay (self):
        return f" {self.name} has earned {self.rate * self.hours} dollars after being a good little capatilist for {self.hours} hours"

class salery(employe):
    def __init__ (self, name, pto, pay ):
        super().__init__ (name,pto)
        self.pay = pay
    def calc_pay(self):
        return f"{self.name} has earned {self.pay} after a whole week of work, he did such a good job!!! "
    


bob = salery ( "Kyle", 10, 40)
sam = hourly ("Bill" , 10 , 5)        
print (bob.log_hours(5) , " ",  bob.take_pto (9)," ", bob.calc_pay() )
print (sam.log_hours(5), sam.take_pto(9), " ",   sam.calc_pay())
