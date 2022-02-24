from flask import Blueprint, request, render_template
from urllib import parse
from bs4 import BeautifulSoup
import json, random, requests, dbconfig_LostArk

Character = Blueprint("Character", __name__, url_prefix="/LostArk/Character")
db_Class = dbconfig_LostArk.DataBase()

def str2Bs4(string):
    return BeautifulSoup(string, "html.parser")

@Character.route("/Character-Another")
def function_Character_Another():
    NickName = request.args.get("NickName")

    if NickName == None:
        return json.dumps({"Result": "Error", "Error_Result": "NickName"})

    if parse.quote_plus(NickName).replace("%20", "").replace("+", "") == "":
        return json.dumps({"Result": "Error", "Error_Result": "NickName"})

    Character_Url = f"https://lostark.game.onstove.com/Profile/Character/{parse.quote_plus(NickName).replace('%20', '').replace('+', '')}"
    Character_Get = requests.get(Character_Url)
    Character_Html = Character_Get.text
    Character_Soup = BeautifulSoup(Character_Html, "html.parser")

    if Character_Soup.find("div", attrs={"class": "profile-attention"}) is not None:
        return json.dumps({"Result": "Error", "Error_Result": "Not Found NickName"})

    Character_Server_List = Character_Soup.find_all("strong", attrs={"class": "profile-character-list__server"})
    Character_List = Character_Soup.find_all("ul", attrs={"class": "profile-character-list__char"})

    Result_List = {
        "Result": "Success"
    }

    for i in range(len(Character_Server_List)):
        Result_List[Character_Server_List[i].get_text().replace("@", "")] = {}

        Character_List_Button = Character_List[i].find_all("button")

        for j in range(len(Character_List_Button)):
            Result_List[Character_Server_List[i].get_text().replace("@", "")][j] = {
                "Name": Character_List_Button[j].find("span").get_text(),
                "Level": Character_List_Button[j].get_text().strip().replace(Character_List_Button[j].find("span").get_text(), ""),
            }

    return json.dumps(Result_List, ensure_ascii=False)

@Character.route("/Character-Data")
def function_Character_Data():
    NickName = request.args.get("NickName")

    if NickName == None:
        return json.dumps({"Result": "Error", "Error_Result": "NickName"})

    if parse.quote_plus(NickName).replace("%20", "").replace("+", "") == "":
        return json.dumps({"Result": "Error", "Error_Result": "NickName"})

    Character_Url = f"https://lostark.game.onstove.com/Profile/Character/{parse.quote_plus(NickName).replace('%20', '').replace('+', '')}"
    Character_Get = requests.get(Character_Url)
    Character_Html = Character_Get.text
    Character_Soup = BeautifulSoup(Character_Html, "html.parser")

    if Character_Soup.find("div", attrs={"class": "profile-attention"}) is not None:
        return json.dumps({"Result": "Error", "Error_Result": "Not Found NickName"})
    
    Character_Name = Character_Soup.find("span", attrs={"class": "profile-character-info__name"}).get_text()
    Character_Server_Name = Character_Soup.find("span", attrs={"class": "profile-character-info__server"}).get_text().replace("@", "")
    Character_Class_Name = Character_Soup.find("img", attrs={"class": "profile-character-info__img"})["alt"]
    Character_Class_Emblem = Character_Soup.find("img", attrs={"class": "profile-character-info__img"})["src"]

    Character_Expedition_Level = Character_Soup.find("div", attrs={"class": "level-info__expedition"}).find_all("span")[1].get_text()
    Character_Battle_Level = Character_Soup.find("div", attrs={"class": "level-info__item"}).find_all("span")[1].get_text()
    Character_Equip_Item_Level = Character_Soup.find("div", attrs={"class": "level-info2__expedition"}).find_all("span")[1].get_text()
    Character_Max_Item_Level = Character_Soup.find("div", attrs={"class": "level-info2__item"}).find_all("span")[1].get_text()

    Character_Title = Character_Soup.find("div", attrs={"class": "game-info__title"}).find_all("span")[1].get_text()
    Character_Guild = Character_Soup.find("div", attrs={"class": "game-info__guild"}).find_all("span")[1].get_text()
    Character_Pvp = Character_Soup.find("div", attrs={"class": "level-info__pvp"}).find_all("span")[1].get_text()

    Character_Wisdom_Name = Character_Soup.find("div", attrs={"class": "game-info__wisdom"}).find_all("span")[2].get_text()
    Character_Wisdom_Level = Character_Soup.find("div", attrs={"class": "game-info__wisdom"}).find_all("span")[1].get_text()

    Character_Basic_Data = Character_Soup.find("div", attrs={"class": "profile-ability-basic"}).find_all("span")
    if len(Character_Basic_Data) == 0:
        Character_Atk = 0
        Character_Hp = 0
    else:
        Character_Atk = int(Character_Basic_Data[1].get_text())
        Character_Hp = int(Character_Basic_Data[3].get_text())

    Character_Battle_Data = Character_Soup.find("div", attrs={"class": "profile-ability-battle"}).find_all("span")
    if len(Character_Battle_Data) == 0:
        Character_Critical = 0
        Character_Specialty = 0
        Character_Subdue = 0
        Character_Agility = 0
        Character_Endurance = 0
        Character_Proficiency = 0
    else:
        Character_Critical = int(Character_Battle_Data[1].get_text())
        Character_Specialty = int(Character_Battle_Data[3].get_text())
        Character_Subdue = int(Character_Battle_Data[5].get_text())
        Character_Agility = int(Character_Battle_Data[7].get_text())
        Character_Endurance = int(Character_Battle_Data[9].get_text())
        Character_Proficiency = int(Character_Battle_Data[11].get_text())

    Character_Engrave = {}
    Character_Engrave_Name_List = Character_Soup.find("div", attrs={"class": "profile-ability-engrave"}).find_all("span")
    Character_Engrave_Discription_List = Character_Soup.find("div", attrs={"class": "profile-ability-engrave"}).find_all("p")

    for i in range(len(Character_Engrave_Name_List)):
        Character_Engrave[i] = {
            "Name": Character_Engrave_Name_List[i].get_text(),
            "Discription": Character_Engrave_Discription_List[i].get_text().replace("\n", "")
        }

    Character_Tendency_List = str(Character_Soup.find_all("script", attrs={"type": "text/javascript"})[7]).split("value: [")[1].split("],")[0].replace("\r\n", "").replace(" ", "").split(",")
    Character_Tendency = {
        "Intellect": int(Character_Tendency_List[0]),
        "Bravery": int(Character_Tendency_List[1]),
        "Charm": int(Character_Tendency_List[2]),
        "Kindness": int(Character_Tendency_List[3]),
    }

    Result_List = {
        "Result": "Success",
        "Info": {
            "NickName": Character_Name,
            "Server": Character_Server_Name,
            "Class": {
                "Name": Character_Class_Name,
                "Icon": Character_Class_Emblem
            },
            "Level": {
                "Expedition": Character_Expedition_Level,
                "Battle": Character_Battle_Level,
                "Item": {
                    "Equip": Character_Equip_Item_Level,
                    "Max": Character_Max_Item_Level
                }
            },
            "Title": Character_Title,
            "Guild": Character_Guild,
            "Pvp": Character_Pvp,
            "Wisdom": {
                "Name": Character_Wisdom_Name,
                "Level": Character_Wisdom_Level
            },
            "Basic": {
                "Attack": Character_Atk,
                "HealthPoint": Character_Hp
            },
            "Battle": {
                "Critical": Character_Critical,
                "Specialty": Character_Specialty,
                "Subdue": Character_Subdue,
                "Agility": Character_Agility,
                "Endurance": Character_Endurance,
                "Proficiency": Character_Proficiency
            },
            "Engrave": Character_Engrave,
            "Tendency": Character_Tendency
        }
    }

    return json.dumps(Result_List, ensure_ascii=False)

