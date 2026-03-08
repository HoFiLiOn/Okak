import sqlite3
import os
from datetime import datetime
from config import DB_PATH

def get_db():
    """Получить соединение с БД"""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_database():
    """Создание всех таблиц"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Пользователи
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            first_name TEXT,
            money REAL DEFAULT 1000.0,
            day INTEGER DEFAULT 1,
            cubes INTEGER DEFAULT 0,
            shields INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Портфель (акции)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS portfolio (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            ticker TEXT,
            amount INTEGER DEFAULT 0,
            buy_price REAL,
            bought_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(user_id),
            UNIQUE(user_id, ticker)
        )
    """)
    
    # Инвентарь (предметы)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            item_id TEXT,
            name TEXT,
            emoji TEXT,
            description TEXT,
            category TEXT,
            effect TEXT,
            acquired_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    """)
    
    # История кубков
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cubes_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            season_name TEXT,
            place INTEGER,
            earned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    """)
    
    # Достижения
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS achievements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            achievement_id TEXT,
            achieved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(user_id),
            UNIQUE(user_id, achievement_id)
        )
    """)
    
    # Активные эффекты
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS active_effects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            effect_type TEXT,
            expires_at TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    """)
    
    # Подписки
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS subscriptions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            sub_type TEXT,
            bonus INTEGER,
            expires_at TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    """)
    
    # Компании
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS companies (
            ticker TEXT PRIMARY KEY,
            name TEXT,
            price REAL,
            prev_price REAL
        )
    """)
    
    # История цен
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS price_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticker TEXT,
            price REAL,
            recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # История сделок
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            type TEXT,
            ticker TEXT,
            amount INTEGER,
            price REAL,
            total REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    """)
    
    # Промокоды
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS promocodes (
            code TEXT PRIMARY KEY,
            bonus INTEGER,
            max_uses INTEGER,
            used_count INTEGER DEFAULT 0,
            created_by INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Использованные промокоды
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS used_promos (
            user_id INTEGER,
            promo_code TEXT,
            used_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (user_id, promo_code),
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    """)
    
    # Сезон
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS season (
            id INTEGER PRIMARY KEY CHECK (id = 1),
            name TEXT,
            start_date TIMESTAMP,
            end_date TIMESTAMP,
            active BOOLEAN DEFAULT 1
        )
    """)
    
    # Логи админов
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS admin_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            admin_id INTEGER,
            action TEXT,
            target TEXT,
            details TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    conn.close()
    print("✅ База данных создана!")

# ========== ПОЛЬЗОВАТЕЛИ ==========

def get_user(user_id):
    """Получить пользователя (создать если нет)"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    user = cursor.fetchone()
    
    if not user:
        cursor.execute("""
            INSERT INTO users (user_id, money, day, cubes)
            VALUES (?, 1000.0, 1, 0)
        """, (user_id,))
        conn.commit()
        cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        user = cursor.fetchone()
    
    conn.close()
    return dict(user)

def update_user_money(user_id, amount):
    """Изменить деньги пользователя"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE users SET money = money + ? WHERE user_id = ?",
        (amount, user_id)
    )
    conn.commit()
    conn.close()

def update_user_cubes(user_id, amount):
    """Изменить кубки пользователя"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE users SET cubes = cubes + ? WHERE user_id = ?",
        (amount, user_id)
    )
    conn.commit()
    conn.close()

