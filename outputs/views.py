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


    # def retrieve(self, request, *args, **kwargs):
    #     output = Output.objects.filter(id=kwargs.get('pk', None))
    #     if output.exists():
    #         out = output.last()
    #         returning = [

    #         ]
    #         print(returning)
    #         # output_items = OutputItem.objects.filter(output=out)
    #         # if output_items.exists():
    #         #     items = []
    #         #     for item in output_items:
    #         #         items.append(serialize('json', [item]))
    #         #     returning['items'] = items  
    #         return Response(returning)  
    #     return Response({"success":False, "message":"Berilgan id raqam bo'yicha xarajat mavjud emas !"})
    
# class OutputItemViewset(ModelViewSet):
#     serializer_class = OutputItemSerializer
#     permission_classes = IsAuthenticated,
#     queryset = OutputItem.objects.all()

#     def create(self, request, *args, **kwargs):
#         output = Output.objects.filter(id=self.request.data.get('output_id', None))
#         print("23", request.data)
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid()
#         if output.exists():
#             print(serializer.validated_data)
#             object = OutputItem.objects.create(**serializer.validated_data)
#             object.output = output.last()
#             object.save()
#             return Response({"success":True, 'message':"Obyekt muvaffaqiyatli yasaldi"})
#         raise ValueError({"success":False, "message":"Output kiritilmadi"})

    