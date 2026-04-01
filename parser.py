def generate_html(events):
    html = '''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Афиша Dj Alex Blond</title>
    <style>
        body { background: transparent; font-family: Arial, sans-serif; margin: 0; padding: 0; }
        .afisha { background: #020306; border-radius: 16px; padding: 16px; color: #fff; box-shadow: 0 4px 12px rgba(0,0,0,0.3); }
        .afisha h3 { margin: 0 0 12px; font-size: 18px; font-weight: normal; display: flex; align-items: center; gap: 8px; }
        .afisha h3 span:first-child { font-size: 22px; }
        .event { margin-bottom: 20px; border-bottom: 1px solid #2a2a2a; padding-bottom: 12px; }
        .event:last-child { border-bottom: none; margin-bottom: 0; padding-bottom: 0; }
        .event-title { font-weight: bold; margin-bottom: 4px; font-size: 16px; }
        .event-title a { color: #E8E8E8; text-decoration: none; transition: color 0.2s; }
        .event-title a:hover { color: #6EB4D2; }
        .event-date { font-size: 12px; color: #B8B3B3; margin-bottom: 4px; }
        .event-place { font-size: 12px; color: #B8B3B3; }
        .event-genres { font-size: 11px; color: #6EB4D2; margin-top: 2px; opacity: 0.8; }
    </style>
</head>
<body>
<div class="afisha">
    <h3>
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
