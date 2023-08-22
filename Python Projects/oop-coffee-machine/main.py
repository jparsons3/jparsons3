from menu import Menu, MenuItem
from coffee_maker import CoffeeMaker
from money_machine import MoneyMachine

MACHINE_ON = True

coffeemachine = CoffeeMaker()
coffeemenu = Menu()
transaction = MoneyMachine()
options = coffeemenu.get_items()

while MACHINE_ON: 
    user_input = input(f"What would you like? ({options}): ").lower()
    if user_input == "off":
        MACHINE_ON = False
    elif user_input == "report": 
        coffeemachine.report()
        transaction.report()
    elif user_input == "espresso" or user_input == "latte" or user_input == "cappuccino":
        selection = coffeemenu.find_drink(user_input)
        #print(f"this is the {user_input} price: ${selection.cost}")
        if coffeemachine.is_resource_sufficient(selection) == True:
            if transaction.make_payment(selection.cost):
                coffeemachine.make_coffee(selection)
            
            
            
