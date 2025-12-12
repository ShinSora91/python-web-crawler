# productInfo.py (간단한 버전)

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from typing import Tuple, Optional


# def get_product_basic_info(driver: WebDriver) -> Tuple[Optional[str], Optional[str], Optional[str]]:
#     """
#     상품 상세페이지에서 카테고리, 브랜드, 상품명 정보만 추출합니다.
#
#     Args:
#         driver: Selenium WebDriver 객체
#
#     Returns:
#         tuple: (카테고리, 브랜드, 상품명)
#                정보를 찾지 못한 경우 해당 항목은 None 반환
#     """
#     category = None
#     brand = None
#     product_name = None
#
#     try:
#         # 1. 카테고리 정보 추출
#         try:
#             category_element = driver.find_element(By.XPATH, '//*[@id="main"]/div[1]/div/a[3]')
#             category = category_element.text.strip()
#         except NoSuchElementException:
#             print("카테고리 요소를 찾을 수 없습니다.")
#
#         # 2. 브랜드 정보 추출
#         try:
#             brand_element = driver.find_element(By.XPATH, '//*[@id="main"]/div[2]/div/div[2]/div/div[1]/div[1]/a')
#             brand = brand_element.text.strip()
#         except NoSuchElementException:
#             print("브랜드 요소를 찾을 수 없습니다.")
#
#         # 3. 상품명 정보 추출
#         try:
#             product_name_element = driver.find_element(By.XPATH,
#                                                        '//*[@id="main"]/div[2]/div/div[2]/div/div[1]/div[2]/h3')
#             product_name = product_name_element.text.strip()
#         except NoSuchElementException:
#             print("상품명 요소를 찾을 수 없습니다.")
#
#         return category, brand, product_name
#
#     except Exception as e:
#         print(f"상품 정보 추출 중 오류 발생: {e}")
#         return None, None, None

from typing import Optional, Tuple
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

def get_product_basic_info(driver: WebDriver) -> Tuple[Optional[str], Optional[str], Optional[str]]:
    """
    상품 상세페이지에서 카테고리, 브랜드, 상품명 정보만 추출합니다.

    Returns:
        tuple: (카테고리, 브랜드, 상품명)
               정보를 찾지 못한 경우 해당 항목은 None 반환
    """
    category = None
    brand = None
    product_name = None

    try:
        # 1. 카테고리 정보 추출
        try:
            category_element = driver.find_element(By.XPATH, '//*[@id="main"]/div[1]/div/a[3]')
            text = category_element.text or category_element.get_attribute("textContent")
            category = text.strip() if text else None
        except NoSuchElementException:
            print("카테고리 요소를 찾을 수 없습니다. (XPath: //*[@id=\"main\"]/div[1]/div/a[3])")

        # 2. 브랜드 정보 추출 (우선 a 시도, 없으면 button 시도)
        # 첫번째 시도: a 요소
        try:
            brand_element = driver.find_element(By.XPATH,
                                                '//*[@id="main"]/div[2]/div/div[2]/div/div[1]/div[1]/a')
            text = brand_element.text or brand_element.get_attribute("textContent")
            brand = text.strip() if text else None
            if brand:
                print(f"브랜드 요소 발견 (a): raw={repr(text)}")
        except NoSuchElementException:
            print("브랜드(a) 요소를 찾을 수 없습니다. 다음으로 button을 시도합니다.")

        # 두번째 시도: button 요소 (앞에서 brand가 None일 때만)
        if not brand:
            try:
                brand_btn_element = driver.find_element(By.XPATH,
                                                        '//*[@id="main"]/div[2]/div/div[2]/div/div[1]/div[1]/button')
                text = brand_btn_element.text or brand_btn_element.get_attribute("textContent")
                brand = text.strip() if text else None
                if brand:
                    print(f"브랜드 요소 발견 (button): raw={repr(text)}")
                else:
                    print("브랜드 요소는 찾았으나 텍스트가 비어있습니다. (button)")
            except NoSuchElementException:
                print("브랜드(button) 요소도 찾을 수 없습니다.")

        # 3. 상품명 정보 추출
        try:
            product_name_element = driver.find_element(By.XPATH,
                                                       '//*[@id="main"]/div[2]/div/div[2]/div/div[1]/div[2]/h3')
            text = product_name_element.text or product_name_element.get_attribute("textContent")
            product_name = text.strip() if text else None
        except NoSuchElementException:
            print("상품명 요소를 찾을 수 없습니다. (XPath: //*[@id=\"main\"]/div[2]/div/div[2]/div/div[1]/div[2]/h3)")

        return category, brand, product_name

    except Exception as e:
        print(f"상품 정보 추출 중 오류 발생: {e}")
        return None, None, None



def print_product_info(category: str, brand: str, product_name: str):
    """
    상품 정보를 콘솔에 출력합니다.

    Args:
        category: 카테고리
        brand: 브랜드
        product_name: 상품명
    """
    print("\n" + "=" * 50)
    print("상품 기본 정보")
    print("=" * 50)
    print(f"카테고리: {category if category else '정보 없음'}")
    print(f"브랜드: {brand if brand else '정보 없음'}")
    print(f"상품명: {product_name if product_name else '정보 없음'}")
    print("=" * 50)


def save_product_info(category: str, brand: str, product_name: str, filename: str = "product_info.txt"):
    """
    상품 정보를 파일에 저장합니다.

    Args:
        category: 카테고리
        brand: 브랜드
        product_name: 상품명
        filename: 저장할 파일명
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"카테고리: {category if category else '정보 없음'}\n")
            f.write(f"브랜드: {brand if brand else '정보 없음'}\n")
            f.write(f"상품명: {product_name if product_name else '정보 없음'}\n")

        print(f"\n상품 정보가 '{filename}'에 저장되었습니다.")

    except Exception as e:
        print(f"파일 저장 중 오류: {e}")


# 테스트용 코드
if __name__ == "__main__":
    # 테스트를 위한 임포트
    import undetected_chromedriver as uc
    import time

    # 테스트 드라이버 설정
    options = uc.ChromeOptions()
    options.add_argument("--start-maximized")

    driver = uc.Chrome(options=options, use_subprocess=False)

    try:
        # 테스트 페이지
        test_url = "https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo=A000000233879"
        print(f"테스트 페이지 접속: {test_url}")
        driver.get(test_url)
        time.sleep(5)

        # 상품 정보 추출
        category, brand, product_name = get_product_basic_info(driver)

        # 정보 출력
        print_product_info(category, brand, product_name)

        # 파일 저장
        save_product_info(category, brand, product_name, "test_product_info.txt")

    except Exception as e:
        print(f"테스트 중 오류: {e}")

    finally:
        driver.quit()