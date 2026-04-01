import requests
from bs4 import BeautifulSoup
import sys
import re

URL = "https://dj.ru/djalexblond/afisha"
HEADERS = {"User-Agent": "Mozilla/5.0"}

def fetch_banner():
    try:
        resp = requests.get(URL, headers=HEADERS, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, 'html.parser')
        # Ищем элемент с классом top-decoration и извлекаем background-image
        top_decoration = soup.select_one('.top-decoration')
        if top_decoration and top_decoration.get('style'):
            style = top_decoration.get('style')
            match = re.search(r'background-image:\s*url\([\'"]?(.*?)[\'"]?\)', style)
            if match:
                banner_url = match.group(1)
                if banner_url.startswith('/'):
                    banner_url = 'https://dj.ru' + banner_url
                return banner_url
        return None
    except Exception as e:
        print(f"Ошибка загрузки баннера: {e}", file=sys.stderr)
        return None

def generate_html(banner_url):
    html = '''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Афиша Dj Alex Blond</title>
    <style>
        body {
            background: transparent;
            font-family: 'Bebas Neue Cyrillic', 'Arial', sans-serif;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }
        .afisha {
            max-width: 100%;
            text-align: center;
            padding: 16px;
            box-sizing: border-box;
        }
        .afisha h3 {
            font-family: 'Bebas Neue Cyrillic', 'Arial', sans-serif;
            font-size: 28px;
            color: #64A8FF;
            margin: 0 0 20px 0;
            font-weight: normal;
            letter-spacing: 1px;
        }
        .banner-img {
            max-width: 100%;
            height: auto;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
            display: block;
            margin: 0 auto;
        }
    </style>
</head>
<body>
<div class="afisha">
    <h3>Афиша выступлений</h3>
'''
    if banner_url:
        html += f'    <img class="banner-img" src="{banner_url}" alt="Афиша">\n'
    else:
        html += '    <p>Баннер не загружен</p>\n'
    html += '''
</div>
</body>
</html>'''
    return html

def main():
    banner_url = fetch_banner()
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(generate_html(banner_url))

if __name__ == "__main__":
    main()
