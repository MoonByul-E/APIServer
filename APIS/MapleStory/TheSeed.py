from flask import Blueprint, request, render_template
import json, random, dbconfig_MapleStory

TheSeed = Blueprint("TheSeed", __name__, url_prefix="/MapleStory/TheSeed")
db_Class = dbconfig_MapleStory.DataBase()

print("TheSeed 로딩 시작.")

TheSeed_Box_Level_List = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]

TheSeed_AliciaRingBox = {}
TheSeed_HideRingBox = {}
TheSeed_ShineRingBox = {}
TheSeed_Ring_Level = {}

for i in range(1, 11):
    TheSeed_AliciaRingBox[i] = {}

    TheSeed_AliciaRingBox_SQL = f"SELECT * FROM TheSeed_AliciaRingBox_{i}"
    TheSeed_AliciaRingBox_ROW = db_Class.executeAll(TheSeed_AliciaRingBox_SQL)

    TheSeed_AliciaRingBox_Name = []
    TheSeed_AliciaRingBox_Probability = []

    for TheSeed_AliciaRingBox_Data in TheSeed_AliciaRingBox_ROW:
        TheSeed_AliciaRingBox_Name.append(TheSeed_AliciaRingBox_Data["Name"])
        TheSeed_AliciaRingBox_Probability.append(int(TheSeed_AliciaRingBox_Data["Probability"].replace(".", "")))

    TheSeed_AliciaRingBox[i]["Name"] = TheSeed_AliciaRingBox_Name
    TheSeed_AliciaRingBox[i]["Probability"] = TheSeed_AliciaRingBox_Probability

TheSeed_HideRingBox_SQL = f"SELECT * FROM TheSeed_HideRingBox"
TheSeed_HideRingBox_ROW = db_Class.executeAll(TheSeed_HideRingBox_SQL)

TheSeed_HideRingBox_Name = []
TheSeed_HideRingBox_Probability = []

for TheSeed_HideRingBox_Data in TheSeed_HideRingBox_ROW:
    TheSeed_HideRingBox_Name.append(TheSeed_HideRingBox_Data["Name"])
    TheSeed_HideRingBox_Probability.append(int(TheSeed_HideRingBox_Data["Probability"].replace(".", "")))

TheSeed_HideRingBox["Name"] = TheSeed_HideRingBox_Name
TheSeed_HideRingBox["Probability"] = TheSeed_HideRingBox_Probability

TheSeed_ShineRingBox_SQL = f"SELECT * FROM TheSeed_ShineRingBox"
TheSeed_ShineRingBox_ROW = db_Class.executeAll(TheSeed_ShineRingBox_SQL)

TheSeed_ShineRingBox_Name = []
TheSeed_ShineRingBox_Probability = []

for TheSeed_ShineRingBox_Data in TheSeed_ShineRingBox_ROW:
    TheSeed_ShineRingBox_Name.append(TheSeed_ShineRingBox_Data["Name"])
    TheSeed_ShineRingBox_Probability.append(int(TheSeed_ShineRingBox_Data["Probability"].replace(".", "")))

TheSeed_ShineRingBox["Name"] = TheSeed_ShineRingBox_Name
TheSeed_ShineRingBox["Probability"] = TheSeed_ShineRingBox_Probability

TheSeed_Ring_Level_SQL = f"SELECT * FROM TheSeed_Ring_Level"
TheSeed_Ring_Level_ROW = db_Class.executeAll(TheSeed_Ring_Level_SQL)

TheSeed_Ring_Level_Name = []
TheSeed_Ring_Level_Probability = []

for TheSeed_Ring_Level_Data in TheSeed_Ring_Level_ROW:
    TheSeed_Ring_Level_Name.append(TheSeed_Ring_Level_Data["Name"])
    TheSeed_Ring_Level_Probability.append(int(TheSeed_Ring_Level_Data["Probability"].replace(".", "")))

TheSeed_Ring_Level["Name"] = TheSeed_Ring_Level_Name
TheSeed_Ring_Level["Probability"] = TheSeed_Ring_Level_Probability

print("TheSeed 로딩 종료.")

