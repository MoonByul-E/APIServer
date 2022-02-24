from bs4 import BeautifulSoup
import requests, dbconfig, json

db_Class = dbconfig.DataBase()

MasterPiece_Red_Url = "https://maplestory.nexon.com/Guide/CashShop/Probability/MasterpieceRed"
MasterPiece_Red_Get = requests.get(MasterPiece_Red_Url)
MasterPiece_Red_Html = MasterPiece_Red_Get.text
MasterPiece_Red_Soup = BeautifulSoup(MasterPiece_Red_Html, "html.parser")
MasterPiece_Red_List = MasterPiece_Red_Soup.find_all("table", attrs={"class": "my_page_tb2"})

MasterPiece_List = {}
Pice_List = ["Cap", "Clothes", "Cloak_Gloves", "Shoes", "Weapon"]

for i in range(len(MasterPiece_Red_List)):
    Item_List = {}
    MasterPiece_Red_Item_List = MasterPiece_Red_List[i].find_all("tr")
    del MasterPiece_Red_Item_List[0]
    
    for j in range(len(MasterPiece_Red_Item_List)):
        Temp_List = {}

        ItemName = MasterPiece_Red_Item_List[j].find("span").get_text()
        ItemProbability = MasterPiece_Red_Item_List[j].find_all("td")[len(MasterPiece_Red_Item_List[j].find_all("td")) - 1].get_text().replace("%", "")
        Temp_List["Name"] = ItemName
        Temp_List["Probability"] = ItemProbability

        Item_List[j] = Temp_List

    MasterPiece_List[Pice_List[i]] = Item_List

for Item_Type in MasterPiece_List:
    SQL = f"""CREATE TABLE MasterPiece_Red_{Item_Type}(
                Name char(50),
                Probability char(30)
            );"""
    db_Class.execute(SQL)
    print(f"MasterPiece_Red_{Item_Type} 테이블 생성.")

    for Item_List in MasterPiece_List[Item_Type]:
        SQL = f"""INSERT INTO MasterPiece_Red_{Item_Type} VALUES ('{MasterPiece_List[Item_Type][Item_List]["Name"]}', '{MasterPiece_List[Item_Type][Item_List]["Probability"]}')"""
        db_Class.execute(SQL)
        print(f"아이템: {MasterPiece_List[Item_Type][Item_List]['Name']} - 확률: {MasterPiece_List[Item_Type][Item_List]['Probability']}% 추가 완료.")

    db_Class.commit()

MasterPiece_Black_Url = "https://maplestory.nexon.com/Guide/CashShop/Probability/MasterpieceBlack"
MasterPiece_Black_Get = requests.get(MasterPiece_Black_Url)
MasterPiece_Black_Html = MasterPiece_Black_Get.text
MasterPiece_Black_Soup = BeautifulSoup(MasterPiece_Black_Html, "html.parser")
MasterPiece_Black_List = MasterPiece_Black_Soup.find_all("table", attrs={"class": "my_page_tb2"})

MasterPiece_List = {}
Pice_List = ["Cap", "Clothes", "Cloak_Gloves", "Shoes", "Weapon"]

for i in range(len(MasterPiece_Black_List)):
    Item_List = {}
    MasterPiece_Black_Item_List = MasterPiece_Black_List[i].find_all("tr")
    del MasterPiece_Black_Item_List[0]
    
    for j in range(len(MasterPiece_Black_Item_List)):
        Temp_List = {}

        ItemName = MasterPiece_Black_Item_List[j].find("span").get_text()
        ItemProbability = MasterPiece_Black_Item_List[j].find_all("td")[len(MasterPiece_Black_Item_List[j].find_all("td")) - 1].get_text().replace("%", "")
        Temp_List["Name"] = ItemName
        Temp_List["Probability"] = ItemProbability

        Item_List[j] = Temp_List

    MasterPiece_List[Pice_List[i]] = Item_List

for Item_Type in MasterPiece_List:
    SQL = f"""CREATE TABLE MasterPiece_Black_{Item_Type}(
                Name char(50),
                Probability char(30)
            );"""
    db_Class.execute(SQL)
    print(f"MasterPiece_Black_{Item_Type} 테이블 생성.")

    for Item_List in MasterPiece_List[Item_Type]:
        SQL = f"""INSERT INTO MasterPiece_Black_{Item_Type} VALUES ('{MasterPiece_List[Item_Type][Item_List]["Name"]}', '{MasterPiece_List[Item_Type][Item_List]["Probability"]}')"""
        db_Class.execute(SQL)
        print(f"아이템: {MasterPiece_List[Item_Type][Item_List]['Name']} - 확률: {MasterPiece_List[Item_Type][Item_List]['Probability']}% 추가 완료.")

    db_Class.commit()
db_Class.close()

print("갱신이 완료되었습니다.")

#print(json.dumps(MasterPiece_List, indent=4, ensure_ascii=False))