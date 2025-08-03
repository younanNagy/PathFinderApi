from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Node
from celery.result import AsyncResult
from .PathService import findPath
from .tasks import slow_find_path_task
from django.conf import settings

class CreateNode(APIView):
    def post(self, request):
        name = request.data.get('name')
        child_name = request.data.get('child')

        if not name:
            return Response({'error': 'Name is required'}, status=status.HTTP_400_BAD_REQUEST)

        child = Node.objects.filter(name=child_name).first() if child_name else None
        node, created = Node.objects.get_or_create(name=name, defaults={'child': child})
        if not created and child:
            node.child = child
            node.save()
        return Response({
            'name': node.name,
            'child': node.child.name if node.child else None
        }, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)

class FindPath(APIView):
    def get(self, request):
        from_node = request.query_params.get('FromNode')
        to_node = request.query_params.get('ToNode')
        result = findPath(from_node, to_node)
        return Response({'path': result}, status=status.HTTP_200_OK)

class SlowFindPath(APIView):
    def post(self, request):
        print(settings.CELERY_BROKER_URL)
        from_node = request.data.get('FromNode')
        to_node = request.data.get('ToNode')
        task = slow_find_path_task.delay(from_node, to_node)
        return Response({'task_id': task.id}, status=status.HTTP_202_ACCEPTED)

class GetSlowPathResult(APIView):
    def get(self, request):
        task_id = request.query_params.get('task_id')
        if not task_id:
            return Response({'error': 'task_id required'}, status=status.HTTP_400_BAD_REQUEST)

        result = AsyncResult(task_id)
        if result.ready():
            return Response({'status': result.status, 'result': result.result})
        return Response({'status': result.status})