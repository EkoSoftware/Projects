import os
from tkinter import filedialog
import json


class Inköpslista:
    def __init__(self):
        self.clear_screen = 'cls' if os.name == 'nt' else 'clear'
        
        self.home = {"Gul Lök": 20,                                                                 # Lite basråvaror som jag bjuder på.
                     "Paprika": 9,                                                     
                     "Tomater": 10,
                     "Kött": 7,
                     "Ägg": 30,}
        
        self.shopping_list = {}
        
        self.navigation = {"1":    lambda: self.get_ShoppingList(),                                # Lambda funktionen tillåter programmet att associera ett index med en annan funktion/metod
                           "List": lambda: self.get_ShoppingList(),
                           "2":    lambda: self.get_ItemsAtHome(),
                           "Cupboard": lambda: self.get_ItemsAtHome(),
                           "3":    lambda: self.add_purchase(),
                           "Add":  lambda: self.add_purchase(),
                           "4":    lambda: self.remove_purchase(),
                           "Remove": lambda: self.remove_purchase(),
                           "5":    lambda: self.edit_purchase(),
                           "Edit": lambda: self.edit_purchase(),
                           "9":    lambda: self.start_screen(),
                           "Main": lambda: self.start_screen(),
                           "Exit": lambda: self.start_screen(),
                           "Save": lambda: self.save_file(),
                           "Load": lambda: self.load_file()}
        
    
        """
        Användargränssnitt:
        """
    
    def print_interface(self):                                                      # Jag valde att skapa en funktion som skriver ut gränssnittet när den anropas.
        os.system(self.clear_screen)                                                              # För att göra koden så kortfattad som möjligt.
        print("-"*76)
        print("[1. View List] [2. View Cupboard] [3. Add] [4. Remove] [5. Edit] | [9. Main] ")
        print("-"*76)
        
    
    def print_items(self):                                                                      # Samma här
        print(f"\tItem : Amount",end=""); print("Checked Item : Amount".rjust(50))
        
        for item, amount in self.shopping_list.items(): 
            if not self.shopping_list[item][1]:
                print(f"{item.title()} : {amount[0]}")
            else:
                print(f"{'[x]'+item.title():>60} : {amount[0]}")
        
    def start_screen(self):
        self.print_interface()                                                            # Ibland är det svårt att komma ihåg vem man hälsat på.
        print("[Save] File \t [Load] File".center(70))
        print(("What would you like to do? ".center(76)))
        choice = input("> ".rjust(36)).strip().title()
        if choice in self.navigation.keys(): self.navigation[choice]()
            
    def strikethrough(self, text):
        text, result = str(text), ''
        for char in text: result = result + char + '\u0336'
        return result
    
        """
        Dom riktiga hjältarna:
        """
   
    
    
    def get_ShoppingList(self):                                                                 
        self.print_interface()
        self.print_items()
        
        print("-"*76)
        print("Enter an items name to mark it as checked.")

        while True:                                                                                         # Loopar funktionen om man inte gör ett gitligt val
            item = input("Check> ").strip().title()                                                # Så att man inte kan skita ner terminalen med text.
            if item in self.navigation.keys(): self.navigation[item](); break                      
            elif item in self.shopping_list.keys(): 
                if self.shopping_list[item][1] == False:        
                    self.shopping_list[item][1] = True
                elif self.shopping_list[item][1] == True:
                    self.shopping_list[item][1] = False
                    
                
            elif item not in self.shopping_list.keys():
                self.get_ShoppingList();break        
            self.get_ShoppingList()
            
    def get_ItemsAtHome(self):
        self.print_interface()
        print("Ingredients in storage:\n","-"*76, sep="")
        
        for key, value in self.home.items(): print(f"{key} : {value}")                          
        
        while True: 
            choice = input().strip().title()
            if choice in self.navigation.keys(): self.navigation[choice](); break
            else: self.get_ItemsAtHome()
    
        
    def add_purchase(self):                                                                                 
        self.print_interface()
        self.print_items()
        print("-"*76)                                                           
        
        while True:                                                                                 # Har placerat användaren i loop för att inte kunna skita ner gränssnittet med onödig text
            item = input("Enter an item:\n> ").strip().title()                                      # Navigationssiffrorna fungerar så länge inte siffor ska slås in
            if item in self.navigation.keys(): self.navigation[item](); break
            elif item == "": self.add_purchase(); break
            elif item in self.shopping_list.keys(): print(f"{item} is already in your list."); continue
            
            while True:
                amount = input("Amount of item:\t\t\t\t\t\t    \"exit\" to cancel\nAdd> ")             # La in ett avslutskommando ifall man ångrar sig.
                if amount == "exit": self.add_purchase()
                elif amount != "":
                    self.shopping_list[item] = [amount, False, self.strikethrough(item)]
                    self.add_purchase()
                    break                                                                    
                    
                else: print(f"Invalid input: {amount}, please use numerical values.")
            break
         
    def remove_purchase(self):
        self.print_interface()
        self.print_items()
        print("-"*76)
        

        while True:
            item = input("Item to remove ?\nRemove> ").strip().title()
            if item in self.navigation.keys(): self.navigation[item](); break
            elif item == "": self.remove_purchase(); break
            elif item in self.shopping_list.keys():
                self.shopping_list.pop(item)
                self.remove_purchase();break
            else:
                print(f"{item} does not exist, please check for spelling errors.")
        
        
    def edit_purchase(self):
        self.print_interface()
        self.print_items()
        print("-"*76)
        while True:
            item = input("Which item would you like to edit?\nEdit> ").strip().title()
            if item in self.navigation.keys(): self.navigation[item](); break

            elif item in self.shopping_list.keys():
                while True:
                    amount = input("New value?\t\t\t\t\t\t    \"Cancel\"to cancel\n").strip().title()
                    if amount == "Cancel": self.edit_purchase(); break 
                    elif amount != "": 
                        self.shopping_list[item][0] = amount
                        self.edit_purchase()
                        break
                    else: print("Invalid input.")

            elif item not in self.shopping_list.keys(): 
                print(f"{item} does not exist, please check for spelling errors.")
                

    def save_file(self):                                                                        # Jag valde att spara filerna i Javascript Object Notation
        self.print_interface()                                                                  # Eftersom det används som en länk emellan olika programmeringspråk.
        self.print_items()                                                                      
        print("-"*76)                                                                           
        
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")])
        
        if file_path:
            with open(file_path, 'w') as fp:
                json.dump(self.shopping_list, fp)
        
        input("File saved successfully...\nPress \"Enter\" to continue.")
        self.start_screen()

                    
    def load_file(self):
        self.print_interface()
        self.print_items()
        print("-"*76)
        
        load_path = filedialog.askopenfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")])
        if load_path:
            with open(load_path, "r") as fp:
                load_dict = json.load(fp)
            self.shopping_list.update(load_dict)
        self.get_ShoppingList()    
        
        
            
"""
Main loop
"""
############
shop = Inköpslista()
while True: 
    shop.start_screen()
    
    
