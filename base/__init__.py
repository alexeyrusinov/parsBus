import json, requests
import datetime

#получаю текущее вермя
now = datetime.datetime.now()
# получаю текущю дату
now_day = str(now.day)
# преобразую минуты и часы в строки и скоадываю
my_time = str(now.hour) + str(now.minute)
# на выходе инт без нулей
times = int(my_time)



 # подставляю текущий день
url = "https://autovokzal.org/upload/php/result.php?id=1331&date=%272021-11-" + now_day  + "%27&station=ekb"


response = requests.get(url)
response.raise_for_status()
dic = response.json()

#write json file
with open('data.json', 'w', encoding='utf8') as f:
    json.dump(dic, f, ensure_ascii=False, indent=4)

#Read json file
with open('data.json') as f:
    data = json.load(f)

# убираю из строки html
for item in data["rasp"]:
    item["name_route"] = item["name_route"].replace('<br/>', '')

# преобразую время отаправаления в число отбрасывая ноль
for item in data["rasp"]:
    item["time_otpr"] = int("".join(filter(str.isdigit, item["time_otpr"])))

#write json file
with open('new_data.json', 'w', encoding='utf8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)


for i in data["rasp"]:
    if i["time_otpr"] < times:
        continue
    if i["cancel"] == "Отмена":
        i["cancel"] = "canceled"
    if i["cancel"] == "":
        i["cancel"] = "waiting"
    print(f"Time: {i['time_otpr']}, status: {i['cancel']}, free place: {i['free_place']}, name bus: {i['name_bus']}, {i['name_route']}")
