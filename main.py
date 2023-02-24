import math
import random
import time
import sys

pause = 0.2
endTurnPause = 1
turnNumber = 0
chars = []
foes = []

#skills
class Skill():
    def __init__(self):
        self.name = ''
        self.info = ""
        self.info2 = ""

class OneTargetAttack(Skill):
    def __init__(self):
        super().__init__()
        self.type = "onetarget"
        self.damage = 1

class SelfSupport(Skill):
    def __init__(self):
        super().__init__()
        self.type = "selfsupport"

class HomingAmulet(OneTargetAttack):
    def __init__(self):
        super().__init__()
        self.damage = 4
        self.cost = 0
        self.name = 'Homing Amulet'
        self.info = f"Cost: {self.cost} Points"
        self.info2 = f"Deals {self.damage} Damage"
        self.costType = "spend"

class FantasySeal(OneTargetAttack):
    def __init__(self):
        super().__init__()
        self.damage = 10
        self.cost = 5
        self.name = 'Fastasy Seal'
        self.info = f"Cost: {self.cost} Points"
        self.info2 = f"Deals {self.damage} Damage"
        self.costType = "spend"

class FantasyHeaven(OneTargetAttack):
    def __init__(self):
        super().__init__()
        self.damage = 40
        self.cost = 30
        self.name = 'Fantasy Heaven'
        self.info = f"Cost: {self.cost} Points"
        self.info2 = f"Deals {self.damage} Damage"
        self.costType = "spend"

class Graze(SelfSupport):
    def __init__(self):
        super().__init__()
        self.name = "Graze"
        self.cooldownTurns = 2
        self.cooldown = 0
        self.info = f"Cooldown: 1 Turn"
        self.info2 = f"Graze incoming attacks."
        self.costType = "cooldown"

class MagicMissile(OneTargetAttack):
    def __init__(self):
        super().__init__()
        self.damage = 6
        self.cost = 2
        self.name = 'Magic Missile'
        self.info = f"Cost: {self.cost} Magic"
        self.info2 = f"Deals {self.damage} Damage"
        self.costType = "spend"

class MasterSpark(OneTargetAttack):
    def __init__(self):
        super().__init__()
        self.damage = 30
        self.cost = 12
        self.name = 'Master Spark'
        self.info = f"Cost: {self.cost} Magic"
        self.info2 = f"Deals {self.damage} Damage"
        self.costType = "spend"
    
class Focus(SelfSupport):
    def __init__(self):
        super().__init__()
        self.name = "Focus"
        self.cost = 0
        self.info = f"Cost: {self.cost} Magic"
        self.info2 = f"Recovers 5 Magic"
        self.costType = "spend"

# All characters have these stats.
class Character:
    def __init__(self, name="", hp=0):
        self.name = name
        self.hp = hp
        self.hpMax = hp

class Reimu(Character):
    def __init__(self):
        super().__init__("Reimu Hakurei", 32)
        self.sp = 0
        self.term = "Points"
        self.skills = [Graze(),HomingAmulet(),FantasySeal(),FantasyHeaven()]
        self.graze = False

class Marisa(Character):
    def __init__(self):
        super().__init__("Marisa Kirisame", 24)
        self.sp = 30
        self.update()

    def update(self):
        self.info = f'Magic {self.sp}'

class Foe:
    def __init__(self, name="", hp=0):
        self.name = name
        self.hp = hp
        self.hpMax = hp
        self.nextSkill = 0
        self.nextTarget = 0
        self.insightSkill = 0
        self.insightTarget = 0
        self.insightDisplay = ''

class Marisa_Foe(Foe):
    def __init__(self):
        super().__init__("Marisa Kirisame", 50)
        self.sp = 20
        self.term = "Magic"

def box(text):
    boxSize = 100
    print(f'{"":-^{boxSize+2}}')
    rows = len(text)
    for x in range(0,rows):
        columns = len(text[x])
        margin = boxSize//columns
        print ("|",end="")
        for y in text[x]:
            print(f'{y: ^{margin}}',end="")
        print ("|")
    print(f'{"":-^{boxSize+2}}')

def percentage(part, whole, size):
    return size * float(part) / float(whole)

def healthbar(HP,maxHP,size):
    if maxHP <= size:
        bar = ('|'*HP)
        result = (f'[{bar: <{maxHP}}]')
    elif maxHP > size:
        percent = math.ceil(percentage(HP,maxHP,size))
        bar = ('|'*percent)
        result = (f'[{bar: <{size}}]')
    return result

def ask (lowRange,highRange):
    while True:
        try:
            result = int(input("Choose a number: "))
        except:
            continue
        if lowRange <= result <= highRange:
            return result
        
def askList (numberList):
    while True:
        try:
            result = int(input("Choose a number: "))
        except:
            continue
        if result in numberList:
            return result

def getPartyList(unit,koed,enemy):
    if isinstance(unit,Character):
        party = []
        if enemy:
            for foe in foes:
                if koed:
                    party.append(foe) 
                elif foe.hp > 0:
                    party.append(foe)
        else:
            for char in chars:
                if koed:
                    party.append(char)
                elif char.hp > 0:
                    party.append(char)
        return party
    elif isinstance(unit,Foe):
        party = []
        for foe in foes:
            if koed:
                party.append(foe) 
            elif foe.hp > 0:
                party.append(foe)
        return party

def chooseTarget(char,skill):
    if skill.type == "onetarget":
        party = getPartyList(char,True,True)
        if len(party) != 1:
            display = [[f'-- Choose an target for {skill.name} --'],
                       [str(party.index(foe)+1)+ ". " + foe.name for foe in party]]
            box(display)
            result = ask(1,len(party))
            result = party[result-1]
        else:
            result = party[0]
        return result
    
