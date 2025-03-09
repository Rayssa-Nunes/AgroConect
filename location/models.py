from django.db import models

from accounts.models import CustomUser

class FairAddress(models.Model):
    address = models.CharField('Logradouro', max_length=128)
    district = models.CharField('Bairro', max_length=128)
    city = models.CharField('Cidade', max_length=128)
    state = models.CharField('Estado', max_length=2)
    cep = models.CharField('CEP', max_length=8)
    latitude = models.CharField('Latitude', max_length=128, blank=True, null=True)
    longitude = models.CharField('Longitude', max_length=128, blank=True, null=True)

    class Meta:
        verbose_name = 'Endereço da Feira'
        verbose_name_plural = 'Endereços da Feira' 

    def __str__(self):
        return f"{self.address}, {self.city} - {self.state}"


class Fair(models.Model):
    users = models.ManyToManyField(CustomUser, related_name='fairs')
    address = models.ForeignKey(FairAddress, related_name='fairs', on_delete=models.SET_NULL, null=True, blank=True, default=None)

    class Meta:
        verbose_name = 'Feira'
        verbose_name_plural = 'Feiras'

    def __str__(self):
        return f"{self.address}"


class FairDay(models.Model):
    DAYS_CHOICES = [
        ('seg', 'Segunda-feira'),
        ('ter', 'Terça-feira'),
        ('qua', 'Quarta-feira'),
        ('qui', 'Quinta-feira'),
        ('sex', 'Sexta-feira'),
        ('sab', 'Sábado'),
        ('dom', 'Domingo'),
    ]

    fair = models.ForeignKey('Fair', on_delete=models.CASCADE, related_name='fair_days', default=1)
    day = models.CharField(choices=DAYS_CHOICES, max_length=30)
    opening_time = models.TimeField(default='00:00:00')
    closing_time = models.TimeField(default='00:00:00')

    class Meta:
        verbose_name = 'Dia da Feira'
        verbose_name_plural = 'Dias das Feiras'
        # unique_together = ('address', 'day')

    def __str__(self):
        return f"{self.get_day_display()}  - {self.opening_time} to {self.closing_time}"
    