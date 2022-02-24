from flask import Blueprint, request, render_template
from urllib import parse
from bs4 import BeautifulSoup
import json, random, requests, dbconfig_LostArk

Character = Blueprint("Character", __name__, url_prefix="/LostArk/Character")
db_Class = dbconfig_LostArk.DataBase()

@Character.route("/Character-Another")
def function_Character_Another():
    NickName = request.args.get("NickName")

    if NickName == None:
        return json.dumps({"Result": "Error", "Error_Result": "NickName"})

    Character_Url = f"https://lostark.game.onstove.com/Profile/Character/{parse.quote_plus(NickName)}"
    Character_Get = requests.get(Character_Url)
    Character_Html = Character_Get.text
    Character_Soup = BeautifulSoup(Character_Html, "html.parser")

    Character_List = Character_Soup.find("div", attrs={"class": "profile-character-list"})
    Character_ServerName = Character_List.find_all("strong", attrs={"class": "profile-character-list__server"})
    Character_NameList = Character_List.find_all("ul", attrs={"class": "profile-character-list__char"})
    
    Result_List = {}
    Result_List["Result"] = "Success"

    Character_Server_List = []
    Character_Name_List = []
    Character_Class_List = []
    Character_Lv_List = []

    for i in range(len(Character_ServerName)):
        for Character_Name_Data in Character_NameList[i].find_all("button"):
            Character_Server_List.append(Character_ServerName[i].get_text().strip().replace("@", ""))
            Character_Name_List.append(Character_Name_Data.find("span").get_text())
            Character_Class_List.append(Character_Name_Data.find("img")["alt"])
            Character_Lv_List.append(int(Character_Name_Data.get_text().strip().replace(Character_Name_Data.find("span").get_text(), "").replace("Lv.", "")))

    for j in range(len(Character_Server_List)):
        Result_List[j] = {}
        
        Result_List[j]["Server"] = Character_Server_List[j]
        Result_List[j]["Name"] = Character_Name_List[j]
        Result_List[j]["Lv"] = Character_Lv_List[j]
        Result_List[j]["Class"] = Character_Class_List[j]

    return json.dumps(Result_List, ensure_ascii=False)

