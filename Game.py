import random
import csv

class entity:
    
    def __init__(self, attack, defence, name, level, health_bar, heal_item, heavy_attack, magic, magic_def):
        self.name = name
        self.defence = defence
        self.attack = attack
        self.health_bar = health_bar
        self.level = level
        self.heal_item = heal_item
        self.magic = magic
        self.heavy_attack = heavy_attack
        self.magic_def = magic_def
        self.max_health = health_bar

    def take_damage(self, damage, damage_type):
        points = 0
        if damage_type == "a":
            points = damage - self.defence / 2
        elif damage_type == "m":
            points = damage - self.magic_def / 2
        
        if points < 0:
            points = 0
        
        self.health_bar -= points

        return points

    def heal(self):
        if self.heal_item > 0:
            self.heal_item -= 1
            self.health_bar += 35
            if self.health_bar > self.max_health:
                self.health_bar = self.max_health    
    
class Boss(entity):
    boss_counter = 0

    def __init__(self, attack, defence, name, level, health_bar, heal_item, heavy_attack, magic, magic_def, type_p, hint, xp):
        super().__init__(attack, defence, name, level, health_bar, heal_item, heavy_attack, magic, magic_def)
        self.type_p = type_p
        self.hint = hint
        if self.type_p == "brute":
            self.heavy_attack_charge = 5
        else:
            self.heavy_attack_charge = 3
        self.xp_on_death = xp
        
    def type_p_string(self):
        type_p = ""
        if self.type_p == "mag":
            type_p = "a powerful wizzard"
        elif self.type_p == "brute":
            type_p = "a strong brute"
        elif self.type_p == "mix":
            type_p = "a swordsman with wizarding capabilities"
        return type_p

    def __repr__(self):
        type_p = Boss.type_p_string(self)
        description = "{name} is a level {level} boss and {type}. {hint}".format(name = self.name, level = self.level, type = type_p, hint = self.hint)
        return description
    
    def boss_take_damage(self, damage, type_damage):
        points = super().take_damage(damage, type_damage)
        if self.health_bar > 0:
            print("{name} has taken {points} points of damage, their health is now at {health} points".format(name = self.name, points = points, health = self.health_bar))
        else:
            print("{name} has been defeated!".format(name = self.name))

    def attack_player(self, target):
        action = random.randint(1, 3)
        
        #Brute Boss
        if self.type_p == "brute":
            if action == 1:
                print("{name} performs heavy attack!".format(name = self.name))
                target.player_take_damage(self.heavy_attack, "a")
            elif action == 2 or action == 3:
                print("{name} attacks!".format(name = self.name,))
                target.take_damage(self.attack, "a")
        
        #Magic Boss
        elif self.type_p == "mag":
            print("{name} casts a spell!".format(name = self.name))
            target.player_take_damage(self.magic, "m")
        
        #Mix Boss
        elif self.type_p == "mix":
            if action == 1:
                if self.heavy_attack_charge == 0:
                    target.player_take_damage(self.heavy_attack / 4, 'a')
                    print("{name} attempts heavy attack but fails!".format(name = self.name))
                else:
                    print("{name} performs heavy attack!".format(name = self.name))
                    self.heavy_attack_charge -= 1
                target.player_take_damage(self.heavy_attack, "a")
            elif action == 2:
                print("{name} attacks!".format(name = self.name))
                target.player_take_damage(self.attack, "a")
            elif action == 3:
                print("{name} casts a spell!".format(name = self.name))
                target.player_take_damage(self.magic, "a")
        
    def boss_heal(self):
        super().heal()
        print("{name} has healed. They are now at {health_bar} health points".format(name = self.name, health_bar = self.health_bar))

