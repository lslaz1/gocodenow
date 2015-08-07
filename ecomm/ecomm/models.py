from django.db import models

class Order(models.Model):
    status = models.IntegerField()

class Product(models.Model):
	name = models.TextField()
	description = models.TextField()
	price = models.DecimalField(max_digits=6, decimal_places=2)
	orderproducts = models.ManyToManyField(Order, through='OrderProduct')

class OrderProduct(models.Model):
	order = models.ForeignKey(Order)
	product = models.ForeignKey(Product)
	quantity = models.IntegerField()