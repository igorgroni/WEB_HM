import pika
import json
from faker import Faker
from mongoengine import connect, Document, StringField, BooleanField
from models import Contact


connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='contacts_queue')


fake = Faker()

for _ in range(10):  
    full_name = fake.name()
    email = fake.email()

    
    contact = Contact(full_name=full_name, email=email)
    contact.save()


    message = {
        'contact_id': str(contact.id),
    }
    channel.basic_publish(
        exchange='', routing_key='contacts_queue', body=json.dumps(message))

print("Фейкові контакти створено та відправлено в чергу")
connection.close()

