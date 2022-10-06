from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet,ViewSet
from rest_framework.response import Response
from rest_framework import authentication,permissions
from ekart.serializer import *
from rest_framework.decorators import action

# Create your views here.
class CategoryView(ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = [permissions.IsAdminUser]

    @action(methods=["POST"],detail=True)
    def add_product(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        cat=Category.objects.get(id=id)
        serializer=ProductSerializer(data=request.data,context={"category":cat})
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
    @action(methods=["GET"],detail=True)
    def products(self,request,*args,**kwargs):
        cid=kwargs.get("pk")
        cat=Category.objects.get(id=cid)
        products=cat.products_set.all()
        serializer=ProductSerializer(products,many=True)
        return Response(serializer.data)

class ProductsView(ViewSet):

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def list(self,request,*args,**kwargs):
        all_products=Products.objects.all()
        serializer=ProductSerializer(all_products,many=True)
        return Response(data=serializer.data)
    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        product=Products.objects.get(id=id)
        serializer=ProductSerializer(product,many=False)
        return Response(data=serializer.data)

    @action(methods=['POST'],detail=True)
    def add_to_cart(self,request,*args,**kwargs):
        pid=kwargs.get('pk')
        product=Products.objects.get(id=pid)
        user=request.user
        carts=Carts.objects.create(user=user,product=product)
        serializer=CartSerializer(data=request.data,context={'product':product,'user':user})
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)


    @action(methods=["POST"],detail=True)

    def add_review(self,request,*args,**kwargs):
        id=kwargs.get('pk')
        product=Products.objects.get(id=id)
        serializer=ReviewSerializer(data=request.data,context={'product':product,'user':request.user})
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)


class CartViews(ModelViewSet):
    queryset = Carts.objects.all()
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Carts.objects.filter(user=self.request.user)




    # def list(self, request, *args, **kwargs):
    #     carts=Carts.objects.filter(user=request.user)
    #     serializer=CartSerializer(carts,many=True)
    #     return Response(data=serializer.data)









#localhost:8000/ekart/categories/1/get_products/

#localhost:8000/ekart/carts/1/
# class CartsView(ModelViewSet):
    # serializer_class = CartSerializer
    # queryset = Carts.objects.all()
    #
    # def create(self, request, *args, **kwargs):
    #     id=kwargs.get("pk")
    #     pro=Products.objects.get(id=id)
    #     user=request.user
    #     Carts.objects.create(user=user,product=pro)
    #     return Response(data="created")