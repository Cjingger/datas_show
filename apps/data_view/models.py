from django.db import models

# Create your models here.
class PerDataCount(models.Model):

    dataNum = models.IntegerField(
        default=0,
        verbose_name="年份数据量"
    )
    dataBase = models.CharField(
        max_length=20,
        verbose_name="数据库名称"
    )
    year = models.IntegerField(
        default=0,
        verbose_name="年份"

    )

    class Meta():
        verbose_name = "各数据库每年数据量"

    def __str__(self):
        return f"{self.id}: {self.dataNum}{self.dataBase}"

