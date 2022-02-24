from bs4 import BeautifulSoup
import requests, dbconfig, json

db_Class = dbconfig.DataBase()

WispsWonderBerry_Url = "https://maplestory.nexon.com/Guide/CashShop/Probability/WispsWonderBerry"
WispsWonderBerry_Get = requests.get(WispsWonderBerry_Url)
WispsWonderBerry_Html = WispsWonderBerry_Get.text
WispsWonderBerry_Soup = BeautifulSoup(WispsWonderBerry_Html, "html.parser")
WispsWonderBerry_List = WispsWonderBerry_Soup.find("table", attrs={"class": "my_page_tb2"}).find_all("tr")
del WispsWonderBerry_List[0]

Item_List = []
Item_Probability = []

for WispsWonderBerry in WispsWonderBerry_List:
    Item_List.append(WispsWonderBerry.find("span").get_text())
    Item_Probability.append(WispsWonderBerry.find_all("td")[len(WispsWonderBerry.find_all("td")) - 1].get_text().replace("%", ""))

SQL = f"""CREATE TABLE WispsWonderBerry(
                    Name char(50),
                    Probability char(30)
        );"""
db_Class.execute(SQL)
print("테이블 생성 완료.")

for i in range(len(Item_List)):
    SQL = f"INSERT INTO WispsWonderBerry VALUES ('{Item_List[i]}', '{Item_Probability[i]}')"
    db_Class.execute(SQL)
    print(f"아이템: {Item_List[i]} - 확률: {Item_Probability[i]}% 추가 완료.")

db_Class.commit()
db_Class.close()

print("갱신이 완료되었습니다.")

print(Item_Probability)