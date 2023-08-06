django-discounts-cart
=====================

Приложение для Django - Управление скидками и корзиной в интернет
магазине.

version 1.1.7

Django >= 1.7 и Python 2.7

Скидки добавляются через админ-панель.

Скидки можно будет добавить на каждую категорию и продукт.

Также можно настроить поведение скидок.


Установка:
~~~~~~~~~~

::

    1) pip install django-discounts-cart

    2) Добавьте в INSTALLED_APPS
        'discounts_cart',

    3) Добавьте в context_processors
        'discounts_cart.context_processors.vars_cart',

    4) Добавьте discounts-cart в urls.py вашего проекта
        url(r'^cart/', include('discounts_cart.urls', namespace='discounts_cart')),

    5) Добавьте в проект
        jquery.cookie.js --> http://plugins.jquery.com/cookie/
        cart.js          --> https://github.com/genkosta/django-discounts-cart/blob/master/cart.js
        templates/discounts_cart/in_cart_link.html --> https://github.com/genkosta/django-discounts-cart/tree/master/templates/discounts_cart

    6) Обновить миграции
        python manage.py migrate discounts_cart


В приложении для определенного типа товара, создаем модели
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    В приложениях не забываем настраивать __init__.py и apps.py
    Пример:
        __init__.py
            default_app_config = 'products.apps.ProductsConfig'
        
        apps.py
            from django.apps import AppConfig
            
            class ProductsConfig(AppConfig):
                name = 'products'
                verbose_name = 'Products'


    Пример настройки моделей:
    ( для примера, можно посмотреть здесь --> https://github.com/genkosta/django-discounts-cart/tree/master/examples )

    from django.db import models
    from discounts_cart.models import DiscountsInCategories, DiscountsInProducts

    class Brand(DiscountsInCategories):
        pass

    class Category(DiscountsInCategories):
        pass

    class Parameter(DiscountsInCategories):
        pass

    # Product - Обязательное название модели, во всех приложениях товаров
    class Product(DiscountsInProducts):
        brand = models.ForeignKey(Brand)
        categories = models.ManyToManyField(Category)
        parameters = models.ManyToManyField(Parameter)
        
    # Обязательный метод
    def view_price(self):
        pattern = re.compile(r'\.[0]+$')
        return '{0} {1}'.format(pattern.sub('', str(self.price)), self.currency)
    view_price.short_description = _('Price')

    # Обязательный метод
    @property
    def get_correct_price(self):
        return self.price  # Only Decimal type

    # Add names of fields to calculate discounts
    # Обязательный метод
    @staticmethod
    def get_field_names():
        field_names_dect = {
            'foreign_key': ('brand',),
            'many_to_many': ('categories', 'parameters')
        }
        return field_names_dect

Добавляем в шаблоны
~~~~~~~~~~~~~~~~~~~

base.html
^^^^^^^^^

::

    <!-- Cart -->
    <div id="id_cart">
      <div><strong>Cart</strong></div>
        <span>count:</span>&ensp;<span class="cart_count">{{ cart_count }}</span><br>
        <span>amount:</span>&ensp;<span class="cart_amount">{{ cart_amount }}</span><br>
        {% url 'discounts_cart:view_cart' as cart_url %}
        <a href="{% if cart_count %}{{ cart_url }}{% else %}javascript:void(0);{% endif %}"
           class="cart_view_product_list" data-cart_url="{{ cart_url }}">
            <img src="{% static 'img/cart.png' %}"><br><span>Open</span></a>
    </div>

    <a href="{% url 'home' %}">Home</a>&emsp;
    <a href="{% url 'home' %}?sort_by_optimal_discount=1">Sort by optimal discount</a>
    
home.html
^^^^^^^^^

::

    {% extends 'base.html' %}
    {% load staticfiles discounts_cart %}
    
    
    {% block content %}
      <!-- View products -->
      {% for product in products %}
        <div>
          <p>
              Product: {{ product.name }}<br>
              Discount {{ product.view_optimal_discount }}<br>
              Price: {{ product.view_price }} < > {{ product.view_optimal_price }} {{ product.currency }}
          </p>
    
          {% cart_add_select_product 'products' 'product' product.id 'In cart' 'From cart' flag_img=True %}
        </div>
        <br>
      {% endfor %}
    
      <!-- Возможные варианты использования шаблонного тега cart_add_select_prod -->
      {% comment %}
          {% cart_add_select_product 'app' 'model' prod_id 'In cart' 'From cart' %}
              or
          {% cart_add_select_product 'app' 'model' prod_id 'In cart' 'From cart' flag_img=True %}
              or
          {% cart_add_select_product 'app' 'model' prod_id flag_img=True %}  <!-- only images -->
      {% endcomment %}
    
      <!-- README
        Аргументы для шаблонного тега - cart_add_select_prod_*:
            1) app  - ( имя приложения )
            2) model  - ( класс модели )
            3) prod_id  - ( ID товара - Пример: product.id)
            4) name_in_cart default=''  - ( Название ссылок или кнопок - Пример: 'In cart' )
            5) name_from_cart default=''  - ( Название ссылок или кнопок - Пример: 'From cart' )
            6) add_more_name default='Add more'  - ( Название ссылок для увеличения количества того же продукта )
            7) flag_img - default=False - ( логический флаг, позволяет отображать иконки на ссылках или кнопках,
                                            настройка изображений через классы - cart_img_in, cart_img_from )
    
        Classes ( для настройки внешнего вида, ссылок и кнопок - 'In cart' и 'From cart' ):
            1) cart_controls  - ( обертка <div> для ссылок и кнопок )
            2) cart_item_select_product  - ( для настройки ссылок и кнопок - 'In cart' и 'From cart' )
            3) cart_img_in, cart_img_from  - ( для настройки иконок на ссылках и кнопках, если добавлен flag_img=True )
    
        CSS:
        <style type="text/css">
            .cart_add_more_product {  // обязательно добавить в стили <<<
              display: none;
            }
    
            .cart_add_more_product_active {  // обязательно добавить в стили <<<
              display: block;
            }
    
            // Добавить если используется flag_img=True
            .cart_img_in, .cart_img_from {
              display: block;
              width: 40px;
              height: 40px;
              background-size: cover;
            }
    
            .cart_img_in {
              background: url("../img/in_cart.png") no-repeat center;  // добавьте свою иконку
            }
    
            .cart_img_from  {
              background: url("../img/from_cart.png") no-repeat center;  // добавьте свою иконку
            }
        </style>
      -->
    {% endblock %}

