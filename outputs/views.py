from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework import generics, status
from .models import Output, OutputItem
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.validators import ValidationError
from django.core.serializers import serialize

class OutputViewset(ModelViewSet):
    serializer_class = OutputSerializer
    permission_classes = IsAuthenticated,
    queryset = Output.objects.all()

    def create(self, request, *args, **kwargs):
        items = request.data.pop('items', False)
        output = Output.objects.create(**request.data)
        if items:
            for item in items:
                o_item = OutputItem.objects.create(**item)
                o_item.output = output
                o_item.save()
        output.save()
        return Response({"success":True, "message":"Chiqim muvaffaqiyatli saqlandi"})

    def partial_update(self, request, *args, **kwargs):
        # 1 Umumiy Output malumotlarini yangilash ✔️
        # 2 OutputItem malumotlarini yangilash  ✔️
        # 3 Yangi OutputItem qo'shish ✔️

        output = Output.objects.get(id=kwargs['pk'])
        items = request.data.pop('items', False)
        if items:
            for item in items:
                object = OutputItem.objects.filter(id=item.pop('id', None))
                if object.exists():
                    object = object.last()
                    if object.output == output:
                        for key, value in item.items():
                            setattr(object, key, value)
                        object.save()
                else:
                    object = OutputItem.objects.create(**item)
                    object.output = output
                    object.save()

        super().partial_update(request, *args, **kwargs)
        return Response({"success":True, "message":"Chiqim malumotlari yangilandi"})

    def retrieve(self, request, *args, **kwargs):
        object = Output.objects.filter(id=kwargs.get('pk', None))
        if object.exists():
            return super().retrieve(request, *args, **kwargs)
        else:
            return Response({"success":False, "message":"Bunday chiqim malumotlari mavjud emas !"})
    
    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Response({"success":True, "message":"Chiqim malumotlari o'chirildi"})
