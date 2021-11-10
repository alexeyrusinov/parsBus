import json, requests, datetime
from pandas import DataFrame

# get time
now = datetime.datetime.now()
# get date
now_day = str(now.day)
# convert int (minutes and hours) to string and sum
my_time = str(now.hour) + str(now.minute)
# get time int
times = int(my_time)


# past now day
url = "https://autovokzal.org/upload/php/result.php?id=1331&date=%272021-11-" + now_day  + "%27&station=ekb"

# get json
response = requests.get(url)
response.raise_for_status()
dic = response.json()


#write json file
with open('data.json', 'w', encoding='utf8') as f:
    json.dump(dic, f, ensure_ascii=False, indent=4)

#Read json file
with open('data.json') as f:
    data = json.load(f)


items_to_keep = []
for item in data["rasp"]:
    # convert str ["time_otpr"] to int
    item["time_otpr"] = int("".join(filter(str.isdigit, item["time_otpr"])))
    # add buses with the nearest time
    if item["time_otpr"] > times:
        items_to_keep.append(item)
    # delete html code and abbreviation of name
    item["name_route"] = item["name_route"].replace('г.Екатеринбург (Южный АВ) -<br/>', 'Екб (Южный АВ)')


#write json file
with open('new_data.json', 'w', encoding='utf8') as f:
    json.dump(items_to_keep, f, ensure_ascii=False, indent=4)


df = DataFrame(items_to_keep, columns = ['time_otpr', 'cancel', 'free_place', 'name_bus', 'name_route'])
# output result without index pandas
print(df.to_string(index=False))