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
    
    ├── cart/
    │   ├── __init__.py
    │   ├── admin.py
    │   ├── apps.py
    │   ├── models.py
    │   ├── views.py
    │   ├── urls.py
    │   ├── utils.py
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

    category = models.ManyToManyField('product.Category', related_name='products', blank=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='products', null=True, blank=True)

    size = models.CharField(max_length=20, default="No size specified.")
    description = models.TextField(default="No description available.")
    image = models.ImageField(upload_to='products/')

    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True)
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

### cart/models.py
- Cart (WIP) (.../models.py):
```python
class Cart(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        null=True, blank=True
    )
    session_key = models.CharField(max_length=40, null=True, blank=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def items(self):
        return self.cartitem_set.all()

    @property
    def total_price(self):
        return sum(item.get_price() for item in self.items)
```

- CartItem (WIP) (.../models.py):
```python
class CartItem(models.Model):
    id = models.AutoField(primary_key=True)

    #   Прив'язка до Cart, яка може бути:
    # - DB cart для логіненого юзера
    # - анонімний через session (тут буде лише DB для юзерів)

    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='items')

    # Ціна буде отримуватись через зв'язок з Product (product.price)

    # Використав MinValueValidator, бо треба щоб мінімальне значення було 1
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Cart {self.cart.id}"

    # Використав @property щоб шаблони могли викликати як атрибут (cart_item.total_price)
    @property
    def total_price(self):
        return self.product.price * self.quantity

    def add_to_cart(self, quantity):
        self.quantity += quantity
        self.save(update_fields=['quantity'])

    def get_price(self):
        return self.product.price

    def get_total_price(self):
        return self.total_price
```

- SessionCartItem (WIP) (.../models.py):
```python
class SessionCartItem:
    def __init__(self, product, quantity):
        self.id = None               # у CartItem є id, тут можна None
        self.cart = None             # теж None
        self.product = product
        self.quantity = quantity

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in SessionCart"

    @property
    def total_price(self):
        return self.product.price * self.quantity

    def add_to_cart(self, quantity):
        self.quantity += quantity

    def get_price(self):
        return self.product.price

    def get_total_price(self):
        return self.total_price

```

### checkout/models
- Order (WIP) (.../models/order.py):
```python
class Order(models.Model):
    id = models.AutoField(primary_key=True)

    user = models.ForeignKey('core.CustomUser', on_delete=models.CASCADE, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=OrderStatus.choices, default=OrderStatus.PENDING)

    @property
    def total_price(self):
        return sum(item.total_price for item in self.items.all())
```

- OrderItem (WIP) (.../models/order_item.py):
```python
class OrderItem(models.Model):
    id = models.AutoField(primary_key=True)

    order = models.ForeignKey('Order', related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey('product.Product', related_name='product', on_delete=models.CASCADE)

    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def total_price(self):
        return self.price * self.quantity
```

- OrdersHistory (WIP) (.../models/orders_history.py):
```python
class OrdersHistory(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('core.CustomUser', on_delete=models.CASCADE, null=True, blank=True)
    order_data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
```

- OrderStatus (WIP) (.../models/order_status.py):
```python
class OrderStatus(models.TextChoices):
    PENDING = 'PENDING', 'Pending'
    COMPLETED = 'COMPLETED', 'Completed'
    CANCELLED = 'CANCELLED', 'Cancelled'
```



## Інше
- Використовується система шаблонів Jinja2.


## Пояснення
- ...
- В майбутньому буде доданий Docker файл для контейнеризації проєкту.