def update_user_day(user_id):
    """Увеличить день"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE users SET day = day + 1, last_seen = CURRENT_TIMESTAMP WHERE user_id = ?",
        (user_id,)
    )
    conn.commit()
    conn.close()

def get_user_by_id(user_id):
    """Получить пользователя по ID"""
    conn = get_db()
    cursor = conn.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    return dict(user) if user else None

def get_user_by_username(username):
    """Получить пользователя по юзернейму"""
    conn = get_db()
    cursor = conn.execute("SELECT * FROM users WHERE username = ?", (username.lower().replace("@", ""),))
    user = cursor.fetchone()
    conn.close()
    return dict(user) if user else None

def get_all_users(limit=100, offset=0):
    """Получить всех пользователей"""
    conn = get_db()
    cursor = conn.execute("""
        SELECT * FROM users 
        ORDER BY last_seen DESC 
        LIMIT ? OFFSET ?
    """, (limit, offset))
    users = cursor.fetchall()
    conn.close()
    return [dict(u) for u in users]

def get_users_count():
    """Количество пользователей"""
    conn = get_db()
    cursor = conn.execute("SELECT COUNT(*) FROM users")
    count = cursor.fetchone()[0]
    conn.close()
    return count

# ========== ПОРТФЕЛЬ ==========

def buy_stock(user_id, ticker, amount, price):
    """Купить акции"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Проверяем есть ли уже
    cursor.execute(
        "SELECT amount FROM portfolio WHERE user_id = ? AND ticker = ?",
        (user_id, ticker)
    )
    existing = cursor.fetchone()
    
    if existing:
        cursor.execute("""
            UPDATE portfolio 
            SET amount = amount + ? 
            WHERE user_id = ? AND ticker = ?
        """, (amount, user_id, ticker))
    else:
        cursor.execute("""
            INSERT INTO portfolio (user_id, ticker, amount, buy_price)
            VALUES (?, ?, ?, ?)
        """, (user_id, ticker, amount, price))
    
    # Списываем деньги
    cursor.execute(
        "UPDATE users SET money = money - ? WHERE user_id = ?",
        (price * amount, user_id)
    )
    
    # Логируем сделку
    cursor.execute("""
        INSERT INTO transactions (user_id, type, ticker, amount, price, total)
        VALUES (?, 'buy', ?, ?, ?, ?)
    """, (user_id, ticker, amount, price, price * amount))
    
    conn.commit()
    conn.close()

def sell_stock(user_id, ticker, amount, price):
    """Продать акции"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("""
        UPDATE portfolio 
        SET amount = amount - ? 
        WHERE user_id = ? AND ticker = ?
    """, (amount, user_id, ticker))
    
    # Удаляем если 0
    cursor.execute("""
        DELETE FROM portfolio 
        WHERE user_id = ? AND ticker = ? AND amount <= 0
    """, (user_id, ticker))
    
    # Начисляем деньги
    cursor.execute(
        "UPDATE users SET money = money + ? WHERE user_id = ?",
        (price * amount, user_id)
    )
    
    # Логируем сделку
    cursor.execute("""
        INSERT INTO transactions (user_id, type, ticker, amount, price, total)
        VALUES (?, 'sell', ?, ?, ?, ?)
    """, (user_id, ticker, amount, price, price * amount))
    
    conn.commit()
    conn.close()

def get_portfolio(user_id):
    """Получить портфель пользователя"""
    conn = get_db()
    cursor = conn.execute("""
        SELECT p.ticker, p.amount, c.name, c.price 
        FROM portfolio p
        JOIN companies c ON p.ticker = c.ticker
        WHERE p.user_id = ?
    """, (user_id,))
    portfolio = cursor.fetchall()
    conn.close()
    return [dict(p) for p in portfolio]

def get_user_transactions(user_id, limit=20):
    """История сделок пользователя"""
    conn = get_db()
    cursor = conn.execute("""
        SELECT * FROM transactions 
        WHERE user_id = ? 
        ORDER BY created_at DESC 
        LIMIT ?
    """, (user_id, limit))
    transactions = cursor.fetchall()
    conn.close()
    return [dict(t) for t in transactions]

# ========== КОМПАНИИ ==========

def init_companies():
    """Инициализация компаний"""
    from config import DEFAULT_COMPANIES
    
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM companies")
    if cursor.fetchone()[0] == 0:
        for ticker, data in DEFAULT_COMPANIES.items():
            cursor.execute("""
                INSERT INTO companies (ticker, name, price, prev_price)
                VALUES (?, ?, ?, ?)
            """, (ticker, data['name'], data['price'], data['prev_price']))
    
    conn.commit()
    conn.close()

def get_all_companies():
    """Получить все компании"""
    conn = get_db()
    cursor = conn.execute("SELECT * FROM companies ORDER BY ticker")
    companies = cursor.fetchall()
    conn.close()
    return [dict(c) for c in companies]

def get_company(ticker):
    """Получить компанию по тикеру"""
    conn = get_db()
    cursor = conn.execute("SELECT * FROM companies WHERE ticker = ?", (ticker,))
    company = cursor.fetchone()
    conn.close()
    return dict(company) if company else None

def update_company_price(ticker, new_price):
    """Обновить цену компании"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Получаем старую цену
    cursor.execute("SELECT price FROM companies WHERE ticker = ?", (ticker,))
    old_price = cursor.fetchone()[0]
    
    # Обновляем
    cursor.execute("""
        UPDATE companies 
        SET prev_price = ?, price = ? 
        WHERE ticker = ?
    """, (old_price, new_price, ticker))
    
    # Сохраняем в историю
    cursor.execute("""
        INSERT INTO price_history (ticker, price)
        VALUES (?, ?)
    """, (ticker, new_price))
    
    conn.commit()
    conn.close()

