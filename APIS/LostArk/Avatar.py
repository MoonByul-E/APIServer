from flask import Blueprint, request, render_template
import json, random, dbconfig_LostArk

Avatar = Blueprint("Avatar", __name__, url_prefix="/LostArk/Avatar")
db_Class = dbconfig_LostArk.DataBase()

print("LostArk Avatar 로딩 시작.")

Avatar_Avatar_List = ["Jump", "Promise"]
Avatar_Class_List = ["Warlord", "Berserker", "Destroyer", "Holyknight", "BattleMaster", "Infighter", "SoulMaster", "LanceMaster", "DevilHunter", "Blaster", "HawkEye", "Scouter", "Bard", "Summoner", "Arcana", "Blade", "Demonic", "Reaper", "Gunslinger", "Striker", "Sorceress"]
Avatar_Parts_List = ["Weapon", "Head", "Top", "Bottom"]
Avatar_Parts_Dic = {
    "Weapon": "무기",
    "Head": "머리",
    "Top": "상의",
    "Bottom": "하의"
}
Avatar_List = {}

for Avatar_Avatar in Avatar_Avatar_List:
    Avatar_List[Avatar_Avatar] = {}
    
    for Avatar_Class in Avatar_Class_List:
        Avatar_List[Avatar_Avatar][Avatar_Class] = {}

        if Avatar_Avatar == "Promise" and Avatar_Class == "Sorceress":
            continue

        Avatar_GetData_SQL = f"SELECT * FROM {Avatar_Avatar}_{Avatar_Class}"
        Avatar_GetData_ROW = db_Class.executeAll(Avatar_GetData_SQL)

        Avatar_Parts_Name_List = []
        Avatar_Item_Name_List = []
        Avatar_Item_Probability_List = []

        for Avatar_Data in Avatar_GetData_ROW:
            Avatar_Parts_Name_List.append(Avatar_Data["Parts"])
            Avatar_Item_Name_List.append(Avatar_Data["Name"])
            Avatar_Item_Probability_List.append(int(Avatar_Data["Probability"].replace(".", "")))
        
        Avatar_List[Avatar_Avatar][Avatar_Class]["Parts"] = Avatar_Parts_Name_List
        Avatar_List[Avatar_Avatar][Avatar_Class]["Name"] = Avatar_Item_Name_List
        Avatar_List[Avatar_Avatar][Avatar_Class]["Probability"] = Avatar_Item_Probability_List

db_Class.close()

print("LostArk Avatar 로딩 종료.")

