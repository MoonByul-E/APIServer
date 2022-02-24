from bs4 import BeautifulSoup
import requests, dbconfig

db_Class = dbconfig.DataBase()

TheSeed_Url_List = ["https://maplestory.nexon.com/Guide/OtherProbability/ringBox/aliciaRingBox", "https://maplestory.nexon.com/Guide/OtherProbability/ringBox/hideRingBox", "https://maplestory.nexon.com/Guide/OtherProbability/ringBox/shineRingBox"]
TheSeed_Box_List = {
    "알리샤 반지 상자(1급)": "AliciaRingBox_1",
    "알리샤 반지 상자(2급)": "AliciaRingBox_2",
    "알리샤 반지 상자(3급)": "AliciaRingBox_3",
    "알리샤 반지 상자(4급)": "AliciaRingBox_4",
    "알리샤 반지 상자(5급)": "AliciaRingBox_5",
    "알리샤 반지 상자(6급)": "AliciaRingBox_6",
    "알리샤 반지 상자(7급)": "AliciaRingBox_7",
    "알리샤 반지 상자(8급)": "AliciaRingBox_8",
    "알리샤 반지 상자(9급)": "AliciaRingBox_9",
    "알리샤 반지 상자(10급)": "AliciaRingBox_10",
    "숨겨진 반지 상자": "HideRingBox",
    "빛나는 반지 상자": "ShineRingBox"
}

for TheSeed_Url in TheSeed_Url_List:
    TheSeed_Get = requests.get(TheSeed_Url)
    TheSeed_Html = TheSeed_Get.text
    TheSeed_Soup = BeautifulSoup(TheSeed_Html, "html.parser")
    TheSeed_Name = TheSeed_Soup.find_all("h3", attrs={"class": "sq_bul"})
    TheSeed_List = TheSeed_Soup.find_all("table", attrs={"class": "type2_table"}) 

    for i in range(len(TheSeed_List)):
        TheSeed_Table = TheSeed_List[i]

        TheSeed_Box_Name = TheSeed_Name[i + 1].get_text().split('아이템')[0].replace('의', '').strip()

        SQL = f"""CREATE TABLE TheSeed_{TheSeed_Box_List[TheSeed_Box_Name]}(
                    Name char(50),
                    Probability char(30)
                );"""
        db_Class.execute(SQL)
        print("테이블 생성 완료.")

        TheSeed_Items = TheSeed_Table.find_all("td")
        
        for j in range(0, len(TheSeed_Items), 2):
            TheSeed_Item_Name = TheSeed_Items[j].get_text()
            TheSeed_Item_Probability = TheSeed_Items[j + 1].get_text().replace('%', '')

            SQL = f"INSERT INTO TheSeed_{TheSeed_Box_List[TheSeed_Box_Name]} VALUES ('{TheSeed_Item_Name}', '{TheSeed_Item_Probability}')"
            db_Class.execute(SQL)
            print(f"아이템: {TheSeed_Item_Name} - 확률: {TheSeed_Item_Probability}% 추가 완료.")

            db_Class.commit()

db_Class.close()
print("갱신이 완료되었습니다.")