@TheSeed.route("/AliciaRingBox-Simulator")
def function_TheSeed_AliciaRingBox():
    Box_Level = "1"

    if request.args.get("Box_Level") != None:
        Box_Level = request.args.get("Box_Level")

    Box_Level_Check = False

    for i in range(len(TheSeed_Box_Level_List)):
        if Box_Level == TheSeed_Box_Level_List[i]:
            Box_Level_Check = True

    if Box_Level_Check == False:
        return json.dumps({"Result": "Error", "Error_Result": "Box_Level"})

    Random = random.randrange(1, sum(TheSeed_AliciaRingBox[int(Box_Level)]["Probability"]))
    
    TheSeed_AliciaRingBox_Item_Name = ""
    TheSeed_AliciaRingBox_Item_Probability = 0

    before_Probability = 1
    after_Probability = TheSeed_AliciaRingBox[int(Box_Level)]["Probability"][0]

    for j in range(len(TheSeed_AliciaRingBox[int(Box_Level)]["Name"])):
        #print(f"{before_Probability} <= {Random} <= {after_Probability}")
        if Random >= before_Probability and Random <= after_Probability:
            TheSeed_AliciaRingBox_Item_Name = TheSeed_AliciaRingBox[int(Box_Level)]["Name"][j]
            TheSeed_AliciaRingBox_Item_Probability = TheSeed_AliciaRingBox[int(Box_Level)]["Probability"][j]
            break

        before_Probability += TheSeed_AliciaRingBox[int(Box_Level)]["Probability"][j]
        after_Probability += TheSeed_AliciaRingBox[int(Box_Level)]["Probability"][j + 1]

    if TheSeed_AliciaRingBox_Item_Name[-1:] == "링" or TheSeed_AliciaRingBox_Item_Name == "링 오브 썸":
        if TheSeed_AliciaRingBox_Item_Name[-2:] != "어링":
            Ring_Level_Random = random.randrange(1, sum(TheSeed_Ring_Level["Probability"]))

            TheSeed_Ring_Level_Name = ""
            TheSeed_Ring_Level_Probability = 0

            before_Probability = 1
            after_Probability = TheSeed_Ring_Level["Probability"][0]

            for k in range(len(TheSeed_Ring_Level["Name"])):
                print(f"{before_Probability} <= {Ring_Level_Random} <= {after_Probability}")
                if Ring_Level_Random >= before_Probability and Ring_Level_Random <= after_Probability:
                    TheSeed_Ring_Level_Name = TheSeed_Ring_Level["Name"][k]
                    TheSeed_Ring_Level_Probability = TheSeed_Ring_Level["Probability"][k]
                    break

                before_Probability += TheSeed_Ring_Level["Probability"][k]
                after_Probability += TheSeed_Ring_Level["Probability"][k + 1]

            TheSeed_AliciaRingBox_Item_Name = f"{TheSeed_AliciaRingBox_Item_Name} Lv.{TheSeed_Ring_Level_Name}"

            print(TheSeed_AliciaRingBox_Item_Probability / 100000)
            print(TheSeed_Ring_Level_Probability)

            Ring_Probability = (((TheSeed_AliciaRingBox_Item_Probability / 100000) / 100) * (TheSeed_Ring_Level_Probability / 100)) * 100

            return json.dumps({"Result": "Success", "Item_Name": TheSeed_AliciaRingBox_Item_Name, "Item_Probability": TheSeed_AliciaRingBox_Item_Probability / 100000, "Ring_Probability": round(Ring_Probability, 5)}, ensure_ascii=False)

    return json.dumps({"Result": "Success", "Item_Name": TheSeed_AliciaRingBox_Item_Name, "Item_Probability": TheSeed_AliciaRingBox_Item_Probability / 100000}, ensure_ascii=False)

@TheSeed.route("/AliciaRingBox-Probability")
def function_TheSeed_AliciaRingBox_Probability():
    Box_Level = "1"

    if request.args.get("Box_Level") != None:
        Box_Level = request.args.get("Box_Level")

    Box_Level_Check = False

    for i in range(len(TheSeed_Box_Level_List)):
        if Box_Level == TheSeed_Box_Level_List[i]:
            Box_Level_Check = True

    if Box_Level_Check == False:
        return json.dumps({"Result": "Error", "Error_Result": "Box_Level"})

    Result_List = {}
    Result_List["Result"] = "Success"

    for j in range(len(TheSeed_AliciaRingBox[int(Box_Level)]["Name"])):
        Temp_List = {}
        Temp_List["Item_Name"] = TheSeed_AliciaRingBox[int(Box_Level)]["Name"][j]
        Temp_List["Item_Probability"] = TheSeed_AliciaRingBox[int(Box_Level)]["Probability"][j] / 100000
        Result_List[j] = Temp_List

    return json.dumps(Result_List, ensure_ascii=False)

