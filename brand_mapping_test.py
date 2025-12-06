from brand_mapping import get_brand_id, generate_sql_file


# brand_sql.txt 없을시 brand_data.json 을 참고하여 생성
# generate_sql_file()

test_brands = ['AHC']
for brand in test_brands:
    brand_id = get_brand_id(brand)
    print(f"  '{brand}' -> ID: {brand_id}")


