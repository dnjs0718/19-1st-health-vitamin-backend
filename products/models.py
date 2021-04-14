from django.db    import models

class Menu(models.Model):
    name = models.CharField(max_length=45)
    class Meta:
        db_table = 'menus'

class MainCategory(models.Model):
    menu = models.ForeignKey(Menu, on_delete= models.SET_NULL, null=True)
    name = models.CharField(max_length=45)
    class Meta:
        db_table = 'main_categories'

class SubCategory(models.Model):
    main_categories = models.ForeignKey(MainCategory, on_delete= models.SET_NULL, null=True)
    name            = models.CharField(max_length=45)
    class Meta:
        db_table = 'sub_categories'

class Discount(models.Model):
    rate = models.PositiveIntegerField()
    class Meta:
        db_table = 'discounts'

class ShippingFee(models.Model):
    price        = models.PositiveIntegerField()
    minimum_free = models.PositiveIntegerField()
    class Meta:
        db_table = 'shipping_fees'

class Product(models.Model):
    name          = models.CharField(max_length=45)
    price         = models.PositiveIntegerField()
    detail        = models.TextField()
    stock         = models.PositiveIntegerField()
    expired_at    = models.DateField()
    is_hit        = models.BooleanField(default=0)
    is_option     = models.BooleanField(default=0)
    discounts     = models.ForeignKey('Discount',on_delete=models.SET_NULL, null=True)
    shipping_fees = models.ForeignKey('ShippingFee', on_delete=models.SET_NULL, null=True)
    sub_cateories = models.ManyToManyField('SubCategory',through='SubCategory_Product')
    options       = models.ManyToManyField('self',through='Option',symmetrical=False)
    class Meta:
        db_table = 'products'

class Option(models.Model):
    products = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='main_product', null=True)
    options  = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='main_product_option')
    class Meta:
        db_table = 'options'

class SubCategory_Product(models.Model):
    sub_categories = models.ForeignKey('SubCategory', on_delete=models.SET_NULL, null=True)
    products       = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True)
    class Meta:
        db_table = 'sub_category_products'

class Image(models.Model):
    products  = models.ForeignKey('Product',on_delete=models.CASCADE)
    image_url = models.URLField()
    class Meta:
        db_table = 'images'








    