@TheSeed.route("/HideRingBox-Simulator")
def function_TheSeed_HideRingBox():
    Random = random.randrange(1, sum(TheSeed_HideRingBox["Probability"]))

    TheSeed_HideRingBox_Item_Name = ""
    TheSeed_HideRingBox_Item_Probability = 0

    before_Probability = 1
    after_Probability = TheSeed_HideRingBox["Probability"][0]
    for i in range(len(TheSeed_HideRingBox["Probability"])):
        if Random >= before_Probability and Random <= after_Probability:
            TheSeed_HideRingBox_Item_Name = TheSeed_HideRingBox["Name"][i]
            TheSeed_HideRingBox_Item_Probability = TheSeed_HideRingBox["Probability"][i]
            break
            
        before_Probability += TheSeed_HideRingBox["Probability"][i]
        after_Probability += TheSeed_HideRingBox["Probability"][i + 1]

    if TheSeed_HideRingBox_Item_Name[-1:] == "링" or TheSeed_HideRingBox_Item_Name == "링 오브 썸":
        if TheSeed_HideRingBox_Item_Name[-2:] != "어링":
            Ring_Level_Random = random.randrange(1, sum(TheSeed_Ring_Level["Probability"]))

            TheSeed_Ring_Level_Name = ""
            TheSeed_Ring_Level_Probability = 0

            before_Probability = 1
            after_Probability = TheSeed_Ring_Level["Probability"][0]

            for k in range(len(TheSeed_Ring_Level["Name"])):
                print(f"{before_Probability} <= {Ring_Level_Random} <= {after_Probability}")
                if Ring_Level_Random >= before_Probability and Ring_Level_Random <= after_Probability:
                    TheSeed_Ring_Level_Name = TheSeed_Ring_Level["Name"][k]
                    TheSeed_Ring_Level_Probability = TheSeed_Ring_Level["Probability"][k]
                    break

                before_Probability += TheSeed_Ring_Level["Probability"][k]
                after_Probability += TheSeed_Ring_Level["Probability"][k + 1]

            TheSeed_HideRingBox_Item_Name = f"{TheSeed_HideRingBox_Item_Name} Lv.{TheSeed_Ring_Level_Name}"

            print(TheSeed_HideRingBox_Item_Probability / 100000)
            print(TheSeed_Ring_Level_Probability)

            Ring_Probability = (((TheSeed_HideRingBox_Item_Probability / 100000) / 100) * (TheSeed_Ring_Level_Probability / 100)) * 100

            return json.dumps({"Result": "Success", "Item_Name": TheSeed_HideRingBox_Item_Name, "Item_Probability": TheSeed_HideRingBox_Item_Probability / 100000, "Ring_Probability": round(Ring_Probability, 5)}, ensure_ascii=False)

    return json.dumps({"Result": "Success", "Item_Name": TheSeed_HideRingBox_Item_Name, "Item_Probability": TheSeed_HideRingBox_Item_Probability / 100000}, ensure_ascii=False)

@TheSeed.route("/HideRingBox-Probability")
def function_TheSeed_HideRingBox_Probability():
    Box_Level = "1"

    if request.args.get("Box_Level") != None:
        Box_Level = request.args.get("Box_Level")

    Box_Level_Check = False

    for i in range(len(TheSeed_Box_Level_List)):
        if Box_Level == TheSeed_Box_Level_List[i]:
            Box_Level_Check = True

    if Box_Level_Check == False:
        return json.dumps({"Result": "Error", "Error_Result": "Box_Level"})

    Result_List = {}
    Result_List["Result"] = "Success"

    for j in range(len(TheSeed_HideRingBox["Name"])):
        Temp_List = {}
        Temp_List["Item_Name"] = TheSeed_HideRingBox["Name"][j]
        Temp_List["Item_Probability"] = TheSeed_HideRingBox["Probability"][j] / 100000
        Result_List[j] = Temp_List

    return json.dumps(Result_List, ensure_ascii=False)

