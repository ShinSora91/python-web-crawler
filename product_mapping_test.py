# 다른 파이썬 파일에서
from product_mapping import create_product_id, update_product_data_sql

# 새로운 제품 ID 생성
product_name = "새로운 제품"
product_id = create_product_id(product_name)

if product_id > 0:
    # SQL 파일 업데이트
    sql_statement = update_product_data_sql(
        product_id=product_id,
        product_detail_info_id=product_id,  # 예시: product_id와 동일하게 설정
        brand_id=1,
        category_id=1,
        product_name=product_name
    )
    print(f"제품이 성공적으로 추가되었습니다. ID: {product_id}")
else:
    print("이미 존재하는 제품명입니다.")