@Avatar.route("/Avatar-Simulator")
def function_Avatar():
    Avatar_Type = "Jump"
    Class_Type = "Warlord"
    Parts_Type = "Weapon"

    if request.args.get("Avatar_Type") != None:
        Avatar_Type = request.args.get("Avatar_Type")

    Avatar_Type_Check = False

    for i in range(len(Avatar_Avatar_List)):
        if Avatar_Type == Avatar_Avatar_List[i]:
            Avatar_Type_Check = True

    if Avatar_Type_Check == False:
        return json.dumps({"Result": "Error", "Error_Result": "Avatar_Type"})

    if request.args.get("Class_Type") != None:
        Class_Type = request.args.get("Class_Type")

    Class_Type_Check = False

    for j in range(len(Avatar_Class_List)):
        if Class_Type == Avatar_Class_List[j]:
            Class_Type_Check = True

    if Class_Type_Check == False:
        return json.dumps({"Result": "Error", "Error_Result": "Class_Type"})

    if request.args.get("Parts_Type") != None:
        Parts_Type = request.args.get("Parts_Type")

    Parts_Type_Check = False

    for k in range(len(Avatar_Parts_List)):
        if Parts_Type == Avatar_Parts_List[k]:
            Parts_Type_Check = True

    if Parts_Type_Check == False:
        return json.dumps({"Result": "Error", "Error_Result": "Parts_Type"})

    if Avatar_Type == "Promise" and Class_Type == "Sorceress":
        return json.dumps({"Result": "Error", "Error_Result": "Class_Type"})
    
    Avatar_Name_List = []
    Avatar_Probability_List = []

    Parts = Avatar_List[Avatar_Type][Class_Type]["Parts"]
    for l in range(len(Parts)):
        if Parts[l] == Avatar_Parts_Dic[Parts_Type]:
            Avatar_Name_List.append(Avatar_List[Avatar_Type][Class_Type]["Name"][l])
            Avatar_Probability_List.append(Avatar_List[Avatar_Type][Class_Type]["Probability"][l])

    Random = random.randrange(1, sum(Avatar_Probability_List))

    Avatar_Item_Name = ""
    Avatar_Item_Probability = 0

    before_Probability = 1
    after_Probability = Avatar_Probability_List[0]

    for m in range(len(Avatar_Name_List)):
        print(f"{before_Probability} <= {Random} <= {after_Probability}")
        if Random >= before_Probability and Random <= after_Probability:
            Avatar_Item_Name = Avatar_Name_List[m]
            Avatar_Item_Probability = Avatar_Probability_List[m]
            break

        before_Probability += Avatar_Probability_List[m]
        after_Probability += Avatar_Probability_List[m + 1]

    return json.dumps({"Result": "Success", "Avatar_Name": Avatar_Item_Name, "Avatar_Probability": Avatar_Item_Probability / 100}, ensure_ascii=False)

@Avatar.route("/Avatar-Probability")
def function_Avatar_Probability():
    Avatar_Type = "Jump"
    Class_Type = "Warlord"
    Parts_Type = "Weapon"

    if request.args.get("Avatar_Type") != None:
        Avatar_Type = request.args.get("Avatar_Type")

    Avatar_Type_Check = False

    for i in range(len(Avatar_Avatar_List)):
        if Avatar_Type == Avatar_Avatar_List[i]:
            Avatar_Type_Check = True

    if Avatar_Type_Check == False:
        return json.dumps({"Result": "Error", "Error_Result": "Avatar_Type"})

    if request.args.get("Class_Type") != None:
        Class_Type = request.args.get("Class_Type")

    Class_Type_Check = False

    for j in range(len(Avatar_Class_List)):
        if Class_Type == Avatar_Class_List[j]:
            Class_Type_Check = True

    if Class_Type_Check == False:
        return json.dumps({"Result": "Error", "Error_Result": "Class_Type"})

    if request.args.get("Parts_Type") != None:
        Parts_Type = request.args.get("Parts_Type")

    Parts_Type_Check = False

    for k in range(len(Avatar_Parts_List)):
        if Parts_Type == Avatar_Parts_List[k]:
            Parts_Type_Check = True

    if Parts_Type_Check == False:
        return json.dumps({"Result": "Error", "Error_Result": "Parts_Type"})

    if Avatar_Type == "Promise" and Class_Type == "Sorceress":
        return json.dumps({"Result": "Error", "Error_Result": "Class_Type"})

    Result_List = {}
    Result_List["Result"] = "Success"

    Avatar_Name_List = []
    Avatar_Probability_List = []

    Parts = Avatar_List[Avatar_Type][Class_Type]["Parts"]
    for l in range(len(Parts)):
        if Parts[l] == Avatar_Parts_Dic[Parts_Type]:
            Avatar_Name_List.append(Avatar_List[Avatar_Type][Class_Type]["Name"][l])
            Avatar_Probability_List.append(Avatar_List[Avatar_Type][Class_Type]["Probability"][l])

    for m in range(len(Avatar_Name_List)):
        Temp_List = {}
        Temp_List["Item_Name"] = Avatar_Name_List[m]
        Temp_List["Item_Probability"] = Avatar_Probability_List[m] / 100
        Result_List[m] = Temp_List

    return json.dumps(Result_List, ensure_ascii=False)