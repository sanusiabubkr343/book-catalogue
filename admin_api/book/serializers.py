from rest_framework import serializers
from .models import AdminBook,User

class AdminBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminBook
        fields = '__all__'

class AdminCreateBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminBook
        fields = '__all__'
        read_only_fields = ["id","borrowed_by","borrowed_until","created_at","updated_at","is_available"]


class UnavailableBooksSerializer(serializers.ModelSerializer):
    available_date = serializers.DateField(read_only=True,source='borrowed_until')
    class Meta:
        model = AdminBook
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']



class UsersAndBorrowedBooksSerializer(serializers.ModelSerializer):
    borrowed_books = AdminBookSerializer(many=True,source='books')
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name','borrowed_books']

     


