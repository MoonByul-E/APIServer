from flask import Blueprint, request, render_template
import json, random, dbconfig_MapleStory

RoyalStyle = Blueprint("RoyalStyle", __name__, url_prefix="/MapleStory/RoyalStyle")
db_Class = dbconfig_MapleStory.DataBase()

print("RoyalStyle 로딩 시작.")

RoyalStyle_Item_Name_List = []
RoyalStyle_Item_Probability_List = []

RoyalStyle_GetData_SQL = "SELECT * FROM RoyalStyle;"
RoyalStyle_GetData_ROW = db_Class.executeAll(RoyalStyle_GetData_SQL)

for RoyalStyle_GetData_Item in RoyalStyle_GetData_ROW:
    RoyalStyle_Item_Name_List.append(RoyalStyle_GetData_Item["Name"])
    RoyalStyle_Item_Probability_List.append(int(float(RoyalStyle_GetData_Item["Probability"]) * 10))

db_Class.close()

print("RoyalStyle 로딩 완료.")

@RoyalStyle.route("/RoyalStyle-Simulator")
def function_RoyalStyle():
    Random = random.randrange(1, sum(RoyalStyle_Item_Probability_List))
    
    RoyalStyle_Item_Name = ""
    RoyalStyle_Item_Probability = 0

    before_Probability = 1
    after_Probability = RoyalStyle_Item_Probability_List[0]
    for i in range(len(RoyalStyle_Item_Probability_List)):
        if Random >= before_Probability and Random <= after_Probability:
            RoyalStyle_Item_Name = RoyalStyle_Item_Name_List[i]
            RoyalStyle_Item_Probability = RoyalStyle_Item_Probability_List[i] / 10
            break
            
        before_Probability += RoyalStyle_Item_Probability_List[i]
        after_Probability += RoyalStyle_Item_Probability_List[i + 1]

    return json.dumps({"Result": "Success", "Item_Name": RoyalStyle_Item_Name, "Item_Probability": RoyalStyle_Item_Probability}, ensure_ascii=False)

@RoyalStyle.route("/RoyalStyle-Probability")
def function_RoyalStyle_Probability():
    Result_List = {}
    Result_List["Result"] = "Success"

    for i in range(len(RoyalStyle_Item_Name_List)):
        Temp_List = {}
        Temp_List["Item_Name"] = RoyalStyle_Item_Name_List[i]
        Temp_List["Item_Probability"] = RoyalStyle_Item_Probability_List[i] / 10
        Result_List[i] = Temp_List

    return json.dumps(Result_List, ensure_ascii=False)