def update_all_prices():
    """Обновить цены всех компаний"""
    import random
    
    companies = get_all_companies()
    for company in companies:
        change = random.uniform(-0.1, 0.1)
        new_price = round(company['price'] * (1 + change), 2)
        update_company_price(company['ticker'], new_price)

def get_price_history(ticker, limit=30):
    """История цен компании"""
    conn = get_db()
    cursor = conn.execute("""
        SELECT price, recorded_at FROM price_history 
        WHERE ticker = ? 
        ORDER BY recorded_at DESC 
        LIMIT ?
    """, (ticker, limit))
    history = cursor.fetchall()
    conn.close()
    return [dict(h) for h in history]

# ========== ИНВЕНТАРЬ ==========

def add_to_inventory(user_id, item):
    """Добавить предмет в инвентарь"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO inventory (user_id, item_id, name, emoji, description, category, effect)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        user_id,
        item['item_id'],
        item['name'],
        item['emoji'],
        item['description'],
        item['category'],
        item['effect']
    ))
    
    conn.commit()
    conn.close()

def remove_from_inventory(user_id, item_id):
    """Удалить предмет из инвентаря"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM inventory WHERE id = ? AND user_id = ?",
        (item_id, user_id)
    )
    conn.commit()
    conn.close()

def get_inventory(user_id, page=1, per_page=8):
    """Получить инвентарь с пагинацией"""
    conn = get_db()
    offset = (page - 1) * per_page
    
    cursor = conn.execute("""
        SELECT * FROM inventory 
        WHERE user_id = ? 
        ORDER BY acquired_at DESC 
        LIMIT ? OFFSET ?
    """, (user_id, per_page, offset))
    
    items = cursor.fetchall()
    
    cursor.execute("SELECT COUNT(*) FROM inventory WHERE user_id = ?", (user_id,))
    total = cursor.fetchone()[0]
    
    conn.close()
    return [dict(i) for i in items], total

def get_inventory_count(user_id):
    """Количество предметов в инвентаре"""
    conn = get_db()
    cursor = conn.execute("SELECT COUNT(*) FROM inventory WHERE user_id = ?", (user_id,))
    count = cursor.fetchone()[0]
    conn.close()
    return count

# ========== КУБКИ ==========

def add_cube(user_id, season_name, place):
    """Добавить кубок пользователю"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO cubes_history (user_id, season_name, place)
        VALUES (?, ?, ?)
    """, (user_id, season_name, place))
    
    cursor.execute(
        "UPDATE users SET cubes = cubes + 1 WHERE user_id = ?",
        (user_id,)
    )
    
    conn.commit()
    conn.close()

def get_cubes_history(user_id):
    """История кубков пользователя"""
    conn = get_db()
    cursor = conn.execute("""
        SELECT season_name, place, earned_at FROM cubes_history 
        WHERE user_id = ? 
        ORDER BY earned_at DESC
    """, (user_id,))
    history = cursor.fetchall()
    conn.close()
    return [dict(h) for h in history]

