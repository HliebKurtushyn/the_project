# Архітектура проєкту

## Структура
```
the_project/
    ├── manage.py                # Основний файл
    ├── README.md                
    ├── .gitignore               
    ├── requirements.txt  
           
    ├── core/                    
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
    
    ├── product/
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
### core/models.py
- CustomUser (core/models.py) (WIP!!!):
```python
class CustomUser(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username
```

### product/models
- Product (.../models/product.py):
```python
class Product(models.Model):
    name = models.CharField(max_length=100)
    
    category = models.ManyToManyField('product.Category', related_name='products', default="test_category")
    brand = models.ManyToManyField('product.Brand', related_name='products', default="test_brand")
    
    size = models.CharField(max_length=20, default="No size specified.")
    description = models.TextField(default="No description available.")
    image = models.ImageField(upload_to='products/')
    
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    discount = IntegerField(max_length=3, default=0)
    discount_end_date = models.DateField(null=True, blank=True)
    
    stock = models.IntegerField(max_length=5, default=0)
    
    
    def __str__(self):
        return self.name
```


- Brand (.../models/brand.py):
```python
class Brand(models.Model):
    name = models.CharField(max_length=100)
    ...

    def __str__(self):
        return self.name
```


- Category (.../models/category.py):
```python
class Category(models.Model):
    name = models.CharField(max_length=100)
    ...

    def __str__(self):
        return self.name
```


## Інше
- Використовується система шаблонів Jinja2.


## Пояснення
- ...
- В майбутньому буде доданий Docker файл для контейнеризації проєкту.
