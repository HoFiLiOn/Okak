import random
from datetime import datetime

def get_price_change(old, new):
    """Получить изменение цены в процентах"""
    if old == 0:
        return "0.00%"
    return f"{((new - old) / old) * 100:+.2f}%"

def format_number(num):
    """Форматирование чисел (1000 -> 1,000)"""
    return f"{num:,.2f}".replace(",", " ")

def format_timestamp(timestamp):
    """Форматирование временной метки"""
    if not timestamp:
        return "никогда"
    
    try:
        dt = datetime.fromisoformat(timestamp.replace(' ', 'T'))
        now = datetime.now()
        delta = now - dt
        
        if delta.days > 30:
            return dt.strftime("%d.%m.%Y")
        elif delta.days > 0:
            return f"{delta.days} дн. назад"
        elif delta.seconds > 3600:
            return f"{delta.seconds // 3600} ч. назад"
        elif delta.seconds > 60:
            return f"{delta.seconds // 60} мин. назад"
        else:
            return "только что"
    except:
        return timestamp

def split_message(text, max_length=3500):
    """Разбить длинное сообщение на части"""
    if len(text) <= max_length:
        return [text]
    
    parts = []
    while text:
        if len(text) <= max_length:
            parts.append(text)
            break
        
        split_point = text.rfind('\n', 0, max_length)
        if split_point == -1:
            split_point = text.rfind(' ', 0, max_length)
        if split_point == -1:
            split_point = max_length
        
        parts.append(text[:split_point])
        text = text[split_point:].lstrip()
    
    return parts

def generate_chart(values, height=5):
    """Сгенерировать ASCII график"""
    if not values:
        return ""
    
    max_val = max(values)
    min_val = min(values)
    
    if max_val == min_val:
        return "⚖️ Стабильно"
    
    chart = []
    for i in range(height, 0, -1):
        level = min_val + (max_val - min_val) * (i / height)
        line = ""
        for val in values:
            if val >= level:
                line += "█"
            else:
                line += "░"
        chart.append(line)
    
    return "\n".join(chart)

def get_achievement_info(achievement_id):
    """Информация о достижении"""
    achievements = {
        'first_trade': {
            'name': 'Первая сделка',
            'description': 'Соверши свою первую сделку',
            'emoji': '🎯'
        },
        'trader_100': {
            'name': 'Трейдер',
            'description': 'Соверши 100 сделок',
            'emoji': '📊'
        },
        'capital_10k': {
            'name': 'Инвестор',
            'description': 'Накопи 10,000$',
            'emoji': '💰'
        },
        'capital_100k': {
            'name': 'Богач',
            'description': 'Накопи 100,000$',
            'emoji': '💎'
        },
        'millionaire': {
            'name': 'Миллионер',
            'description': 'Накопи 1,000,000$',
            'emoji': '👑'
        },
        'first_cube': {
            'name': 'Победитель',
            'description': 'Получи первый кубок',
            'emoji': '🏆'
        },
        'cubes_10': {
            'name': 'Легенда',
            'description': 'Собери 10 кубков',
            'emoji': '🏅'
        }
    }
    return achievements.get(achievement_id, {'name': 'Достижение', 'description': '', 'emoji': '🎖️'})