# ========== ДОСТИЖЕНИЯ ==========

def add_achievement(user_id, achievement_id):
    """Добавить достижение"""
    conn = get_db()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO achievements (user_id, achievement_id)
            VALUES (?, ?)
        """, (user_id, achievement_id))
        conn.commit()
        conn.close()
        return True
    except:
        conn.close()
        return False

def get_user_achievements(user_id):
    """Получить достижения пользователя"""
    conn = get_db()
    cursor = conn.execute("""
        SELECT achievement_id, achieved_at FROM achievements 
        WHERE user_id = ? 
        ORDER BY achieved_at DESC
    """, (user_id,))
    achievements = cursor.fetchall()
    conn.close()
    return [dict(a) for a in achievements]

def check_achievements(user_id):
    """Проверить и выдать достижения"""
    user = get_user(user_id)
    portfolio = get_portfolio(user_id)
    transactions = get_user_transactions(user_id, 100)
    
    new_achievements = []
    
    # Первая сделка
    if len(transactions) > 0:
        if add_achievement(user_id, 'first_trade'):
            new_achievements.append('first_trade')
    
    # 100 сделок
    if len(transactions) >= 100:
        if add_achievement(user_id, 'trader_100'):
            new_achievements.append('trader_100')
    
    # Капитал 10,000
    total = user['money']
    for p in portfolio:
        total += p['amount'] * p['price']
    
    if total >= 10000:
        if add_achievement(user_id, 'capital_10k'):
            new_achievements.append('capital_10k')
    
    if total >= 100000:
        if add_achievement(user_id, 'capital_100k'):
            new_achievements.append('capital_100k')
    
    if total >= 1000000:
        if add_achievement(user_id, 'millionaire'):
            new_achievements.append('millionaire')
    
    # Кубки
    if user['cubes'] >= 1:
        if add_achievement(user_id, 'first_cube'):
            new_achievements.append('first_cube')
    
    if user['cubes'] >= 10:
        if add_achievement(user_id, 'cubes_10'):
            new_achievements.append('cubes_10')
    
    return new_achievements

# ========== АКТИВНЫЕ ЭФФЕКТЫ ==========

def add_effect(user_id, effect_type, duration_hours):
    """Добавить активный эффект"""
    from datetime import datetime, timedelta
    
    expires = datetime.now() + timedelta(hours=duration_hours)
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO active_effects (user_id, effect_type, expires_at)
        VALUES (?, ?, ?)
    """, (user_id, effect_type, expires.isoformat()))
    conn.commit()
    conn.close()

def get_active_effects(user_id):
    """Получить активные эффекты"""
    from datetime import datetime
    
    conn = get_db()
    cursor = conn.execute("""
        SELECT * FROM active_effects 
        WHERE user_id = ? AND expires_at > ?
    """, (user_id, datetime.now().isoformat()))
    effects = cursor.fetchall()
    conn.close()
    return [dict(e) for e in effects]

def remove_expired_effects():
    """Удалить истекшие эффекты"""
    from datetime import datetime
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM active_effects WHERE expires_at < ?", (datetime.now().isoformat(),))
    conn.commit()
    conn.close()

# ========== ПОДПИСКИ ==========

