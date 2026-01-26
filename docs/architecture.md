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
    │   ├── models/
    │       ├── __init__.py
    │       ├── product.py
    │       ├── brand.py
    │       └── category.py
    │   ├── views.py
    │   ├── urls.py
    │   └── migrations/
    │       └── __init__.py
    
    ├── templates/               # шаблони
    │   ├── product/
    │       └── product.html
    │   ├── base.html

    ├── media/                  # Приклад папки Media (НЕ статичні картинки)
    │   └── products/
    │       └── image.jpg

    ├── static/                  # Приклад Static (CSS / JS / СТАТИЧНІ картинки)
    │   └── css/
    │       └── account/
    │           └── styles.css
    │   └── js/
    │       └── account/
    │            └── scripts.js
    │   └── images/
    │       └── logo.png
    
    ├── docs/                    # Документація
    │   ├── architecture.md      # Як все влаштовано технічно
    │   ├── for_team.md          # Інформація для команди
    │   ├── overview.md          # Ідея проєкту, задум
    │   ├── roles.md             # Хто за що відповідає
    │   ├── trash.md             # Можна писати що хочеш. Нотатки, чорновик.. взагалі всеодно
    │   └── workflow.md          # Правила для проекту (git коміти, стиль і т.д.)
```

## Моделі
### core/models.py
- CustomUser (core/models.py) (WIP!!!):
```python
class CustomUser(AbstractUser):
    ...

    def __str__(self):
        return self.username
```

### product/models
- Product (.../models/product.py):
```python
class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    category = models.ManyToManyField('product.Category', related_name='products', default="test_category", blank=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='products', default="test brand", null=True, blank=True)

    size = models.CharField(max_length=20, default="No size specified.")
    description = models.TextField(default="No description available.")
    image = models.ImageField(upload_to='products/')

    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, blank=True)
    discount_end_date = models.DateField(null=True, blank=True)

    stock = models.IntegerField(default=0)


    def __str__(self):
        return self.name
```


- Brand (.../models/brand.py):
```python
class Brand(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)


    def __str__(self):
        return self.name
```


- Category (.../models/category.py):
```python
class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)


    def __str__(self):
        return self.name
```


## Інше
- Використовується система шаблонів Jinja2.


## Пояснення
- ...
- В майбутньому буде доданий Docker файл для контейнеризації проєкту.
