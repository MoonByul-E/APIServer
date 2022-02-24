from bs4 import BeautifulSoup
import requests, dbconfig

db_Class = dbconfig.DataBase()

Royal_Url_List = ["https://maplestory.nexon.com/Guide/CashShop/Probability/RoyalHairCoupon", "https://maplestory.nexon.com/Guide/CashShop/Probability/RoyalPlasticSurgeryCoupon"]
Royal_Type_List = ["Hair", "PlasticSurgery"]

for i in range(len(Royal_Url_List)):
    Royal_Url = Royal_Url_List[i]
    Royal_Get = requests.get(Royal_Url)
    Royal_Html = Royal_Get.text
    Royal_Soup = BeautifulSoup(Royal_Html, "html.parser")
    Royal_List = Royal_Soup.find_all("table", attrs={"class": "my_page_tb2"}) 

    Royal_Name_List = []
    Royal_Probability_List = []

    Royal_Sex_List = ["Man", "Woman"]

    for Royal_Sex in Royal_List:
        Royal_Sex_Item = Royal_Sex.find_all("tr")
        del Royal_Sex_Item[0]

        Item_List = []
        Item_Probability = []

        for Royal in Royal_Sex_Item:
            Item_List.append(Royal.find("span").get_text())
            Item_Probability.append(Royal.find_all("td")[len(Royal.find_all("td")) - 1].get_text().replace("%", ""))

        Royal_Name_List.append(Item_List)
        Royal_Probability_List.append(Item_Probability)

    for j in range(len(Royal_Name_List)):
        SQL = f"""CREATE TABLE Beauty_Royal_{Royal_Type_List[i]}_{Royal_Sex_List[j]}(
                            Name char(50),
                            Probability char(10)
                );"""
        db_Class.execute(SQL)
        print("테이블 생성 완료.")

        for k in range(len(Royal_Name_List[j])):
            SQL = f"INSERT INTO Beauty_Royal_{Royal_Type_List[i]}_{Royal_Sex_List[j]} VALUES ('{Royal_Name_List[j][k]}', '{Royal_Probability_List[j][k]}')"
            db_Class.execute(SQL)
            print(f"아이템: {Royal_Name_List[j][k]} - 확률: {Royal_Probability_List[j][k]}% 추가 완료.")

        db_Class.commit()

db_Class.close()
print("갱신이 완료되었습니다.")
