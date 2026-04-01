import requests
from bs4 import BeautifulSoup
import sys

URL = "https://dj.ru/djalexblond/afisha"
HEADERS = {"User-Agent": "Mozilla/5.0"}

def fetch_event_data():
    try:
        resp = requests.get(URL, headers=HEADERS, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, 'html.parser')
        first_event = soup.select_one('li.poster__i')
        if not first_event:
            print("Не найдено событий", file=sys.stderr)
            return None

        img_tag = first_event.select_one('img.poster__img')
        img_url = img_tag.get('src') if img_tag else None
        if img_url and img_url.startswith('/'):
            img_url = 'https://dj.ru' + img_url

        title_tag = first_event.select_one('h3.poster__h a')
        title = title_tag.get_text(strip=True) if title_tag else ''

        dj_tag = first_event.select_one('.poster__info-i_type_dj a')
        dj = dj_tag.get_text(strip=True) if dj_tag else ''

        genre_tags = first_event.select('.poster__info-i_type_genre a')
        genres = ', '.join([g.get_text(strip=True) for g in genre_tags])

        place_tag = first_event.select_one('.poster__info-i_type_map')
        if place_tag:
            place = place_tag.get_text(' ', strip=True)
            place = ' '.join(place.split())
        else:
            place = ''

        return {
            'img': img_url,
            'title': title,
            'dj': dj,
            'genres': genres,
            'place': place
        }
    except Exception as e:
        print(f"Ошибка загрузки: {e}", file=sys.stderr)
        return None

def generate_html(data):
    html = '''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Афиша Dj Alex Blond</title>
    <style>
        @font-face {
            font-family: 'Bebas Neue Cyrillic';
            src: url('BebasNeueCyrillic.ttf') format('truetype');
            font-weight: normal;
            font-style: normal;
            font-display: swap;
        }
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
            max-width: 500px;
            width: 100%;
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
            width: 100%;
            max-width: 224px;   /* уменьшено на 20% (было 280px) */
            height: auto;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
            display: block;
            margin: 0 auto 20px auto;
        }
        .event-title {
            font-family: 'Bebas Neue Cyrillic', 'Arial', sans-serif;
            font-size: 24px;
            font-weight: bold;
            color: #fff;
            margin: 0 0 8px 0;
        }
        .event-dj {
            font-size: 18px;
            color: #ccc;
            margin: 0 0 8px 0;
        }
        .event-genres {
            font-size: 14px;
            color: #64A8FF;
            margin: 0 0 12px 0;
        }
        .event-place {
            font-size: 14px;
            color: #aaa;
            margin: 0;
        }
    </style>
</head>
<body>
<div class="afisha">
    <h3>Афиша выступлений</h3>
'''
    if data and data['img']:
        html += f'    <img class="banner-img" src="{data["img"]}" alt="Афиша">\n'
    else:
        html += '    <p>Баннер не загружен</p>\n'
    
    if data:
        html += f'''
    <div class="event-title">{data['title']}</div>
    <div class="event-dj">{data['dj']}</div>
    <div class="event-genres">{data['genres']}</div>
    <div class="event-place">{data['place']}</div>
'''
    else:
        html += '    <p>Нет данных о событии</p>\n'
    
    html += '''
</div>
</body>
</html>'''
    return html

def main():
    data = fetch_event_data()
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(generate_html(data))

if __name__ == "__main__":
    main()
