from bs4 import BeautifulSoup
import requests, dbconfig

db_Class = dbconfig.DataBase()

GoldApple_Url = "https://maplestory.nexon.com/Guide/CashShop/Probability/GoldApple"
GoldApple_Get = requests.get(GoldApple_Url)
GoldApple_Html = GoldApple_Get.text
GoldApple_Soup = BeautifulSoup(GoldApple_Html, "html.parser")
GoldApple_List = GoldApple_Soup.find("table", attrs={"class": "my_page_tb2"}).find_all("tr")
del GoldApple_List[0]

Item_List = []
Item_Probability = []

for GoldApple in GoldApple_List:
    Item_List.append(GoldApple.find("span").get_text())
    Item_Probability.append(GoldApple.find_all("td")[len(GoldApple.find_all("td")) - 1].get_text().replace("%", ""))

SQL = f"""CREATE TABLE GoldApple(
                    Name char(50),
                    Probability char(30)
        );"""
db_Class.execute(SQL)
print("테이블 생성 완료.")

for i in range(len(Item_List)):
    SQL = f"INSERT INTO GoldApple VALUES ('{Item_List[i].replace('%', '%%')}', '{Item_Probability[i]}')"
    db_Class.execute(SQL)
    print(f"아이템: {Item_List[i]} - 확률: {Item_Probability[i]}% 추가 완료.")

db_Class.commit()
db_Class.close()

print("갱신이 완료되었습니다.")
