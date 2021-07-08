"Peter Nguyen"
"6/20/2021"
"CIS2348"
"1860823"
"Final Project Part 2"

# Importing in csv and date &time
import csv
from datetime import datetime

# This is where the input csv files will be read
from typing import Dict, Any

if __name__ == '__main__':
    items: Dict[str, Dict[Any, Any]] = {}
    # These files are the inputs so we can create an output based on them
    files = ['ManufacturerList.csv', 'PriceList.csv', 'ServiceDatesList.csv']
    for file in files:
        with open(file, 'r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for line in csv_reader:
                item_id = line[0]
                if file == files[0]:
                    items[item_id] = {}
                    manufacturer = line[1]
                    item_type = line[2]
                    damaged = line[3]
                    items[item_id]['manufacturer'] = manufacturer.strip()
                    items[item_id]['item_type'] = item_type.strip()
                    items[item_id]['damaged'] = damaged
                elif file == files[1]:
                    price = line[1]
                    items[item_id]['price'] = price
                elif file == files[2]:
                    service_date = line[1]
                    items[item_id]['service_date'] = service_date
#PART 2
# Get info for manufacturers and types from csv
types = []
manufacturers = []
for item in items:
    checked_manufacturer = items[item]['manufacturer']
    checked_type = items[item]['item_type']
    if checked_manufacturer not in types:
        manufacturers.append(checked_manufacturer)
    if checked_type not in types:
        types.append(checked_type)

# Getting input
user_input = None
while user_input != 'q':
    user_input = input("\nEnter an item manufacturer and item type or enter 'q' to quit:\n")
    if user_input == 'q': # This is for when the user wants to quit by typing q
        break
    else:
        # Making sure the input is right and will match
        input_manufacturer = None
        input_type = None
        user_input = user_input.split()
        invalid_input = False
        for word in user_input:
            if word in manufacturers:
                if input_manufacturer:
                    invalid_input = True # Making sure that only 1 manufacturer was in the input
                else:
                    input_manufacturer = word
            elif word in types:
                if input_type:
                    invalid_input = True # Making sure that only 1 type was in the input
                else:
                    input_type = word
        if not input_manufacturer or not input_type or invalid_input:
            print("No such item in inventory") # Output for when the input is invalid or item not found
        else:
            # Making a list for highest to lowest
            keys = sorted(items.keys(), key=lambda x: items[x]['price'], reverse=True)
            # Making a list for matches found
            matching_items = []
            # This is for the  “You may, also, consider:” for similar items
            similar_items = {}
            for item in keys:
                if items[item]['item_type'] == input_type:
                    # Items that are damaged or expired will not be put on the similar list
                    today = datetime.now().date()
                    service_date = items[item]['service_date']
                    service_expiration = datetime.strptime(service_date, "%m/%d/%Y").date()
                    expired = service_expiration < today
                    if items[item]['manufacturer'] == input_manufacturer:
                        if not expired and not items[item]['damaged']:
                            matching_items.append((item, items[item]))
                    else:
                        if not expired and not items[item]['damaged']:
                            similar_items[item] = items[item]

            # If a matched item is found the output will put out the id, manufacturer, item_type, price.
            if matching_items:
                item = matching_items[0]
                id = item[0]
                manufacturer = item[1]['manufacturer']
                item_type = item[1]['item_type']
                price = item[1]['price']
                print("Your item is: {}, {}, {}, {}\n".format(id, manufacturer, item_type, price))

                # This is the output for “You may, also, consider:” or similar items
                if similar_items:
                    matched_price = price
                    # This is for the price match or items close to the price
                    closest_item = None
                    closest_price_diff = None
                    for item in similar_items:
                        if closest_price_diff == None:
                            closest_item = similar_items[item]
                            closest_price_diff = abs(int(matched_price) - int(similar_items[item]['price']))
                            id = item
                            manufacturer = similar_items[item]['manufacturer']
                            item_type = similar_items[item]['item_type']
                            price = similar_items[item]['price']
                            continue
                        price_diff = abs(int(matched_price) - int(similar_items[item]['price']))
                        if price_diff < closest_price_diff:
                            closest_item = item
                            closest_price_diff = price_diff
                            id = item
                            manufacturer = similar_items[item]['manufacturer']
                            item_type = similar_items[item]['item_type']
                            price = similar_items[item]['price']
                    print("You may, also, consider: {}, {}, {}, {}\n".format(id, manufacturer, item_type, price))  # Output for the similar items

            else:
                print("No such item in inventory")
