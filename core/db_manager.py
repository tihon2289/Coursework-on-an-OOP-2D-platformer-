# --- СТАРТ ФАЙЛА core/db_manager.py ---
import sqlite3
import hashlib

class DatabaseManager:
    def __init__(self, db_name="game_users.db"):
        self.db_name = db_name
        self._create_tables()

    def _hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def _create_tables(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE,
                    password TEXT,
                    levels_completed INTEGER DEFAULT 0
                )
            ''')
            # Новая таблица для хранения звезд
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS level_stars (
                    user_id INTEGER,
                    level_num INTEGER,
                    stars INTEGER,
                    PRIMARY KEY (user_id, level_num)
                )
            ''')
            conn.commit()

    def register(self, username, password):
        if len(username) < 3 or len(password) < 3:
            return False, "Логин и пароль от 3 символов!"
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', 
                               (username, self._hash_password(password)))
                conn.commit()
                return True, "Успешная регистрация! Теперь войдите."
            except sqlite3.IntegrityError:
                return False, "Такой логин уже существует!"

    def login(self, username, password):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id, levels_completed FROM users WHERE username=? AND password=?', 
                           (username, self._hash_password(password)))
            user = cursor.fetchone()
            if user:
                return True, user[0], user[1], "Успешный вход!"
            return False, None, None, "Неверный логин или пароль!"

    def update_progress(self, user_id, level_num, stars):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            # Обновляем общий прогресс
            cursor.execute('SELECT levels_completed FROM users WHERE id=?', (user_id,))
            current_progress = cursor.fetchone()[0]
            if level_num > current_progress:
                cursor.execute('UPDATE users SET levels_completed=? WHERE id=?', (level_num, user_id))
            
            # Сохраняем звезды (только если новый результат лучше старого)
            cursor.execute('SELECT stars FROM level_stars WHERE user_id=? AND level_num=?', (user_id, level_num))
            result = cursor.fetchone()
            if result is None:
                cursor.execute('INSERT INTO level_stars (user_id, level_num, stars) VALUES (?, ?, ?)', (user_id, level_num, stars))
            elif stars > result[0]:
                cursor.execute('UPDATE level_stars SET stars=? WHERE user_id=? AND level_num=?', (stars, user_id, level_num))
            conn.commit()

    def get_user_stars(self, user_id):
        # Возвращает словарь {номер_уровня: количество_звезд}
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT level_num, stars FROM level_stars WHERE user_id=?', (user_id,))
            return {row[0]: row[1] for row in cursor.fetchall()}