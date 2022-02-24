from flask import Blueprint, request, render_template
import json, random, dbconfig_MapleStory

MasterPiece = Blueprint("MasterPiece", __name__, url_prefix="/MapleStory/MasterPiece")
db_Class = dbconfig_MapleStory.DataBase()

print("MasterPiece 로딩 시작.")

MasterPiece_Type_List = ["Red", "Black"]
MasterPiece_Item_Type_List = ["Cap", "Clothes", "Cloak_Gloves", "Shoes", "Weapon"]
MasterPiece_List = {}

for i in range(len(MasterPiece_Type_List)):
    MasterPiece_List[MasterPiece_Type_List[i]] = {}

    for j in range(len(MasterPiece_Item_Type_List)):
        MasterPiece_List[MasterPiece_Type_List[i]][MasterPiece_Item_Type_List[j]] = {}

        MasterPiece_GetData_SQL = f"SELECT * FROM MasterPiece_{MasterPiece_Type_List[i]}_{MasterPiece_Item_Type_List[j]}"
        MasterPiece_GetData_ROW = db_Class.executeAll(MasterPiece_GetData_SQL)

        MasterPiece_Item_Name_List = []
        MasterPiece_Item_Probability_List = []

        for k in range(len(MasterPiece_GetData_ROW)):
            MasterPiece_Item_Name_List.append(MasterPiece_GetData_ROW[k]["Name"])
            MasterPiece_Item_Probability_List.append(int(float(MasterPiece_GetData_ROW[k]["Probability"])*100))

        MasterPiece_List[MasterPiece_Type_List[i]][MasterPiece_Item_Type_List[j]]["Name"] = MasterPiece_Item_Name_List
        MasterPiece_List[MasterPiece_Type_List[i]][MasterPiece_Item_Type_List[j]]["Probability"] = MasterPiece_Item_Probability_List

db_Class.close()

print("MasterPiece 로딩 종료.")

@MasterPiece.route("/MasterPiece-Simulator")
def function_MasterPiece():
    MasterPiece_Type = "Red"
    MasterPiece_Item_Type = "Cap"

    if request.args.get("MasterPiece_Type") != None:
        MasterPiece_Type = request.args.get("MasterPiece_Type")
    
    if request.args.get("MasterPiece_Item_Type") != None:
        MasterPiece_Item_Type = request.args.get("MasterPiece_Item_Type")

    MasterPiece_Type_Check = False
    MasterPiece_Item_Type_Check = False

    for i in range(len(MasterPiece_Type_List)):
        if MasterPiece_Type == MasterPiece_Type_List[i]:
            MasterPiece_Type_Check = True

    for j in range(len(MasterPiece_Item_Type_List)):
        if MasterPiece_Item_Type == MasterPiece_Item_Type_List[j]:
            MasterPiece_Item_Type_Check = True

    if MasterPiece_Type_Check == False:
        return json.dumps({"Result": "Error", "Error_Result": "MasterPiece_Type"})

    if MasterPiece_Item_Type_Check == False:
        return json.dumps({"Result": "Error", "Error_Result": "MasterPiece_Item_Type"})

    Random = random.randrange(1, sum(MasterPiece_List[MasterPiece_Type][MasterPiece_Item_Type]["Probability"]))

    MasterPiece_Item_Name = ""
    MasterPiece_Item_Probability = 0

    before_Probability = 1
    after_Probability = MasterPiece_List[MasterPiece_Type][MasterPiece_Item_Type]["Probability"][0]

    for k in range(len(MasterPiece_List[MasterPiece_Type][MasterPiece_Item_Type]["Name"])):
        print(f"{before_Probability} <= {Random} <= {after_Probability}")
        if Random >= before_Probability and Random <= after_Probability:
            MasterPiece_Item_Name = MasterPiece_List[MasterPiece_Type][MasterPiece_Item_Type]["Name"][k]
            MasterPiece_Item_Probability = MasterPiece_List[MasterPiece_Type][MasterPiece_Item_Type]["Probability"][k]
            break

        before_Probability += MasterPiece_List[MasterPiece_Type][MasterPiece_Item_Type]["Probability"][k]
        after_Probability += MasterPiece_List[MasterPiece_Type][MasterPiece_Item_Type]["Probability"][k + 1]

    return json.dumps({"Result": "Success", "Item_Name": MasterPiece_Item_Name, "Item_Probability": MasterPiece_Item_Probability / 100}, ensure_ascii=False)

@MasterPiece.route("/MasterPiece-Probability")
def function_MasterPiece_Probability():
    MasterPiece_Type = "Red"
    MasterPiece_Item_Type = "Cap"

    if request.args.get("MasterPiece_Type") != None:
        MasterPiece_Type = request.args.get("MasterPiece_Type")
    
    if request.args.get("MasterPiece_Item_Type") != None:
        MasterPiece_Item_Type = request.args.get("MasterPiece_Item_Type")

    MasterPiece_Type_Check = False
    MasterPiece_Item_Type_Check = False

    for i in range(len(MasterPiece_Type_List)):
        if MasterPiece_Type == MasterPiece_Type_List[i]:
            MasterPiece_Type_Check = True

    for j in range(len(MasterPiece_Item_Type_List)):
        if MasterPiece_Item_Type == MasterPiece_Item_Type_List[j]:
            MasterPiece_Item_Type_Check = True

    if MasterPiece_Type_Check == False:
        return json.dumps({"Result": "Error", "Error_Result": "MasterPiece_Type"})

    if MasterPiece_Item_Type_Check == False:
        return json.dumps({"Result": "Error", "Error_Result": "MasterPiece_Item_Type"})

    Result_List = {}
    Result_List["Result"] = "Success"

    for i in range(len(MasterPiece_List[MasterPiece_Type][MasterPiece_Item_Type]["Name"])):
        Temp_List = {}
        Temp_List["Item_Name"] = MasterPiece_List[MasterPiece_Type][MasterPiece_Item_Type]["Name"][i]
        Temp_List["Item_Probability"] = MasterPiece_List[MasterPiece_Type][MasterPiece_Item_Type]["Probability"][i] / 100
        Result_List[i] = Temp_List

    return json.dumps(Result_List, ensure_ascii=False)