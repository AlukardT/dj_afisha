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
        return events
    except Exception as e:
        print(f"Ошибка парсинга: {e}", file=sys.stderr)
        return []

def generate_html(events):
    html = '''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Афиша Dj Alex Blond</title>
    <style>
        body { background: transparent; font-family: Arial, sans-serif; margin: 0; padding: 0; }
        .afisha { background: #0a0a0a; border-radius: 16px; padding: 16px; color: #fff; }
        .afisha h3 { margin: 0 0 12px; font-size: 18px; color: #6EB4D2; }
        .event { margin-bottom: 20px; border-bottom: 1px solid #2a2a2a; padding-bottom: 12px; }
        .event:last-child { border-bottom: none; }
        .event-title { font-weight: bold; margin-bottom: 4px; }
        .event-title a { color: #fff; text-decoration: none; }
        .event-title a:hover { color: #6EB4D2; }
        .event-date { font-size: 12px; color: #aaa; margin-bottom: 4px; }
        .event-place { font-size: 12px; color: #ccc; }
        .event-genres { font-size: 11px; color: #888; margin-top: 2px; }
    </style>
</head>
<body>
<div class="afisha">
    <h3>🎧 Ближайшие события</h3>
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
    events = fetch_events()
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(generate_html(events))

if __name__ == "__main__":
    main()
