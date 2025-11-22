from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.db.models import Sum
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from recipes.models import Ingredient, Recipe, Tag, Favorite, ShoppingCart, RecipeIngredient
from .serializers import (
    IngredientSerializer, RecipeReadSerializer, RecipeWriteSerializer, 
    TagSerializer, RecipeShortSerializer
)
from .pagination import CustomPagination
from .filters import IngredientFilter, RecipeFilter
from .permissions import IsOwnerOrAdmin

class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny,)
    pagination_class = None

class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AllowAny,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter
    pagination_class = None

class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (IsOwnerOrAdmin,)
    pagination_class = CustomPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RecipeReadSerializer
        return RecipeWriteSerializer

    def _add_to_model(self, request, pk, model):
        recipe = get_object_or_404(Recipe, id=pk)
        if model.objects.filter(user=request.user, recipe=recipe).exists():
            return Response({'errors': 'Уже добавлено'}, status=status.HTTP_400_BAD_REQUEST)
        model.objects.create(user=request.user, recipe=recipe)
        serializer = RecipeShortSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def _remove_from_model(self, request, pk, model):
        recipe = get_object_or_404(Recipe, id=pk)
        obj = model.objects.filter(user=request.user, recipe=recipe)
        if obj.exists():
            obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({'errors': 'Объект не найден'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post', 'delete'], permission_classes=[IsAuthenticated])
    def favorite(self, request, pk):
        if request.method == 'POST':
            return self._add_to_model(request, pk, Favorite)
        return self._remove_from_model(request, pk, Favorite)

    @action(detail=True, methods=['post', 'delete'], permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, pk):
        if request.method == 'POST':
            return self._add_to_model(request, pk, ShoppingCart)
        return self._remove_from_model(request, pk, ShoppingCart)

    @action(detail=False, permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        ingredients = RecipeIngredient.objects.filter(
            recipe__shopping_cart__user=request.user
        ).values(
            'ingredient__name', 'ingredient__measurement_unit'
        ).annotate(total=Sum('amount')).order_by('ingredient__name')

        shopping_list = 'Список покупок:\n\n'
        for item in ingredients:
            shopping_list += f"{item['ingredient__name']} ({item['ingredient__measurement_unit']}) — {item['total']}\n"

        response = HttpResponse(shopping_list, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename="shopping_cart.txt"'
        return response