@Character.route("/Character-Item")
def function_Character_Item():
    NickName = request.args.get("NickName")

    if NickName == None:
        return json.dumps({"Result": "Error", "Error_Result": "NickName"})

    if parse.quote_plus(NickName).replace("%20", "").replace("+", "") == "":
        return json.dumps({"Result": "Error", "Error_Result": "NickName"})

    Character_Url = f"https://lostark.game.onstove.com/Profile/Character/{parse.quote_plus(NickName).replace('%20', '').replace('+', '')}"
    Character_Get = requests.get(Character_Url)
    Character_Html = Character_Get.text
    Character_Soup = BeautifulSoup(Character_Html, "html.parser")

    if Character_Soup.find("div", attrs={"class": "profile-attention"}) is not None:
        return json.dumps({"Result": "Error", "Error_Result": "Not Found NickName"})

    Character_Item_List = Character_Soup.find("div", attrs={"class": "profile-equipment__slot"}).find_all("div")
    
    Character_Equip_Type = {
        0: "머리 방어구",
        1: "어깨 방어구",
        2: "상의",
        3: "하의",
        4: "장갑",
        5: "무기",
        6: "목걸이",
        7: "귀걸이1",
        8: "귀걸이2",
        9: "반지1",
        10: "반지2",
        11: "팔찌",
        12: "어빌리티 스톤"
    }

    Result_List = {
        "Result": "Success",
        "Items": {}
    }

    for i in range(len(Character_Item_List) - 2):
        if Character_Item_List[i]["data-grade"] == "":
            continue
        Character_Item_Script = json.loads(str(Character_Soup.find("script", attrs={"type": "text/javascript"})).replace('<script type="text/javascript">', '').replace("$.Profile = ", "").replace(";", "").replace("</script>", "").strip())

        Character_Item_Data = Character_Item_Script["Equip"][Character_Item_List[i]["data-item"]]
        Character_Item_Name = str2Bs4(Character_Item_Data["Element_000"]["value"]).get_text()
        Character_Item_Upgrade = "0"

        if Character_Item_Name[:1] == "+":
            Character_Item_Upgrade = Character_Item_Name.split(" ")[0]
            Character_Item_Name = " ".join(Character_Item_Name.split(" ")[1:])
        
        Character_Item_Parts = str2Bs4(Character_Item_Data["Element_001"]["value"]["leftStr0"]).get_text()
        Character_Item_Level = str2Bs4(Character_Item_Data["Element_001"]["value"]["leftStr2"]).get_text()
        Character_Item_Quality = Character_Item_Data["Element_001"]["value"]["qualityValue"]

        Character_Item_Option = {}
        
        if str2Bs4(Character_Item_Data["Element_005"]["value"]["Element_000"]).get_text() == "기본 효과": # 머리, 어깨, 상의, 하의, 장갑, 무기, 목걸이, 귀걸이, 반지
            Character_Item_Option["Basic"] = {}

            Character_Item_Option_Basic_List = Character_Item_Data["Element_005"]["value"]["Element_001"].split("<BR>")
            for j in range(len(Character_Item_Option_Basic_List)):
                Character_Item_Option_Basic_Name = str2Bs4(Character_Item_Option_Basic_List[j]).get_text().split("+")[0].strip()
                Character_Item_Option_Basic_Value = f'+{str2Bs4(Character_Item_Option_Basic_List[j]).get_text().split("+")[1].strip()}'
                
                Character_Item_Option["Basic"][Character_Item_Option_Basic_Name] = Character_Item_Option_Basic_Value

        if str2Bs4(Character_Item_Data["Element_005"]["value"]["Element_000"]).get_text() == "팔찌 효과": # 팔찌
            Character_Item_Option["Bracelet Option"] = {}

            Character_Item_Option_Bracelet_List = Character_Item_Data["Element_005"]["value"]["Element_001"].split("<BR>")
            Character_Item_Option_Bracelet_Other_List = []
            for k in range(len(Character_Item_Option_Bracelet_List)):
                if "+" in str2Bs4(Character_Item_Option_Bracelet_List[k]).get_text(): # + 확인
                    Character_Item_Option_Bracelet_Name = str2Bs4(Character_Item_Option_Bracelet_List[k]).get_text().split("+")[0].strip()
                    Character_Item_Option_Bracelet_Value = f'+{str2Bs4(Character_Item_Option_Bracelet_List[k]).get_text().split("+")[1].strip()}'

                    Character_Item_Option["Bracelet Option"][Character_Item_Option_Bracelet_Name] = Character_Item_Option_Bracelet_Value

                else:
                    Character_Item_Option_Bracelet_Other_List.append(str2Bs4(Character_Item_Option_Bracelet_List[k]).get_text())

            Character_Item_Option["Bracelet Option"]["Other"] = Character_Item_Option_Bracelet_Other_List

        if "Element_000" in Character_Item_Data["Element_004"]["value"]:
            if str2Bs4(Character_Item_Data["Element_004"]["value"]["Element_000"]).get_text() == "기본 효과": # 팔찌
                Character_Item_Option["Basic"] = {}

                Character_Item_Option_Basic_List = Character_Item_Data["Element_004"]["value"]["Element_001"].split("<BR>")
                for l in range(len(Character_Item_Option_Basic_List)):
                    Character_Item_Option_Basic_Name = str2Bs4(Character_Item_Option_Basic_List[l]).get_text().split("+")[0].strip()
                    Character_Item_Option_Basic_Value = f'+{str2Bs4(Character_Item_Option_Basic_List[l]).get_text().split("+")[1].strip()}'
                    
                    Character_Item_Option["Basic"][Character_Item_Option_Basic_Name] = Character_Item_Option_Basic_Value

        if str2Bs4(Character_Item_Data["Element_005"]["value"]["Element_000"]).get_text() == "세공 단계 보너스": # 팔찌
            Character_Item_Option["Work Bonus Option"] = {}

            Character_Item_Option_Work_List = Character_Item_Data["Element_005"]["value"]["Element_001"].split("<BR>")
            for m in range(len(Character_Item_Option_Work_List)):
                Character_Item_Option_Work_Name = str2Bs4(Character_Item_Option_Work_List[m]).get_text().split("+")[0].strip()
                Character_Item_Option_Work_Value = f'+{str2Bs4(Character_Item_Option_Work_List[m]).get_text().split("+")[1].strip()}'
                
                Character_Item_Option["Work Bonus Option"][Character_Item_Option_Work_Name] = Character_Item_Option_Work_Value

        if "Element_000" in Character_Item_Data["Element_006"]["value"]:
            if str2Bs4(Character_Item_Data["Element_006"]["value"]["Element_000"]).get_text() == "추가 효과": # 머리, 어깨, 상의, 하의, 장갑, 무기, 목걸이, 귀걸이, 반지
                Character_Item_Option["Plus"] = {}

                Character_Item_Option_Plus_List = Character_Item_Data["Element_006"]["value"]["Element_001"].split("<BR>")
                for n in range(len(Character_Item_Option_Plus_List)):
                    Character_Item_Option_Plus_Name = str2Bs4(Character_Item_Option_Plus_List[n]).get_text().split("+")[0].strip()
                    Character_Item_Option_Plus_Value = f'+{str2Bs4(Character_Item_Option_Plus_List[n]).get_text().split("+")[1].strip()}'
                    
                    Character_Item_Option["Plus"][Character_Item_Option_Plus_Name] = Character_Item_Option_Plus_Value

        if "Element_000" in Character_Item_Data["Element_007"]["value"]: # 트라이포드
            if "topStr" in Character_Item_Data["Element_007"]["value"]["Element_000"]:
                if str2Bs4(Character_Item_Data["Element_007"]["value"]["Element_000"]["topStr"]).get_text() == "트라이포드 효과": # 머리, 어깨, 상의, 하의, 장갑, 무기
                    Character_Item_Option["Triford"] = {}

                    Character_Item_Option_Triford_List = Character_Item_Data["Element_007"]["value"]["Element_000"]["contentStr"]
                    o = 0
                    for Character_Item_Option_Triford in Character_Item_Option_Triford_List:
                        Character_Item_Option_Triford_Name = str2Bs4(Character_Item_Option_Triford_List[Character_Item_Option_Triford]["contentStr"]).get_text().split("Lv")[0].strip()
                        Character_Item_Option_Triford_Level = str2Bs4(Character_Item_Option_Triford_List[Character_Item_Option_Triford]["contentStr"]).get_text().split("Lv")[1].strip()

                        Character_Item_Option["Triford"][o] = {
                            "Name": Character_Item_Option_Triford_Name,
                            "Level": Character_Item_Option_Triford_Level
                        }

                        o += 1

        if "Element_008" in Character_Item_Data:
            if "Element_000" in Character_Item_Data["Element_008"]["value"]: # 트라이포드 재련 안됨
                if "topStr" in Character_Item_Data["Element_008"]["value"]["Element_000"]:
                    if str2Bs4(Character_Item_Data["Element_008"]["value"]["Element_000"]["topStr"]).get_text() == "트라이포드 효과": # 머리, 어깨, 상의, 하의, 장갑, 무기
                        Character_Item_Option["Triford"] = {}

                        Character_Item_Option_Triford_List = Character_Item_Data["Element_008"]["value"]["Element_000"]["contentStr"]
                        o = 0
                        for Character_Item_Option_Triford in Character_Item_Option_Triford_List:
                            Character_Item_Option_Triford_Name = str2Bs4(Character_Item_Option_Triford_List[Character_Item_Option_Triford]["contentStr"]).get_text().split("Lv")[0].strip()
                            Character_Item_Option_Triford_Level = str2Bs4(Character_Item_Option_Triford_List[Character_Item_Option_Triford]["contentStr"]).get_text().split("Lv")[1].strip()

                            Character_Item_Option["Triford"][o] = {
                                "Name": Character_Item_Option_Triford_Name,
                                "Level": Character_Item_Option_Triford_Level
                            }

                            o += 1

        if "Element_000" in Character_Item_Data["Element_007"]["value"]: # 무작위 각인
            if type(Character_Item_Data["Element_007"]["value"]["Element_000"]) == str:
                if str2Bs4(Character_Item_Data["Element_007"]["value"]["Element_000"]).get_text() == "무작위 각인 효과": # 목걸이, 귀걸이, 반지
                    Character_Item_Option["Engraving Effects"] = {}

                    Character_Item_Option_Engraving_List = Character_Item_Data["Element_007"]["value"]["Element_001"].split("<BR>")
                    for p in range(len(Character_Item_Option_Engraving_List)):
                        Character_Item_Option_Engraving_Name = str2Bs4(Character_Item_Option_Engraving_List[p]).get_text().split("+")[0].strip()
                        Character_Item_Option_Engraving_Value = f'+{str2Bs4(Character_Item_Option_Engraving_List[p]).get_text().split("+")[1].strip()}'
                        
                        Character_Item_Option["Engraving Effects"][p] = {
                            "Name": Character_Item_Option_Engraving_Name,
                            "Value": Character_Item_Option_Engraving_Value
                        }

        if "Element_000" in Character_Item_Data["Element_006"]["value"]: # 무작위 각인
            if type(Character_Item_Data["Element_006"]["value"]["Element_000"]) == str:
                if str2Bs4(Character_Item_Data["Element_006"]["value"]["Element_000"]).get_text() == "무작위 각인 효과": # 목걸이, 귀걸이, 반지
                    Character_Item_Option["Engraving Effects"] = {}

                    Character_Item_Option_Engraving_List = Character_Item_Data["Element_006"]["value"]["Element_001"].split("<BR>")
                    for p in range(len(Character_Item_Option_Engraving_List)):
                        Character_Item_Option_Engraving_Name = str2Bs4(Character_Item_Option_Engraving_List[p]).get_text().split("+")[0].strip()
                        Character_Item_Option_Engraving_Value = f'+{str2Bs4(Character_Item_Option_Engraving_List[p]).get_text().split("+")[1].strip()}'
                        
                        Character_Item_Option["Engraving Effects"][p] = {
                            "Name": Character_Item_Option_Engraving_Name,
                            "Value": Character_Item_Option_Engraving_Value
                        }

        Character_Item_Set = {}

        if "Element_008" in Character_Item_Data: # 세트 효과
            if "Element_000" in Character_Item_Data["Element_008"]["value"]:
                if type(Character_Item_Data["Element_008"]["value"]["Element_000"]) == str:
                    if str2Bs4(Character_Item_Data["Element_008"]["value"]["Element_000"]).get_text() == "세트 효과 레벨": # 머리, 어깨, 상의, 하의, 장갑, 무기
                        Character_Item_Set["Name"] = str2Bs4(Character_Item_Data["Element_008"]["value"]["Element_001"]).get_text().split("Lv.")[0].strip()
                        Character_Item_Set["Level"] = str2Bs4(Character_Item_Data["Element_008"]["value"]["Element_001"]).get_text().split("Lv.")[1].strip()

        if "Element_009" in Character_Item_Data: # 세트 효과 활성화
            if "Element_000" in Character_Item_Data["Element_009"]["value"]:
                if type(Character_Item_Data["Element_009"]["value"]["Element_000"]) == dict:
                    if "contentStr" in Character_Item_Data["Element_009"]["value"]["Element_000"]:
                        Character_Item_Set["Set Enabled"] = {}

                        Character_Item_Set_Item_List = Character_Item_Data["Element_009"]["value"]["Element_000"]["contentStr"]
                        Character_Item_Set_Item_Enabled_List = []
                        Character_Item_Set_Item_Disabled_List = []

                        for Character_Item_Set_Item in Character_Item_Set_Item_List:
                            Character_Item_Set_Items = str2Bs4(Character_Item_Set_Item_List[Character_Item_Set_Item]["contentStr"]).get_text()
                            if "Lv" in Character_Item_Set_Items:
                                Character_Item_Set_Item_Enabled_List.append(Character_Item_Set_Items)
                            else:
                                Character_Item_Set_Item_Disabled_List.append(Character_Item_Set_Items)

                        if Character_Item_Set_Item_Enabled_List != []:
                            Character_Item_Set["Set Enabled"]["Enabled"] = Character_Item_Set_Item_Enabled_List

                        if Character_Item_Set_Item_Disabled_List != []:
                            Character_Item_Set["Set Enabled"]["Disabled"] = Character_Item_Set_Item_Disabled_List

            if type(Character_Item_Data["Element_009"]["value"]) == dict:
                for q in range(1, len(Character_Item_Data["Element_009"]["value"])):
                    if f"Element_00{q}" in Character_Item_Data["Element_009"]["value"]:
                        if "contentStr" in Character_Item_Data["Element_009"]["value"]["Element_001"]:
                            if not "Set Effects" in Character_Item_Set:
                                Character_Item_Set["Set Effects"] = {}

                            Character_Item_Set["Set Effects"][str2Bs4(Character_Item_Data["Element_009"]["value"][f"Element_00{q}"]["topStr"]).get_text().split("[")[0]] = {
                                "Name": str2Bs4(Character_Item_Data["Element_009"]["value"][f"Element_00{q}"]["topStr"]).get_text().split("[")[0],
                                "Level": str(Character_Item_Data["Element_009"]["value"][f"Element_00{q}"]["topStr"]).split("#FFD200'>")[1].split("<")[0],
                                "Value": str2Bs4(Character_Item_Data["Element_009"]["value"][f"Element_00{q}"]["contentStr"]["Element_000"]["contentStr"]).get_text()
                            }

        if "Element_009" in Character_Item_Data: # 세트 효과
            if "Element_000" in Character_Item_Data["Element_009"]["value"]:
                if type(Character_Item_Data["Element_009"]["value"]["Element_000"]) == str:
                    if str2Bs4(Character_Item_Data["Element_009"]["value"]["Element_000"]).get_text() == "세트 효과 레벨": # 머리, 어깨, 상의, 하의, 장갑, 무기
                        Character_Item_Set["Name"] = str2Bs4(Character_Item_Data["Element_009"]["value"]["Element_001"]).get_text().split("Lv.")[0].strip()
                        Character_Item_Set["Level"] = str2Bs4(Character_Item_Data["Element_009"]["value"]["Element_001"]).get_text().split("Lv.")[1].strip()

        if "Element_010" in Character_Item_Data: # 세트 효과 활성화
            if "Element_000" in Character_Item_Data["Element_010"]["value"]:
                if type(Character_Item_Data["Element_010"]["value"]["Element_000"]) == dict:
                    if "contentStr" in Character_Item_Data["Element_010"]["value"]["Element_000"]:
                        Character_Item_Set["Set Enabled"] = {}

                        Character_Item_Set_Item_List = Character_Item_Data["Element_010"]["value"]["Element_000"]["contentStr"]
                        Character_Item_Set_Item_Enabled_List = []
                        Character_Item_Set_Item_Disabled_List = []

                        for Character_Item_Set_Item in Character_Item_Set_Item_List:
                            Character_Item_Set_Items = str2Bs4(Character_Item_Set_Item_List[Character_Item_Set_Item]["contentStr"]).get_text()
                            if "Lv" in Character_Item_Set_Items:
                                Character_Item_Set_Item_Enabled_List.append(Character_Item_Set_Items)
                            else:
                                Character_Item_Set_Item_Disabled_List.append(Character_Item_Set_Items)

                        if Character_Item_Set_Item_Enabled_List != []:
                            Character_Item_Set["Set Enabled"]["Enabled"] = Character_Item_Set_Item_Enabled_List

                        if Character_Item_Set_Item_Disabled_List != []:
                            Character_Item_Set["Set Enabled"]["Disabled"] = Character_Item_Set_Item_Disabled_List

            if type(Character_Item_Data["Element_010"]["value"]) == dict:
                for r in range(1, len(Character_Item_Data["Element_010"]["value"])):
                    if f"Element_00{r}" in Character_Item_Data["Element_010"]["value"]:
                        if "contentStr" in Character_Item_Data["Element_010"]["value"]["Element_001"]:
                            if not "Set Effects" in Character_Item_Set:
                                Character_Item_Set["Set Effects"] = {}

                            Character_Item_Set["Set Effects"][str2Bs4(Character_Item_Data["Element_010"]["value"][f"Element_00{r}"]["topStr"]).get_text().split("[")[0]] = {
                                "Name": str2Bs4(Character_Item_Data["Element_010"]["value"][f"Element_00{r}"]["topStr"]).get_text().split("[")[0],
                                "Level": str(Character_Item_Data["Element_010"]["value"][f"Element_00{r}"]["topStr"]).split("#FFD200'>")[1].split("<")[0],
                                "Value": str2Bs4(Character_Item_Data["Element_010"]["value"][f"Element_00{r}"]["contentStr"]["Element_000"]["contentStr"]).get_text()
                            }

        #print(Character_Item_Data)
        Character_Item_Icon = Character_Item_Data["Element_001"]["value"]["slotData"]["iconPath"]
        
        Result_List["Items"][Character_Equip_Type[i]] = {
            "Name": Character_Item_Name,
            "Upgrade": Character_Item_Upgrade,
            "Parts": Character_Item_Parts,
            "Level": Character_Item_Level,
            "Quality": Character_Item_Quality,
            "Option": Character_Item_Option,
        }

        if Character_Item_Set != {}:
            Result_List["Items"][Character_Equip_Type[i]]["Set"] = Character_Item_Set
        
        Result_List["Items"][Character_Equip_Type[i]]["Icon"] = f"https://cdn-lostark.game.onstove.com/{Character_Item_Icon}"

    if Result_List["Items"] == {}:
        Result_List["Items"] = "장착된 아이템이 없습니다."

    return json.dumps(Result_List, ensure_ascii=False)

