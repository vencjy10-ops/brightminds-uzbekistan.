CREATE TABLE IF NOT EXISTS programs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category TEXT NOT NULL,
    title TEXT NOT NULL,
    org TEXT NOT NULL,
    desc_ru TEXT NOT NULL,
    desc_uz TEXT NOT NULL,
    desc_en TEXT NOT NULL,
    link TEXT NOT NULL
);

INSERT INTO programs (category, title, org, desc_ru, desc_uz, desc_en, link)
VALUES 
('it', 'CS50x: Introduction to Computer Science', '🏛 Harvard University', 
 'Изучи основы Computer Science, C, Python, SQL и Web на уровне студентов Гарварда. Идеально под твои интересы.',
 'Garvard talabalari darajasida Computer Science, C, Python, SQL va Web asoslarini o''rganing. Sizga juda mos keladi.',
 'Learn the foundations of Computer Science, C, Python, SQL, and Web development at Harvard level. Perfect match for you.',
 'https://harvard.edu'),

('volunteering', 'Citizen Science Projects', '🚀 Zooniverse Platform',
 'Помогай ученым исследовать космос, природу и климат. Набирай реальные часы для резюме в США.',
 'Olimlarga kosmos, tabiat va iqlimni o''rganishda yordam bering. AQSh oliy o''quv yurtlari rezyumesi uchun soat yiging.',
 'Help scientists analyze space, nature, and climate data. Earn real volunteering hours for your US college resume.',
 'https://zooniverse.org'),

('marketing', 'Digital Marketing Certification', '📈 HubSpot Academy',
 'Освой основы продвижения сайтов, SEO и контент-маркетинг. Бесплатный бизнес-сертификат.',
 'Veb-saytlarni reklama qilish, SEO va kontent-marketing asoslarini o''zlashtiring. Bepul biznes sertifikati.',
 'Master the principles of website promotion, SEO, and inbound content marketing. Free professional certification.',
 'https://hubspot.com');
