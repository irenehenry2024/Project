
from django.contrib import admin
from .models import CustomUser
from django.contrib import admin
from . import models 
admin.site.register(CustomUser)
admin.site.register(models.Recipe)


from django import forms
from django.core.exceptions import ValidationError
from django.db.models import Q
from .models import Thread, ChatMessage
# Register your models here.
admin.site.register(ChatMessage)


class ChatMessage(admin.TabularInline):
    model = ChatMessage


class ThreadAdmin(admin.ModelAdmin):
    inlines = [ChatMessage]
    class Meta:
        model = Thread

admin.site.register(Thread, ThreadAdmin)
from django.contrib import admin
from .models import FoodCategory, Food, Image, FoodLog, Weight

class FoodAdmin(admin.ModelAdmin):
    list_display = ('food_name', 'quantity', 'calories', 'fat', 'carbohydrates', 'protein', 'category')
    list_filter = ('category',)
    search_fields = ('food_name', 'category__category_name')

class FoodLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'food_consumed')
    list_filter = ('user',)
    search_fields = ('user__username', 'food_consumed__food_name')

class WeightAdmin(admin.ModelAdmin):
    list_display = ('user', 'weight', 'entry_date')
    list_filter = ('user',)
    search_fields = ('user__username',)

admin.site.register(FoodCategory)
admin.site.register(Food, FoodAdmin)
admin.site.register(Image)
admin.site.register(FoodLog, FoodLogAdmin)
admin.site.register(Weight, WeightAdmin)