@Character.route("/Character-Avatar")
def function_Character_Avatar():
    NickName = request.args.get("NickName")

    if NickName == None:
        return json.dumps({"Result": "Error", "Error_Result": "NickName"})

    if parse.quote_plus(NickName).replace("%20", "").replace("+", "") == "":
        return json.dumps({"Result": "Error", "Error_Result": "NickName"})

    Character_Url = f"https://lostark.game.onstove.com/Profile/Character/{parse.quote_plus(NickName).replace('%20', '').replace('+', '')}"
    Character_Get = requests.get(Character_Url)
    Character_Html = Character_Get.text
    Character_Soup = BeautifulSoup(Character_Html, "html.parser")

    if Character_Soup.find("div", attrs={"class": "profile-attention"}) is not None:
        return json.dumps({"Result": "Error", "Error_Result": "Not Found NickName"})

    Character_Avatar_List = Character_Soup.find("div", attrs={"class": "profile-avatar__slot"}).find_all("div")

    Character_Avatar_Type_List = {
        "1": "무기 아바타",
        "1-1": "무기 덧입기 아바타",
        "2": "악기 아바타",
        "2-1": "악기 덧입기 아바타",
        "3": "머리 아바타",
        "3-1": "머리 덧입기 아바타",
        "4": "얼굴1 아바타",
        "4-1": "얼굴1 덧입기 아바타",
        "5": "얼굴2 아바타",
        "5-1": "얼굴2 덧입기 아바타",
        "6": "상의 아바타",
        "6-1": "상의 덧입기 아바타",
        "7": "하의 아바타",
        "7-1": "하의 덧입기 아바타",
    }

    Result_List = {
        "Result": "Success",
        "Avatars": {}
    }

    for i in range(len(Character_Avatar_List)):
        if Character_Avatar_List[i]["data-grade"] == "":
            continue
        Character_Avatar_Script = json.loads(str(Character_Soup.find("script", attrs={"type": "text/javascript"})).replace('<script type="text/javascript">', '').replace("$.Profile = ", "").replace(";", "").replace("</script>", "").strip())

        Character_Avatar_Type = Character_Avatar_Type_List[Character_Avatar_List[i]["class"][0][4:]]

        Character_Avatar_Data = Character_Avatar_Script["Equip"][Character_Avatar_List[i]["data-item"]]
        
        Character_Avatar_Name = str2Bs4(Character_Avatar_Data["Element_000"]["value"]).get_text()
        Character_Avatar_Parts = str2Bs4(Character_Avatar_Data["Element_001"]["value"]["leftStr0"]).get_text()
        Character_Avatar_Icon = str2Bs4(Character_Avatar_Data["Element_001"]["value"]["slotData"]["iconPath"]).get_text()

        Character_Avatar_Class = str2Bs4(Character_Avatar_Data["Element_002"]["value"]).get_text()
        Character_Avatar_Transaction_Split = Character_Avatar_Data["Element_003"]["value"].split("<BR>")
        if len(Character_Avatar_Transaction_Split) == 1:
            Character_Avatar_Attribution = str2Bs4(Character_Avatar_Transaction_Split[0]).get_text().strip()
            Character_Avatar_Transaction = 0
        else:
            Character_Avatar_Attribution = str2Bs4(Character_Avatar_Transaction_Split[0]).get_text().strip()
            Character_Avatar_Transaction = int(str2Bs4(Character_Avatar_Transaction_Split[1]).get_text().strip().replace("거래 ", "").replace("회 가능", ""))

        Character_Avatar_Basic_Element = "Element_005"
        Character_Avatar_Tendency_Element = "Element_006"

        if Character_Avatar_Data["Element_005"]["type"] == "SingleTextBox": # 덧입기 아바타
            Character_Avatar_Basic_Element = "Element_006"
            Character_Avatar_Tendency_Element = "Element_007"

        Character_Avatar_Basic = {}

        if "Element_000" in Character_Avatar_Data[Character_Avatar_Basic_Element]["value"]:
            if str2Bs4(Character_Avatar_Data[Character_Avatar_Basic_Element]["value"]["Element_000"]).get_text() == "기본 효과":
                Character_Avatar_Basic_List = str2Bs4(Character_Avatar_Data[Character_Avatar_Basic_Element]["value"]["Element_001"]).get_text().split("+")

                Character_Avatar_Basic[Character_Avatar_Basic_List[0].strip()] = f"+{Character_Avatar_Basic_List[1].strip()}"

        Character_Avatar_Tendency = {}

        if type(Character_Avatar_Data[Character_Avatar_Tendency_Element]["value"]) == dict:
            if str2Bs4(Character_Avatar_Data[Character_Avatar_Tendency_Element]["value"]["titleStr"]).get_text() == "성향":
                Character_Avatar_Tendency_List = str2Bs4(Character_Avatar_Data[Character_Avatar_Tendency_Element]["value"]["contentStr"]).get_text().split("&")[1:]
                for i in range(len(Character_Avatar_Tendency_List)):
                    Character_Avatar_Tendency_List_Split = Character_Avatar_Tendency_List[i].split(" ")
                    
                    Character_Avatar_Tendency[Character_Avatar_Tendency_List_Split[1].strip()] = int(Character_Avatar_Tendency_List_Split[3].strip())

        Result_List["Avatars"][Character_Avatar_Type] = {
            "Name": Character_Avatar_Name,
            "Parts": Character_Avatar_Parts,
            "Class": Character_Avatar_Class,
            "Transaction": {
                "Attribution": Character_Avatar_Attribution,
                "Transaction_Count": Character_Avatar_Transaction
            },
            "Icon": f"https://cdn-lostark.game.onstove.com/{Character_Avatar_Icon}"
        }

        if Character_Avatar_Basic != {}:
            Result_List["Avatars"][Character_Avatar_Type]["Basic"] = Character_Avatar_Basic

        if Character_Avatar_Tendency != {}:
            Result_List["Avatars"][Character_Avatar_Type]["Tendency"] = Character_Avatar_Tendency
    return json.dumps(Result_List, ensure_ascii=False)

