# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models

from apps.curso.models import Curso
from apps.pagseguro.api import PagSeguroItem


class Product(models.Model):
    name = models.CharField('Nome', max_length=100)
    price = models.DecimalField('Preço', decimal_places=2, max_digits=100)


class OrderProduct(models.Model):
    product = models.ForeignKey(Curso, on_delete=models.CASCADE)
    price = models.DecimalField('Preço', decimal_places=2, max_digits=100)
    quantity = models.IntegerField('Quantidade')

    def to_pagseguro(self):
        return PagSeguroItem(
            id=self.product.id,
            description=self.product.nome,
            amount=self.price,
            quantity=self.quantity
        )


class Order(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(OrderProduct, blank=True)
