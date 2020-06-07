from tkinter import *
from tkinter.ttk import *
import analyzer
import gui_text_formatter

print("Data loading...")
data = analyzer.readData("monsters.txt")
print("Data loaded")

largeFont = ("Meiryo", 16)
mediumFont = ("Meiryo", 12)
smallFont = ("Meiryo", 8)

window = Tk()
window.title("キャラバンハート転身計算ツール")
window.geometry('400x350')
instructionLabel = Label(window, text="現在のステータスを入力してください", font=largeFont)
instructionLabel.pack(side = TOP)

monsterSelectLabel = Label(window, text="モンスター名", font=mediumFont)
monsterSelectLabel.pack(side = TOP)
monsterSelectCombo = Combobox(window, state="readonly")
monsterNameList = []
for monster in data:
    monsterNameList.append(monster.monster_name)
monsterSelectCombo.config(values = monsterNameList)
monsterSelectCombo.current(1)
monsterSelectCombo.pack(side = TOP)

statsInputLabel = Label(window, text="ステータス", font=mediumFont)
statsInputLabel.pack(side = TOP)

statsInputFrame = Frame(window)
statsInputFrame.pack(side = TOP)
def validateLevel(P):
    if P == "":
        return True
    elif str.isdigit(P) and int(P) < 100:
        return True
    else:
        return False
validateLevelCallback = (window.register(validateLevel),
                '%P')
lvlLabel = Label(statsInputFrame, text="Lv", font=smallFont)
lvlLabel.grid(column=0, row=0)
lvlInput = Entry(statsInputFrame, validate='key', validatecommand=validateLevelCallback, width=5)
lvlInput.grid(column=1, row=0)
def validateStat(P):
    if P == "":
        return True
    elif str.isdigit(P) and int(P) < 1000:
        return True
    else:
        return False
validateStatCallback = (window.register(validateStat),
                '%P')
hpLabel = Label(statsInputFrame, text="HP", font=smallFont)
hpLabel.grid(column=0, row=1)
hpInput = Entry(statsInputFrame, validate='key', validatecommand=validateStatCallback, width=5)
hpInput.grid(column=1, row=1)
hpInput.focus()
mpLabel = Label(statsInputFrame, text="MP", font=smallFont)
mpLabel.grid(column=2, row=1)
mpInput = Entry(statsInputFrame, validate='key', validatecommand=validateStatCallback, width=5)
mpInput.grid(column=3, row=1)
attackLabel = Label(statsInputFrame, text="攻撃", font=smallFont)
attackLabel.grid(column=0, row=2)
attackInput = Entry(statsInputFrame, validate='key', validatecommand=validateStatCallback, width=5)
attackInput.grid(column=1, row=2)
defenseLabel = Label(statsInputFrame, text="防御", font=smallFont)
defenseLabel.grid(column=2, row=2)
defenseInput = Entry(statsInputFrame, validate='key', validatecommand=validateStatCallback, width=5)
defenseInput.grid(column=3, row=2)
speedLabel = Label(statsInputFrame, text="素早さ", font=smallFont)
speedLabel.grid(column=0, row=3)
speedInput = Entry(statsInputFrame, validate='key', validatecommand=validateStatCallback, width=5)
speedInput.grid(column=1, row=3)
intelligenceLabel = Label(statsInputFrame, text="賢さ", font=smallFont)
intelligenceLabel.grid(column=2, row=3)
intelligenceInput = Entry(statsInputFrame, validate='key', validatecommand=validateStatCallback, width=5)
intelligenceInput.grid(column=3, row=3)


def expLimitChecked():
    checked = expLimitState.get()
    if checked:
        expLimitInput.config(state='enabled')
    else:
        expLimitInput.config(state='disabled')

expLimitState = BooleanVar()
expLimitState.set(False)
expLimitCheck = Checkbutton(window, text='経験値制限をかける', var=expLimitState, command=expLimitChecked)
expLimitCheck.pack(side = TOP)
expLimitInput=Entry(window, width=20, state='disabled')
expLimitInput.pack(side = TOP)

def clicked():
    monster = monsterSelectCombo.get()
    monsterTables = [ m for m in data if m.monster_name == monster ]
    monsterTable = monsterTables[0].table
    lvl = int(lvlInput.get().strip() or 1) 
    hp = int(hpInput.get().strip() or 0)
    mp = int(mpInput.get().strip() or 0)
    attack = int(attackInput.get().strip() or 0)
    defense = int(defenseInput.get().strip() or 0)
    speed = int(speedInput.get().strip() or 0)
    intelligence = int(intelligenceInput.get().strip() or 0)
    stats = [hp, mp, attack, defense, speed, intelligence]

    exp = int(expLimitInput.get().strip() or 0)
    if expLimitState.get() == False:
        exp = 0
    path, stats = analyzer.findBestPath(monsterTable, lvl, stats, exp)
    pathText = gui_text_formatter.formatReincarnateTimingMessage(path, exp)
    resultDetailsLabel.configure(text=pathText)
btn = Button(window, text="決定", command=clicked)
btn.pack(side = TOP)

resultLabel = Label(window, text="結果：")
resultLabel.pack(side = TOP)

resultDetailsLabel = Label(window)
resultDetailsLabel.pack(side = TOP)

window.mainloop()

