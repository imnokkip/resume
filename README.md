# Моё резюме

---

## 📌 О проекте

Сайт, написанный на **python** с использованием **flask**. Это место, куда я буду выкладывать свои проекты и отслеживать прогресс. В проекте я использовал технологию **jinja** для подгрузки проектов из админ панели.

---

## 🚀 Возможности

- **редактирование всей информации на странице**
- **Контроль содержимого через админ-панель**
- **вход в админку, через ограниченную по времени сессию**

---

## 🛠️ Технологии

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-2.0+-000000?style=for-the-badge&logo=flask&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)
![Jinja](https://img.shields.io/badge/Jinja-B41717?style=for-the-badge&logo=jinja&logoColor=white)
![Markdown](https://img.shields.io/badge/Markdown-000000?style=for-the-badge&logo=markdown&logoColor=white)

---

## 🖥️ Запуск

1. Клонируй репозиторий:
   ```bash
   git clone https://github.com/imnokkip/Meeting-Master
   cd resume
   ```

2. Установи зависимости (рекомендуется использовать `uv`):
   ```bash
   pip install flask markdown dotenv {серверная утилита типа gunicorn}
   ```

3. настройка админа:
   ```bash
   создайте файл .env и впишите:
   SECRET_KEY=your-super-secret-key-here-12345
   ADMIN_USERNAME=admin
   ADMIN_PASSWORD=your-strong-password-here
   ```

4. настройка запуска:
   Создайте wsgi.py и впишите:
   from app import app
   if __name__ == "__main__":
     app.run()
5. Запуск:
   ```bash
   gunicorn --bind {целевой ip:port} wsgi:app
   ```
  ---
