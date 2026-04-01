import requests
from bs4 import BeautifulSoup
import sys

URL = "https://dj.ru/djalexblond/afisha"
HEADERS = {"User-Agent": "Mozilla/5.0"}

def fetch_events():
    try:
        resp = requests.get(URL, headers=HEADERS, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, 'html.parser')
        
        # Ищем баннер (top-decoration)
        banner = ''
        top_dec = soup.select_one('.top-decoration')
        if top_dec and top_dec.get('style'):
            style = top_dec.get('style')
            import re
            match = re.search(r'background-image:\s*url\([\'"]?(.*?)[\'"]?\)', style)
            if match:
                banner = match.group(1)
                if banner and not banner.startswith('http'):
                    banner = 'https://dj.ru' + banner
        
        events = []
        items = soup.select('li.poster__i')
        print(f"Найдено {len(items)} событий", file=sys.stderr)
        for item in items[:5]:
            title_tag = item.select_one('h3.poster__h a')
            if not title_tag:
                continue
            title = title_tag.get_text(strip=True)
            link = title_tag.get('href')
            if link and not link.startswith('http'):
                link = 'https://dj.ru' + link

            date_block = item.select_one('.poster__date')
            date_text = date_block.get_text(' ', strip=True) if date_block else ''

            place_tag = item.select_one('.poster__info-i_type_map')
            place = place_tag.get_text(' ', strip=True) if place_tag else ''

            genre_tags = item.select('.poster__info-i_type_genre a')
            genres = ', '.join([g.get_text(strip=True) for g in genre_tags])

            events.append({
                'title': title,
                'link': link,
                'date': date_text,
                'place': place,
                'genres': genres,
            })
        return events, banner
    except Exception as e:
        print(f"Ошибка парсинга: {e}", file=sys.stderr)
        return [], ''

def generate_html(events, banner):
    html = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Афиша Dj Alex Blond</title>
    <style>
        body {{ background: transparent; font-family: Arial, sans-serif; margin: 0; padding: 0; }}
        .afisha {{ background: #020306; border-radius: 16px; padding: 16px; color: #fff; box-shadow: 0 4px 12px rgba(0,0,0,0.3); }}
        .banner {{ width: 100%; border-radius: 12px; margin-bottom: 16px; overflow: hidden; }}
        .banner img {{ width: 100%; height: auto; display: block; }}
        .afisha h3 {{ margin: 0 0 12px; font-size: 18px; font-weight: normal; display: flex; align-items: center; gap: 8px; }}
        .afisha h3 span:first-child {{ font-size: 22px; }}
        .event {{ margin-bottom: 20px; border-bottom: 1px solid #2a2a2a; padding-bottom: 12px; }}
        .event:last-child {{ border-bottom: none; margin-bottom: 0; padding-bottom: 0; }}
        .event-title {{ font-weight: bold; margin-bottom: 4px; font-size: 16px; }}
        .event-title a {{ color: #E8E8E8; text-decoration: none; transition: color 0.2s; }}
        .event-title a:hover {{ color: #6EB4D2; }}
        .event-date {{ font-size: 12px; color: #B8B3B3; margin-bottom: 4px; }}
        .event-place {{ font-size: 12px; color: #B8B3B3; }}
        .event-genres {{ font-size: 11px; color: #6EB4D2; margin-top: 2px; opacity: 0.8; }}
    </style>
</head>
<body>
<div class="afisha">
'''
    if banner:
        html += f'''    <div class="banner">
        <img src="{banner}" alt="Афиша">
    </div>
'''
    else:
        html += '''    <h3>
        <span>📅</span>
        <span>Афиша выступлений</span>
    </h3>
'''
    if not events:
        html += '<p>Нет мероприятий.</p>'
    else:
        for e in events:
            html += f'''
    <div class="event">
        <div class="event-title"><a href="{e['link']}" target="_blank">{e['title']}</a></div>
        <div class="event-date">{e['date']}</div>
        <div class="event-place">{e['place']}</div>
        <div class="event-genres">{e['genres']}</div>
    </div>
'''
    html += '''
</div>
</body>
</html>'''
    return html

def main():
    events, banner = fetch_events()
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(generate_html(events, banner))

if __name__ == "__main__":
    main()
