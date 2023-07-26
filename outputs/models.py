from django.db import models
from accounts.models import Kitchen

class Output(models.Model):
    name = models.CharField(max_length=50, verbose_name='Chiqim nomi')
    kitchen = models.ForeignKey(Kitchen, on_delete=models.CASCADE, verbose_name='Oshxona')
    description = models.CharField(max_length=500, blank=True, null=True, verbose_name='Batafsil')
    is_product = models.BooleanField(default=False, verbose_name="Maxsulot olindimi")
    cost = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Chiqim umumiy summasi', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Chiqim vaqti')    

    @property
    def get_cost(self):
        items = OutputItem.objects.filter(output=self)
        cost = 0
        for i in items:
            cost += i.price         
        return cost if self.is_product == True else self.cost
    
    def __str__(self) -> str:
       return f"{self.name}, {self.get_cost}"
    
    
class OutputItem(models.Model):
    output = models.ForeignKey(Output, on_delete=models.SET_NULL, blank=True, null=True)
    product = models.CharField(max_length=50, verbose_name='Maxsulot nomi')
    description = models.CharField(max_length=500, blank=True, null=True, verbose_name="Batafsil")
    amount = models.CharField(max_length=25, verbose_name='Miqdori')
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Narxi') 

    def __str__(self) -> str:
        return f"{self.product} : {self.price}"