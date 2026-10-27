from flask import Flask, render_template, request, jsonify, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

# Хранилище данных прямо в памяти для стабильности на бесплатном тарифе Render
_INITIALIZED = False
def get_db_connection():
    conn = sqlite3.connect('opportunities.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    global _INITIALIZED
    if not _INITIALIZED:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS opportunities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                organization TEXT NOT NULL,
                category TEXT NOT NULL,
                min_age INTEGER DEFAULT 14,
                format TEXT NOT NULL,
                description TEXT NOT NULL,
                link TEXT NOT NULL
            )
        ''')
        
        # Проверяем, пустая ли база. Если пустая — заполняем стартовыми программами
        cursor.execute("SELECT COUNT(*) FROM opportunities")
        if cursor.fetchone()[0] == 0:
            sample_data = [
                ('CS50x: Introduction to Computer Science', 'Harvard University', 'it', 14, 'Online', 'Легендарный курс по основам программирования. Изучи C, Python, SQL и веб-разработку абсолютно бесплатно.', 'https://harvard.edu'),
                ('Citizen Science Projects', 'Zooniverse Platform', 'volunteering', 10, 'Online', 'Помогай ученым исследовать космос, дикую природу и климат. Набирай реальные часы для резюме в США.', 'https://zooniverse.org'),
                ('Digital Marketing Certification', 'HubSpot Academy', 'marketing', 13, 'Online', 'Освой основы продвижения сайтов, SEO, контент-маркетинг и автоматизацию бизнес-процессов.', 'https://hubspot.com'),
                ('Berea College Full-Ride Грант', 'Berea College (USA)', 'marketing', 17, 'Offline', 'Официальная программа полного финансирования для иностранцев. Покрывает 100% стоимости обучения и жилья.', 'https://berea.edu'),
                ('Онлайн-волонтерство ООН (UNV)', 'United Nations Volunteers', 'volunteering', 15, 'Online', 'Официальная платформа ООН. Помощь международным проектам в дизайне, переводах и ИТ. Выдается сертификат.', 'https://unv.org')
            ]
            cursor.executemany('''
                INSERT INTO opportunities (title, organization, category, min_age, format, description, link)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', sample_data)
        
        conn.commit()
        conn.close()
        _INITIALIZED = True

@app.route('/')
def index():
    init_db()
    return render_template('index.html')

# МАРШРУТ ДЛЯ СТРАНИЦЫ АДМИНКИ
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    init_db()
    conn = get_db_connection()
    
    if request.method == 'POST':
        # Собираем данные из полей веб-формы
        title = request.form['title']
        organization = request.form['organization']
        category = request.form['category']
        min_age = int(request.form['min_age'])
        description = request.form['description']
        link = request.form['link']
        
        # Записываем новый курс в SQL базу данных в один клик!
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO opportunities (title, organization, category, min_age, format, description, link)
            VALUES (?, ?, ?, ?, 'Online', ?, ?)
        ''', (title, organization, category, min_age, description, link))
        conn.commit()
        return redirect(url_for('admin'))
        
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM opportunities ORDER BY id DESC")
    all_items = cursor.fetchall()
    conn.close()
    return render_template('admin.html', items=all_items)

@app.route('/api/search')
def search():
    init_db()
    age = request.args.get('age', default=0, type=int)
    categories = request.args.getlist('categories')

    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM opportunities WHERE min_age <= ?"
    params = [age if age > 0 else 20]

    if categories and 'all' not in categories:
        placeholders = ', '.join(['?'] * len(categories))
        query += f" AND category IN ({placeholders})"
        params.extend(categories)

    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()

    opportunities = []
    for row in rows:
        opportunities.append({
            'id': row['id'],
            'title': row['title'],
            'organization': row['organization'],
            'category': row['category'],
            'min_age': row['min_age'],
            'format': row['format'],
            'description': row['description'],
            'link': row['link']
        })

    return jsonify(opportunities)

if __name__ == '__main__':
    # Render автоматически передает нужный порт через переменную окружения PORT.
    # Если её нет, сервер запустится на стандартном порту 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
