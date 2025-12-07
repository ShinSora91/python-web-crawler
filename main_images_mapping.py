import os

# SQL 파일 경로
SQL_FILE_PATH = "product_main_images_sql.txt"


def create_initial_product_main_images_sql():
    """
    초기 product_main_images_sql.txt 파일을 생성합니다.
    파일이 이미 존재하면 아무 작업도 하지 않습니다.
    """
    try:
        with open(SQL_FILE_PATH, 'r', encoding='utf-8') as f:
            content = f.read()
            if not content.strip():  # 빈 파일인 경우
                initial_sql = "INSERT INTO product_main_images (product_id, image_type, display_order, image_url) VALUES"
                with open(SQL_FILE_PATH, 'w', encoding='utf-8') as f_write:
                    f_write.write(initial_sql)
    except FileNotFoundError:
        # 파일이 없을 경우 생성
        initial_sql = "INSERT INTO product_main_images (product_id, image_type, display_order, image_url) VALUES"
        with open(SQL_FILE_PATH, 'w', encoding='utf-8') as f:
            f.write(initial_sql)


def update_product_main_images_sql(product_id, main_image_urls):
    """
    product_main_images_sql.txt 파일에 제품 이미지 INSERT 문을 추가합니다.

    Args:
        product_id (int): 제품 ID
        main_image_urls (list): 이미지 URL 배열

    Returns:
        list: 생성된 INSERT 문 리스트
    """
    if not main_image_urls or len(main_image_urls) == 0:
        return []

    # SQL 파일 읽기
    try:
        with open(SQL_FILE_PATH, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        # 파일이 없을 경우 초기 내용 생성
        content = "INSERT INTO product_main_images (product_id, image_type, display_order, image_url) VALUES"

    # 내용 정리
    content = content.strip()

    # 마지막 세미콜론 제거
    if content.endswith(';'):
        content = content[:-1].rstrip()

    # INSERT 문 생성
    insert_statements = []

    for idx, image_url in enumerate(main_image_urls):
        display_order = idx
        image_type = 'THUMBNAIL' if display_order == 0 else 'GALLERY'

        insert_statement = f"({product_id}, '{image_type}', {display_order}, '{image_url}')"
        insert_statements.append(insert_statement)

    # VALUES로 끝나는지 확인 (첫 데이터 추가)
    if content.endswith('VALUES'):
        # 첫 데이터이므로 줄바꿈 후 추가
        new_content = content
        for i, stmt in enumerate(insert_statements):
            if i == 0:
                new_content += f"\n{stmt}"
            else:
                new_content += f",\n{stmt}"
        new_content += ";"
    else:
        # 기존 데이터가 있으므로 콤마 추가 후 새 데이터 추가
        new_content = content
        for stmt in insert_statements:
            new_content += f",\n{stmt}"
        new_content += ";"

    # SQL 파일 저장
    with open(SQL_FILE_PATH, 'w', encoding='utf-8') as f:
        f.write(new_content)

    return insert_statements


# 모듈 임포트 시 초기 SQL 파일 생성
create_initial_product_main_images_sql()


# 테스트 함수
def test_main_images_sql():
    """메인 이미지 SQL 업데이트 기능 테스트"""

    print("=== 제품 메인 이미지 SQL 테스트 ===\n")

    # 테스트 데이터 1
    product_id_1 = 1
    images_1 = [
        'https://image.oliveyoung.co.kr/cfimages/cf-goods/uploads/images/thumbnails/10/0000/0018/A00000018491610ko.jpg?l=ko&QT=85&SF=webp&sharpen=1x0.5',
        'https://image.oliveyoung.co.kr/cfimages/cf-goods/uploads/images/thumbnails/10/0000/0018/A00000018491607ko.jpg?l=ko&QT=85&SF=webp&sharpen=1x0.5',
        'https://image.oliveyoung.co.kr/cfimages/cf-goods/uploads/images/thumbnails/10/0000/0018/A00000018491608ko.jpg?l=ko&QT=85&SF=webp&sharpen=1x0.5'
    ]

    print(f"제품 ID {product_id_1}의 이미지 추가 중...")
    result_1 = update_product_main_images_sql(product_id_1, images_1)
    print(f"추가된 INSERT 문 개수: {len(result_1)}\n")

    # 테스트 데이터 2
    product_id_2 = 2
    images_2 = [
        'https://image.oliveyoung.co.kr/cfimages/cf-goods/uploads/images/thumbnails/10/0000/0023/A00000023272408ko.jpg?l=ko&QT=85&SF=webp&sharpen=1x0.5',
        'https://image.oliveyoung.co.kr/cfimages/cf-goods/uploads/images/thumbnails/10/0000/0023/A00000023272409ko.jpg?l=ko&QT=85&SF=webp&sharpen=1x0.5'
    ]

    print(f"제품 ID {product_id_2}의 이미지 추가 중...")
    result_2 = update_product_main_images_sql(product_id_2, images_2)
    print(f"추가된 INSERT 문 개수: {len(result_2)}\n")

    # 결과 파일 확인
    print("=== 생성된 SQL 파일 내용 ===")
    try:
        with open(SQL_FILE_PATH, 'r', encoding='utf-8') as f:
            content = f.read()
        print(content)
    except FileNotFoundError:
        print("SQL 파일을 찾을 수 없습니다.")

    print("\n=== 테스트 완료 ===")


# 테스트 코드
if __name__ == "__main__":
    # 초기 SQL 파일 생성 확인
    create_initial_product_main_images_sql()

    # 테스트 실행
    test_main_images_sql()