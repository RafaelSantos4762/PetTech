from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Produto


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Produto
        fields = ['id_produto','descricao']

