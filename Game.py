import random
import csv
#add new actions heavy_attack, magic, maybe the user gets to choose from a range of starter classes, mage, brute, swordsman?
#bosses also have speacial abilities, with weekness and strengths
#add level up tree that allows you to choose two attributes to level up, including health_bar?
#bosses have dialouge? Maybe some strings to personalise the bosses
#implament item drops, health_item, attribute_boost (temp), skip_question(temp) these could be boss drops
#refine strings and presentation of game in console + alter xp given by each boss

#Unlimited mode: Like an arcade game, once you have reached level 8 you can go against an onslaught of bosses back to back. This could be considered hardcore mode, highscore gets saved.
#This is my final list of things to do, once I have done this and it all works, im going to finish this project.


class Boss:
    boss_counter = 0

    def __init__(self, attack, defence, name, level, health_bar, heal_item, heavy_attack, magic, magic_def, type_p, hint):
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
        self.type_p = type_p
        self.hint = hint
        
    
    def __repr__(self):
        type_p = ""
        if self.type_p == "mag":
            type_p = "wizzard"
        elif self.type_p == "brute":
            type_p = "brute"
        elif self.type_p == "mix":
            type_p = "swordsman with wizzarding capabilities"
        description = "{name} is a level {level} boss and a {type}. {hint}".format(name = self.name, level = self.level, type = type_p, hint = self.hint)
        return description
    
    def take_damage(self, damage, type_damage):
        points = 0
        if type_damage == "a":
            points = damage - self.defence
        elif type_damage == "m":
            points = damage - self.magic_def
        
        self.health_bar -= points
        if self.health_bar > 0:
            print("{name} has taken {points} points of damage, there health is now at {health} points".format(name = self.name, points = points, health = self.health_bar))
        else:
            print("{name} has been defeated!".format(name = self.name))

    def attack_player(self, target):
        if self.type_p == "brute":
            action = random.randint(1, 2)
            if action == 1:
                print("{name} performs heavy attack!".format(name = self.name))
                target.take_damage(self.heavy_attack, "a")
            elif action == 2:
                print("{name} attacks!".format(name = self.name,))
                target.take_damage(self.attack, "a")
        elif self.type_p == "mag":
            print("{name} casts a spell!".format(name = self.name))
            target.take_damage(self.magic, "m")
        elif self.type_p == "mix":
            action = random.randint(1, 3)
            if action == 1:
                print("{name} performs heavy attack!".format(name = self.name))
                target.take_damage(self.heavy_attack, "a")
            elif action == 2:
                print("{name} attacks!".format(name = self.name))
                target.take_damage(self.attack, "a")
            elif action == 3:
                print("{name} casts a spell!".format(name = self.name))
                target.take_damage(self.magic, "a")
        

    def heal(self):
        if self.heal_item > 0:
            self.heal_item -= 1
            self.health_bar += 35
            if self.health_bar > self.max_health:
                self.health_bar = self.max_health

            print("{name} has healed. They are now at {health_bar} health points".format(name = self.name, health_bar = self.health_bar))

