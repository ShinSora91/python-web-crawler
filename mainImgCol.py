# mainImgCol.py (수정 버전 - swiper-slide-active 클래스 사용)

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from typing import List
import re


def clean_image_url(url: str) -> str:
    """
    이미지 URL에서 불필요한 쿼리 파라미터를 제거합니다.
    """
    if not url:
        return url

    # &QT, &SF, &sharpen 등의 파라미터 제거
    cleaned = re.sub(r'&(QT|SF|sharpen)=[^&]*', '', url)
    return cleaned


def get_active_image_element(driver: WebDriver):
    """
    현재 활성화된 슬라이드의 이미지 요소를 찾습니다.
    """
    try:
        # 방법 1: swiper-slide-active 클래스를 가진 슬라이드에서 이미지 찾기
        active_slide = driver.find_element(By.CSS_SELECTOR, '.swiper-slide-active')
        image_element = active_slide.find_element(By.TAG_NAME, 'img')
        return image_element
    except NoSuchElementException:
        # 방법 2: GoodsDetailCarousel_content__GTQMD 클래스에서 찾기
        try:
            image_element = driver.find_element(By.CSS_SELECTOR, '.GoodsDetailCarousel_content__GTQMD img')
            return image_element
        except NoSuchElementException:
            # 방법 3: visual-swiper 내부에서 찾기
            try:
                swiper = driver.find_element(By.CSS_SELECTOR, '.visual-swiper')
                image_element = swiper.find_element(By.CSS_SELECTOR, 'img[src*="cf-goods"]')
                return image_element
            except NoSuchElementException:
                # 방법 4: data-swiper-slide-index 속성으로 찾기 (인덱스 0)
                try:
                    slide_index_0 = driver.find_element(By.CSS_SELECTOR, '[data-swiper-slide-index="0"]')
                    image_element = slide_index_0.find_element(By.TAG_NAME, 'img')
                    return image_element
                except NoSuchElementException:
                    raise NoSuchElementException("활성 이미지 요소를 찾을 수 없습니다.")


def wait_for_image_change(driver: WebDriver, previous_src: str, timeout: int = 5):
    """
    이미지가 변경될 때까지 기다립니다.
    """
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            current_element = get_active_image_element(driver)
            current_src = current_element.get_attribute('src') or current_element.get_attribute('data-src')

            if current_src and current_src != previous_src:
                return True
        except:
            pass
        time.sleep(0.5)
    return False