@Character.route("/Character-Jewel")
def function_Character_Jewel():
    NickName = request.args.get("NickName")

    if NickName == None:
        return json.dumps({"Result": "Error", "Error_Result": "NickName"})

    if parse.quote_plus(NickName).replace("%20", "").replace("+", "") == "":
        return json.dumps({"Result": "Error", "Error_Result": "NickName"})

    Character_Url = f"https://lostark.game.onstove.com/Profile/Character/{parse.quote_plus(NickName).replace('%20', '').replace('+', '')}"
    Character_Get = requests.get(Character_Url)
    Character_Html = Character_Get.text
    Character_Soup = BeautifulSoup(Character_Html, "html.parser")

    if Character_Soup.find("div", attrs={"class": "profile-attention"}) is not None:
        return json.dumps({"Result": "Error", "Error_Result": "Not Found NickName"})

    Result_List = {
        "Result": "Success"
    }

    Character_Avatar_List = Character_Soup.find("div", attrs={"class": "jewel__wrap"}).find_all("span", attrs={"class": "jewel_btn"})

    if len(Character_Avatar_List) == 0:
        Result_List["Jewel"] = "장착된 보석이 없습니다."

    else:
        Result_List["Jewel"] = {}

        for i in range(len(Character_Avatar_List)):
            Character_Jewel_List = {}
            
            Character_Avatar_Script = json.loads(str(Character_Soup.find("script", attrs={"type": "text/javascript"})).replace('<script type="text/javascript">', '').replace("$.Profile = ", "").replace(";", "").replace("</script>", "").strip())

            Character_Jewel_Data = Character_Avatar_Script["Equip"][Character_Avatar_List[i]["data-item"]]

            Character_Jewel_Type = Character_Avatar_List[i].find("span", attrs={"class", "info"}).get_text()
            Character_Jewel_Name = str2Bs4(Character_Jewel_Data["Element_000"]["value"]).get_text()
            Character_Jewel_Grade = str2Bs4(Character_Jewel_Data["Element_001"]["value"]["leftStr0"]).get_text()
            Character_Jewel_Level = str2Bs4(Character_Jewel_Data["Element_001"]["value"]["leftStr2"]).get_text()
            Character_Jewel_Effect = str2Bs4(Character_Jewel_Data["Element_004"]["value"]["Element_001"]).get_text()
            Character_Jewel_Icon = str2Bs4(Character_Jewel_Data["Element_001"]["value"]["slotData"]["iconPath"]).get_text()

            Result_List["Jewel"][Character_Jewel_Type] = {
                "Name": Character_Jewel_Name,
                "Grade": Character_Jewel_Grade,
                "Level": Character_Jewel_Level,
                "Effect": Character_Jewel_Effect,
                "Icon": f"https://cdn-lostark.game.onstove.com/{Character_Jewel_Name}"
            }

    return json.dumps(Result_List, ensure_ascii=False)

