from bs4 import BeautifulSoup
import requests, dbconfig

db_Class = dbconfig.DataBase()

Probability_Url = "https://cdn-lostark.game.onstove.com/uploadfiles/e7ee30dc84d14fe89bdd6293b0f04f12.html"
Probability_Get = requests.get(Probability_Url)

Probability_Get.raise_for_status()
Probability_Get.encoding = 'UTF-8'

Probability_Html = Probability_Get.text
Probability_Soup = BeautifulSoup(Probability_Html, "html.parser")
Probability_List = Probability_Soup.find_all("div", attrs={"class": "group"})

Probability_Title_List = {
    "T2 보석 상자 (1~2Lv)": "T2_12",
    "T2 보석 상자 (1~3Lv)": "T2_13",
    "T3 보석 상자 (1~2Lv)": "T3_12",
    "T3 보석 상자 (1~3Lv)": "T3_13",
    "전설~영웅 카드 팩": "Legend_Hero_CardPack",
    "전설~희귀 카드 팩": "Legend_Rare_CardPack",
    "전체 카드 팩": "All_CardPack",
    "전설 카드 팩": "Legend_CardPack",
    "영웅 카드 팩": "Hero_CardPack",
    "희귀 카드 팩": "Rare_CardPack",
    "고급 카드 팩": "High_CardPack",
    "일반 카드 팩": "Normal_CardPack",
    "유물 호감도 상자": "Relic_Box",
    "전설 호감도 상자": "Legend_Box",
    "영웅 호감도 상자": "Hero_Box",
    "펫효과1": "Pet_1",
    "펫효과2": "Pet_2"
}

Probability_Avatar_List = {
    "전설 아바타 「도약」": "Jump",
    "전설 아바타 「약속」": "Promise"
}

Probability_Class_List = {
    "워로드": "Warlord",
    "버서커": "Berserker",
    "디스트로이어": "Destroyer",
    "홀리나이트": "Holyknight",
    "배틀마스터": "BattleMaster",
    "인파이터": "Infighter",
    "기공사": "SoulMaster",
    "창술사": "LanceMaster",
    "데빌헌터": "DevilHunter",
    "블래스터": "Blaster",
    "호크아이": "HawkEye",
    "스카우터": "Scouter",
    "바드": "Bard",
    "서머너": "Summoner",
    "아르카나": "Arcana",
    "블레이드": "Blade",
    "데모닉": "Demonic",
    "리퍼": "Reaper",
    "건슬링어": "Gunslinger",
    "스트라이커": "Striker",
    "소서리스": "Sorceress"
}

for Probability_Table in Probability_List:
    Probability_Title = Probability_Table.find("h2").get_text()
    Probability_Table_Count = len(Probability_Table.find("thead").find_all("th"))
    Probability_Table_Name = Probability_Table.find("thead").find_all("th")
    Probability_Table_Body = Probability_Table.find("tbody").find_all("td")

    if Probability_Table_Count == 3:
        SQL = f"""CREATE TABLE {Probability_Title_List[Probability_Title]}(
                    Grade char(30),
                    Name char(50),
                    Probability char(30)
                );"""
        db_Class.execute(SQL)
        print("테이블 생성 완료.")

        for i in range(0, len(Probability_Table_Body), 3):
            if Probability_Table_Body[i].get_text() == "합계":
                continue
            SQL = f"INSERT INTO {Probability_Title_List[Probability_Title]} VALUES ('{Probability_Table_Body[i].get_text()}', '{Probability_Table_Body[i + 1].get_text().replace('%', '%%')}', '{Probability_Table_Body[i + 2].get_text().replace('%', '')}')"
            db_Class.execute(SQL)
            print(f"등급: {Probability_Table_Body[i].get_text()} - 아이템: {Probability_Table_Body[i + 1].get_text()} - 확률: {Probability_Table_Body[i + 2].get_text().replace('%', '')}% 추가 완료.")

    elif Probability_Table_Count == 8:
        Probability_Avatar_Name = Probability_Title.split(":")[0].strip()
        Probability_Class_Name = Probability_Title.split(":")[1].strip()
        SQL = f"""CREATE TABLE {Probability_Avatar_List[Probability_Avatar_Name]}_{Probability_Class_List[Probability_Class_Name]}(
                    Parts char(30),
                    Name char(50),
                    Probability char(30)
                );"""
        db_Class.execute(SQL)
        print("테이블 생성 완료.")
        
        for i in range(0, len(Probability_Table_Body), 2):
            if Probability_Table_Body[i].get_text().strip() == "합계" or Probability_Table_Body[i].get_text().strip() == "-":
                continue

            Probability_Item_Name = ""
            Probability_Item_Name_List = ["머리", "상의", "하의"]

            for Probability_Items_Name in Probability_Item_Name_List:
                if Probability_Items_Name == Probability_Table_Body[i].get_text()[-2:]:
                    Probability_Item_Name = Probability_Items_Name
                    break
                else:
                    Probability_Item_Name = "무기"

            SQL = f"INSERT INTO {Probability_Avatar_List[Probability_Avatar_Name]}_{Probability_Class_List[Probability_Class_Name]} VALUES ('{Probability_Item_Name}', '{Probability_Table_Body[i].get_text().replace('%', '%%')}', '{Probability_Table_Body[i + 1].get_text().replace('%', '')}')"
            db_Class.execute(SQL)
            print(f"부위: {Probability_Item_Name} - 아이템: {Probability_Table_Body[i].get_text()} - 확률: {Probability_Table_Body[i + 1].get_text().replace('%', '')}% 추가 완료.")
    
    db_Class.commit()
db_Class.close()
print("갱신이 완료되었습니다.")