class Player(entity):
    player_xp_level_req = [50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 1000]

    def __init__(self, name, health_bar, attack, defence, level, xp, heal_item, boss_level, magic, heavy_attack, magic_def):
        super().__init__(attack, defence, name, level, health_bar, heal_item, heavy_attack, magic, magic_def)
        self.level = level
        self.xp = xp
        self.boss_level = boss_level
        self.heavy_attack_charge = 3
    
    def __repr__(self):
        description = "{name}, here are your stats: level {level}, attack {attack}, heavy attack {heavy}, defence {defence}, magic, {magic}, magic defence {magic_def}, max health {health} .".format(name = self.name, level = self.level, attack = self.attack, defence = self.defence, heavy = self.heavy_attack, magic_def = self.magic_def, magic = self.magic, health = self.max_health)
        return description

    def if_boss_dead(self, target):
        if target.health_bar <= 0:
            print("{xp}xp for defeating the boss, keep it up!".format(xp = boss.xp_on_death))
            self.gain_xp(boss.xp_on_death)

    def attack_boss(self, target, type):
        
        if type == "a": #attack
            print("{name} attacks! 5xp gained".format(name  = self.name))
            target.boss_take_damage(self.attack, "a")
        
        if type == "m": #magic
            print("{name} casts magic! 5xp gained".format(name  = self.name))
            target.boss_take_damage(self.magic, "m")
        
        if type == "h": #heavy_attack
            if self.heavy_attack_charge == 0:
                print("{name} attempts heavy attack but fails!".format(name  = self.name))
                print("Hint: You only have energy for 3 heavy attacks per fight")
                target.boss_take_damage(self.heavy_attack / 4, "a")
                self.if_boss_dead(target)
                return
            else: 
                print("{name} performs heavy attack! 5xp gained".format(name  = self.name))
                target.boss_take_damage(self.heavy_attack, "a")
                self.heavy_attack_charge -= 1

        self.gain_xp(5)
        self.if_boss_dead(target)
    
    def player_take_damage(self, damage, type):
        points = super().take_damage(damage, type)
        if self.health_bar > 0:       
            print("You have taken {points} points of damage, your health is now at {health} points".format(points = points, health = self.health_bar))
        else:
            print("You have been defeated!")

    def player_heal(self):
        if self.heal_item == 0:
            print("You have no healing potions, you have wasted a turn!")
        else:
            if self.health_bar == self.max_health:
                print("You have wasted a healing potion!")
                self.heal_item -= 1
            else:
                super().heal()
                print("You are now at {health_bar} health points".format(health_bar = self.health_bar))
        
    def new_heal_item(self):
        self.heal_item += 1
        print("You have earned a health potion, you now have {heal_item}.".format(heal_item = self.heal_item))
  
    def gain_xp(self, xp):
        self.xp += xp
        if self.xp > self.player_xp_level_req[self.level - 1]:
            self.level_up()
        print("XP: {xp}/{req}".format(xp = self.xp, req = self.player_xp_level_req[self.level - 1]))

    #levels up user and upgrades stats
    def level_up(self):
        self.xp = self.xp - self.player_xp_level_req[self.level - 1]
        self.level += 1
        print("Congrats you are now level {level}!".format(level = self.level))
        
        valid_input = False
        while valid_input == False:
            print("Choose two stats you would like to upgrade e.g. 1/3 upgrades attack and magic or 1/1 to upgrade attack twice ")
            user_upgrade = input("Attack: 1, Heavy Attack: 2, Magic: 3, Magic Defence: 4, Defence: 5: ")
            split_strings = user_upgrade.split("/")
            
            invalid_input = False
            for num in split_strings:
                if num == "1":
                    self.attack += 6
                elif num == "2":
                    self.heavy_attack += 6
                elif num == "3":
                    self.magic += 6
                elif num == "4":
                    self.magic_def += 6
                elif num == "5":
                    self.defence += 6
                else:
                    invalid_input = True
                    print("Invalid input :(")
            
            if invalid_input == False:
                valid_input = True
        
        self.max_health += 20
        print(player)

    #saves players stats
    def save_to_csv(self):
        filename = "{name}'s_player_profile.csv".format(name = self.name)
        fieldnames = ["name", "attack", "defence", "level", "xp", "heal_item", "boss_level", "magic", "heavy_attack", "magic_def"]
        
        list_of_attributes = {
            "name": self.name,
            "attack": self.attack,
            "defence": self.defence,
            "level": self.level,
            "xp": self.xp,
            "heal_item": self.heal_item,
            "boss_level": self.boss_level,
            "magic": self.magic,
            "heavy_attack": self.heavy_attack,
            "magic_def": self.magic_def
        }
        
        with open(filename, 'w') as file:
            writer_object = csv.DictWriter(file, fieldnames = fieldnames)
            writer_object.writeheader()
            writer_object.writerow(list_of_attributes)

    #loads an existing player's profile
    def load_csv(self):
        filename = "{name}'s_player_profile.csv".format(name = self.name)
        with open(filename, 'r') as file:
            reader_object = csv.DictReader(file)
            attributes = [row for row in reader_object]
            
            player_data = attributes[0]

            self.name = player_data["name"]
            self.attack = int(player_data["attack"])
            self.defence = int(player_data["defence"])
            self.level = int(player_data["level"])
            self.xp = int(player_data["xp"])
            self.heal_item = int(player_data["heal_item"])
            self.boss_level = int(player_data["boss_level"])
            self.magic = int(player_data["magic"])
            self.heavy_attack = int(player_data["heavy_attack"])
            self.magic_def = int(player_data["magic_def"])
    
    #Adds a new player to the valid user csv
    def add_valid_user(self):
        with open("user_check.csv", 'a') as file:
            file_writer = csv.writer(file)
            file_writer.writerow([self.name.upper()])

