from flask import Blueprint, request, render_template
import json, random, dbconfig_MapleStory

Cube = Blueprint("Cube", __name__, url_prefix="/MapleStory/Cube")
db_Class = dbconfig_MapleStory.DataBase()

print("Cube 로딩 시작.")

Cube_Type_List = ["Red", "Black", "Addi", "Strange", "Master", "Artisan"]
Cube_Grade_List = ["Rare", "Epic", "Unique", "Legendary"]
Cube_Item_Type_List = ["Weapon", "Emblem","SubWeapon", "ForceShield_SoulRing", "Shield", "Cap", "Top", "Clothes", "Bottom", "Shoes", "Gloves", "Cloak", "Belt", "Shoulder", "Face", "Eye", "EarRing", "Ring", "Pendant", "MachineHeart"]
Cube_Item_Level_List = ["120", "100"]
Cube_Option_Line_List = ["0", "1", "2"]

Cube_Upgrade_Probability = {}
Cube_Option_Probability = {}

for Cube_Type in Cube_Type_List:
    Cube_Upgrade_Probability[Cube_Type] = {}

    Cube_Upgrade_GetData_SQL = f"SELECT * FROM Cube_Upgrade_Probability_{Cube_Type}"
    Cube_Upgrade_GetData_ROW = db_Class.executeAll(Cube_Upgrade_GetData_SQL)

    Cube_Upgrade_GetData_Name = []
    Cube_Upgrade_GetData_Probability = []
    for Cube_Upgrade_GetData_Item in Cube_Upgrade_GetData_ROW:
        Cube_Upgrade_GetData_Name.append(Cube_Upgrade_GetData_Item["Name"])
        Cube_Upgrade_GetData_Probability.append(int(Cube_Upgrade_GetData_Item["Probability"].replace(".", "")))

    Cube_Upgrade_Probability[Cube_Type]["Name"] = Cube_Upgrade_GetData_Name
    Cube_Upgrade_Probability[Cube_Type]["Probability"] = Cube_Upgrade_GetData_Probability

    Cube_Option_Probability[Cube_Type] = {}
    
    for Cube_Item_Type in Cube_Item_Type_List:
        Cube_Option_Probability[Cube_Type][Cube_Item_Type] = {}

        for Cube_Item_Level in Cube_Item_Level_List:
            Cube_Option_Probability[Cube_Type][Cube_Item_Type][Cube_Item_Level] = {}

            for Cube_Option_Line in Cube_Option_Line_List:
                Cube_Option_Probability[Cube_Type][Cube_Item_Type][Cube_Item_Level][Cube_Option_Line] = {}

                for Cube_Grade in Cube_Grade_List:
                    Cube_Option_GetData_SQL = f"SELECT * FROM Cube_Option_Probability_{Cube_Type} WHERE Item_Type = '{Cube_Item_Type}' and Item_Level = '{Cube_Item_Level}' and Option_Line = {Cube_Option_Line} and Grade = '{Cube_Grade}'"
                    Cube_Option_GetData_ROW = db_Class.executeAll(Cube_Option_GetData_SQL)
                    if Cube_Option_GetData_ROW:
                        Cube_Option_Probability[Cube_Type][Cube_Item_Type][Cube_Item_Level][Cube_Option_Line][Cube_Grade] = {}

                        Cube_Option_GetData_Name = []
                        Cube_Option_GetData_Probability = []
                        for Cube_Option_GetData in Cube_Option_GetData_ROW:
                            Cube_Option_GetData_Name.append(Cube_Option_GetData["Name"])
                            Cube_Option_GetData_Probability.append(int(Cube_Option_GetData["Probability"].replace(".", "")))
                        
                        Cube_Option_Probability[Cube_Type][Cube_Item_Type][Cube_Item_Level][Cube_Option_Line][Cube_Grade]["Name"] = Cube_Option_GetData_Name
                        Cube_Option_Probability[Cube_Type][Cube_Item_Type][Cube_Item_Level][Cube_Option_Line][Cube_Grade]["Probability"] = Cube_Option_GetData_Probability

print("Cube 로딩 종료.")

