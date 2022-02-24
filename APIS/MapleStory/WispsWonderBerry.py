from flask import Blueprint, request, render_template
import json, random, dbconfig_MapleStory

WispsWonderBerry = Blueprint("WispsWonderBerry", __name__, url_prefix="/MapleStory/WispsWonderBerry")
db_Class = dbconfig_MapleStory.DataBase()

WispsWonderBerry_Item_Name_List = []
WispsWonderBerry_Item_Probability_List = []

WispsWonderBerry_GetData_SQL = "SELECT * FROM WispsWonderBerry"
WispsWonderBerry_GetData_ROW = db_Class.executeAll(WispsWonderBerry_GetData_SQL)

for RoyalStyle_GetData_Item in WispsWonderBerry_GetData_ROW:
    WispsWonderBerry_Item_Name_List.append(RoyalStyle_GetData_Item["Name"])
    WispsWonderBerry_Item_Probability_List.append(int(float(RoyalStyle_GetData_Item["Probability"]) * 100))

db_Class.close()

@WispsWonderBerry.route("/WispsWonderBerry-Simulator")
def function_WispsWonderBerry():
    Random = random.randrange(1, sum(WispsWonderBerry_Item_Probability_List))
    
    WispsWonderBerry_Item_Name = ""
    WispsWonderBerry_Item_Probability = 0

    before_Probability = 1
    after_Probability = WispsWonderBerry_Item_Probability_List[0]
    for i in range(len(WispsWonderBerry_Item_Probability_List)):
        if Random >= before_Probability and Random <= after_Probability:
            WispsWonderBerry_Item_Name = WispsWonderBerry_Item_Name_List[i]
            WispsWonderBerry_Item_Probability = WispsWonderBerry_Item_Probability_List[i] / 100
            break
            
        before_Probability += WispsWonderBerry_Item_Probability_List[i]
        after_Probability += WispsWonderBerry_Item_Probability_List[i + 1]

    return json.dumps({"Result": "Success", "Item_Name": WispsWonderBerry_Item_Name, "Item_Probability": WispsWonderBerry_Item_Probability}, ensure_ascii=False)

@WispsWonderBerry.route("/WispsWonderBerry-Probability")
def function_WispsWonderBerry_Probability():
    Result_List = {}
    Result_List["Result"] = "Success"

    for i in range(len(WispsWonderBerry_Item_Name_List)):
        Temp_List = {}
        Temp_List["Item_Name"] = WispsWonderBerry_Item_Name_List[i]
        Temp_List["Item_Probability"] = WispsWonderBerry_Item_Probability_List[i] / 100
        Result_List[i] = Temp_List

    return json.dumps(Result_List, ensure_ascii=False)