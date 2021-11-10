import json, requests
import datetime
from pandas import DataFrame

# get time
now = datetime.datetime.now()
# get date
now_day = str(now.day)
# convert int (minutes and hours) to string and sum
my_time = str(now.hour) + str(now.minute)
# output int
times = int(my_time)


 # past now day
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


# delete html code and abbreviation of name
for item in data["rasp"]:
    item["name_route"] = item["name_route"].replace('г.Екатеринбург (Южный АВ) -<br/>', 'Екб (Южный АВ)')


# convert str ["time_otpr"] to int
for item in data["rasp"]:
    item["time_otpr"] = int("".join(filter(str.isdigit, item["time_otpr"])))


#write json file
with open('new_data.json', 'w', encoding='utf8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)


df = DataFrame(data['rasp'], columns = ['time_otpr', 'cancel', 'free_place', 'name_bus', 'name_route'])
# output result without index pandas
print(df.to_string(index=False))







# # print result
# for i in data["rasp"]:
#     if i["time_otpr"] < times:
#         continue
#     if i["cancel"] == "Отмена":
#         i["cancel"] = "canceled"
#     if i["cancel"] == "":
#         i["cancel"] = "waiting"
#     print(f"Time: {i['time_otpr']}, status: {i['cancel']}, free place: {i['free_place']}, name bus: {i['name_bus']}, {i['name_route']}")
