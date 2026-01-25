# Архітектура проєкту

## Структура
```
the_project/
    ├── manage.py                # Основний файл
    ├── README.md                
    ├── .gitignore               
    ├── requirements.txt  
           
    ├── core/                    # Приклад апки (буде багато)
    │   ├── __init__.py
    │   ├── admin.py
    │   ├── apps.py
    │   ├── models.py
    │   ├── views.py
    │   ├── urls.py
    │   └── migrations/
    │       └── __init__.py
    
    ├── account/
    │   ├── __init__.py
    │   ├── admin.py
    │   ├── apps.py
    │   ├── models.py
    │   ├── views.py
    │   ├── urls.py
    │   └── migrations/
    │       └── __init__.py
    
    ├── templates/               # шаблони
    │   └── account/
    │       └── base.html
    
    ├── static/                  # CSS / JS / картинки
    │   └── css/
    │       └── account/
    │           └── styles.css
    │   └── js/
    │       └── account/
    │            └── scripts.js
    
    ├── docs/                    # Документація
    │   ├── architecture.md      # Як все влаштовано технічно
    │   ├── for_team.md          # Інформація для команди
    │   ├── overview.md          # Ідея проєкту, задум
    │   ├── roles.md             # Хто за що відповідає
    │   └── trash.md             # Можна писати що хочеш. Нотатки, чорновик.. взагалі всеодно
    │   ├── workflow.md          # Правила для проекту (git коміти, стиль і т.д.)
```

## Моделі
CustomUser (core/models.py) (WIP!!!):
```python
class CustomUser(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username
```


## Інше
- Використовується система шаблонів Jinja2.


## Пояснення
- ...
- В майбутньому буде доданий Docker файл для контейнеризації проєкту.