cart.html
^^^^^^^^^

::

    {% extends 'base.html' %}
    {% load staticfiles %}
    
    
    {% block content %}
      <!-- Products list -->
      {% for product in products %}
        <p>
            Product: {{ product.name }}<br>
            Count: {{ product.count }}<br>
            Price: {{ product.view_optimal_price }} {{ product.currency }}
        </p>
      {% endfor %}
    
      <p>_ _ _ _ _ _ _ _ _ _</p>
    
      <!-- Total amount -->
      <p>Итого</p>
      <p>Total count:&ensp;<span class="cart_count">{{ cart_count }}</span></p>
      <p>Total amount:&ensp;<span class="cart_amount">{{ cart_amount }}</span></p>
      {% if cart_count %}
    
      <p>_ _ _ _ _ _ _ _ _ _</p>
    
      <!-- Recalculate with a promo-code -->
      <P>Пересчитать с промо-кодом</P>
      <p>Total count:&ensp;<span class="cart_count_recalculation">0</span></p>
      <p>Total amount:&ensp;<span class="cart_amount_recalculation">0</span></p>
      <form id="id_cart_check_promo_code_form" action="{% url 'discounts_cart:recalculation_cart_with_promo_code' %}" method="post">
        <input id="id_cart_promo_code_text" type="text" name="promo_code" value="" placeholder="Enter promo-code">
        <button>Recalculation</button>
      </form>
    
      <p>_ _ _ _ _ _ _ _ _ _</p>
    
      <!-- Payment -->
      <p>Платеж</p>
      <form id="id_cart_payment_form" action="{% url 'payments' %}" method="post">{% csrf_token %}
        <input id="id_cart_promo_code_text" type="text" name="promo_code" value="" placeholder="Enter promo-code, if present">
        <button>Payment</button><br>
        <label for="id_cart_promo_code_text">( Если промо-код не подходит, он будет не учтен. )</label>
      </form>
      {% endif %}
    {% endblock %}

Для сортировки по оптимальным скидкам
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    Пример:
    
    home views.py
        
    from products.models import Product  # или Phone или Стиральные машины
    
    def home(request):
    
        if request.GET.get('sort_by_optimal_discount', False):
            # Выборка всех активных, плюс сортировка по оптимальным скидкам
            products = Product.products.sort_by_optimal_discount()
        else:
            # Выборка всех активных
            products = Product.products.active()
            # или
            # products = Product.objects.filter(active=True)
    
        return render(request, 'home.html', {
            'products': products
        })

Для контроля над скидками, после завершения оплаты, добавить
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

( Если промо-коды настроены как удаляемые, они будут удалятся. )

::

    Пример:
    
    payment views.py
    
    from discounts_cart.utils import control_promo_codes, recalculation_payment

    def payment(request):

        if request.method == 'POST':
        
            # Recalculation before payment ( for checking )
            result = recalculation_payment(request)
            count_products = result['count']
            amount = result['amount']
            
            # Control promo-codes
            promo_code = request.POST['promo_code'].strip()
            control_promo_codes(request, promo_code)

Cron
~~~~

( По желанию, добавить комманды в Cron. )

::

    # Деактивировать использованные скидки
    python manage.py discounts_cart deact
    или
    # Удалить использованные скидки
    python manage.py discounts_cart del
