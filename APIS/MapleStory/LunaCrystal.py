from flask import Blueprint, request, render_template
import json, random, dbconfig_MapleStory

LunaCrystal = Blueprint("LunaCrystal", __name__, url_prefix="/MapleStory/LunaCrystal")
db_Class = dbconfig_MapleStory.DataBase()

print("LunaCrystal 로딩 시작.")

LunaCrystal_Type_List = ["Sweet", "Dream"]
LunaCrystal_List = {}

for i in range(len(LunaCrystal_Type_List)):
    LunaCrystal_List[LunaCrystal_Type_List[i]] = {}

    LunaCrystal_GetData_SQL = f"SELECT * FROM LunaCrystal_{LunaCrystal_Type_List[i]}"
    LunaCrystal_GetData_ROW = db_Class.executeAll(LunaCrystal_GetData_SQL)

    LunaCrystal_Item_Name_List = []
    LunaCrystal_Item_Probability_List = []

    for j in range(len(LunaCrystal_GetData_ROW)):
        LunaCrystal_Item_Name_List.append(LunaCrystal_GetData_ROW[j]["Name"])
        LunaCrystal_Item_Probability_List.append(int(float(LunaCrystal_GetData_ROW[j]["Probability"]) * 100))

    LunaCrystal_List[LunaCrystal_Type_List[i]]["Name"] = LunaCrystal_Item_Name_List
    LunaCrystal_List[LunaCrystal_Type_List[i]]["Probability"] = LunaCrystal_Item_Probability_List

db_Class.close()

print("LunaCrystal 로딩 종료.")

@LunaCrystal.route("/LunaCrystal-Simulator")
def function_LunaCrystal():
    LunaCrystal_Type = "Sweet"

    if request.args.get("LunaCrystal_Type") != None:
        LunaCrystal_Type = request.args.get("LunaCrystal_Type")

    LunaCrystal_Type_Check = False

    for i in range(len(LunaCrystal_Type_List)):
        if LunaCrystal_Type == LunaCrystal_Type_List[i]:
            LunaCrystal_Type_Check = True

    if LunaCrystal_Type_Check == False:
        return json.dumps({"Result": "Error", "Error_Result": "LunaCrystal_Type"})

    Random = random.randrange(1, sum(LunaCrystal_List[LunaCrystal_Type]["Probability"]))

    LunaCrystal_Item_Name = ""
    LunaCrystal_Item_Probability = 0

    before_Probability = 1
    after_Probability = LunaCrystal_List[LunaCrystal_Type]["Probability"][0]

    for j in range(len(LunaCrystal_List[LunaCrystal_Type]["Name"])):
        #print(f"{before_Probability} <= {Random} <= {after_Probability}")
        if Random >= before_Probability and Random <= after_Probability:
            LunaCrystal_Item_Name = LunaCrystal_List[LunaCrystal_Type]["Name"][j]
            LunaCrystal_Item_Probability = LunaCrystal_List[LunaCrystal_Type]["Probability"][j]
            break

        before_Probability += LunaCrystal_List[LunaCrystal_Type]["Probability"][j]
        after_Probability += LunaCrystal_List[LunaCrystal_Type]["Probability"][j + 1]

    return json.dumps({"Result": "Success", "Item_Name": LunaCrystal_Item_Name, "Item_Probability": LunaCrystal_Item_Probability / 100}, ensure_ascii=False)

@LunaCrystal.route("/LunaCrystal-Probability")
def function_LunaCrystal_Probability():
    LunaCrystal_Type = "Sweet"

    if request.args.get("LunaCrystal_Type") != None:
        LunaCrystal_Type = request.args.get("LunaCrystal_Type")

    LunaCrystal_Type_Check = False

    for i in range(len(LunaCrystal_Type_List)):
        if LunaCrystal_Type == LunaCrystal_Type_List[i]:
            LunaCrystal_Type_Check = True

    if LunaCrystal_Type_Check == False:
        return json.dumps({"Result": "Error", "Error_Result": "LunaCrystal_Type"})

    Result_List = {}
    Result_List["Result"] = "Success"

    for j in range(len(LunaCrystal_List[LunaCrystal_Type]["Name"])):
        Temp_List = {}
        Temp_List["Item_Name"] = LunaCrystal_List[LunaCrystal_Type]["Name"][j]
        Temp_List["Item_Probability"] = LunaCrystal_List[LunaCrystal_Type]["Probability"][j] / 100
        Result_List[j] = Temp_List

    return json.dumps(Result_List, ensure_ascii=False)