class Player:
    player_xp_level_req = [50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 1000]

    def __init__(self, name, health_bar = 100, attack = 10, defence = 20, level = 1, xp = 0, heal_item = 1, boss_level = 1, magic = 10, heavy_attack = 20, magic_def = 5):
        self.health_bar = health_bar
        self.max_health = health_bar
        self.attack = attack
        self.defence = defence
        self.name = name
        self.level = level
        self.xp = xp
        self.heal_item = heal_item
        self.boss_level = boss_level
        self.magic = magic
        self.heavy_attack = heavy_attack
        self.magic_def = magic_def
    
    def __repr__(self):
        description = "{name}, here are your stats: level {level}, attack {attack}, heavy_attack {heavy}, defence {defence}, magic, {magic}, magic defence {magic_def}, max health {health} .".format(name = self.name, level = self.level, attack = self.attack, defence = self.defence, heavy = self.heavy_attack, magic_def = self.magic_def, magic = self.magic, health = self.max_health)
        return description

    def if_boss_dead(self, target):
        if target.health_bar <= 0:
            print("100xp for defeating the boss, keep it up!")
            self.gain_xp(100)

    def attack_boss(self, target, type):
        if type == "a": #attack
            print("{name} attacks! 5xp gained".format(name  = self.name))
            target.take_damage(self.attack, "a")
            self.gain_xp(5)
            self.if_boss_dead(target)
        if type == "m": #magic
            print("{name} casts magic! 5xp gained".format(name  = self.name))
            target.take_damage(self.magic, "m")
            self.gain_xp(5)
            self.if_boss_dead(target)
        if type == "h": #heavy_attack
            print("{name} performs heavy attack! 5xp gained".format(name  = self.name))
            target.take_damage(self.heavy_attack, "a")
            self.gain_xp(5)
            self.if_boss_dead(target)
    
    def take_damage(self, damage, type):
        points = damage - self.defence
        if type == "a":
            points = damage - self.defence
        elif type == "m":
            points = damage - self.magic_def
        self.health_bar -= points
        if self.health_bar > 0:       
            print("You have taken {points} points of damage, your health is now at {health} points".format(points = points, health = self.health_bar))
        else:
            print("You have been defeated!")

    def heal(self):
        if self.heal_item > 0:
            health_bar = self.health_bar
            self.heal_item -= 1
            self.health_bar += 35
            if self.health_bar > 100:
                self.health_bar = self.max_health

            if health_bar == self.health_bar:
                print("You have wasted a healing potion!")
            else:
                print("You are not at {health_bar} health points".format(health_bar = self.health_bar))
        else:
            print("You have no healing potions, you have wasted a turn!")

    def new_heal_item(self):
        self.heal_item += 1
        print("You have earned a health potion, you now have {heal_item}.".format(heal_item = self.heal_item))
        
    def gain_xp(self, xp):
        self.xp += xp
        if self.xp > self.player_xp_level_req[self.level - 1]:
            self.level_up()
        print("XP: {xp}/{req}".format(xp = self.xp, req = self.player_xp_level_req[self.level - 1]))

    def level_up(self):
        self.xp = self.xp - self.player_xp_level_req[self.level - 1]
        self.level += 1
        valid_input = False
        print("Congrats you are now level {level}!".format(level = self.level))
        while valid_input == False:
            print("Choose two stats you would like to upgrade e.g. 1/3 upgrades attack and magic or 1/1 to upgrade attack twice ")
            user_upgrade = input("Attack: 1, Heavy Attack: 2, Magic: 3, Magic Defence: 4, Defence: 5")
            split_strings = user_upgrade.split("/")
            #Checks to see if input is valid, loop will continue if input is invalid
            error = False
            for num in split_strings:
                if num == "1":
                    self.attack += 10
                elif num == "2":
                    self.heavy_attack += 10
                elif num == "3":
                    self.magic += 10
                elif num == "4":
                    self.magic_def += 10
                elif num == "5":
                    self.defence += 10
                else:
                    error = True
                    print("Invalid input :(")
            
            if error == False:
                valid_input = True
        self.max_health += 20
        print(player)


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
    
    def add_valid_user(self):
        with open("user_check.csv", 'a') as file:
            file_writer = csv.writer(file)
            file_writer.writerow([self.name.upper()])

def create_player(name):
    new_player = Player(name)
    return new_player

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

        boss_object = Boss(int(attack), int(defence), name, int(level), int(health_bar), int(heal_item), int(heavy_attack), int(magic), int(magic_def), type_p, hint)
        return boss_object

def question_generator(level):
    
    if level == 1:
        num1 = random.randint(1, 10)
        num2 = random.randint(1, 10)
        symbols = ["+", "-"]
        symbol = random.choice(symbols)
        
        if symbol == "+":
            answer = num1 + num2
            string = "What is {num1} + {num2}?".format(num1 = num1, num2 = num2)
            return string, answer
        
        if symbol == "-":
            answer = num1 - num2
            string = "What is {num1} - {num2}?".format(num1 = num1, num2 = num2)
            return string, answer

    elif level == 2:
        num1 = random.randint(1, 20)
        num2 = random.randint(1, 20)
        symbols = ["+", "-"]
        symbol = random.choice(symbols)
        
        if symbol == "+":
            answer = num1 + num2
            string = "What is {num1} + {num2}?".format(num1 = num1, num2 = num2)
            return string, answer
        
        if symbol == "-":
            answer = num1 - num2
            string = "What is {num1} - {num2}?".format(num1 = num1, num2 = num2)
            return string, answer

    elif level == 3:
        num1 = random.randint(1, 40)
        num2 = random.randint(1, 40)
        symbols = ["+", "-"]
        symbol = random.choice(symbols)
        
        if symbol == "+":
            answer = num1 + num2
            string = "What is {num1} + {num2}?".format(num1 = num1, num2 = num2)
            return string, answer
        
        if symbol == "-":
            answer = num1 - num2
            string = "What is {num1} - {num2}?".format(num1 = num1, num2 = num2)
            return string, answer
            
    elif level == 4:
        num1 = random.randint(1, 80)
        num2 = random.randint(1, 80)
        symbols = ["+", "-"]
        symbol = random.choice(symbols)
        
        if symbol == "+":
            answer = num1 + num2
            string = "What is {num1} + {num2}?".format(num1 = num1, num2 = num2)
            return string, answer
        
        if symbol == "-":
            answer = num1 - num2
            string = "What is {num1} - {num2}?".format(num1 = num1, num2 = num2)
            return string, answer     

    elif level == 5:
        num1 = random.randint(1, 100)
        num2 = random.randint(1, 100)
        symbols = ["+", "-", "/"]
        symbol = random.choice(symbols)
        
        if symbol == "+":
            answer = num1 + num2
            string = "What is {num1} + {num2}?".format(num1 = num1, num2 = num2)
            return string, answer
        
        if symbol == "-":
            answer = num1 - num2
            string = "What is {num1} - {num2}?".format(num1 = num1, num2 = num2)
            return string, answer

        if symbol == "/":
            num1 = random.randint(2, 4)
            num2 = random.randint(2, 20)
            if num1 % 2 == 1: num1 +=1
            if num2 % 2 == 1: num1 +=1

            answer = num1 / num2
            string = "What is {num1} / {num2}?".format(num1 = num1, num2 = num2)
            return string, answer        


    elif level == 6:
        num1 = random.randint(1, 40)
        num2 = random.randint(1, 40)
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

        if symbol == "/":
            num1 = random.randint(2, 4)
            num2 = random.randint(2, 40)
            if num1 % 2 == 1: num1 +=1
            if num2 % 2 == 1: num1 +=1
            
            answer = num1 / num2
            string = "What is {num1} / {num2}?".format(num1 = num1, num2 = num2)
            return string, answer          

        if symbol == "*":
            answer = num1 * num2
            string = "What is {num1} * {num2}?".format(num1 = num1, num2 = num2)
            return string, answer      

    elif level == 7:
        num1 = random.randint(1, 50)
        num2 = random.randint(1, 50)
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

        if symbol == "/":
            num1 = random.randint(2, 6)
            num2 = random.randint(2, 40)
            if num1 % 2 == 1: num1 +=1
            if num2 % 2 == 1: num1 +=1
            
            answer = num1 / num2
            string = "What is {num1} / {num2}?".format(num1 = num1, num2 = num2)
            return string, answer         

        if symbol == "*":
            answer = num1 * num2
            string = "What is {num1} * {num2}?".format(num1 = num1, num2 = num2)
            return string, answer     

    elif level == 8:
        num1 = random.randint(1, 100)
        num2 = random.randint(1, 100)
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

        if symbol == "/":
            num1 = random.randint(2, 10)
            num2 = random.randint(2, 60)
            if num1 % 2 == 1: num1 +=1
            if num2 % 2 == 1: num1 +=1     

        if symbol == "*":
            answer = num1 * num2
            string = "What is {num1} * {num2}?".format(num1 = num1, num2 = num2)
            return string, answer   

