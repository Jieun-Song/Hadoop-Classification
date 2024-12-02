import requests

def download_gist_file(gist_url, save_path):
    """
    GitHub Gist 파일을 다운로드하는 함수

    Parameters:
        gist_url (str): Gist Raw 파일 URL
        save_path (str): 파일을 저장할 경로 및 이름
    """
    try:
        response = requests.get(gist_url)
        response.raise_for_status()  # HTTP 에러 발생 시 예외 처리
        with open(save_path, 'wb') as file:
            file.write(response.content)
        print(f"파일이 성공적으로 다운로드되었습니다: {save_path}")
    except requests.exceptions.RequestException as e:
        print(f"파일 다운로드 중 오류 발생: {e}")

# Gist의 RAW 파일 URL
gist_raw_url = "https://gist.githubusercontent.com/Nine1ll/3ec361da95ccd39101051ab57f86cf46/raw/a1a451421097fa9a93179cb1f1f0dc392f1f9da9/stopwords.txt"
# 저장 경로 및 파일 이름
save_file_path = "stopwords.txt"
download_gist_file(gist_raw_url, save_file_path)