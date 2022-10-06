from django.shortcuts import render
from rest_framework.viewsets import ViewSet,ModelViewSet
from api.serializer import PostSerializer,UserSerializer,CommentSerializer
from rest_framework.response import Response
from api.models import Posts
from rest_framework import authentication,permissions
from rest_framework.decorators import action


class PostViews(ViewSet):
    # authentication_classes = [authentication.BasicAuthentication]
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def list(self,request,*args,**kwargs):
        qs=Posts.objects.all()
        serializer=PostSerializer(qs,many=True)
        return Response(data=serializer.data)


    def create(self,request,*args,**kwargs):
        serializer=PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return  Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)

    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Posts.objects.get(id=id)
        serializer=PostSerializer(qs)
        return Response(data=serializer.data)


    def update(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Posts.objects.get(id)
        serilizer=PostSerializer(instance=qs,data=request.data)
        if serilizer.is_valid():
            serilizer.save()
            return  Response(data=serilizer.data)
        else:
            return Response(data=serilizer.errors)


    def destroy(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Posts.objects.get(id)
        qs.delete
        return Response({"msg":"deleted"})


class UsersView(ViewSet):
    def create(self,request,*args,**kwargs):
        serializer=UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)

class PostModelView(ModelViewSet):
    serializer_class = PostSerializer
    queryset = Posts.objects.all()
    # authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]


    def create(self,request,*args,**kwargs):
        serializer=PostSerializer(data=request.data,context={"usr":request.user})
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)

    @action(methods=['GET'],detail=False)
    def my_post(self,request,*args,**kwargs):
        user=request.user
        qs=user.post.all()
        serializer=PostSerializer(qs,many=True)
        return Response(data=serializer.data)


    @action(methods=['GET'],detail=True)
    def get_comments(self,request,*args,**kwargs):
        pst_id=kwargs.get('pk')
        pst=Posts.objects.get(id=pst_id)
        cmt=pst.comments_set.all()
        searializer=CommentSerializer(cmt,many=True)
        return Response(data=searializer.data)

    @action(methods=['GET'],detail=True)
    def post_comments(self,request,*args,**kwargs):
        id=kwargs.get('pk')
        pst=Posts.objects.get(id=id)
        serializer=CommentSerializer(data=request.data,context={'user':request.user,'post':pst})
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)

    @action(methods=["POST"],detail=True)
    def add_like(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        pst=Posts.objects.get(id=id)
        user=request.user
        pst.liked_by.add(user)
        return Response(data="ok")

    @action(methods=["GET"], detail=True)
    def get_like(self,request,*args,**kwargs):
        id = kwargs.get("pk")
        pst = Posts.objects.get(id=id)
        cnt=pst.liked_by.all().count()
        return Response(data=cnt)



