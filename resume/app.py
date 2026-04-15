from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.utils import secure_filename
from functools import wraps
import markdown
import json
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', '0')


UPLOAD_FOLDER = './resume/static/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME', 'admin')
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'admin123')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            flash('Пожалуйста, войдите в систему', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

DATA_FILE = './data/projects.json'
os.makedirs('data', exist_ok=True)

DEFAULT_DATA = {
    'name': 'Анна Михайлова',
    'title': 'Frontend-разработчик',
    'bio': 'Создаю сайты и веб-приложения',
    'location': 'Москва',
    'experience': '2 года',
    'github': 'https://github.com/anna',
    'kwork': 'https://kwork.ru/anna',
    'phone': '+7 (999) 123-45-67',
    'email': 'anna@example.com',
    'skills': [
        {'name': 'Python', 'percent': 85},
        {'name': 'JavaScript', 'percent': 80},
        {'name': 'React', 'percent': 75},
        {'name': 'HTML/CSS', 'percent': 90},
        {'name': 'Flask', 'percent': 70}
    ],
    'projects': [
        {
            'id': 1,
            'title': 'Аналитика',
            'description': 'Панель с графиками',
            'tech': ['React', 'D3.js'],
            'image': 'default.jpg',
            'link': 'https://github.com/anna/project1'
        },
        {
            'id': 2,
            'title': 'Task Manager',
            'description': 'Менеджер задач',
            'tech': ['Vue.js', 'Node.js'],
            'image': 'default.jpg',
            'link': 'https://github.com/anna/project2'
        }
    ]
}

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return DEFAULT_DATA.copy()

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@app.route('/')
def index():
    data = load_data()
    data['bio_html'] = markdown.markdown(data['bio'])
    return render_template('index.html', **data)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('logged_in'):
        return redirect(url_for('admin'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['logged_in'] = True
            flash('Вы успешно вошли в систему!', 'success')
            return redirect(url_for('admin'))
        else:
            flash('Неверное имя пользователя или пароль', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('Вы вышли из системы', 'success')
    return redirect(url_for('index'))

@app.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    data = load_data()
    
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'update_profile':
            data['name'] = request.form.get('name')
            data['title'] = request.form.get('title')
            data['bio'] = request.form.get('bio')
            data['location'] = request.form.get('location')
            data['experience'] = request.form.get('experience')
            data['github'] = request.form.get('github')
            data['kwork'] = request.form.get('kwork')
            data['phone'] = request.form.get('phone')
            data['email'] = request.form.get('email')
            skills_list = []
            names = request.form.get('skill_names', '').split(',')
            percents = request.form.get('skill_percents', '').split(',')
            for i in range(min(len(names), len(percents))):
                if names[i].strip():
                    skills_list.append({'name': names[i].strip(), 'percent': int(percents[i].strip())})
            data['skills'] = skills_list
            flash('Сохранено!')
            
        elif action == 'add_project':
            image_name = 'default.jpg'
            if 'image' in request.files:
                file = request.files['image']
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    image_name = filename
            
            new_id = max([p['id'] for p in data['projects']], default=0) + 1
            data['projects'].append({
                'id': new_id,
                'title': request.form.get('title'),
                'description': request.form.get('description'),
                'tech': [t.strip() for t in request.form.get('tech', '').split(',') if t.strip()],
                'image': image_name,
                'link': request.form.get('link', '#')
            })
            flash('Проект добавлен!')
            
        elif action == 'delete_project':
            pid = int(request.form.get('project_id'))
            for p in data['projects']:
                if p['id'] == pid and p['image'] != 'default.jpg':
                    img_path = os.path.join(app.config['UPLOAD_FOLDER'], p['image'])
                    if os.path.exists(img_path):
                        os.remove(img_path)
            data['projects'] = [p for p in data['projects'] if p['id'] != pid]
            flash('Проект удален!')
            
        elif action == 'edit_project':
            pid = int(request.form.get('project_id'))
            for p in data['projects']:
                if p['id'] == pid:
                    p['title'] = request.form.get('title')
                    p['description'] = request.form.get('description')
                    p['tech'] = [t.strip() for t in request.form.get('tech', '').split(',') if t.strip()]
                    p['link'] = request.form.get('link', '#')
                    
                    if 'image' in request.files:
                        file = request.files['image']
                        if file and allowed_file(file.filename):
                            if p['image'] != 'default.jpg':
                                old_img = os.path.join(app.config['UPLOAD_FOLDER'], p['image'])
                                if os.path.exists(old_img):
                                    os.remove(old_img)
                            filename = secure_filename(file.filename)
                            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                            p['image'] = filename
                    break
            flash('Обновлено!')
        
        save_data(data)
        return redirect(url_for('admin'))
    
    return render_template('admin.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)