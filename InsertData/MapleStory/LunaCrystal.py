from bs4 import BeautifulSoup
import requests, dbconfig

db_Class = dbconfig.DataBase()

LunaCrystal_Url_List = ["https://maplestory.nexon.com/Guide/CashShop/Probability/LunaCrystalSweet", "https://maplestory.nexon.com/Guide/CashShop/Probability/LunaCrystalDream"]
LunaCrystal_Type_List = ["Sweet", "Dream"]

for i in range(len(LunaCrystal_Url_List)):
    LunaCrystal_Url = LunaCrystal_Url_List[i]
    LunaCrystal_Get = requests.get(LunaCrystal_Url)
    LunaCrystal_Html = LunaCrystal_Get.text
    LunaCrystal_Soup = BeautifulSoup(LunaCrystal_Html, "html.parser")
    LunaCrystal_List = LunaCrystal_Soup.find("table", attrs={"class": "my_page_tb2"}).find_all("tr")
    del LunaCrystal_List[0]

    LunaCrystal_Item_List = []
    LunaCrystal_Item_Probability = []

    for LunaCrystal in LunaCrystal_List:
        LunaCrystal_Item_List.append(LunaCrystal.find("span").get_text())
        LunaCrystal_Item_Probability.append(LunaCrystal.find_all("td")[len(LunaCrystal.find_all("td")) - 1].get_text().replace("%", ""))

    SQL = f"""CREATE TABLE LunaCrystal_{LunaCrystal_Type_List[i]}(
                        Name char(50),
                        Probability char(30)
            );"""
    db_Class.execute(SQL)
    print("테이블 생성 완료.")

    for j in range(len(LunaCrystal_Item_List)):
        SQL = f"INSERT INTO LunaCrystal_{LunaCrystal_Type_List[i]} VALUES ('{LunaCrystal_Item_List[j]}', '{LunaCrystal_Item_Probability[j]}')"
        db_Class.execute(SQL)
        print(f"아이템: {LunaCrystal_Item_List[j]} - 확률: {LunaCrystal_Item_Probability[j]}% 추가 완료.")

    db_Class.commit()

db_Class.close()
print("갱신이 완료되었습니다.")