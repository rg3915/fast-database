from django.contrib.postgres.fields import JSONField
from django.db import models


class Shop(models.Model):
    name = models.CharField(max_length=50, unique=True)
    data = JSONField(null=True, blank=True)
    created = models.DateTimeField(
        'criado em',
        auto_now_add=True,
        auto_now=False
    )

    class Meta:
        verbose_name = 'compra'
        verbose_name_plural = 'compras'

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField('título', max_length=50)
    quantity = models.PositiveIntegerField('quantidade')

    class Meta:
        verbose_name = 'produto'
        verbose_name_plural = 'produtos'

    def __str__(self):
        return self.title