@Character.route("/Character-Card")
def function_Character_Card():
    NickName = request.args.get("NickName")

    if NickName == None:
        return json.dumps({"Result": "Error", "Error_Result": "NickName"})

    if parse.quote_plus(NickName).replace("%20", "").replace("+", "") == "":
        return json.dumps({"Result": "Error", "Error_Result": "NickName"})

    Character_Url = f"https://lostark.game.onstove.com/Profile/Character/{parse.quote_plus(NickName).replace('%20', '').replace('+', '')}"
    Character_Get = requests.get(Character_Url)
    Character_Html = Character_Get.text
    Character_Soup = BeautifulSoup(Character_Html, "html.parser")

    if Character_Soup.find("div", attrs={"class": "profile-attention"}) is not None:
        return json.dumps({"Result": "Error", "Error_Result": "Not Found NickName"})

    Result_List = {
        "Result": "Success"
    }

    Character_Card_List = Character_Soup.find("ul", attrs={"class": "card-list"}).find_all("div", attrs={"class": "card-slot"})
    
    if len(Character_Card_List) == 0:
        Result_List["Card"] = "장착된 카드가 없습니다."

    else:
        Result_List["Card"] = {}

        for i in range(len(Character_Card_List)):
            Character_Card_Script = json.loads(str(Character_Soup.find("script", attrs={"type": "text/javascript"})).replace('<script type="text/javascript">', '').replace("$.Profile = ", "").replace(";", "").replace("</script>", "").strip())

            Character_Card_Data = Character_Card_Script["Card"][Character_Card_List[i]["data-item"]]

            Character_Card_Name = str2Bs4(Character_Card_Data["Element_000"]["value"]).get_text()
            Character_Card_Awake = Character_Card_Data["Element_001"]["value"]["awakeCount"]
            Character_Card_Awake_Max = Character_Card_Data["Element_001"]["value"]["awakeTotal"]
            Character_Card_Image = Character_Card_Data["Element_001"]["value"]["iconData"]["iconPath"]
            Character_Card_Discription = Character_Card_Data["Element_002"]["value"]

            Result_List["Card"][i] = {
                "Name": Character_Card_Name,
                "Discription": Character_Card_Discription,
                "Awake": {
                    "Count": Character_Card_Awake,
                    "Max": Character_Card_Awake_Max
                },
                "Image": f"https://cdn-lostark.game.onstove.com/{Character_Card_Image}"
            }

    Character_Card_Set_Check = Character_Soup.find("div", attrs={"class": "profile-card__content"}).find("p", attrs={"class": "profile-nodata"})

    if not Character_Card_Set_Check is None:
        Result_List["Set"] = "장착된 카드가 없습니다."

    else:
        Result_List["Set"] = {}

        Character_Card_Set_Name_List = Character_Soup.find("div", attrs={"class": "profile-card__content"}).find_all("div", attrs={"class": "card-effect__title"})
        Character_Card_Set_Effect_List = Character_Soup.find("div", attrs={"class": "profile-card__content"}).find_all("div", attrs={"class": "card-effect__dsc"})

        for j in range(len(Character_Card_Set_Name_List)):
            Result_List["Set"][j] = {
                "Name": Character_Card_Set_Name_List[j].get_text(),
                "Discription": Character_Card_Set_Effect_List[j].get_text(),
            }

    return json.dumps(Result_List, ensure_ascii=False)

