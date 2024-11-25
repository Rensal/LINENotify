import requests
import re

from bs4 import BeautifulSoup
from datetime import datetime

# サイトから情報を取得する関数
def get_site_info(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'
    }
    response = requests.get(url, headers=headers) # headersユーザーエージェントをブラウザと同じように設定

    soup = BeautifulSoup(response.text, 'html.parser')

    # 該当する要素を取得
    price_element = soup.find('li', class_='sub-pro-jia').find('span')

    # テキストを取得して出力
    if price_element:
        price = price_element.get_text(strip=True)

        return price 
    else:
        print("該当する要素が見つかりませんでした。")

# LINEにメッセージを送る関数
def send_line_message(message):

    # 取得したトークン
    line_notify_token = 'XXXXXXXXXXXXXXXXXXXXXXXXXXX'  # グループ用
    line_notify_api = 'https://notify-api.line.me/api/notify'
    headers = {'Authorization': f'Bearer {line_notify_token}'}
    data = {'message': message}
    
    # LINEにメッセージを送信
    requests.post(line_notify_api, headers=headers, data=data)

# スクリプト実行
# if __name__ == "__main__": # ローカル実行用
def lambda_handler(event, context): # AWS実行用

     # 情報を取得したいサイトのURL
    pro_url = 'https://gamekaitori.jp/search?type=&q=4549995532562#searchtop'  # iphone16 pro 128
    promax256_url = 'https://gamekaitori.jp/search?type=&q=4549995536447#searchtop' # iphone16 pro max 256
    promax512_url = 'https://gamekaitori.jp/search?type=&q=4549995536485#searchtop' # iphone16 pro max 512
 

    # サイトから情報を取得
    pro = get_site_info(pro_url) # iphone16 pro
    promax256 = get_site_info(promax256_url) # iphone16 pro max 256GB
    promax512 = get_site_info(promax512_url) # iphone16 pro max 512GB

    # 定価
    teikaPro = 159800 # iphone16 pro
    teikaProMax256 = 189800 # iphone16 pro max 256
    teikaProMax512 = 219800 # iphone16 pro max 512

    # 数字以外の文字を取り除き、int型に変換
    price_number_pro = int(re.sub(r'[^\d]', '', pro))
    price_number_promax256 = int(re.sub(r'[^\d]', '', promax256))
    price_number_promax512 = int(re.sub(r'[^\d]', '', promax512))

    difference_pro = format(price_number_pro - teikaPro,',')
    difference_promax256 = format(price_number_promax256 - teikaProMax256,',')
    difference_promax512 = format(price_number_promax512 - teikaProMax512,',')

    # 区切り線
    separator_line = f'\n----------------------------------------------'

    # メッセージの作成
    message_pro = f'\n{datetime.now().strftime("%Y/%m/%d")}{separator_line}\n・iPhone 16 Pro 128GB\n買取：{pro}\n定価：{format(teikaPro,',')}円\n利益：{difference_pro}円{separator_line}'
    message_promax256 = f'\n・iPhone 16 Pro Max 256GB\n買取：{promax256}\n定価：{format(teikaProMax256,',')}円\n利益：{difference_promax256}円{separator_line}'
    message_promax512 = f'\n・iPhone 16 Pro Max 512GB\n買取：{promax512}\n定価：{format(teikaProMax512,',')}円\n利益：{difference_promax512}円{separator_line}'

    print(f"{message_pro}{message_promax256}{message_promax512}")
    # 取得した情報をLINEに送信
    send_line_message(f"{message_pro}{message_promax256}{message_promax512}")
