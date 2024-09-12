import pika
import json
from frontend_api.book.models import Book, User
from django.conf import settings
from django.utils.dateparse import parse_date


def process_borrowed_books_updates(ch, method, properties, body):
    data = json.loads(body)
    event_type = data['event_type']
    book_data = data['book_data']

    try:
        if event_type == 'borrow':
            book = Book.objects.get(external_id=book_data['external_id'])
            book.title = book_data['title']
            book.author = book_data['author']
            book.publisher = book_data['publisher']
            book.category = book_data['category']
            book.is_available = book_data['is_available']
            if book_data['borrowed_by']:
                book.borrowed_by = User.objects.get(external_id=book_data['borrowed_by'])
            if book_data['borrowed_until']:
                book.borrowed_until = parse_date(book_data['borrowed_until'])
            book.save()
        
    except Book.DoesNotExist:
        pass
    except User.DoesNotExist:
        pass


def process_user_updates(ch, method, properties, body):
    data = json.loads(body)
    event_type = data['event_type']
    user_data = data['user_data']

    try:
        if event_type == 'add':
            User.objects.create(
                external_id=user_data['external_id'],
                email=user_data['email'],
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
            )
        elif event_type == 'update':
            user = User.objects.get(external_id=user_data['external_id'])
            user.email = user_data['email']
            user.first_name = user_data['first_name']
            user.last_name = user_data['last_name']
            user.save()
        elif event_type == 'delete':
            User.objects.filter(external_id=user_data['external_id']).delete()
    except User.DoesNotExist:
        pass


def start_user_update_consumer():
    connection = pika.BlockingConnection(pika.ConnectionParameters(settings.RABBITMQ_URL))
    channel = connection.channel()
    
    # Declaring the user_updates queue
    channel.queue_declare(queue='user_updates', durable=True)
    channel.basic_consume(queue='user_updates', on_message_callback=process_user_updates, auto_ack=True)
    
    # Declaring the book_updates queue
    channel.queue_declare(queue='book_updates', durable=True)
    channel.basic_consume(queue='book_updates', on_message_callback=process_borrowed_books_updates, auto_ack=True)
    
    # Start consuming messages from the queues
    channel.start_consuming()