def get_main_image_urls(driver: WebDriver, num_images: int = 3) -> List[str]:
    """
    현재 상세 페이지에서 메인 이미지 슬라이더의 이미지 URL을 지정된 개수만큼 수집합니다.
    swiper-slide-active 클래스를 사용하여 현재 보이는 이미지를 정확히 찾습니다.
    """
    image_urls = []  # 순서대로 URL 저장

    # 상세 페이지 로딩 대기
    print(f"이미지 URL 수집 시작... (목표: {num_images}개)")
    time.sleep(4)  # 페이지 로딩을 위한 충분한 대기

    # 먼저 첫 번째 이미지(인덱스 0)로 이동 시도
    try:
        print("첫 번째 이미지(인덱스 0)로 이동 시도...")
        # 왼쪽 버튼 여러 번 클릭하여 처음으로 이동
        prev_button = driver.find_element(By.CSS_SELECTOR, '.swiper-button-prev')
        for _ in range(10):  # 최대 10번 클릭
            try:
                driver.execute_script("arguments[0].click();", prev_button)
                time.sleep(0.5)

                # 현재 활성 슬라이드 인덱스 확인
                active_slide = driver.find_element(By.CSS_SELECTOR, '.swiper-slide-active')
                slide_index = active_slide.get_attribute('data-swiper-slide-index')
                if slide_index == '0':
                    print("첫 번째 이미지(인덱스 0)로 이동 성공")
                    break
            except:
                pass
    except Exception as e:
        print(f"첫 번째 이미지로 이동 실패 (계속 진행): {e}")

    for i in range(num_images):
        print(f"\n[{i + 1}/{num_images}] 이미지 수집 중...")

        try:
            # 1. 현재 활성화된 이미지 요소 찾기
            image_element = get_active_image_element(driver)

            # 현재 슬라이드 정보 출력
            try:
                active_slide = driver.find_element(By.CSS_SELECTOR, '.swiper-slide-active')
                slide_index = active_slide.get_attribute('data-swiper-slide-index')
                print(f"  현재 슬라이드 인덱스: {slide_index}")
            except:
                print("  슬라이드 인덱스 확인 불가")

            # 2. 이미지 URL 가져오기
            img_src = image_element.get_attribute('src')

            # src가 없는 경우 data-src 확인 (lazy loading)
            if not img_src:
                img_src = image_element.get_attribute('data-src')

            # alt 속성에서도 URL 가져오기 (백업)
            if not img_src:
                img_alt = image_element.get_attribute('alt')
                if img_alt and img_alt.startswith('http'):
                    img_src = img_alt

            # URL이 상대경로인 경우 절대경로로 변환
            if img_src and img_src.startswith('//'):
                img_src = 'https:' + img_src

            # 3. URL 정제 (쿼리 파라미터 제거)
            if img_src and (img_src.startswith('http') or img_src.startswith('https:')):
                cleaned_url = clean_image_url(img_src)
                image_urls.append(cleaned_url)
                print(f"  URL 추가: {cleaned_url[:80]}...")
            else:
                print(f"  이미지 URL을 찾을 수 없음")
                print(f"  img_src 값: {img_src}")
                # 빈 문자열 추가
                image_urls.append("")

            # 4. 페이지네이션 정보 출력
            try:
                current_page = driver.find_element(By.CSS_SELECTOR, '.swiper-pagination-current').text
                total_page = driver.find_element(By.CSS_SELECTOR, '.swiper-pagination-total').text
                print(f"  페이지: {current_page}/{total_page}")
            except:
                print("  페이지 정보 확인 불가")

            # 마지막 이미지가 아닌 경우에만 다음 이미지로 이동
            if i < num_images - 1:
                # 5. 다음 이미지 버튼 클릭
                try:
                    next_button = driver.find_element(By.CSS_SELECTOR, '.swiper-button-next')

                    # 현재 이미지 URL 저장 (변경 확인용)
                    previous_src = img_src

                    # JavaScript를 사용하여 강제 클릭
                    driver.execute_script("arguments[0].click();", next_button)
                    print("  다음 버튼 클릭")

                    # 이미지 변경 대기
                    if wait_for_image_change(driver, previous_src, 3):
                        print("  이미지 변경 확인됨")
                    else:
                        print("  이미지 변경되지 않음 (동일 이미지일 수 있음)")

                    # 추가 대기
                    time.sleep(1)

                except NoSuchElementException:
                    print("  다음 버튼을 찾을 수 없습니다.")
                    # 버튼이 없으면 키보드 이벤트로 대체
                    from selenium.webdriver.common.keys import Keys
                    body = driver.find_element(By.TAG_NAME, 'body')
                    body.send_keys(Keys.ARROW_RIGHT)
                    time.sleep(2)
                    print("  오른쪽 화살표 키 입력")

                except Exception as e:
                    print(f"  다음 버튼 클릭 중 오류: {e}")
                    break

        except NoSuchElementException as e:
            print(f"  이미지 요소를 찾을 수 없음: {e}")
            # 빈 문자열 추가
            image_urls.append("")
            time.sleep(1)

        except StaleElementReferenceException:
            # 요소가 새로고침되어 발생하는 오류
            print(f"  요소 참조 오류 발생. 재시도합니다.")

            # 잠시 대기 후 다시 시도
            time.sleep(1.5)

            try:
                image_element = get_active_image_element(driver)
                img_src = image_element.get_attribute('src') or image_element.get_attribute('data-src')

                if img_src and img_src.startswith('//'):
                    img_src = 'https:' + img_src

                if img_src and img_src.startswith('http'):
                    cleaned_url = clean_image_url(img_src)
                    image_urls.append(cleaned_url)
                    print(f"  재시도 성공: {cleaned_url[:80]}...")
                else:
                    image_urls.append("")

            except Exception as retry_e:
                print(f"  재시도 실패: {retry_e}")
                image_urls.append("")

            continue

        except Exception as e:
            # 다른 종류의 오류 발생
            print(f"  예상치 못한 에러 발생: {type(e).__name__}: {str(e)}")
            # 빈 문자열 추가
            image_urls.append("")
            time.sleep(1)

    print(f"\n총 {len(image_urls)}개의 이미지 URL 수집 완료.")

    # 수집된 URL 출력
    print("\n=== 수집 결과 ===")
    for idx, url in enumerate(image_urls, 1):
        if url:
            print(f"{idx}. {url}")
        else:
            print(f"{idx}. [URL 수집 실패]")

    return image_urls