#Creates player with default starting attributes
def create_player(name):
    new_player = Player(name, 100, 10, 20, 1, 0, 1, 1, 10, 20, 5)
    return new_player

#Creates boss from CSV
def create_boss(level):
    with open("Boss_profiles.csv", 'r') as boss_file:
        reader_object = csv.DictReader(boss_file)
        boss_dict = {}
        for boss in reader_object:
            if boss["level"] == str(level):
                boss_dict = boss
        
        level = boss_dict["level"]
        name = boss_dict["name"]
        defence = boss_dict["defence"]
        attack = boss_dict["attack"]
        health_bar = boss_dict["health_bar"]
        heal_item = boss_dict["heal_item"]
        magic = boss_dict["magic"]
        heavy_attack = boss_dict["heavy_attack"]
        magic_def = boss_dict["magic_def"]
        type_p = boss_dict["type_p"]
        hint = boss_dict["hint"]
        xp = boss_dict["xp_on_death"]

        boss_object = Boss(int(attack), int(defence), name, int(level), int(health_bar), int(heal_item), int(heavy_attack), int(magic), int(magic_def), type_p, hint, int(xp))
        return boss_object

#Random question generator
def question_generator(level):
    num1 = random.randint(1, 10 * level)
    num2 = random.randint(1, 10 * level)
    
    symbols = ["+", "-"]
    if level > 3:
        symbols = ["+", "-", "/"]
    elif level > 5:
        symbols = ["+", "-", "/", "*"]
    
    symbol = random.choice(symbols)

    if symbol == "+":
        answer = num1 + num2
        string = "What is {num1} + {num2}?".format(num1 = num1, num2 = num2)
        return string, answer
        
    if symbol == "-":
        answer = num1 - num2
        string = "What is {num1} - {num2}?".format(num1 = num1, num2 = num2)
        return string, answer

    if symbol == "*":
        num1 = random.randint(1, 12)
        
        answer = num1 * num2
        string = "What is {num1} * {num2}?".format(num1 = num1, num2 = num2)
        return string, answer 

    if symbol == "/":
        #Divide generates its own numbers else questions are unreasonably difficult
        num1 = random.randint(2, 10 * level)
        num2 = random.randint(2, 4)
        
        answer = num1 / num2
        string = "What is {num1} / {num2}?".format(num1 = num1, num2 = num2)
        
        if answer.is_integer():
            answer = int(answer)
        
        return string, answer          

