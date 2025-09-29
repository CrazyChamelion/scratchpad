# class that stores worlkout, arobic , anerobic name, minutes, hours 
# class that stores meals, name,  calories, fat, carbs, protein 
# class that stores day, workout and meals
# enum == days of week 
# month
# year

class workout:  
    def __init__ (self, arboic, anerobic, name, time, cal ): 
        self.arobic = arboic
        self.anerobic = anerobic
        self.name = name
        self.time = time 
        self.type = "workout"
        self.cal = cal
    def __str__ (self):
        return f" {self.type}, {self.name}, arobic is {self.arobic}, aneroic is {self.anerobic}, time is {self.time} cal is {self.cal}"
    def __repr__(self):
        return self.__str__()

class meal:  
    def __init__ (self,  calorie, name, fat, carb, protien, fiber, ): 
        self.calorie = calorie
        self.name = name
        self.fat = fat
        self.carb = carb
        self.protien = protien
        self.fiber = fiber
        self.type = "meal"
    def __str__ (self):
        return f" {self.type}, {self.name}, calorie count is {self.calorie}, grams of fat are {self.fat}, grams of carbs are {self.carb} , grams of protien are {self.protien}, grams of fiber are {self.fiber} "    
    def __repr__(self):
        return self.__str__()

class day:
    def __init__ (self, day , meal1 , meal2, meal3 , workout1, workout2):
        self.meal1 = meal1
        self.meal2 = meal2 
        self.meal3 = meal3 
        self.workout1 = workout1
        self.workout2 = workout2 
        self.meals = []
        self.workouts = []
        self.meals.append (self.meal1 )
        self.meals.append (self.meal2)
        self.meals.append (self.meal3)
        self.workouts.append (self.workout1)
        self.workouts.append (self.workout2)
        self.day = day

    def total_workout(self):
        tcalbrn = 0
        for w in self.workouts:
            tcalbrn = tcalbrn + w.cal
        return tcalbrn
    
    def total_food (self):
        tcaleat = 0 
        for w in self.meals:
            tcaleat = tcaleat +w.calorie
        return tcaleat
    
    def __str__ (self):
        return f"  {self.day }, meals are {self.meals}, workouts are {self.workouts}  "
    
    def __repr__(self):
        return self.__str__()

class week:
    def __init__ (self):
        self.days=[]
    def add_day(self,day):
        self.days.append (day)
    def __str__ (self):
        return f"{self.days} "
    def __repr__(self):
        return self.__str__()
         
    def lost_weight(self):
        cal_gain = 0
        cal_loss = 0
        for d in self.days:
            cal_gain = cal_gain + d.total_food()
            cal_loss = cal_loss + d.total_workout()
        if cal_gain < cal_loss:
            return True
        return False
        

tennis = workout(3 , 2 , "tennis" , 100 , 69)
running = workout(4 , 2 , "running" , 60 , 67)
pizza = meal (800 , "pizza" , 60 , 80, 1, 3)
salad = meal (400 , "salad" , 0 , 10, 5, 5)
tacos = meal (600 , "tacos" , 30 , 15, 10, 3)


monday = day ("Monday" , pizza, salad, tacos, running , tennis )

week1 = week ()
week1.add_day(monday)

print (monday.total_workout ())
print (monday.total_food ())
print (week1.lost_weight())

#print (tennis)
#print (running)
#print (pizza)
#print (monday)
#print (week1)
