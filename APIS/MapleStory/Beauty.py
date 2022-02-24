from flask import Blueprint, request, render_template
import json, random, dbconfig_MapleStory

Beauty = Blueprint("Beauty", __name__, url_prefix="/MapleStory/Beauty")
db_Class = dbconfig_MapleStory.DataBase()

print("Beauty 로딩 시작.")

Beauty_Type_List = ["Hair", "PlasticSurgery"]
Beauty_Sex_List = ["Man", "Woman"]
Beauty_List = {}

for i in range(len(Beauty_Type_List)):
    Beauty_List[Beauty_Type_List[i]] = {}

    for j in range(len(Beauty_Sex_List)):
        Beauty_List[Beauty_Type_List[i]][Beauty_Sex_List[j]] = {}

        Beauty_GetData_SQL = f"SELECT * FROM Beauty_Royal_{Beauty_Type_List[i]}_{Beauty_Sex_List[j]}"
        Beauty_GetData_ROW = db_Class.executeAll(Beauty_GetData_SQL)

        Beauty_Item_Name_List = []
        Beauty_Item_Probability_List = []

        for k in range(len(Beauty_GetData_ROW)):
            Beauty_Item_Name_List.append(Beauty_GetData_ROW[k]["Name"])
            Beauty_Item_Probability_List.append(int(float(Beauty_GetData_ROW[k]["Probability"])*100))

        Beauty_List[Beauty_Type_List[i]][Beauty_Sex_List[j]]["Name"] = Beauty_Item_Name_List
        Beauty_List[Beauty_Type_List[i]][Beauty_Sex_List[j]]["Probability"] = Beauty_Item_Probability_List

db_Class.close()

print("Beauty 로딩 종료.")

@Beauty.route("/RoyalHair-Simulator")
def function_RoyalHair():
    Sex_Type = "Man"
    
    if request.args.get("Sex_Type") != None:
        Sex_Type = request.args.get("Sex_Type")

    Sex_Type_Check = False

    for i in range(len(Beauty_Sex_List)):
        if Sex_Type == Beauty_Sex_List[i]:
            Sex_Type_Check = True

    if Sex_Type_Check == False:
        return json.dumps({"Result": "Error", "Error_Result": "Sex_Type"})

    Random = random.randrange(1, sum(Beauty_List["Hair"][Sex_Type]["Probability"]))

    Hair_Item_Name = ""
    Hair_Item_Probability = 0

    before_Probability = 1
    after_Probability = Beauty_List["Hair"][Sex_Type]["Probability"][0]

    for j in range(len(Beauty_List["Hair"][Sex_Type]["Name"])):
        print(f"{before_Probability} <= {Random} <= {after_Probability}")
        if Random >= before_Probability and Random <= after_Probability:
            Hair_Item_Name = Beauty_List["Hair"][Sex_Type]["Name"][j]
            Hair_Item_Probability = Beauty_List["Hair"][Sex_Type]["Probability"][j]
            break

        before_Probability += Beauty_List["Hair"][Sex_Type]["Probability"][j]
        after_Probability += Beauty_List["Hair"][Sex_Type]["Probability"][j + 1]

    return json.dumps({"Result": "Success", "Hair_Name": Hair_Item_Name, "Hair_Probability": Hair_Item_Probability / 100}, ensure_ascii=False)

@Beauty.route("/RoyalHair-Probability")
def function_RoyalHair_Probability():
    Sex_Type = "Man"
    
    if request.args.get("Sex_Type") != None:
        Sex_Type = request.args.get("Sex_Type")

    Sex_Type_Check = False

    for i in range(len(Beauty_Sex_List)):
        if Sex_Type == Beauty_Sex_List[i]:
            Sex_Type_Check = True

    if Sex_Type_Check == False:
        return json.dumps({"Result": "Error", "Error_Result": "Sex_Type"})

    Result_List = {}
    Result_List["Result"] = "Success"

    for j in range(len(Beauty_List["Hair"][Sex_Type]["Name"])):
        Temp_List = {}
        Temp_List["Hair_Name"] = Beauty_List["Hair"][Sex_Type]["Name"][j]
        Temp_List["Hair_Probability"] = Beauty_List["Hair"][Sex_Type]["Probability"][j] / 100
        Result_List[j] = Temp_List

    return json.dumps(Result_List, ensure_ascii=False)

@Beauty.route("/RoyalPlasticSurgery-Simulator")
def function_RoyalPlasticSurgery():
    Sex_Type = "Man"
    
    if request.args.get("Sex_Type") != None:
        Sex_Type = request.args.get("Sex_Type")

    Sex_Type_Check = False

    for i in range(len(Beauty_Sex_List)):
        if Sex_Type == Beauty_Sex_List[i]:
            Sex_Type_Check = True

    if Sex_Type_Check == False:
        return json.dumps({"Result": "Error", "Error_Result": "Sex_Type"})

    Random = random.randrange(1, sum(Beauty_List["PlasticSurgery"][Sex_Type]["Probability"]))

    PlasticSurgery_Item_Name = ""
    PlasticSurgery_Item_Probability = 0

    before_Probability = 1
    after_Probability = Beauty_List["PlasticSurgery"][Sex_Type]["Probability"][0]

    for j in range(len(Beauty_List["PlasticSurgery"][Sex_Type]["Name"])):
        print(f"{before_Probability} <= {Random} <= {after_Probability}")
        if Random >= before_Probability and Random <= after_Probability:
            PlasticSurgery_Item_Name = Beauty_List["PlasticSurgery"][Sex_Type]["Name"][j]
            PlasticSurgery_Item_Probability = Beauty_List["PlasticSurgery"][Sex_Type]["Probability"][j]
            break

        before_Probability += Beauty_List["PlasticSurgery"][Sex_Type]["Probability"][j]
        after_Probability += Beauty_List["PlasticSurgery"][Sex_Type]["Probability"][j + 1]

    return json.dumps({"Result": "Success", "PlasticSurgery_Name": PlasticSurgery_Item_Name, "PlasticSurgery_Probability": PlasticSurgery_Item_Probability / 100}, ensure_ascii=False)

@Beauty.route("/RoyalPlasticSurgery-Probability")
def function_RoyalPlasticSurgery_Probability():
    Sex_Type = "Man"
    
    if request.args.get("Sex_Type") != None:
        Sex_Type = request.args.get("Sex_Type")

    Sex_Type_Check = False

    for i in range(len(Beauty_Sex_List)):
        if Sex_Type == Beauty_Sex_List[i]:
            Sex_Type_Check = True

    if Sex_Type_Check == False:
        return json.dumps({"Result": "Error", "Error_Result": "Sex_Type"})

    Result_List = {}
    Result_List["Result"] = "Success"

    for j in range(len(Beauty_List["PlasticSurgery"][Sex_Type]["Name"])):
        Temp_List = {}
        Temp_List["PlasticSurgery_Name"] = Beauty_List["PlasticSurgery"][Sex_Type]["Name"][j]
        Temp_List["PlasticSurgery_Probability"] = Beauty_List["PlasticSurgery"][Sex_Type]["Probability"][j] / 100
        Result_List[j] = Temp_List

    return json.dumps(Result_List, ensure_ascii=False)