@Cube.route("/Cube-Simulator")
def function_Cube():
    Cube_Type_Input = "Red"
    Cube_Grade_Input = "Rare"
    Cube_Item_Type_Input = "Weapon"
    Cube_Item_Level_Input = "120"

    if request.args.get("Cube_Type") != None:
        Cube_Type_Input = request.args.get("Cube_Type")

    if request.args.get("Cube_Grade") != None:
        Cube_Grade_Input = request.args.get("Cube_Grade")

    if request.args.get("Cube_Grade") != None:
        Cube_Grade_Input = request.args.get("Cube_Grade")

    if request.args.get("Cube_Item_Level") != None:
        Cube_Item_Level_Input = request.args.get("Cube_Item_Level")

    Cube_Type_Input_Check = False
    Cube_Grade_Input_Check = False
    Cube_Item_Type_Input_Check = False
    Cube_Item_Level_Input_Check = False

    for Cube_Type_Input_Check_ in Cube_Type_List:
        if Cube_Type_Input == Cube_Type_Input_Check_:
            Cube_Type_Input_Check = True

    for Cube_Grade_Input_Check_ in Cube_Grade_List:
        if Cube_Grade_Input == Cube_Grade_Input_Check_:
            Cube_Grade_Input_Check = True

    for Cube_Item_Type_Input_Check_ in Cube_Item_Type_List:
        if Cube_Item_Type_Input == Cube_Item_Type_Input_Check_:
            Cube_Item_Type_Input_Check = True

    for Cube_Item_Level_Input_Check_ in Cube_Item_Level_List:
        if Cube_Item_Level_Input == Cube_Item_Level_Input_Check_:
            Cube_Item_Level_Input_Check = True
            
    if Cube_Type_Input_Check == False:
        return json.dumps({"Result": "Error", "Error_Result": "Cube_Type"})

    if Cube_Grade_Input_Check == False:
        return json.dumps({"Result": "Error", "Error_Result": "Cube_Grade"})

    if Cube_Item_Type_Input_Check == False:
        return json.dumps({"Result": "Error", "Error_Result": "Cube_Item_Type"})

    if Cube_Item_Level_Input_Check == False:
        return json.dumps({"Result": "Error", "Error_Result": "Cube_Item_Level"})

    #print(f"{Cube_Grade_List.index(Cube_Grade_Input)} > {Cube_Grade_List.index(Cube_Upgrade_Probability[Cube_Type_Input]['Name'][len(Cube_Upgrade_Probability[Cube_Type_Input]['Name']) - 1]) + 1}")
    if Cube_Grade_List.index(Cube_Grade_Input) > Cube_Grade_List.index(Cube_Upgrade_Probability[Cube_Type_Input]["Name"][len(Cube_Upgrade_Probability[Cube_Type_Input]["Name"]) - 1]) + 1:
        return json.dumps({"Result": "Error", "Error_Result": "Cube_Grade"})

    Cube_Upgrade_Check = False
    for Cube_Upgrade_Check_ in Cube_Upgrade_Probability[Cube_Type_Input]["Name"]:
        if Cube_Upgrade_Check_ == Cube_Grade_Input:
            Cube_Upgrade_Check = True

    if Cube_Upgrade_Check == True:
        Cube_Upgrade_Random = random.randrange(1, 1000000)

        if Cube_Upgrade_Random >= 1 and Cube_Upgrade_Random <= Cube_Upgrade_Probability[Cube_Type_Input]["Probability"][Cube_Upgrade_Probability[Cube_Type_Input]["Name"].index(Cube_Grade_Input)]:
            Cube_Grade_Input = Cube_Grade_List[Cube_Grade_List.index(Cube_Grade_Input) + 1]

    Option_First_Random = random.randrange(1, sum(Cube_Option_Probability[Cube_Type_Input][Cube_Item_Type_Input][Cube_Item_Level_Input]["0"][Cube_Grade_Input]["Probability"]))
    Option_Second_Random = random.randrange(1, sum(Cube_Option_Probability[Cube_Type_Input][Cube_Item_Type_Input][Cube_Item_Level_Input]["1"][Cube_Grade_Input]["Probability"]))
    Option_Third_Random = random.randrange(1, sum(Cube_Option_Probability[Cube_Type_Input][Cube_Item_Type_Input][Cube_Item_Level_Input]["2"][Cube_Grade_Input]["Probability"]))

    Option_First_Name = ""
    Option_First_Probability = 0

    Option_Second_Name = ""
    Option_Second_Probability = 0

    Option_Thrid_Name = ""
    Option_Thrid_Probability = 0

    Option_First_Before_Probability = 1
    Option_First_After_Probability = Cube_Option_Probability[Cube_Type_Input][Cube_Item_Type_Input][Cube_Item_Level_Input]["0"][Cube_Grade_Input]["Probability"][0]

    Option_Second_Before_Probability = 1
    Option_Second_After_Probability = Cube_Option_Probability[Cube_Type_Input][Cube_Item_Type_Input][Cube_Item_Level_Input]["1"][Cube_Grade_Input]["Probability"][0]

    Option_Thrid_Before_Probability = 1
    Option_Thrid_After_Probability = Cube_Option_Probability[Cube_Type_Input][Cube_Item_Type_Input][Cube_Item_Level_Input]["2"][Cube_Grade_Input]["Probability"][0]

    for i in range(len(Cube_Option_Probability[Cube_Type_Input][Cube_Item_Type_Input][Cube_Item_Level_Input]["0"][Cube_Grade_Input]["Name"])):
        #print(f"{Option_First_Before_Probability} <= {Option_First_Random} <= {Option_First_After_Probability}")
        if Option_First_Random >= Option_First_Before_Probability and Option_First_Random <= Option_First_After_Probability:
            Option_First_Name = Cube_Option_Probability[Cube_Type_Input][Cube_Item_Type_Input][Cube_Item_Level_Input]["0"][Cube_Grade_Input]["Name"][i]
            Option_First_Probability = Cube_Option_Probability[Cube_Type_Input][Cube_Item_Type_Input][Cube_Item_Level_Input]["0"][Cube_Grade_Input]["Probability"][i]
            break

        Option_First_Before_Probability += Cube_Option_Probability[Cube_Type_Input][Cube_Item_Type_Input][Cube_Item_Level_Input]["0"][Cube_Grade_Input]["Probability"][i]
        Option_First_After_Probability += Cube_Option_Probability[Cube_Type_Input][Cube_Item_Type_Input][Cube_Item_Level_Input]["0"][Cube_Grade_Input]["Probability"][i + 1]

    for j in range(len(Cube_Option_Probability[Cube_Type_Input][Cube_Item_Type_Input][Cube_Item_Level_Input]["1"][Cube_Grade_Input]["Name"])):
        #print(f"{Option_Second_Before_Probability} <= {Option_Second_Random} <= {Option_Second_After_Probability}")
        if Option_Second_Random >= Option_Second_Before_Probability and Option_Second_Random <= Option_Second_After_Probability:
            Option_Second_Name = Cube_Option_Probability[Cube_Type_Input][Cube_Item_Type_Input][Cube_Item_Level_Input]["1"][Cube_Grade_Input]["Name"][j]
            Option_Second_Probability = Cube_Option_Probability[Cube_Type_Input][Cube_Item_Type_Input][Cube_Item_Level_Input]["1"][Cube_Grade_Input]["Probability"][j]
            break

        Option_Second_Before_Probability += Cube_Option_Probability[Cube_Type_Input][Cube_Item_Type_Input][Cube_Item_Level_Input]["1"][Cube_Grade_Input]["Probability"][j]
        Option_Second_After_Probability += Cube_Option_Probability[Cube_Type_Input][Cube_Item_Type_Input][Cube_Item_Level_Input]["1"][Cube_Grade_Input]["Probability"][j + 1]

    for k in range(len(Cube_Option_Probability[Cube_Type_Input][Cube_Item_Type_Input][Cube_Item_Level_Input]["2"][Cube_Grade_Input]["Name"])):
        #print(f"{Option_Thrid_Before_Probability} <= {Option_Third_Random} <= {Option_Thrid_After_Probability}")
        if Option_Third_Random >= Option_Thrid_Before_Probability and Option_Third_Random <= Option_Thrid_After_Probability:
            Option_Thrid_Name = Cube_Option_Probability[Cube_Type_Input][Cube_Item_Type_Input][Cube_Item_Level_Input]["2"][Cube_Grade_Input]["Name"][k]
            Option_Thrid_Probability = Cube_Option_Probability[Cube_Type_Input][Cube_Item_Type_Input][Cube_Item_Level_Input]["2"][Cube_Grade_Input]["Probability"][k]
            break
        
        Option_Thrid_Before_Probability += Cube_Option_Probability[Cube_Type_Input][Cube_Item_Type_Input][Cube_Item_Level_Input]["2"][Cube_Grade_Input]["Probability"][k]
        Option_Thrid_After_Probability += Cube_Option_Probability[Cube_Type_Input][Cube_Item_Type_Input][Cube_Item_Level_Input]["2"][Cube_Grade_Input]["Probability"][k + 1]
        
    return json.dumps({"Result": "Success", "Grade": Cube_Grade_Input, "Option": {"0": {"Name": Option_First_Name, "Probability": Option_First_Probability / 10000}, "1": {"Name": Option_Second_Name, "Probability": Option_Second_Probability / 10000}, "2": {"Name": Option_Thrid_Name, "Probability": Option_Thrid_Probability / 10000}}}, ensure_ascii=False)