def answer_question(question, answer):
    print(question)
    #print(answer)
    user = input("Answer: ")
    if user == str(answer):
        return True
    else:
        return False

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


print("In this game you are tasked with defeating all 8 bosses. Bosses are defeated when you have depleated there health_bar. To depleate there health_bar you must answer math questions that will increase in difficulty!")
name = input("Start by creating a name for your character or entering a name of an existing character: ")
player = create_player(name)
valid_user = user_check(player.name)
if valid_user == True:
    player.load_csv()
elif valid_user == False:
    player.save_to_csv()
    player.add_valid_user()

print(player)

running = True
while running == True:
    
    player.health_bar = player.max_health
    boss = create_boss(str(player.boss_level))
    print("Your current boss:")
    print(boss)

    if player.boss_level == 8:
        print("Final BOSS!!! HARD MODE")

    if player.boss_level == 2:
        print("For every boss defeated you will gain a health potion, be sure to use these wisely!")

    exit_status = "Keep Going"
    user_ready = False
    while(user_ready == False):
        user_input = input("Are you ready? Type Y for Yes or E to Exit and save")
        if user_input.upper() == "Y":
            user_ready = True
        elif user_input.upper() == "E":
            exit_status = "Exit"
            player.save_to_csv()
            break
    if exit_status == "Exit":
        break


    while boss.health_bar > 0:
        question, answer = question_generator(boss.level)
        user_valid_input = answer_question(question, answer)

        if user_valid_input == True:
            valid_input = False
            print("Correct! Time for action...")
            while valid_input == False:
                user_action = input("Attack: A, Heavy Attack: H, Magic: M, Heal: E ")
                if user_action == "A": #attack
                    player.attack_boss(boss, "a")
                    valid_input = True
                elif user_action.upper() == "E": #heal
                    player.heal()
                    valid_input = True
                elif user_action.upper() == "H": #heavy_attack
                    player.attack_boss(boss, "h")
                    valid_input = True
                elif user_action.upper() == "M": #magic_attack
                    player.attack_boss(boss, "m")
                    valid_input = True
                else:
                    print("Invalid input :(")
        else:
            print("Incorrect!")
            if boss.health_bar <= 50 and boss.heal_item > 0:
                action = random.randint(1, 2)
                if action == 1:
                    boss.attack_player(player)
                elif action == 2:
                    boss.heal()
            else:
                boss.attack_player(player)

        if player.health_bar <= 0:
            print("Not this time :(... you got to the level {level_boss} boss.".format(level_boss = boss.level))
            exit_status = "Exit"
            break

        if boss.health_bar <= 0:
            player.new_heal_item()
            if player.boss_level == 8:
                print("You have completed the game! Welldone, You can continue to play at this level or create another character to restart")
            else:
                player.boss_level += 1

    if exit_status == "Exit":
        break
        
        











