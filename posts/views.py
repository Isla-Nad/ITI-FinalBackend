from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json 
# steps to create API 
from posts.models import Post
from rest_framework.decorators import api_view
from rest_framework.response import Response
from posts.serializers import PostSerializer
from rest_framework import status
#*******************
@api_view(['GET','POST'])
def try1(request):
    if request.method=="POST":
        return Response({"message":"POST method"})
    return Response({"message":"GET method"})

# @csrf_exempt
# def test(request):
#     if request.method=="POST":
#         request_data=json.loads(request.body)
#         return JsonResponse({"data":"post request recieved", "data":request_data})
#     return JsonResponse({"data":"accepted", "message":"GET reuest"})

#**************************get all posts**********************
@api_view(['GET','POST'])
def index(request):
    if request.method=='POST':
        #post posts
        post=Post.objects.create(creator=request.data['creator'],
                                 title=request.data['title'],
                                 body=request.data['body'],
                                 image=request.data['image'])
        post.save()
        return Response({"post":PostSerializer(post).data})
    elif request.method=='GET':
        #get all objects
        posts = Post.get_all_posts()
        serialized_posts=PostSerializer(posts, many=True)
        # for post in posts:
        #     print(PostSerializer(post).data)
        #     serialized_posts.append(PostSerializer(post).data)
        return Response({"posts":serialized_posts.data})

#*******************************************
@api_view(['GET','PUT','DELETE'])
def post_resource(request,id):
   
    post = Post.get_specific_post(id)
   
    if post and request.method == 'PUT':
        serialized_post=PostSerializer(data=request.data, instance=post)
       
        if serialized_post.is_valid():
            serialized_post.save()
            return Response({'post':serialized_post.data}, status=200)
        return Response ({"errors":serialized_post.errors},status=status.HTTP_400_BAD_REQUEST)
    
    elif post and request.method == 'DELETE':
        post.delete()
        return Response({"message":"post deleted successfully!"}, status=status.HTTP_204_NO_CONTENT)
   
    elif post and request.method =='GET': #get specific element
        serialized_post=PostSerializer(post)
        return Response({'data':serialized_post.data}, status=status.HTTP_200_OK)
   
    else:
        return Response({"message":"No Posts Available!"}, status=status.HTTP_205_RESET_CONTENT)



#create api for posts
# @csrf_exempt
# def index(request):
#     #creation
#     if request.method=="POST":
#         request_data=json.loads(request.body)
#         post=Post()
#         post.creator=request_data['creator']
#         post.title=request_data['title']
#         post.body=request_data['body']
#         post.image=request_data['image']
#         post.save()
#         return JsonResponse({"status:":"success"})
#     posts=Post.objects.all()
#     serialized_posts=[]
#     for post in posts:
#         serialized_posts.append({"id":post.id,"title":post.title})
#     return JsonResponse({"data":serialized_posts})