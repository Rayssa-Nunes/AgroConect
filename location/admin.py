from django.contrib import admin
from location.models import Fair, FairAddress, FairDay

@admin.register(FairAddress)
class FairAddressAdmin(admin.ModelAdmin):
    list_display = ('address', 'city', 'state', 'cep') 


class FairUsersInline(admin.TabularInline):  
    model = Fair.users.through
    extra = 1


@admin.register(Fair)
class FairAdmin(admin.ModelAdmin):
    inlines = [FairUsersInline]
    list_display = ('id', 'address')  # Agora exibe todas as feiras
    search_fields = ('address__address', 'address__city')  # Permite busca por endereço
    list_filter = ('address',)  # Adiciona filtro por endereço

    # exclude = ('users',)
    # list_display = ('id', 'user', 'address') 
    # search_fields = ('user__username', 'address__street')  
    # list_filter = ('address',) 


@admin.register(FairDay)
class FairDayAdmin(admin.ModelAdmin):
    list_display = ('fair', 'day', 'opening_time', 'closing_time')
    list_editable = ('day', 'opening_time', 'closing_time')