def add_subscription(user_id, sub_type, bonus, days):
    """Добавить подписку"""
    from datetime import datetime, timedelta
    
    expires = datetime.now() + timedelta(days=days)
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO subscriptions (user_id, sub_type, bonus, expires_at)
        VALUES (?, ?, ?, ?)
    """, (user_id, sub_type, bonus, expires.isoformat()))
    conn.commit()
    conn.close()

def get_active_subscriptions(user_id):
    """Получить активные подписки"""
    from datetime import datetime
    
    conn = get_db()
    cursor = conn.execute("""
        SELECT * FROM subscriptions 
        WHERE user_id = ? AND expires_at > ?
    """, (user_id, datetime.now().isoformat()))
    subs = cursor.fetchall()
    conn.close()
    return [dict(s) for s in subs]

def remove_expired_subscriptions():
    """Удалить истекшие подписки"""
    from datetime import datetime
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM subscriptions WHERE expires_at < ?", (datetime.now().isoformat(),))
    conn.commit()
    conn.close()

# ========== ПРОМОКОДЫ ==========

def create_promocode(code, bonus, max_uses, admin_id):
    """Создать промокод"""
    conn = get_db()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO promocodes (code, bonus, max_uses, created_by)
            VALUES (?, ?, ?, ?)
        """, (code.upper(), bonus, max_uses, admin_id))
        conn.commit()
        conn.close()
        return True
    except:
        conn.close()
        return False

def get_promocode(code):
    """Получить промокод"""
    conn = get_db()
    cursor = conn.execute("SELECT * FROM promocodes WHERE code = ?", (code.upper(),))
    promo = cursor.fetchone()
    conn.close()
    return dict(promo) if promo else None

def use_promocode(user_id, code):
    """Использовать промокод"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Проверяем промокод
    cursor.execute("SELECT * FROM promocodes WHERE code = ?", (code.upper(),))
    promo = cursor.fetchone()
    
    if not promo:
        conn.close()
        return False, "❌ Промокод не найден"
    
    if promo['used_count'] >= promo['max_uses']:
        conn.close()
        return False, "❌ Промокод закончился"
    
    # Проверяем не использовал ли уже
    cursor.execute(
        "SELECT * FROM used_promos WHERE user_id = ? AND promo_code = ?",
        (user_id, code.upper())
    )
    if cursor.fetchone():
        conn.close()
        return False, "❌ Ты уже использовал этот промокод"
    
    # Начисляем бонус
    cursor.execute(
        "UPDATE users SET money = money + ? WHERE user_id = ?",
        (promo['bonus'], user_id)
    )
    
    # Отмечаем использованный
    cursor.execute(
        "INSERT INTO used_promos (user_id, promo_code) VALUES (?, ?)",
        (user_id, code.upper())
    )
    
    # Увеличиваем счетчик
    cursor.execute(
        "UPDATE promocodes SET used_count = used_count + 1 WHERE code = ?",
        (code.upper(),)
    )
    
    conn.commit()
    conn.close()
    return True, f"✅ +${promo['bonus']}"

def get_all_promocodes():
    """Все промокоды"""
    conn = get_db()
    cursor = conn.execute("SELECT * FROM promocodes ORDER BY created_at DESC")
    promos = cursor.fetchall()
    conn.close()
    return [dict(p) for p in promos]

def delete_promocode(code):
    """Удалить промокод"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM promocodes WHERE code = ?", (code.upper(),))
    deleted = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return deleted

# ========== СЕЗОН ==========

def create_season(name, days):
    """Создать новый сезон"""
    from datetime import datetime, timedelta
    
    conn = get_db()
    cursor = conn.cursor()
    
    # Деактивируем старый сезон
    cursor.execute("UPDATE season SET active = 0 WHERE id = 1")
    
    # Создаем новый
    start = datetime.now()
    end = start + timedelta(days=days)
    
    cursor.execute("""
        INSERT OR REPLACE INTO season (id, name, start_date, end_date, active)
        VALUES (1, ?, ?, ?, 1)
    """, (name, start.isoformat(), end.isoformat()))
    
    conn.commit()
    conn.close()

def get_current_season():
    """Получить текущий сезон"""
    conn = get_db()
    cursor = conn.execute("SELECT * FROM season WHERE id = 1")
    season = cursor.fetchone()
    conn.close()
    return dict(season) if season else None

