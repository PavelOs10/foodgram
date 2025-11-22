from django.contrib import admin
from .models import Tag, Ingredient, Recipe, RecipeIngredient, Favorite, ShoppingCart

class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    min_num = 1

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'color')

@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    search_fields = ('name',)

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'count_favorites')
    list_filter = ('author', 'name', 'tags')
    search_fields = ('name', 'author__username')
    inlines = (RecipeIngredientInline,)

   
    def count_favorites(self, obj):
        return obj.favorites.count()
    count_favorites.short_description = 'В избранном'

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')

@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')