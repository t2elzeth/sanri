from rest_framework import generics, mixins

from .models import FileModel
from .serializers import FileModelSerializer


class FileModelAPIView(generics.CreateAPIView):
    queryset = FileModel.objects.all()
    serializer_class = FileModelSerializer


class FileModelDetailAPIView(mixins.DestroyModelMixin,
                             generics.GenericAPIView):
    queryset = FileModel.objects.all()
    serializer_class = FileModelSerializer

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
