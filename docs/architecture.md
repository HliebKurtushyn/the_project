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
    │        └── account/
    │           └── styles.css
    │   └── js/
    │        └── account/
    │            └── scripts.js
    
    ├── docs/                    # Документація
    │   ├── overview.md          # Ідея проєкту, задум
    │   ├── architecture.md      # Як все влаштовано технічно
    │   ├── roles.md             # Хто за що відповідає
    │   ├── workflow.md          # Правила для проекту (git коміти, стиль і т.д.)
    │   └── trash.md             # Можна писати що хочеш. Нотатки, чорновик.. взагалі всеодно
```

## Пояснення
- `CustomUser` модель знаходиться в апці `core/models.py`.
- ...
- В майбутньому буде доданий Docker файл для контейнеризації проєкту.
- 