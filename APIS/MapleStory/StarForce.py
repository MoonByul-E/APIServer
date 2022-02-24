from flask import Blueprint, request, render_template
import json, random

StarForce = Blueprint("StarForce", __name__, url_prefix="/MapleStory/StarForce")

def StarForce_Price(Star, WeaponLevel):
    Price = 0

    if Star >= 0 and Star <= 9:
        Price = 1000 + ((WeaponLevel ** 3) * (Star + 1)) / 25

    elif Star >= 10 and Star <= 14:
        Price = 1000 + ((WeaponLevel ** 3) * ((Star + 1) ** 2.7)) / 400

    elif Star >= 15 and Star <= 24:
        Price = 1000 + ((WeaponLevel ** 3) * ((Star + 1) ** 2.7)) / 200

    return round(Price, -2)

def StarForce_Probability(Star):
    Success = 0
    Keep = 0
    Destroy = 0

    if Star >= 0 and Star <= 2:
        Success = (95 - 5 * Star)
    
    elif Star >= 3 and Star <= 14:
        Success = (100 - 5 * Star)

        if Star == 12:
            Destroy = 0.6
        elif Star == 13:
            Destroy = 1.3
        elif Star == 14:
            Destroy = 1.4
    
    elif Star >= 15 and Star <= 21:
        Success = 30

        if Star >= 15 and Star <= 17:
            Destroy = 2.1
        elif Star >= 18 and Star <= 19:
            Destroy = 2.8
        elif Star >= 20 and Star <= 21:
            Destroy = 7
    
    elif Star == 22:
        Success = 3
        Destroy = 19.4

    elif Star == 23:
        Success = 2
        Destroy = 29.4
    
    elif Star == 24:
        Success = 1
        Destroy = 39.6

    Keep = 100 - Success - Destroy

    return [Success * 10, Keep * 10, Destroy * 10]

@StarForce.route("/StarForce-Simulator")
def function_StarForce():
    StartStar = 0
    WeaponLevel = 150

    if request.args.get("StartStar") != None:
        if request.args.get("StartStar").isdigit(): 
            StartStar = int(request.args.get("StartStar"))
        else:
            return json.dumps({"Result": "Error", "Error_Result": "Star"})
    
    if request.args.get("WeaponLevel") != None:
        if request.args.get("WeaponLevel").isdigit(): 
            WeaponLevel = int(request.args.get("WeaponLevel"))
        else:
            return json.dumps({"Result": "Error", "Error_Result": "WeaponLevel"})

    if not(StartStar >= 0 and StartStar <= 24):
        return json.dumps({"Result": "Error", "Error_Result": "Star"})

    Random = random.randrange(1, 1000)
    Success, Keep, Destroy = StarForce_Probability(StartStar)
    Price = StarForce_Price(StartStar, WeaponLevel)

    Result = ""

    if Random >= 1 and Random <= Success:
        Result = "Success"
    elif Random >= Success + 1 and Random <= Success + Keep:
        Result = "Keep"
    else:
        Result = "Destroy"

    return json.dumps({"Result": "Success", "StartStar": StartStar, "WeaponLevel": WeaponLevel, "Upgrade_Result": Result, "Upgrade_Price": Price, "Upgrade_Probability": {"Success": Success / 10, "Keep": Keep / 10, "Destroy": Destroy / 10}})

@StarForce.route("/StarForce-Price")
def function_StarForce_Price():
    StartStar = 0
    WeaponLevel = 150

    if request.args.get("StartStar") != None:
        if request.args.get("StartStar").isdigit(): 
            StartStar = int(request.args.get("StartStar"))
        else:
            return json.dumps({"Result": "Error", "Error_Result": "Star"})
    
    if request.args.get("WeaponLevel") != None:
        if request.args.get("WeaponLevel").isdigit(): 
            WeaponLevel = int(request.args.get("WeaponLevel"))
        else:
            return json.dumps({"Result": "Error", "Error_Result": "WeaponLevel"})

    if not(StartStar >= 0 and StartStar <= 24):
        return json.dumps({"Result": "Error", "Error_Result": "Star"})

    return json.dumps({"Result": "Success", "StartStar": StartStar, "WeaponLevel": WeaponLevel, "Price": StarForce_Price(StartStar, WeaponLevel)})

@StarForce.route("/StarForce-Probability")
def function_StarForce_Probability():
    StartStar = 0

    if request.args.get("StartStar") != None:
        if request.args.get("StartStar").isdigit(): 
            StartStar = int(request.args.get("StartStar"))
        else:
            return json.dumps({"Result": "Error", "Error_Result": "Star"})

    if not(StartStar >= 0 and StartStar <= 24):
        return json.dumps({"Result": "Error", "Error_Result": "Star"})

    Success, Keep, Destroy = StarForce_Probability(StartStar)

    return json.dumps({"Result": "Success", "StartStar": StartStar, "Probability": {"Success": Success / 10, "Keep": Keep / 10, "Destroy": Destroy / 10}})
