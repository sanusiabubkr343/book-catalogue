from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Book, User
from .serializers import BookSerializer, BorrowerSerializer,UserSerializer
from django.utils.timezone import now
from datetime import timedelta
from rest_framework import generics, mixins, status, viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import AllowAny


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    http_method_names = ["get","post","patch","put","delete"]
   

class BookViewSet(  mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,):
    queryset = Book.objects.filter(is_available=True).select_related('borrowed_by').all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['publisher', 'category']
    search_fields = [
        'author',
        'publisher',
        'category'
    ]
    ordering_fields = [
        'updated_at',
    ]
    permission_classes = [AllowAny]

    @action(detail=True, methods=['post'],serializer_class=BorrowerSerializer)
    def borrow(self, request, pk=None):
        book = self.get_object()

        serializer = BorrowerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_email = serializer.validated_data["user_email"]

        days = int(serializer.validated_data["days_to_be_used"])

        user, _ = User.objects.get_or_create(email=user_email)
        book.borrowed_by = user
        book.borrowed_until = now() + timedelta(days=days)
        book.is_available = False
        book.save()

        response = {
                "message": "Book  borrowed Successfully",
                **BookSerializer(instance=book).data,
            }
        return Response(data=response, status=status.HTTP_200_OK)
