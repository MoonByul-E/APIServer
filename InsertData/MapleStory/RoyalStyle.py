from bs4 import BeautifulSoup
import requests, dbconfig

db_Class = dbconfig.DataBase()

RoyalStyle_Url = "https://maplestory.nexon.com/Guide/CashShop/Probability/RoyalStyle"
RoyalStyle_Get = requests.get(RoyalStyle_Url)
RoyalStyle_Html = RoyalStyle_Get.text
RoyalStyle_Soup = BeautifulSoup(RoyalStyle_Html, "html.parser")
RoyalStyle_List = RoyalStyle_Soup.find("table", attrs={"class": "my_page_tb2"}).find_all("tr")
del RoyalStyle_List[0]

Item_List = []
Item_Probability = []

for RoyalStyle in RoyalStyle_List:
    Item_List.append(RoyalStyle.find("span").get_text())
    Item_Probability.append(RoyalStyle.find_all("td")[len(RoyalStyle.find_all("td")) - 1].get_text().replace("%", ""))

SQL = f"""CREATE TABLE RoyalStyle(
                    Name char(50),
                    Probability char(10)
        );"""
db_Class.execute(SQL)
print("테이블 생성 완료.")

for i in range(len(Item_List)):
    SQL = f"INSERT INTO RoyalStyle VALUES ('{Item_List[i]}', '{Item_Probability[i]}')"
    db_Class.execute(SQL)
    print(f"아이템: {Item_List[i]} - 확률: {Item_Probability[i]}% 추가 완료.")

db_Class.commit()
db_Class.close()

print("갱신이 완료되었습니다.")
