from django.db import models


class ReduceProcentPrice(models.Model):
    reduce_procent = models.IntegerField(
        verbose_name="Кол-во %", help_text="Уменьшить цену всех продуктов на n-ое кол-во процентов.")

    class Meta:
        verbose_name = ('Уменьшить цену продуктов')

    def __str__(self):
        return f"{self.id} - уменьшить"
