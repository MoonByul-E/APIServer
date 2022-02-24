from flask import Blueprint, request, render_template
import json, random, dbconfig_MapleStory

GoldApple = Blueprint("GoldApple", __name__, url_prefix="/MapleStory/GoldApple")
db_Class = dbconfig_MapleStory.DataBase()

print("GoldApple 로딩 시작.")

GoldApple_Item_Name_List = []
GoldApple_Item_Probability_List = []

GoldApple_GetData_SQL = "SELECT * FROM GoldApple;"
GoldApple_GetData_ROW = db_Class.executeAll(GoldApple_GetData_SQL)

for GoldApple_GetData_Item in GoldApple_GetData_ROW:
    GoldApple_Item_Name_List.append(GoldApple_GetData_Item["Name"])
    GoldApple_Item_Probability_List.append(int(float(GoldApple_GetData_Item["Probability"]) * 100000))

db_Class.close()

print("GoldApple 로딩 종료.")

@GoldApple.route("/GoldApple-Simulator")
def function_GoldApple():
    Random = random.randrange(1, sum(GoldApple_Item_Probability_List))
    
    GoldApple_Item_Name = ""
    GoldApple_Item_Probability = 0

    before_Probability = 1
    after_Probability = GoldApple_Item_Probability_List[0]
    for i in range(len(GoldApple_Item_Probability_List)):
        if Random >= before_Probability and Random <= after_Probability:
            GoldApple_Item_Name = GoldApple_Item_Name_List[i]
            GoldApple_Item_Probability = GoldApple_Item_Probability_List[i] / 100000
            break
            
        before_Probability += GoldApple_Item_Probability_List[i]
        after_Probability += GoldApple_Item_Probability_List[i + 1]

    return json.dumps({"Result": "Success", "Item_Name": GoldApple_Item_Name, "Item_Probability": GoldApple_Item_Probability}, ensure_ascii=False)

@GoldApple.route("/GoldApple-Probability")
def function_GoldApple_Probability():
    Result_List = {}
    Result_List["Result"] = "Success"

    for i in range(len(GoldApple_Item_Name_List)):
        Temp_List = {}
        Temp_List["Item_Name"] = GoldApple_Item_Name_List[i]
        Temp_List["Item_Probability"] = GoldApple_Item_Probability_List[i] / 100000
        Result_List[i] = Temp_List

    return json.dumps(Result_List, ensure_ascii=False)