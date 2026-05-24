from django.contrib import admin
from .models import Tweet

@admin.register(Tweet)
class TweetAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'text', 'created_at', 'updated_at')
    list_filter = ('created_at',)
    search_fields = ('text','user__username')