@Cube.route("/Cube-Probability")
def functionCube_Probability():
    Cube_Type_Input = "Red"
    Cube_Grade_Input = "Rare"
    Cube_Item_Type_Input = "Weapon"
    Cube_Item_Level_Input = "120"
    Cube_Option_Line_Input = "0"

    if request.args.get("Cube_Type") != None:
        Cube_Type_Input = request.args.get("Cube_Type")

    if request.args.get("Cube_Grade") != None:
        Cube_Grade_Input = request.args.get("Cube_Grade")

    if request.args.get("Cube_Grade") != None:
        Cube_Grade_Input = request.args.get("Cube_Grade")

    if request.args.get("Cube_Item_Level") != None:
        Cube_Item_Level_Input = request.args.get("Cube_Item_Level")

    if request.args.get("Cube_Option_Line") != None:
        Cube_Option_Line_Input = request.args.get("Cube_Option_Line")

    Cube_Type_Input_Check = False
    Cube_Grade_Input_Check = False
    Cube_Item_Type_Input_Check = False
    Cube_Item_Level_Input_Check = False
    Cube_Option_Line_Input_Check = False

    for Cube_Type_Input_Check_ in Cube_Type_List:
        if Cube_Type_Input == Cube_Type_Input_Check_:
            Cube_Type_Input_Check = True

    for Cube_Grade_Input_Check_ in Cube_Grade_List:
        if Cube_Grade_Input == Cube_Grade_Input_Check_:
            Cube_Grade_Input_Check = True

    for Cube_Item_Type_Input_Check_ in Cube_Item_Type_List:
        if Cube_Item_Type_Input == Cube_Item_Type_Input_Check_:
            Cube_Item_Type_Input_Check = True

    for Cube_Item_Level_Input_Check_ in Cube_Item_Level_List:
        if Cube_Item_Level_Input == Cube_Item_Level_Input_Check_:
            Cube_Item_Level_Input_Check = True

    for Cube_Option_Line_Input_Check_ in Cube_Option_Line_List:
        if Cube_Option_Line_Input == Cube_Option_Line_Input_Check_:
            Cube_Option_Line_Input_Check = True
            
    if Cube_Type_Input_Check == False:
        return json.dumps({"Result": "Error", "Error_Result": "Cube_Type"})

    if Cube_Grade_Input_Check == False:
        return json.dumps({"Result": "Error", "Error_Result": "Cube_Grade"})

    if Cube_Item_Type_Input_Check == False:
        return json.dumps({"Result": "Error", "Error_Result": "Cube_Item_Type"})

    if Cube_Item_Level_Input_Check == False:
        return json.dumps({"Result": "Error", "Error_Result": "Cube_Item_Level"})

    if Cube_Option_Line_Input_Check == False:
        return json.dumps({"Result": "Error", "Error_Result": "Cube_Option_Line"})

    Result_List = {}
    Result_List["Result"] = "Success"

    for i in range(len(Cube_Option_Probability[Cube_Type_Input][Cube_Item_Type_Input][Cube_Item_Level_Input][Cube_Option_Line_Input][Cube_Grade_Input]["Name"])):
        Temp_List = {}
        Temp_List["Name"] = Cube_Option_Probability[Cube_Type_Input][Cube_Item_Type_Input][Cube_Item_Level_Input][Cube_Option_Line_Input][Cube_Grade_Input]["Name"][i]
        Temp_List["Probability"] = Cube_Option_Probability[Cube_Type_Input][Cube_Item_Type_Input][Cube_Item_Level_Input][Cube_Option_Line_Input][Cube_Grade_Input]["Probability"][i] / 10000
        Result_List[i] = Temp_List

    return json.dumps(Result_List, ensure_ascii=False)