@Character.route("/Character-Data")
def function_Character_Data():
    NickName = request.args.get("NickName")

    if NickName == None:
        return json.dumps({"Result": "Error", "Error_Result": "NickName"})

    Character_Url = f"https://lostark.game.onstove.com/Profile/Character/{parse.quote_plus(NickName)}"
    Character_Get = requests.get(Character_Url)
    Character_Html = Character_Get.text
    Character_Soup = BeautifulSoup(Character_Html, "html.parser")

    Character_Data = Character_Soup.find("div", attrs={"class": "profile-info"})

    Character_Server = Character_Soup.find("span", attrs={"class": "profile-character-info__server"}).get_text().replace("@", "")

    Character_Expedition_Lv = int(Character_Data.find("div", attrs={"class": "level-info__expedition"}).find_all("span")[1].get_text().replace("Lv.", ""))
    Character_Battle_Lv = int(Character_Data.find("div", attrs={"class": "level-info__item"}).find_all("span")[1].get_text().replace("Lv.", ""))
    Character_Now_Item_Lv = Character_Data.find("div", attrs={"class": "level-info2__expedition"}).find_all("span")[1].get_text().replace("Lv.", "")
    Character_Max_Item_Lv = Character_Data.find("div", attrs={"class": "level-info2__item"}).find_all("span")[1].get_text().replace("Lv.", "")

    Character_Title = Character_Data.find("div", attrs={"class": "game-info__title"}).find_all("span")[1].get_text()
    Character_Guild = Character_Data.find("div", attrs={"class": "game-info__guild"}).find_all("span")[1].get_text()
    Character_PvP = Character_Data.find("div", attrs={"class": "level-info__pvp"}).find_all("span")[1].get_text()
    Character_Wisdom_Lv = Character_Data.find("div", attrs={"class": "game-info__wisdom"}).find_all("span")[1].get_text()
    Character_Wisdom_Name = Character_Data.find("div", attrs={"class": "game-info__wisdom"}).find_all("span")[2].get_text()

    Character_Basic_Data = Character_Soup.find("div", attrs={"class": "profile-ability-basic"}).find_all("span")
    if len(Character_Basic_Data) == 0:
        Character_Basic_Attack = 0
        Character_Basic_Health = 0
    else:
        Character_Basic_Attack = int(Character_Basic_Data[1].get_text())
        Character_Basic_Health = int(Character_Basic_Data[3].get_text())

    Character_Battle_Data = Character_Soup.find("div", attrs={"class": "profile-ability-battle"}).find_all("span")
    if len(Character_Battle_Data) == 0:
        Character_Battle_Critical = 0
        Character_Battle_Specialty = 0
        Character_Battle_Subdue = 0
        Character_Battle_Agility = 0
        Character_Battle_Endurance = 0
        Character_Battle_Proficiency = 0
    else:
        Character_Battle_Critical = int(Character_Battle_Data[1].get_text())
        Character_Battle_Specialty = int(Character_Battle_Data[3].get_text())
        Character_Battle_Subdue = int(Character_Battle_Data[5].get_text())
        Character_Battle_Agility = int(Character_Battle_Data[7].get_text())
        Character_Battle_Endurance = int(Character_Battle_Data[9].get_text())
        Character_Battle_Proficiency = int(Character_Battle_Data[11].get_text())

    Character_Engrave_Data = Character_Soup.find("div", attrs={"class": "profile-ability-engrave"}).find_all("span")
    Character_Engrave_List = []

    for Character_Engrave in Character_Engrave_Data:
        Character_Engrave_List.append(Character_Engrave.get_text())

    Character_Engrave_Discription_Data = Character_Soup.find("div", attrs={"class": "profile-ability-engrave"}).find_all("p")
    Character_Engrave_Discription_List = []

    for Character_Engrave_Discription in Character_Engrave_Discription_Data:
        Character_Engrave_Discription_List.append(Character_Engrave_Discription.get_text())

    Character_Script_List = Character_Soup.find_all("script", attrs={"type": "text/javascript"})
    Character_Tendency_List = str(Character_Script_List[len(Character_Script_List) - 5]).split("value")[1].split("max")[0].split("[")[1].split("]")[0].replace(" ", "").replace("\r\n", "").split(",")

    """
        서버:                   Character_Server

        원정대 레벨:            Character_Expedition_Lv
        전투 레벨:              Character_Battle_Lv
        현재 아이템 레벨:       Character_Now_Item_Lv
        최대 아이템 레벨:       Character_Max_Item_Lv

        칭호:                   Character_Title
        길드:                   Character_Guild
        PVP:                    Character_PvP
        영지 레벨:              Character_Wisdom_Lv
        영지 이름:              Character_Wisdom_Name

        기본 공격력:            Character_Basic_Attack
        기본 체력:              Character_Basic_Health

        전투 특성 치명:         Character_Battle_Critical
        전투 특성 특화:         Character_Battle_Specialty
        전투 특성 제압:         Character_Battle_Subdue
        전투 특성 신속:         Character_Battle_Agility
        전투 특성 인내:         Character_Battle_Endurance
        전투 특성 숙련:         Character_Battle_Proficiency

        각인 효과 이름 배열:    Character_Engrave_List
        각인 효과 설명 배열:    Character_Engrave_Discription_List

        성향 수치 배열:         Character_Tendency_List
    """
    
    Result = {
        "Result": "Success",
        "NickName": NickName,
        "Server": Character_Server,
        "Lv": {
            "Expedition": Character_Expedition_Lv,
            "Battle": Character_Battle_Lv,
            "Now_Item": Character_Now_Item_Lv,
            "Max_Item": Character_Max_Item_Lv
        },
        "Game": {
            "Title": Character_Title,
            "Guild": Character_Guild,
            "Pvp": Character_PvP,
            "Wisdom": {
                "Name": Character_Wisdom_Name,
                "Lv": Character_Wisdom_Lv
            }
        },
        "Basic": {
            "ATK": Character_Basic_Attack,
            "HP": Character_Basic_Health
        },
        "Battle": {
            "Critical": Character_Battle_Critical,
            "Specialty": Character_Battle_Specialty,
            "Subdue": Character_Battle_Subdue,
            "Agility": Character_Battle_Agility,
            "Endurance": Character_Battle_Endurance,
            "Proficiency": Character_Battle_Proficiency
        },
        "Engrave": {
            "Name": Character_Engrave_List,
            "Discription": Character_Engrave_Discription_List
        },
        "Tendency": {
            "Intellect": int(Character_Tendency_List[0]),
            "Bravery": int(Character_Tendency_List[1]),
            "Charm": int(Character_Tendency_List[2]),
            "Kindness": int(Character_Tendency_List[3]),
        }
    }

    return json.dumps(Result, ensure_ascii=False)

