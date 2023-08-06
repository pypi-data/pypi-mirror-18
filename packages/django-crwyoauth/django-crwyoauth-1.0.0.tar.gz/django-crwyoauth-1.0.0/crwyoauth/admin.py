from django.contrib import admin
from .models import CrwyoauthConfig

# Register your models here.


@admin.register(CrwyoauthConfig)
class CrwyoauthConfigAdmin(admin.ModelAdmin):
    list_display = ('oauth_to', 'authorize_url', 'client_id', 'client_secret', 'call_back')
    list_filter = ('oauth_to',)
