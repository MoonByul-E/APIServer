from bs4 import BeautifulSoup
import requests, dbconfig

db_Class = dbconfig.DataBase()

Cube_Upgrade_List = {
    "레어 → 에픽": "Rare",
    "에픽 → 유니크": "Epic",
    "유니크 → 레전드리": "Unique"
}
Cube_Type_List = ["Red", "Black", "Addi", "Strange", "Master", "Artisan"]

for i in range(len(Cube_Type_List)):
    Cube_GetData_Url = f"https://maplestory.nexon.com/Guide/OtherProbability/cube/{Cube_Type_List[i]}"
    Cube_GetData_Get = requests.get(Cube_GetData_Url)
    Cube_GetData_Html = Cube_GetData_Get.text
    Cube_GetData_Soup = BeautifulSoup(Cube_GetData_Html, "html.parser")
    Cube_GetData_Upgrade = Cube_GetData_Soup.find("table", attrs={"class": "cube_info"})
    del Cube_GetData_Upgrade[0]

    Cube_GetData_Upgrade_Data = Cube_GetData_Upgrade.find_all("tr")
    del Cube_GetData_Upgrade_Data[0]

    SQL = f"""CREATE TABLE Cube_Upgrade_Probability_{Cube_Type_List[i]}(
                Name char(50),
                Probability char(10)
            );"""
    db_Class.execute(SQL)
    print(f"Cube_Upgrade_Probability_{Cube_Type_List[i]} 테이블 생성 완료.")

    for j in range(len(Cube_GetData_Upgrade_Data)):
        Cube_GetData_Upgrade_Name = Cube_GetData_Upgrade_Data[j].find_all("td")[0].get_text()
        Cube_GetData_Upgrade_Value = Cube_GetData_Upgrade_Data[j].find_all("td")[1].get_text().replace("%", "")

        SQL = f"INSERT INTO Cube_Upgrade_Probability_{Cube_Type_List[i]} VALUES ('{Cube_Upgrade_List[Cube_GetData_Upgrade_Name]}', '{Cube_GetData_Upgrade_Value}')"
        db_Class.execute(SQL)
        print(f"이름: {Cube_Upgrade_List[Cube_GetData_Upgrade_Name]} - 확률: {Cube_GetData_Upgrade_Value} 추가 완료.")

    db_Class.commit()

db_Class.close()
print("갱신이 완료되었습니다.")