from bs4 import BeautifulSoup
import requests, dbconfig

db_Class = dbconfig.DataBase()

Cube_Option_Grade_List = {
    "레어": "Rare",
    "에픽": "Epic",
    "유니크": "Unique",
    "레전드리": "Legendary"
}

Cube_Option_Item_Type_List = {
    "무기": "Weapon",
    "엠블렘": "Emblem",
    "보조무기 (포스실드, 소울링 제외)": "SubWeapon",
    "포스실드, 소울링": "ForceShield_SoulRing",
    "방패": "Shield",
    "모자": "Cap",
    "상의": "Top",
    "한벌옷": "Clothes",
    "하의": "Bottom",
    "신발": "Shoes",
    "장갑": "Gloves",
    "망토": "Cloak",
    "벨트": "Belt",
    "어깨장식": "Shoulder",
    "얼굴장식": "Face",
    "눈장식": "Eye",
    "귀고리": "EarRing",
    "반지": "Ring",
    "펜던트": "Pendant",
    "기계심장": "MachineHeart"
}

Cube_Option_Item_Level_List = {
    "120레벨 이상": "120",
    "100레벨": "100"
}

Cube_Option_List = {
    0: "첫 번째 옵션",
    1: "두 번째 옵션",
    2: "세 번째 옵션"
}

Cube_Type_List = ["Red", "Black", "Addi", "Strange", "Master", "Artisan"]
Cube_Type_Name_List = ["레드", "블랙", "에디셔널", "수상한", "장인의", "명장의"]

for i in range(len(Cube_Type_List)):
    Cube_GetData_Url = f"https://maplestory.nexon.com/Guide/OtherProbability/cube/{Cube_Type_List[i]}"
    Cube_GetData_Get = requests.get(Cube_GetData_Url)
    Cube_GetData_Html = Cube_GetData_Get.text
    Cube_GetData_Soup = BeautifulSoup(Cube_GetData_Html, "html.parser")

    SQL = f"""CREATE TABLE Cube_Option_Probability_{Cube_Type_List[i]}(
            Grade char(10),
            Item_Type char(30),
            Item_Level char(10),
            Option_Line char(10),
            Name char(200),
            Probability char(30)
        );"""
    db_Class.execute(SQL)
    print("테이블 생성 완료.")

    Cube_GetData_Option_List = Cube_GetData_Soup.find_all("div", attrs={"class": "cube_option"})
    Cube_GetData_Data_List = Cube_GetData_Soup.find_all("table", attrs={"class": "cube_data"})
    
    for j in range(len(Cube_GetData_Option_List)):
        Cube_GetData_Option_Grade = Cube_GetData_Option_List[j].find_all("span")[0].get_text()
        Cube_GetData_Option_Item_Type = Cube_GetData_Option_List[j].find_all("span")[1].get_text()
        Cube_GetData_Option_Item_Level = Cube_GetData_Option_List[j].find_all("span")[2].get_text()

        Cube_GetData_Data_TD = Cube_GetData_Data_List[j].find_all("td")
        for k in range(0, len(Cube_GetData_Data_TD), 2):
            Cube_GetData_Data_Name = Cube_GetData_Data_TD[k].get_text()
            Cube_GetData_Data_Probability = Cube_GetData_Data_TD[k + 1].get_text()

            if Cube_GetData_Data_Name == "" or Cube_GetData_Data_Name == "잠재옵션":
                continue
            SQL = f"INSERT INTO Cube_Option_Probability_{Cube_Type_List[i]} VALUES ('{Cube_Option_Grade_List[Cube_GetData_Option_Grade]}', '{Cube_Option_Item_Type_List[Cube_GetData_Option_Item_Type]}', '{Cube_Option_Item_Level_List[Cube_GetData_Option_Item_Level]}', '{int((k / 2) % 3)}', '{Cube_GetData_Data_Name.replace('%', '%%').strip()}', '{Cube_GetData_Data_Probability.replace('%', '')}')"
            db_Class.execute(SQL)
            print(f"큐브: {Cube_Type_Name_List[i]} 큐브, 아이템 등급: {Cube_GetData_Option_Grade}, 아이템 종류: {Cube_GetData_Option_Item_Type}, 아이템 레벨: {Cube_GetData_Option_Item_Level}, 옵션 이름: {Cube_GetData_Data_Name}, 옵션 확률: {Cube_GetData_Data_Probability}, 옵션 라인: {Cube_Option_List[int((k / 2) % 3)]}")
    db_Class.commit()
db_Class.close()
print("갱신이 완료되었습니다.")