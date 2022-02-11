import pika
import signal
import psycopg2

# Clean exit on CTRL+C
signal.signal(signal.SIGINT, signal.SIG_DFL)

# Connect to amqp server on 'localhost'
connection = pika.BlockingConnection(pika.ConnectionParameters('127.0.0.1'))
channel = connection.channel()

# Create queue 'hello'
channel.queue_declare(queue='resizequeue' , durable=True)

print('\nWaiting for messages. To exit press CTRL+C\n');

def callback(ch, method, properties, body):
    conn = psycopg2.connect(user="postgres",
                            password="admin",
                            host="127.0.0.1",
                            port="5432",
                            database="elephant")
    cur = conn.cursor()
    id = body.decode('utf-8').split(';')[0]
    # cur.execute('select "Image" from public."Img" where "Id"=\''+id+'\'')
    # image = cur.fetchone()[0]
    cur.close()
    conn.close()
    print("I got ID: " + id)
    

# Setup consume method for message on queue 'hello'
channel.basic_consume(queue='resizequeue', on_message_callback=callback, auto_ack=True)

# Start consuming
channel.start_consuming()