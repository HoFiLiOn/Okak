# ========== НАСТРОЙКИ ==========

# Токен тестового бота (вставь свой)
TOKEN = "8795547713:AAF9AxpaZDhsZS6XTIDn6QveKOvC1F5E2YY"

# ID администраторов
ADMINS = [8388843828, 7040677455]  # Добавь свои ID

# Путь к базе данных
DB_PATH = "data/terminal_trade.db"

# Версия бота
VERSION = "2.0"

# Картинки
IMAGES = {
    'main': 'https://s10.iimage.su/s/05/gIKluIYxLgUpL28XWRh1IzTmdY4DzqMQuX8v39ee9.jpg',
    'companies': 'https://s10.iimage.su/s/05/gf3a1gxxMZn6ArfLKZD3JlzVhy83Bm1cGvNVjC0vI.jpg',
    'stats': 'https://s10.iimage.su/s/05/gioJHlUxz7G3Udtvbpc4t3CAoCSsryhLnSFXWdayc.jpg',
    'inventory': 'https://s10.iimage.su/s/05/grMXdR3xwFaLXdQ74TR9rz7zu8Wb60ezeX89JKuzm.jpg',
    'shop': 'https://s10.iimage.su/s/05/gbuaUsrxIjSjwQcGwcZrUaNcbFXzpITC2qFzhFzrd.jpg',
    'leaderboard': 'https://s10.iimage.su/s/05/gYoBW3cxowvFLbKdb8GJCDKWoEAcQD5DJa0zHCQt6.jpg'
}

# Товары магазина
SHOP_ITEMS = {
    'booster': {
        'name': 'Ускоритель',
        'description': '🚀 Цены будут расти на 50% быстрее 1 день',
        'price': 500,
        'emoji': '🚀',
        'category': 'consumable',
        'effect': 'booster'
    },
    'shield': {
        'name': 'Страховка',
        'description': '🛡️ Защита от 1 убытка',
        'price': 300,
        'emoji': '🛡️',
        'category': 'consumable',
        'effect': 'shield'
    },
    'analyst': {
        'name': 'Аналитик',
        'description': '📊 Прогноз цен на завтра',
        'price': 200,
        'emoji': '📊',
        'category': 'consumable',
        'effect': 'analyst'
    },
    'random': {
        'name': 'Рандом',
        'description': '🎲 Случайный бонус от $50 до $500',
        'price': 100,
        'emoji': '🎲',
        'category': 'consumable',
        'effect': 'random'
    },
    'vip_month': {
        'name': 'VIP на месяц',
        'description': '💎 30 дней: +10% к доходу',
        'price': 5000,
        'emoji': '💎',
        'category': 'subscription',
        'duration': 30,
        'effect': 'vip'
    },
    'trader_month': {
        'name': 'Трейдер PRO',
        'description': '📈 30 дней: +15% к доходу',
        'price': 8000,
        'emoji': '📈',
        'category': 'subscription',
        'duration': 30,
        'effect': 'trader'
    },
    'investor_month': {
        'name': 'Инвестор',
        'description': '💰 30 дней: +20% к доходу',
        'price': 12000,
        'emoji': '💰',
        'category': 'subscription',
        'duration': 30,
        'effect': 'investor'
    },
    'lucky_box': {
        'name': 'Лаки бокс',
        'description': '🎁 Случайный предмет или деньги',
        'price': 300,
        'emoji': '🎁',
        'category': 'special',
        'effect': 'lucky_box'
    }
}

# Текст предыстории
STORY = (
    "📜 *Небольшая предыстория...*\n\n"
    "Ты обычный человек, который однажды утром открыл Telegram и наткнулся на странного бота.\n"
    "В описании было сказано: _«Хочешь стать миллионером? Начни прямо сейчас и покори биржу!»_.\n\n"
    "Сначала ты подумал, что это очередной развод, но любопытство взяло верх.\n"
    "Ты запустил бота и... оказался в мире, где каждое твоё решение может принести состояние или оставить с пустым кошельком.\n\n"
    "Теперь ты трейдер. И от твоих решений зависит, войдёшь ли ты в историю как легенда или исчезнешь в бездне убытков.\n\n"
    "Добро пожаловать в *Terminal Trade*."
)