@TheSeed.route("/ShineRingBox-Simulator")
def function_TheSeed_ShineRingBox():
    Random = random.randrange(1, sum(TheSeed_ShineRingBox["Probability"]))

    TheSeed_ShineRingBox_Item_Name = ""
    TheSeed_ShineRingBox_Item_Probability = 0

    before_Probability = 1
    after_Probability = TheSeed_ShineRingBox["Probability"][0]
    for i in range(len(TheSeed_ShineRingBox["Probability"])):
        if Random >= before_Probability and Random <= after_Probability:
            TheSeed_ShineRingBox_Item_Name = TheSeed_ShineRingBox["Name"][i]
            TheSeed_ShineRingBox_Item_Probability = TheSeed_ShineRingBox["Probability"][i]
            break
            
        before_Probability += TheSeed_ShineRingBox["Probability"][i]
        after_Probability += TheSeed_ShineRingBox["Probability"][i + 1]

    if TheSeed_ShineRingBox_Item_Name[-1:] == "링" or TheSeed_ShineRingBox_Item_Name == "링 오브 썸":
        if TheSeed_ShineRingBox_Item_Name[-2:] != "어링":
            Ring_Level_Random = random.randrange(1, sum(TheSeed_Ring_Level["Probability"]))

            TheSeed_Ring_Level_Name = ""
            TheSeed_Ring_Level_Probability = 0

            before_Probability = 1
            after_Probability = TheSeed_Ring_Level["Probability"][0]

            for k in range(len(TheSeed_Ring_Level["Name"])):
                print(f"{before_Probability} <= {Ring_Level_Random} <= {after_Probability}")
                if Ring_Level_Random >= before_Probability and Ring_Level_Random <= after_Probability:
                    TheSeed_Ring_Level_Name = TheSeed_Ring_Level["Name"][k]
                    TheSeed_Ring_Level_Probability = TheSeed_Ring_Level["Probability"][k]
                    break

                before_Probability += TheSeed_Ring_Level["Probability"][k]
                after_Probability += TheSeed_Ring_Level["Probability"][k + 1]

            TheSeed_ShineRingBox_Item_Name = f"{TheSeed_ShineRingBox_Item_Name} Lv.{TheSeed_Ring_Level_Name}"

            print(TheSeed_ShineRingBox_Item_Probability / 100000)
            print(TheSeed_Ring_Level_Probability)

            Ring_Probability = (((TheSeed_ShineRingBox_Item_Probability / 100000) / 100) * (TheSeed_Ring_Level_Probability / 100)) * 100

            return json.dumps({"Result": "Success", "Item_Name": TheSeed_ShineRingBox_Item_Name, "Item_Probability": TheSeed_ShineRingBox_Item_Probability / 100000, "Ring_Probability": round(Ring_Probability, 5)}, ensure_ascii=False)

    return json.dumps({"Result": "Success", "Item_Name": TheSeed_ShineRingBox_Item_Name, "Item_Probability": TheSeed_ShineRingBox_Item_Probability / 100000}, ensure_ascii=False)

@TheSeed.route("/ShineRingBox-Probability")
def function_TheSeed_ShineRingBox_Probability():
    Box_Level = "1"

    if request.args.get("Box_Level") != None:
        Box_Level = request.args.get("Box_Level")

    Box_Level_Check = False

    for i in range(len(TheSeed_Box_Level_List)):
        if Box_Level == TheSeed_Box_Level_List[i]:
            Box_Level_Check = True

    if Box_Level_Check == False:
        return json.dumps({"Result": "Error", "Error_Result": "Box_Level"})

    Result_List = {}
    Result_List["Result"] = "Success"

    for j in range(len(TheSeed_ShineRingBox["Name"])):
        Temp_List = {}
        Temp_List["Item_Name"] = TheSeed_ShineRingBox["Name"][j]
        Temp_List["Item_Probability"] = TheSeed_ShineRingBox["Probability"][j] / 100000
        Result_List[j] = Temp_List

    return json.dumps(Result_List, ensure_ascii=False)

@TheSeed.route("/RingLevel-Probability")
def function_TheSeed_RingLevel_Probability():
    Result_List = {}
    Result_List["Result"] = "Success"

    for j in range(len(TheSeed_Ring_Level["Name"])):
        Temp_List = {}
        Temp_List["Ring_Level"] = TheSeed_Ring_Level["Name"][j]
        Temp_List["Ring_Probability"] = TheSeed_Ring_Level["Probability"][j]
        Result_List[j] = Temp_List

    return json.dumps(Result_List, ensure_ascii=False)