def end_season():
    """Завершить сезон и выдать награды"""
    from datetime import datetime
    
    season = get_current_season()
    if not season or not season['active']:
        return False, "❌ Нет активного сезона"
    
    # Получаем топ-3
    leaderboard = get_leaderboard(50)
    top3 = leaderboard[:3]
    
    for i, user in enumerate(top3, 1):
        add_cube(user['user_id'], season['name'], i)
        
        # Добавляем призовые
        prize = [5000, 3000, 1000][i-1]
        update_user_money(user['user_id'], prize)
    
    # Деактивируем сезон
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE season SET active = 0 WHERE id = 1")
    conn.commit()
    conn.close()
    
    return True, f"✅ Сезон '{season['name']}' завершен! Победители получили кубки и призы."

def get_season_time_left():
    """Сколько осталось до конца сезона"""
    from datetime import datetime
    
    season = get_current_season()
    if not season or not season['active']:
        return None, None
    
    end = datetime.fromisoformat(season['end_date'])
    now = datetime.now()
    
    if now > end:
        end_season()
        return None, None
    
    delta = end - now
    return delta.days, delta.seconds // 3600

# ========== ЛИДЕРЫ ==========

def update_leaderboard():
    """Обновить таблицу лидеров"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Получаем всех пользователей
    cursor.execute("SELECT user_id, username, money, cubes FROM users")
    users = cursor.fetchall()
    
    leaderboard = []
    for user in users:
        # Считаем стоимость акций
        cursor.execute("""
            SELECT SUM(p.amount * c.price) as stock_value
            FROM portfolio p
            JOIN companies c ON p.ticker = c.ticker
            WHERE p.user_id = ?
        """, (user['user_id'],))
        
        stock_value = cursor.fetchone()[0] or 0
        total = user['money'] + stock_value
        
        leaderboard.append({
            'user_id': user['user_id'],
            'username': user['username'] or f"User_{user['user_id']}",
            'capital': round(total, 2),
            'cubes': user['cubes']
        })
    
    conn.close()
    leaderboard.sort(key=lambda x: x['capital'], reverse=True)
    return leaderboard

def get_leaderboard(limit=10):
    """Получить топ пользователей"""
    leaderboard = update_leaderboard()
    return leaderboard[:limit]

def get_user_rank(user_id):
    """Получить место пользователя"""
    leaderboard = update_leaderboard()
    for i, user in enumerate(leaderboard, 1):
        if user['user_id'] == user_id:
            return i, len(leaderboard)
    return None, len(leaderboard)

# ========== ЛОГИ АДМИНОВ ==========

def log_admin_action(admin_id, action, target=None, details=None):
    """Записать действие админа"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO admin_logs (admin_id, action, target, details)
        VALUES (?, ?, ?, ?)
    """, (admin_id, action, target, details))
    conn.commit()
    conn.close()

def get_admin_logs(limit=50):
    """Получить логи админов"""
    conn = get_db()
    cursor = conn.execute("""
        SELECT * FROM admin_logs 
        ORDER BY created_at DESC 
        LIMIT ?
    """, (limit,))
    logs = cursor.fetchall()
    conn.close()
    return [dict(l) for l in logs]

# ========== СТАТИСТИКА ==========

def get_stats():
    """Общая статистика"""
    conn = get_db()
    cursor = conn.cursor()
    
    users_count = cursor.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    scams_count = 0  # Если есть скам-база
    companies_count = cursor.execute("SELECT COUNT(*) FROM companies").fetchone()[0]
    
    # Активные сегодня
    from datetime import datetime, timedelta
    yesterday = (datetime.now() - timedelta(days=1)).isoformat()
    active_today = cursor.execute(
        "SELECT COUNT(*) FROM users WHERE last_seen > ?",
        (yesterday,)
    ).fetchone()[0]
    
    # Всего денег
    total_money = cursor.execute("SELECT SUM(money) FROM users").fetchone()[0] or 0
    
    conn.close()
    
    return {
        'users': users_count,
        'scams': scams_count,
        'companies': companies_count,
        'active_today': active_today,
        'total_money': total_money
    }

# ========== ИНИЦИАЛИЗАЦИЯ ==========

def init_all():
    """Инициализация всего"""
    init_database()
    init_companies()
    print("✅ Все таблицы созданы, компании добавлены")