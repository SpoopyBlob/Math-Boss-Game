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

    def __init__(self, attack, defence, name, level, health_bar = 100, heal_item = 3):
        self.name = name
        self.defence = defence
        self.attack = attack
        self.health_bar = health_bar
        self.level = level
        self.heal_item = heal_item
    
    def __repr__(self):
        description = "{name} is a level {level} boss with an attack power of {attack} and a defensive power of {defence}".format(name = self.name, level = self.level, attack = self.attack, defence = self.defence)
        return description
    
    def take_damage(self, damage):
        points = damage - self.defence
        self.health_bar -= points
        if self.health_bar > 0:
            print("{name} has taken {points} points of damage, there health is now at {health} points".format(name = self.name, points = points, health = self.health_bar))
        else:
            print("{name} has been defeated!".format(name = self.name))


    def attack_player(self, target):
        print("{name} attacks!".format(name = self.name))
        target.take_damage(self.attack)

    def heal(self):
        if self.heal_item > 0:
            self.heal_item -= 1
            self.health_bar += 35
            if self.health_bar > 100:
                self.health_bar = 100

            print("{name} has healed. They are now at {health_bar} health points".format(name = self.name, health_bar = self.health_bar))

class Player:
    player_xp_level_req = [100, 200, 400, 800, 1000]

    def __init__(self, name, health_bar = 100, attack = 20, defence = 5, level = 1, xp = 0, heal_item = 0, boss_level = 1):
        self.health_bar = health_bar
        self.attack = attack
        self.defence = defence
        self.name = name
        self.level = level
        self.xp = xp
        self.heal_item = heal_item
        self.boss_level = 1
    
    def __repr__(self):
        description = "{name}, you are currently level {level} with {attack} attack and {defence} defence.".format(name = self.name, level = self.level, attack = self.attack, defence = self.defence)
        return description

    def attack_boss(self, target):
        print("{name} attacks! 20xp gained".format(name  = self.name))
        target.take_damage(self.attack)
        self.gain_xp(5)
        if target.health_bar <= 0:
            print("100xp for defeating the boss, keep it up!")
            self.gain_xp(100)
    
    def take_damage(self, damage):
        points = damage - self.defence
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
                self.health_bar = 100

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
        print("Congrats you are now level {level}!".format(level = self.level))

        self.attack = 20 * self.level
        self.defence = 5 * self.level

    def save_to_csv(self):
        filename = "{name}'s_player_profile.csv".format(name = self.name)
        fieldnames = ["name", "attack", "defence", "level", "xp", "heal_item", "boss_level"]
        
        list_of_attributes = {
            "name": self.name,
            "attack": self.attack,
            "defence": self.defence,
            "level": self.level,
            "xp": self.xp,
            "heal_item": self.heal_item,
            "boss_level": self.boss_level
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
    
    def add_valid_user(self):
        with open("user_check.csv", 'a') as file:
            file_writer = csv.writer(file)
            file_writer.writerow([self.name.upper()])

def create_player(name):
    new_player = Player(name)
    return new_player

def create_boss(level):
    names = ["Zarathor the Unyielding", "Lady Thalindra, Warden of the Abyss", "Vorathar, the Dark Seer", "Kragoth the Devourer", "Veylanar, the Eternal Flame", "Aeloria, Queen of the Fallen", "Khorath the Soulbinder", "Malrathar, the Stormbringer"]
    name = names[level - 1]

    attack = 10 * level
    defence = 5 * level

    boss = Boss(attack, defence, name, level)
    Boss.boss_counter += 1
    return boss

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
        num1 = random.randint(1, 20)
        num2 = random.randint(1, 20)
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

    
    elif level == 4:
        num1 = random.randint(1, 30)
        num2 = random.randint(1, 30)
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
            answer = num1 / num2
            string = "What is {num1} / {num2}?".format(num1 = num1, num2 = num2)
            return string, answer        

    elif level == 5:
        num1 = random.randint(1, 40)
        num2 = random.randint(1, 40)
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
            answer = num1 / num2
            string = "What is {num1} / {num2}?".format(num1 = num1, num2 = num2)
            return string, answer        

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

    for user in contents:
        if user["name"] == name.upper():
            return "valid_user"
        else:
            return "new_user"



print("In this game you are tasked with defeating all 8 bosses. Bosses are defeated when you have depleated there health_bar. To depleate there health_bar you must answer math questions that will increase in difficulty!")
name = input("Start by creating a name for your character or entering a name of an existing character: ")
player = create_player(name)
valid_user = user_check(player.name)
if valid_user == "valid_user":
    player.load_csv()
elif valid_user == "new_user":
    player.save_to_csv()
    player.add_valid_user()

print(player)


running = True
while running == True:
    
    boss = create_boss(player.boss_level)
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
            print("Correct! Time for action...")
            user_action = input("To attack type A to heal type E: ")
            if user_action == "A":
                player.attack_boss(boss)
            elif user_action == "E":
               player.heal()
        else:
            print("Incorrect!")
            if boss.health_bar <= 50 and boss.heal_item > 0:
                action = random.randint(1, 2)
                print(action)
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
            if boss_level == 8:
                print("You have completed the game! Welldone, You can continue to play at this level or create another character to restart")
            player.boss_level += 1

    if exit_status == "Exit":
        break
        
        