def useSkill(unit,skill):
    if skill.costType == "spend":
        unit.sp -= skill.cost
        time.sleep(pause)
        print(f"{unit.name} spends {skill.cost} {unit.term},")
    if skill.type == "onetarget":
        if isinstance(unit,Character):
            target = chooseTarget(unit,skill)
        if isinstance(unit,Foe):
            target = unit.nextTarget
        damage = skill.damage
        time.sleep(pause)
        print(f"{unit.name} used {skill.name}!")
        if isinstance(target,Reimu) and target.graze:
            target.sp += damage
            print(f"Reimu gains {damage} points as she grazes it!")
        else:
            target.hp -= damage
            time.sleep(pause)
            print (f'{target.name} took {damage} damage!')
            if target.hp <= 0:
                target.hp = 0
                time.sleep(pause)
                print (f'{target.name} is defeated!')
    elif skill.type == "selfsupport":
        time.sleep(pause)
        print(f"{unit.name} used {skill.name}!")
        if isinstance(skill,Graze):
            unit.graze = True
        if isinstance(skill,Focus):
            unit.sp += 5
            time.sleep(pause)
            print(f"{unit.name} recovered 5 Magic!")

        
def chooseSkill(char):
    display = [[f'-- Choose an action for {char.name} --'],
            [str(char.skills.index(s)+1)+ ". " + s.name for s in char.skills],
            [s.info for s in char.skills],
            [s.info2 for s in char.skills]]
    box(display)
    while True:
        result = ask(1,len(char.skills))
        result = char.skills[result-1]
        if result.costType == "spend":
            if result.cost <= char.sp:
                return result
            else:
                time.sleep(pause)
                print(f"Not enough {char.term}")
        elif result.costType == "cooldown":
            if result.cooldown == 0:
                result.cooldown = result.cooldownTurns
                return result
            else:
                time.sleep(pause)
                if result.cooldown == 1:
                    print(f"{result.name} is on cooldown for {result.cooldown} more turn.")
                else:
                    print(f"{result.name} is on cooldown for {result.cooldown} more turns.")

    

    return result

def displayBattleScreen():
    characters = [char for char in chars]
    enemies = [foe for foe in foes]
    boxList1 = [[foe.name for foe in enemies],
                [f"Health {foe.hp}/{foe.hpMax}" for foe in enemies],
                [healthbar(foe.hp,foe.hpMax,50) for foe in enemies],
                [foe.term+" "+str(foe.sp) for foe in enemies]]
    boxList2 = [[char.name for char in characters],
                [f"HP {char.hp}/{char.hpMax}" for char in characters],
                [healthbar(char.hp,char.hpMax,10) for char in characters],
                [char.term+" "+str(char.sp) for char in characters]]
    box(boxList1)
    box(boxList2)

def unitTurn(unit):
    if isinstance(unit,Character):
        displayBattleScreen()
        useSkill(unit,chooseSkill(unit))
    elif isinstance(unit,Foe):
        useSkill(unit,unit.nextSkill)

def marisaAI(foe):
        foe.insightSkill = random.randint(0, 2)
        foe.insightTarget = 2
        foe.nextTarget = chars[0]
        if turnNumber == 1:
            foe.nextSkill = MagicMissile()
        elif turnNumber == 2:
            foe.nextSkill = MasterSpark()
            foe.insightSkill = 2
        elif foe.sp < 2:
            foe.nextSkill = Focus()
        else:
            foe.nextSkill = MagicMissile()
        if foe.insightSkill == 0:
            foe.insightDisplay = f"It's unclear what {foe.name} is doing!"
        elif foe.insightSkill == 1:
            if isinstance(foe.nextSkill,MagicMissile):
                str1 = f"{foe.name} is tracking Reimu's movement."
                str2 = f"{foe.name} is readying an attack."
                foe.insightDisplay = random.choice([str1, str2]) 
            elif isinstance(foe.nextSkill,Focus):
                str1 = f"{foe.name} is looking at her Mini-Hakkero."
                str2 = f"{foe.name} is closing her eyes."
                foe.insightDisplay = random.choice([str1, str2])
        elif foe.insightSkill == 2:
            foe.insightDisplay = f"{foe.name} is getting ready to use {foe.nextSkill.name}!"

def insightTurn():
    display = []
    for foe in foes:
        if foe.hp > 0:
            if isinstance(foe,Marisa_Foe):
                marisaAI(foe)

    display = [[foe.insightDisplay for foe in foes]]
    box(display)
    
def cleanup():
    for char in chars:
        if isinstance(char,Reimu) and char.graze:
                char.graze = False
        for skill in char.skills:
            if skill.costType == "cooldown":
                if skill.cooldown != 0:
                    skill.cooldown -= 1

    for foe in foes:
        pass

def battleLoop():
    global turnNumber
    turnNumber = 0
    while len([char for char in chars if char.hp > 0]) > 0 and len([foe for foe in foes if foe.hp > 0]) > 0:
        turnNumber += 1
        insightTurn()
        for char in chars:
            if char.hp > 0:
                unitTurn(char)
                time.sleep(endTurnPause)
        for foe in foes:
            if foe.hp > 0:
                unitTurn(foe)
                time.sleep(endTurnPause)
        cleanup()
    if not len([char for char in chars if char.hp > 0]) > 0:
        box([["Your party was defeated!"],["Game Over"]])
    if not len([foe for foe in foes if foe.hp > 0]) > 0:
        box([["You defeated the boss!"],["You Win!"]])







chars = [Reimu()]
foes = [Marisa_Foe()]

battleLoop()