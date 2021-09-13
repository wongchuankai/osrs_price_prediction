import requests
import json
import csv

def getItemDetails_catalogue(itemID):
    BASE_URL = "http://services.runescape.com/m=itemdb_oldschool"
    data = requests.get(BASE_URL + "/api/catalogue/detail.json", params={'item':itemID})
    # json_data = json.dumps(json.loads(data.text), indent=2)
    json_data = json.loads(data.text)
    return json_data

def getItemDetails_graph(itemID):
    BASE_URL = "http://services.runescape.com/m=itemdb_oldschool"
    data = requests.get(BASE_URL + "/api/graph/{}.json".format(itemID))
    json_data = json.loads(data.text)
    return json_data

def get_runes_dataset(filename):
    itemList = list(range(554, 567, 1))
    GE_runes_data = {}
    labels = ['timestamp']

    for itemID in itemList:
        item_data_graph = getItemDetails_graph(itemID)
        current_daily_list = item_data_graph['daily']
        # print(current_daily_list)

        for daily_time_stamp in current_daily_list:
            if(daily_time_stamp in GE_runes_data):
                GE_runes_data[daily_time_stamp].append(current_daily_list[daily_time_stamp])
            else:
                GE_runes_data[daily_time_stamp] = [current_daily_list[daily_time_stamp]]

        item_data_catalogue = getItemDetails_catalogue(itemID)
        labels.append(item_data_catalogue['item']['name'].replace(" ", "_"))
    
    with open(filename+".csv", mode="w", newline='') as data_output:
        data_write = csv.writer(data_output, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        data_write.writerow(labels)

        for daily_time_stamp in GE_runes_data:
            new_rows = [daily_time_stamp]
            new_rows.extend(GE_runes_data[daily_time_stamp])
            data_write.writerow(new_rows)

    return (GE_runes_data)

def main():
    # abyssal_whip_itemID = 4151
    # data = getItemDetails_catalogue(abyssal_whip_itemID)
    # print(data)
    runes_dataset = get_runes_dataset("runes_dataset")
    print(runes_dataset)

if __name__ == "__main__":
    main()





