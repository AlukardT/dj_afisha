import requests
from bs4 import BeautifulSoup
import sys

URL = "https://dj.ru/djalexblond/afisha"
HEADERS = {"User-Agent": "Mozilla/5.0"}

def fetch_first_event_image():
    try:
        resp = requests.get(URL, headers=HEADERS, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, 'html.parser')
        # Ищем первый элемент события
        first_event = soup.select_one('li.poster__i')
        if not first_event:
            print("Не найдено событий", file=sys.stderr)
            return None
        img_tag = first_event.select_one('img.poster__img')
        if img_tag and img_tag.get('src'):
            img_url = img_tag['src']
            # Если URL относительный, делаем абсолютным
            if img_url.startswith('/'):
                img_url = 'https://dj.ru' + img_url
            return img_url
        else:
            print("Изображение не найдено", file=sys.stderr)
            return None
    except Exception as e:
        print(f"Ошибка загрузки: {e}", file=sys.stderr)
        return None

def generate_html(img_url):
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
    if img_url:
        html += f'    <img class="banner-img" src="{img_url}" alt="Афиша">\n'
    else:
        html += '    <p>Изображение не найдено</p>\n'
    html += '''
</div>
</body>
</html>'''
    return html

def main():
    img_url = fetch_first_event_image()
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(generate_html(img_url))

if __name__ == "__main__":
    main()
