import json, requests, datetime
from pandas import DataFrame


now = datetime.datetime.now() # get date and time
now_day = str(now.day)
now_month = str(now.month)
times = now.time().replace(microsecond=0) # del millisecond


# past now day and month
url = "https://autovokzal.org/upload/php/result.php?id=1331&date=%272021-" + now_month + "-" + now_day + "%27&station=ekb"


# catch errors
try:
    response = requests.get(url)  # get json
    response.raise_for_status()
    dic = response.json()
except Exception:
    print(">>>>--------> Errors with getting json <--------<<<<")


#write json file
with open('data.json', 'w', encoding='utf8') as f:
    json.dump(dic, f, ensure_ascii=False, indent=4)

#Read json file
with open('data.json') as f:
    data = json.load(f)


items_to_keep = []
for item in data["rasp"]:
    item["time_otpr"] = datetime.datetime.strptime(item["time_otpr"], "%H:%M").time() # convert str to class 'datetime
    item["name_route"] = item["name_route"].replace('г.Екатеринбург (Южный АВ) -<br/>', 'Екб (Южный АВ) -')   # rename value
    item["cancel"] = item["cancel"].replace("Отмена", "canceled")  # rename value
    item["status"] = item.pop("cancel") # rename key
    if item["time_otpr"] > times:
        items_to_keep.append(item)


#write json file
with open('new_data.json', 'w', encoding='utf8') as f:
    json.dump(items_to_keep, f, ensure_ascii=False, indent=4, sort_keys=True, default=str)


for i in items_to_keep: # print min to the next bus
    if i["status"] == "":
        nex_bus = i["time_otpr"].minute - times.minute
        free_place = i["free_place"]
        print(f" The next bus in {nex_bus} minutes, free places: {free_place} ")
        break


for i in items_to_keep: # convert class 'datetime.time to string deleting seconds
    i["time_otpr"] = i["time_otpr"].strftime("%H:%M")


df = DataFrame(items_to_keep, columns = ["time_otpr", "status", "free_place", "name_bus", "name_route"])
# output result without index pandas
print(df.to_string(index=False))



