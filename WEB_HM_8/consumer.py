import pika
import json
import time
from mongoengine import connect
from models import Contact
from connect import *


connect(
    host=uri, ssl=True)

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='contacts_queue')


def send_email(contact_id):
    # Імітація надсилання email
    print(f"Відправлено email контакту з ID {contact_id}")

    # Позначаємо контакт як відправленого
    contact = Contact.objects(id=contact_id).first()
    if contact:
        contact.is_sent = True
        contact.save()


def callback(ch, method, properties, body):
    message = json.loads(body)
    contact_id = message.get('contact_id')

    if contact_id:
        send_email(contact_id)

    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_consume(queue='contacts_queue', on_message_callback=callback)

print("Очікування повідомлень з черги RabbitMQ. Для виходу натисніть CTRL+C")
channel.start_consuming()
