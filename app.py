from flask import Flask, render_template, request, jsonify
import sqlite3
import os

app = Flask(__name__)
DB_NAME = 'opportunities.db'

# Функция для инициализации базы данных
def init_db():
    # Если старая база есть, мы не перезаписываем её. 
    # Чтобы база обновилась на Render, он сам очистит кэш при сборке.
    if not os.path.exists(DB_NAME):
        conn = sqlite3.connect(DB_NAME)
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
        
        sample_data = [
            # Твои 3 стартовых проекта
            ('CS50x: Introduction to Computer Science', 'Harvard University', 'it', 14, 'Online', 'Легендарный курс по основам программирования. Изучи C, Python, SQL и веб-разработку абсолютно бесплатно и получи официальный сертификат.', 'https://harvard.edu'),
            ('Citizen Science Projects', 'Zooniverse Platform', 'volunteering', 10, 'Online', 'Помогай ученым исследовать космос, дикую природу и климат. Набирай реальные часы для резюме в США и получай международные сертификаты.', 'https://zooniverse.org'),
            ('Digital Marketing Certification', 'HubSpot Academy', 'marketing', 13, 'Online', 'Освой основы продвижения сайтов, SEO, контент-маркетинг и автоматизацию бизнес-процессов. Бесплатный бизнес-сертификат.', 'https://hubspot.com'),
            
            # НОВЫЕ ПРОГРАММЫ FULL-RIDE И ВОЛОНТЕРСТВА
            ('Berea College Full-Ride Грант', 'Berea College (USA)', 'marketing', 17, 'Offline', 'Официальная программа полного финансирования для иностранцев. Покрывает 100% стоимости обучения, проживания в общежитии и шведский стол.', 'https://berea.edu'),
            ('Онлайн-волонтерство ООН (UNV)', 'United Nations Volunteers', 'volunteering', 15, 'Online', 'Официальная платформа ООН. Помощь международным проектам в дизайне, переводах и ИТ. Выдается престижный сертификат Организации Объединенных Наций.', 'https://unv.org'),
            ('Международные ИТ-Хакатоны', 'Devpost Platform', 'it', 13, 'Online', 'Глобальная площадка технологических соревнований. Создавай ИТ-проекты в командах, собирай портфолио для США и выигрывай денежные гранты.', 'https://devpost.com'),
            ('Финансовая помощь Coursera (Financial Aid)', 'Coursera EdTech', 'it', 14, 'Online', 'Пошаговый инструмент получения 100% скидки на профессиональные курсы и сертификаты от Google, IBM, Stanford и Yale University.', 'https://coursera.org'),
            ('Академический обмен и обучение в США', 'Youth For Understanding (YFU)', 'marketing', 15, 'Offline', 'Программы полной и частичной стипендии на проживание и обучение в американских школах для раскрытия лидерского потенциала.', 'https://yfu.org')
        ]
        
        cursor.executemany('''
            INSERT INTO opportunities (title, organization, category, min_age, format, description, link)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', sample_data)
        
        conn.commit()
        conn.close()
        print("База данных SQL успешно обновлена и наполнена новыми Full-Ride программами!")

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/search')
def search():
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
    init_db()
    app.run(host='0.0.0.0', port=10000, debug=False)