def save_urls_to_file(urls: List[str], filename: str = "urls.txt"):
    """
    수집된 URL 리스트를 지정된 파일에 저장합니다.
    """
    if not urls:
        print("저장할 URL이 없습니다.")
        return

    try:
        with open(filename, 'w', encoding='utf-8') as f:
            for i, url in enumerate(urls, 1):
                if url:  # 빈 문자열이 아닌 경우만 저장
                    f.write(f"{i}. {url}\n")
                else:
                    f.write(f"{i}. [URL을 찾을 수 없음]\n")
        print(f"성공적으로 {len(urls)}개의 URL을 '{filename}'에 저장했습니다.")
    except Exception as e:
        print(f"파일 저장 중 에러 발생: {e}")


# 대안: 모든 이미지 URL을 한번에 가져오는 함수
def get_all_image_urls_at_once(driver: WebDriver) -> List[str]:
    """
    페이지의 모든 이미지 URL을 한번에 가져옵니다.
    """
    print("모든 이미지 URL 한번에 수집...")

    image_urls = []

    # 모든 슬라이드 찾기
    try:
        slides = driver.find_elements(By.CSS_SELECTOR, '.swiper-slide')
        print(f"총 {len(slides)}개의 슬라이드 발견")

        for idx, slide in enumerate(slides):
            try:
                # 각 슬라이드의 이미지 찾기
                img_element = slide.find_element(By.TAG_NAME, 'img')
                img_src = img_element.get_attribute('src') or img_element.get_attribute('data-src')

                if not img_src:
                    # alt 속성에서 URL 가져오기
                    img_alt = img_element.get_attribute('alt')
                    if img_alt and img_alt.startswith('http'):
                        img_src = img_alt

                if img_src:
                    if img_src.startswith('//'):
                        img_src = 'https:' + img_src

                    cleaned_url = clean_image_url(img_src)
                    image_urls.append(cleaned_url)

                    # 슬라이드 인덱스 정보
                    slide_index = slide.get_attribute('data-swiper-slide-index')
                    print(f"  슬라이드 {idx} (인덱스: {slide_index}): {cleaned_url[:60]}...")
                else:
                    print(f"  슬라이드 {idx}: 이미지 URL 없음")

            except Exception as e:
                print(f"  슬라이드 {idx} 처리 실패: {e}")

    except Exception as e:
        print(f"슬라이드 수집 실패: {e}")

    return image_urls


# 테스트용 코드
if __name__ == "__main__":
    import undetected_chromedriver as uc

    # 테스트 옵션
    options = uc.ChromeOptions()
    options.add_argument("--start-maximized")

    driver = uc.Chrome(options=options, use_subprocess=False)

    try:
        # 상품 페이지로 이동 (테스트 URL)
        test_url = "https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo=A000000238782"
        print(f"테스트 페이지 접속: {test_url}")
        driver.get(test_url)
        time.sleep(5)

        # 방법 1: 순차적으로 이미지 수집
        print("\n=== 방법 1: 순차적 수집 ===")
        urls1 = get_main_image_urls(driver, 3)

        print("\n=== 방법 2: 한번에 모든 이미지 수집 ===")
        urls2 = get_all_image_urls_at_once(driver)

        # 파일로 저장
        save_urls_to_file(urls1, "sequential_urls.txt")
        save_urls_to_file(urls2, "all_urls.txt")

        # 콘솔에도 최종 결과 출력
        print("\n=== 순차적 수집 결과 ===")
        for i, url in enumerate(urls1, 1):
            print(f"{i}. {url}")

        print("\n=== 전체 이미지 수집 결과 ===")
        for i, url in enumerate(urls2, 1):
            print(f"{i}. {url}")

    except Exception as e:
        print(f"테스트 중 오류: {e}")

    finally:
        driver.quit()