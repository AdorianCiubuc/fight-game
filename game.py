import time
import sys
import random
import json
import os

data = {"level" : 50 ,
         "experience" : 400,
         "boss_level" : 14,
         "life": 300,
         "defence" :50,
         "damage" : 70,
         "critical" : 50,
         "penetrating": 50}
def save_data():
    with open("game_data.json","w") as f:
     json.dump(data,f)

def read_data():
    global data
    with open("game_data.json","r") as f:
     data = json.load(f)

read_data()


class Creator():
    def __init__(self,life,defence,damage):
        self.level = 1
        self.experience = 0
        self.boss_level = 1
        self.life = life
        self.defence = defence
        self.damage = damage
        self.critical = 10
        self.penetrating = 15

    def attack(self,user):
        if random.randint(1,100) <= self.critical:
            if random.randint(1,100) <= self.penetrating:
                user.life -= self.damage * 2
            else:
                user.life -= (self.damage - user.defence) * 2
        else:
            if random.randint(1, 100) <= self.penetrating:
                user.life -= self.damage
            else:
                user.life -= (self.damage - user.defence) * 2
            user.life -= self.damage - user.defence

hero = Creator(data["life"],data["defence"],data["damage"])
hero.level = data["level"]
hero.experience = data["experience"]
hero.boss_level = data["boss_level"]
hero.critical = data["critical"]
hero.penetrating = data["penetrating"]


creature = Creator(40, 10, 20)

def show(a):
    print(f"""
    Life :              {a.life}
    Defence :           {a.defence}
    Damage :            {a.damage}
    Critical Chance :   {a.critical}
    Penetrating :       {a.penetrating}
    """)

def attack_boss():
    boss= Creator(100 +10*hero.boss_level,20+2*hero.boss_level,35+3*hero.boss_level)
    print("Hero : ")
    show(hero)
    print("Boss :")
    show(boss)
    hero_life = hero.life
    version = int(input("""
        Press 1 to show the details
        Press 2 to move on
        """))
    if version == 1:
        while True:
            input("Press enter to attack \n")
            print('Now you are attacking The Boss')
            hero.attack(boss)
            time.sleep(2)
            print(f'The Boss has {boss.life} life.')
            time.sleep(2)
            if boss.life <= 0:
                print('The Boss is dead.You won')

                hero.life = hero_life
                hero.boss_level += 1
                data["boss_level"] +=1
                save_data()
                break

            time.sleep(2)
            print('Now The Boss is attacking you')
            time.sleep(2)
            boss.attack(hero)
            print(f'You have {hero.life} life.\n')
            if hero.life <= 0:
                print('You are dead.Please try again and focus more!')
                hero.life = hero_life
                break
                sys.exit()

    elif version == 2:
        while True:
            hero.attack(boss)
            if boss.life <= 0:
                print('The Boss is dead.You won')

                hero.life = hero_life
                hero.boss_level += 1
                data["boss_level"] +=1
                save_data()
                break
            boss.attack(hero)

            if hero.life <= 0:
                print('You are dead.Please try again and focus more!')
                hero.life = hero_life
                break
                sys.exit()

    elif version > 2 or version < 1:
        print("Wrong answer!")
        time.sleep(1)
        print('The program is ending now!')
        time.sleep(1)
        sys.exit()


def increase_level():
    hero.level +=1
    data["level"] +=1
    save_data()
    print(f"Your level is {hero.level} ")
    print("""
    Press 1 to improve life
    Press 2 to improve Defence
    Press 3 to improve Damage
    Press 4 to improve Critical chance
    Press 5 to improve Penetrating chance
    """)
    option = int(input('Which one do you want to increase?'))
    if option ==1 :
        hero.life +=10
        data["life"] +=10
        save_data()
        print(f"Life increased.Now you have {hero.life} life")
    elif option == 2:
        hero.defence += 2
        data["defence"]+= 2
        save_data()
        print(f"Defence increased.Now you have {hero.defence} defence")

    elif option == 3:
        hero.damage += 2
        data["damage"]+=2
        save_data()
        print(f"Damage increased.Now you have {hero.damage} damage")

    elif option == 4:
        hero.critical += 1
        data["critical"]+=1
        save_data()
        print(f"Critical chance increased.Now you have {hero.defence} critical chance")

    elif option == 5:
        hero.penetrating += 1
        data["penetrating"] +=1
        save_data()
        print(f"Penetrating chance increased.Now you have {hero.defence} penetrating chance")
    else:
        pass

def attack_creature():
    creature_no = int(input("How many Creatures  do you want to attack?"))
    no_exp = creature_no
    hero_life = hero.life
    if creature_no <=0:
        sys.exit()
    version = int(input("""
    Press 1 to show the details
    Press 2 to move on
    """))
    if version ==1:
        while True:
            input("Press enter to attack \n")
            print('Now you are attacking creatures')
            hero.attack(creature)
            time.sleep(2)
            print(f'Creature has {creature.life} life.')
            time.sleep(2)
            if creature.life <= 0 and creature_no == 1:
                print('Creatures are dead.You won')
                hero.experience += no_exp*50
                data["experience"] +=no_exp*50
                save_data()
                hero.life = hero_life
                if hero.experience >= hero.level*100:

                    increase_level()
                    hero.experience = 0
                    data["experience"] = 0
                    save_data()


                break
            elif creature.life <= 0 and creature_no > 1:
                creature_no -= 1
                print(f"You killed 1 creature and {creature_no} are left")
                creature.life = 40

            time.sleep(2)
            print('Now creatures are attacking you')
            time.sleep(2)
            for i in range(creature_no):
                creature.attack(hero)
                print(f'You have {hero.life} life.\n')
                if hero.life <= 0:
                    print('You are dead.Please try again and focus more!')
                    hero.life = hero_life
                    break
                    sys.exit()

    elif version ==2:
        while True:

            hero.attack(creature)
            if creature.life <= 0 and creature_no == 1:
                print('Creatures are dead.You won')
                hero.experience += no_exp*50
                data["experience"] += no_exp * 50
                save_data()
                hero.life = hero_life
                if hero.experience >= hero.level*100:

                    increase_level()
                    hero.experience = 0
                    data["experience"] =0
                    save_data()

                break
            elif creature.life <= 0 and creature_no > 1:
                creature_no -= 1

                creature.life = 40
            for i in range(creature_no):
                creature.attack(hero)

                if hero.life <= 0:
                    print('You are dead.Please try again and focus more!')
                    hero.life = hero_life
                    time.sleep(2)
                    sys.exit()

    elif version >2 or version < 1 :
        print("Wrong answer!")
        time.sleep(1)
        print('The program is ending now!')
        time.sleep(1)
        sys.exit()


def main():
    read_data()
    while True:

        print("""
    Press 1 if you want to attack the creatures
    Press 2 if you want to  attack a Boss
    Press 3 if you want to exit
    """)
        choice=int(input('What do you want to do?'))
        os.system("cls")
        os.system('cls' if os.name =='nt' else 'clear')

        if choice==1:
            attack_creature()
        elif choice ==2:
            attack_boss()
        elif choice ==3:
            print("The program is ending now")
            sys.exit()
        elif choice>2 or choice <1:
            print("Wrong answer!")
            time.sleep(1)
            print('The program is ending now!')
            time.sleep(1)
            sys.exit()


main()