@Character.route("/Character-Item")
def function_Character_Item():
    NickName = request.args.get("NickName")

    if NickName == None:
        return json.dumps({"Result": "Error", "Error_Result": "NickName"})

    Character_Url = f"https://lostark.game.onstove.com/Profile/Character/{parse.quote_plus(NickName)}"
    Character_Get = requests.get(Character_Url)
    Character_Html = Character_Get.text
    Character_Soup = BeautifulSoup(Character_Html, "html.parser")

    Character_Script = Character_Soup.find("script", attrs={"type": "text/javascript"})
    Character_Script_Dict = json.loads(str(Character_Script).replace('<script type="text/javascript">', '').replace("$.Profile = ", "").replace(";", "").replace("</script>", "").strip())

    Character_Equip_Data = Character_Soup.find("div", attrs={"class": "profile-equipment__slot"}).find_all("div")

    Character_Equip_Type = {
        0: "Head",
        1: "Shoulder",
        2: "Top",
        3: "Bottom",
        4: "Gloves",
        5: "Weapon",
        6: "Pendant",
        7: "EarRing1",
        8: "EarRing2",
        9: "Ring1",
        10: "Ring2",
        11: "Bracelet",
        12: "Stone"
    }

    for i in range(len(Character_Equip_Data) - 2):
        Character_Equip = Character_Equip_Data[i]
    
        if Character_Equip["data-grade"] == "":
            continue
        Character_Equip_Data_Item = Character_Equip["data-item"]
        Character_Equip_Data_Dict = Character_Script_Dict["Equip"][Character_Equip_Data_Item]

        Character_Equip_Item_Name = Character_Equip_Data_Dict["Element_000"]["value"].split("'>")[2].split("</FONT>")[0]
        Character_Equip_Item_Type = Character_Equip_Data_Dict["Element_001"]["value"]["leftStr0"].split("'>")[2].split("</FONT>")[0]
        Character_Equip_Item_Lv = Character_Equip_Data_Dict["Element_001"]["value"]["leftStr2"].split("'>")[1].split("</FONT>")[0]
        Character_Equip_Item_Quality = Character_Equip_Data_Dict["Element_001"]["value"]["qualityValue"]
        Character_Equip_Item_Icon = Character_Equip_Data_Dict["Element_001"]["value"]["slotData"]["iconPath"]

        if i <= 5:
            Character_Equip_Item_Option = Character_Equip_Data_Dict["Element_005"]["value"]["Element_001"].split("<BR>")
        else:
            Character_Equip_Item_Option = []#.split("'>")[1].split("</FONT>")[0]
            for j in range(len(Character_Equip_Data_Dict["Element_005"]["value"]["Element_001"].split("<BR>"))):
                Character_Equip_Item_Option.append(Character_Equip_Data_Dict["Element_005"]["value"]["Element_001"].split("<BR>")[j])

        print(f"{Character_Equip_Type[i]} - {Character_Equip_Item_Name} - {Character_Equip_Item_Option}")


    Character_Data = Character_Soup.find("div", attrs={"class": "profile-info"})

    Character_Special_List = Character_Data.find("ul", attrs={"class": "special-info__slot"}).find_all("div", attrs={"class": "slot"})
    
    Character_Special_Name_List = []
    Character_Special_Data_Item_List = []

    for Character_Special_Data in Character_Special_List:
        if Character_Special_Data["data-grade"] == "":
            continue
        Character_Special_Data_Item = Character_Special_Data["data-item"]
        Character_Special_Data_Dict = Character_Script_Dict["Equip"][Character_Special_Data_Item]

        Character_Special_Name = Character_Special_Data_Dict["Element_000"]["value"].split("'>")[2].replace("</FONT></P>", "")

        #print(Character_Special_Data_Dict)

    return "a"