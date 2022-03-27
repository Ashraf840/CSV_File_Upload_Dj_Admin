from django.db import models



class TradeLog(models.Model):
    date = models.DateField(blank=True, null=True)
    trade_code = models.CharField(max_length=50, blank=True, null=True)
    high = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    low = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    open = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    close = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    volume = models.IntegerField(blank=True, null=True)

    def __str__(self) -> str:
        return self.trade_code