#Asks question, returns True if correct, False if not
def ask_question(question, answer):
    print(question)
    user = input("Answer: ")
    if user == str(answer):
        return True
    else:
        return False

#Checks for existing user
def user_check(name):
    with open("user_check.csv", 'r') as file:
        reader_object = csv.DictReader(file)
        contents = [row for row in reader_object]

    valid_user = False
    for user in contents:
        if user["name"] == name.upper():
            valid_user = True
            break
    
    return valid_user

print("In this game you are tasked with defeating all 8 bosses. Bosses are defeated when you have depleted their health_bar. To deplete their health_bar you must answer math questions that will increase in difficulty!")

#Creates a new profile or loads an existing one
name = input("Start by creating a name for your character or entering a name of an existing character: ")
player = create_player(name)
valid_user = user_check(player.name)
if valid_user == True:
    player.load_csv()
elif valid_user == False:
    player.save_to_csv()
    player.add_valid_user()

print(player)

#Main loop
running = True
while running == True:
    
    #Reset player health + attack_charge after every fight
    player.health_bar = player.max_health
    player.heavy_attack_charge = 3
    
    #Create boss
    boss = create_boss(str(player.boss_level))
    print("Your current boss:")
    print(boss)

    if player.boss_level == 8:
        print("Final BOSS!!! HARD MODE")

    if player.boss_level == 2:
        print("For every boss defeated you will gain a health potion, be sure to use these wisely!")

    #A loop that iterates until user enters a valid input
    exit_program = False
    break_loop = False

    while(break_loop == False):
        user_input = input("Are you ready? Type Y for Yes or E to Exit and save")
        if user_input.upper() == "Y":
            break_loop = True
        elif user_input.upper() == "E":
            exit_program = True
            player.save_to_csv()
            break_loop = True
        else:
            print("Invalid input :(")

    if exit_program == True:
        break

    #Loop for boss fight
    while boss.health_bar > 0:
        question, answer = question_generator(boss.level)
        user_correct = ask_question(question, answer)

        #Correct answer: User's turn
        if user_correct == True:
            print("Correct! Time for action...")
            valid_input = False
            while valid_input == False:
                user_action = input("Attack: A, Heavy Attack: H, Magic: M, Heal: E (You have {heal} potions)... ".format(heal = player.heal_item))
                if user_action == "A": #Attack
                    player.attack_boss(boss, "a")
                    valid_input = True
                elif user_action.upper() == "E": #Heal
                    player.player_heal()
                    valid_input = True
                elif user_action.upper() == "H": #Heavy_attack
                    player.attack_boss(boss, "h")
                    valid_input = True
                elif user_action.upper() == "M": #Magic_attack
                    player.attack_boss(boss, "m")
                    valid_input = True
                else:
                    print("Invalid input :(")
        
        #Incorrect answer: Boss' turn
        else:
            print("Incorrect! Answer is {answer}".format(answer = answer))
            if boss.health_bar <= 50 and boss.heal_item > 0:
                action = random.randint(1, 2)
                if action == 1:
                    boss.attack_player(player)
                elif action == 2:
                    boss.boss_heal()
            elif boss.health_bar < 25:
                boss.boss_heal()
            else:
                boss.attack_player(player)

        #On players death the program ends
        if player.health_bar <= 0:
            print("Not this time :(... you got to level {level_boss}.".format(level_boss = boss.level))
            running = False
            break

        #On boss' death...
        if boss.health_bar <= 0:
            player.new_heal_item()
            if player.boss_level == 8:
                print("You have completed the game! Well done, You can continue to play at this level or create another character to restart")
            else:
                player.boss_level += 1
