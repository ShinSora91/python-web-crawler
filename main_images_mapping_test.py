from main_images_mapping import update_product_main_images_sql

# 이미지 URL 배열
images = [
    'https://example.com/thumb.jpg',
    'https://example.com/gallery1.jpg',
    'https://example.com/gallery2.jpg'
]

# 함수 호출
update_product_main_images_sql(product_id=3, main_image_urls=images)