@Character.route("/Character-Skill")
def function_Character_Skill():
    NickName = request.args.get("NickName")

    if NickName == None:
        return json.dumps({"Result": "Error", "Error_Result": "NickName"})

    if parse.quote_plus(NickName).replace("%20", "").replace("+", "") == "":
        return json.dumps({"Result": "Error", "Error_Result": "NickName"})

    Character_Url = f"https://lostark.game.onstove.com/Profile/Character/{parse.quote_plus(NickName).replace('%20', '').replace('+', '')}"
    Character_Get = requests.get(Character_Url)
    Character_Html = Character_Get.text
    Character_Soup = BeautifulSoup(Character_Html, "html.parser")

    if Character_Soup.find("div", attrs={"class": "profile-attention"}) is not None:
        return json.dumps({"Result": "Error", "Error_Result": "Not Found NickName"})

    Result_List = {
        "Result": "Success"
    }

    Character_Skill_Check = Character_Soup.find("div", attrs={"class": "profile-skill__list"}).find("p", attrs={"class": "profile-nodata"})
    if not Character_Skill_Check is None:
        Result_List["Skill"] = "사용할 수 있는 전투스킬이 없습니다."

    else:
        Result_List["Skill"] = {}

        Character_Skill_List = Character_Soup.find("div", attrs={"class": "profile-skill-battle"}).find_all("a", attrs={"class": "button--profile-skill"})

        for i in range(len(Character_Skill_List)):
            Character_Skill_Data = json.loads(Character_Skill_List[i]["data-skill"])

            Character_Skill_Name = Character_Skill_Data["name"]
            Character_Skill_Level = Character_Skill_Data["level"]
            Character_Skill_Type = str2Bs4(Character_Skill_Data["type"]).get_text()
            Character_Skill_Icon = Character_Skill_Data["slotIcon"]
            Character_Skill_Tripod_List = Character_Skill_Data["tripodList"]

            if len(Character_Skill_Tripod_List) != 0:
                Character_Skill_Tripod = {}

                for j in range(len(Character_Skill_Tripod_List)):
                    if not Character_Skill_Tripod_List[j]["level"] in Character_Skill_Tripod:
                        Character_Skill_Tripod[Character_Skill_Tripod_List[j]["level"]] = {}
                    
                    Character_Skill_Tripod[Character_Skill_Tripod_List[j]["level"]][Character_Skill_Tripod_List[j]["slot"]] = {
                        "Name": str2Bs4(Character_Skill_Tripod_List[j]["name"]).get_text(),
                        "Discription": str2Bs4(Character_Skill_Tripod_List[j]["description"]).get_text(),
                        "Level": Character_Skill_Tripod_List[j]["featureLevel"],
                        "Icon": f"https://cdn-lostark.game.onstove.com/{Character_Skill_Tripod_List[j]['slotIcon']}"
                    }

            Character_Skill_Rune = {}

            if "rune" in Character_Skill_Data:
                Character_Skill_Rune_Icon = Character_Skill_Data["rune"]["icon"]
                Character_Skill_Rune_Data = json.loads(Character_Skill_Data["rune"]["tooltip"])

                Character_Skill_Rune_Name = str2Bs4(Character_Skill_Rune_Data["Element_000"]["value"]).get_text()
                Character_Skill_Rune_Type = str2Bs4(Character_Skill_Rune_Data["Element_001"]["value"]["leftStr0"]).get_text()
                Character_Skill_Rune_Value = Character_Skill_Rune_Data["Element_002"]["value"]["Element_001"]
                
                Character_Skill_Rune = {
                    "Name": Character_Skill_Rune_Name,
                    "Type": Character_Skill_Rune_Type,
                    "Value": Character_Skill_Rune_Value
                }


            Result_List["Skill"][Character_Skill_Name] = {
                "Name": Character_Skill_Name,
                "Level": Character_Skill_Level,
                "Type": Character_Skill_Type,
                "Icon": f"https://cdn-lostark.game.onstove.com/{Character_Skill_Icon}"
            }

            if Character_Skill_Tripod != {}:
                Result_List["Skill"][Character_Skill_Name]["Tripod"] = Character_Skill_Tripod

            if Character_Skill_Rune != {}:
                Result_List["Skill"][Character_Skill_Name]["Rune"] = Character_Skill_Rune

    return json.dumps(Result_List, ensure_ascii=False)

@Character.route("/Character-Life")
def function_Character_Life():
    NickName = request.args.get("NickName")

    if NickName == None:
        return json.dumps({"Result": "Error", "Error_Result": "NickName"})

    if parse.quote_plus(NickName).replace("%20", "").replace("+", "") == "":
        return json.dumps({"Result": "Error", "Error_Result": "NickName"})

    Character_Url = f"https://lostark.game.onstove.com/Profile/Character/{parse.quote_plus(NickName).replace('%20', '').replace('+', '')}"
    Character_Get = requests.get(Character_Url)
    Character_Html = Character_Get.text
    Character_Soup = BeautifulSoup(Character_Html, "html.parser")

    if Character_Soup.find("div", attrs={"class": "profile-attention"}) is not None:
        return json.dumps({"Result": "Error", "Error_Result": "Not Found NickName"})

    Result_List = {
        "Result": "Success",
        "Life": {}
    }

    Character_Life = Character_Soup.find("div", attrs={"class": "profile-skill-life"}).find_all("li")
    
    for i in range(len(Character_Life)):
        Result_List["Life"][Character_Life[i].find("strong").get_text()] = Character_Life[i].find("span").get_text()

    return json.dumps(Result_List, ensure_ascii=False)