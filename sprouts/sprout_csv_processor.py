#!/usr/local/bin/python
# csv-reader.py: Example of CSV parsing in python
import csv
import json


# function to parse nutrients into desired format
def parse_nutrients(nutrient_list):
    nutrient_output_list = []
    nutrient_input_dict = {}
    for nutrient in nutrient_list:
        nutrient_input_dict[nutrient['label']] = nutrient

    for key in nutrient_input_dict:
        nutrient_label = key
        nutrient_details = nutrient_input_dict[key]
        # fat
        if nutrient_label == 'Total Fat':
            new_fat_nutrient = nutrient_details
            new_fat_nutrient['subcategories'] = []
            if 'Trans Fat' in nutrient_input_dict:
                new_fat_nutrient['subcategories'].append(nutrient_input_dict['Trans Fat'])
            if 'Saturated Fat' in nutrient_input_dict:
                new_fat_nutrient['subcategories'].append(nutrient_input_dict['Saturated Fat'])
            nutrient_output_list.append(new_fat_nutrient)
            continue

        # sugar
        if nutrient_label == 'Total Carbohydrate':
            new_carbohydrate_nutrient = nutrient_details
            new_carbohydrate_nutrient['subcategories'] = []
            if 'Dietary Fiber' in nutrient_input_dict:
                new_carbohydrate_nutrient['subcategories'].append(nutrient_input_dict['Dietary Fiber'])
            if 'Total Sugars' in nutrient_input_dict:
                new_total_sugar = nutrient_input_dict['Total Sugars']
                new_total_sugar['subcategories'] = []
                if 'Includes Added Sugars' in nutrient_input_dict:
                    new_total_sugar['subcategories'].append(nutrient_input_dict['Includes Added Sugars'])
                new_carbohydrate_nutrient['subcategories'].append(new_total_sugar)
            nutrient_output_list.append(new_carbohydrate_nutrient)
            continue

        if nutrient_label in ['Trans Fat', 'Saturated Fat', 'Dietary Fiber', 'Total Sugars', 'Includes Added Sugars']:
            continue

        nutrient_output_list.append(nutrient_details)

    return nutrient_output_list


# update the filename here to specify which file to process
input_file_name = 'sprouts-full.csv'
with open(input_file_name, 'r') as inputCsvfile:
    reader = csv.DictReader(inputCsvfile)
    output_rows = []
    for row in reader:
        # parse 'ingredients', 'allergen_info', 'dietary_flags', 'disclaimer' information
        key_list = ['ingredients', 'allergen_info', 'dietary_flags', 'disclaimer']
        detail_list = [{'body': row[key], 'header': key} for key in key_list
                       if key in row and row[key] != '']

        static_disclaimer_string = "Product details and images are for convenience only and may not be current, " \
                                   "accurate, or complete. Consult the product label on physical product packaging " \
                                   "for the most current and accurate information, including nutrition information, " \
                                   "ingredients, claims, allergens, and warnings. We do not represent or warrant that " \
                                   "the nutrition, ingredient, claims, allergen, or other product information on our " \
                                   "website or mobile application are current, accurate, or complete. For additional " \
                                   "information, contact the manufacturer. "
        output_dict = {
            "details": detail_list,
            "disclaimer": static_disclaimer_string,
            "nutrients": None,
            "serving_size": None,
            "servings_per_container": None
        }

        nutritional_info = row['nutritional_info']
        if nutritional_info:
            nutritional_info_dict = json.loads(nutritional_info)
            serving_size = nutritional_info_dict['serving_size']
            servings_per_container = nutritional_info_dict['servings_per_container']
            nutrients = nutritional_info_dict['nutrients']
            output_dict['serving_size'] = serving_size
            output_dict['servings_per_container'] = servings_per_container
            output_dict['nutrients'] = parse_nutrients(nutrients)

        row['product_metadata'] = json.dumps(output_dict)
        output_rows.append(row)

    header = ['SKU',
              'UPC',
              'secondary_upc',
              'PLU',
              'L1_category',
              'L2_category',
              'L3_category',
              'private_label_flag',
              'brand_name',
              'consumer_facing_item_name', 'size',
              'unit_of_measure',
              'average_weight_per_each',
              'average_weight_uom',
              'image_url',
              'additional_image_urls',
              'ingredients',
              'allergen_info',
              'dietary_flags',
              'is_weighted_item',
              'is_alcohol',
              'disclaimer',
              'nutritional_info',
              'short_description',
              'product_metadata']
    filename = "sprouts_output.csv"

    with open(filename, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=header)
        writer.writeheader()
        writer.writerows(output_rows)
