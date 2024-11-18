from rest_framework import viewsets, permissions
from rest_framework.response import Response
from .models import Todo
from .serializers import TodoSerializer, TodoCreateUpdateSerializer
from rest_framework.decorators import action


class TodoViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TodoSerializer

    queryset = Todo.objects.all()
    
    serializer_class = TodoSerializer
    
    def get_queryset(self):
        return Todo.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['patch'])
    def mark_completed(self, request, pk=None):
        todo = self.get_object()
        todo.completed = True
        todo.save()
        return Response(TodoSerializer(todo).data)

