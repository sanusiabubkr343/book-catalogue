import pytest
from django.urls import reverse
from rest_framework import status
from book.test.factories import UserFactory,AdminBookFactory,AdminBook

from unittest.mock import patch, MagicMock

pytestmark = pytest.mark.django_db
USER_LIST_URL = "book:user-list"
BOOK_LIST_URL = "book:adminbook-list"
BOOK_DETAIL_URL = "book:adminbook-detail"
USERS_WITH_BORROWED_BOOKS = "book:user-list-users-and-borrowed-books"





class TestProductEndpoints:
    
    @patch('pika.BlockingConnection')
    @patch('pika.URLParameters')
    def test_create_book(self, mock_url_parameters, mock_blocking_connection, api_client, admin_book_data):
        """Test creation of book"""

        # Mock the RabbitMQ connection and channel
        
        mock_blocking_connection.return_value = MagicMock()
        mock_blocking_connection.return_value.channel.return_value = MagicMock()
        # Mock the basic_publish method
        mock_blocking_connection.return_value.channel.return_value.basic_publish.return_value = None

        payload = admin_book_data
        url = reverse(BOOK_LIST_URL)
        response = api_client.post(url, payload)
        assert response.status_code == 201


    def test_delete_book(self,api_client, admin_book_data):
        
        """Test deleting of a product"""
        book = AdminBookFactory()
        
        url = reverse(BOOK_DETAIL_URL, kwargs={"pk": book.id})
        response = api_client.delete(url)
        assert response.status_code == 204



    def test_list_users_in_library(self, api_client):

        UserFactory(email='user1@exa.org')
        UserFactory(email='abubakr@exa.org')
        UserFactory(email='sanusi@exa.org')
        
        url = reverse(USER_LIST_URL)
        response = api_client.get(url)
        print(response)
        assert response.status_code == 200
        assert response.json()["total"] == 3



    def test_list_users_with_books_borrowed_in_library(self, api_client):
        user1 = UserFactory(email='user1@exa.org')
        user2 =  UserFactory(email='abubakr@exa.org')
        user3 =  UserFactory(email='sanusi@exa.org')

        AdminBookFactory.create_batch(2,borrowed_by=user1,is_available=False)
        AdminBookFactory.create_batch(3,borrowed_by=user1,is_available=True)
        AdminBookFactory.create_batch(2,borrowed_by=user2,is_available=False)
        AdminBookFactory.create_batch(2,is_available=False)
        print(AdminBook.objects.all())
        url = reverse(USERS_WITH_BORROWED_BOOKS)
        response = api_client.get(url)
        print(response)
        assert response.status_code == 200
        assert response.json()["total"] == 4



    # def test_get_book(self, api_client):
    #     """Test getting of a book"""
    #     book = BookFactory(is_available=True)
    #     url = reverse(BOOK_DETAIL_URL, kwargs={"pk": book.id})
    #     response = api_client.get(url)
    #     assert response.status_code == 200
    #     assert response.data["title"] == book.title
    #     assert response.data["author"] == book.author



    # def test_filter_books_by_publisher(self, api_client):

    #     BookFactory.create_batch(3,is_available=True,publisher='Mark Dan')
    #     BookFactory.create_batch(2,is_available=True,publisher='James')
    #     BookFactory.create_batch(2,is_available=False)
        
    #     url = reverse(BOOK_LIST_URL)
    #     publisher="James"
    #     joined_url = url + f"?publisher={publisher}"
    #     response = api_client.get(joined_url,format="json")
    #     assert response.status_code == 200
    #     assert response.json()["total"] == 2
    

    # def test_filter_books_by_category(self, api_client):

    #     BookFactory.create_batch(3,is_available=True,category='Mark Dan')
    #     BookFactory.create_batch(2,is_available=True,category='James')
    #     BookFactory.create_batch(2,is_available=False)
        
    #     url = reverse(BOOK_LIST_URL)
    #     category="James"
    #     joined_url = url + f"?category={category}"
    #     response = api_client.get(joined_url,format="json")
    #     assert response.status_code == 200
    #     assert response.json()["total"] == 2


    # def test_update_product(self, api_client,user_data):
    #     print(user_data)
    #     book = BookFactory(is_available=True)

    #     payload = {
    #     "user_email": user_data["email"],
    #     "days_to_be_used":7
        
    #      }
    #     url = reverse(BORROW_URL, kwargs={"pk": book.id})
    #     response = api_client.post(url, payload)
       
       
    #     book.refresh_from_db()

    #     assert response.status_code == 200
    #     assert book.borrowed_by != None
    #     assert book.is_available ==False
    #     assert book.borrowed_until != None
 
        