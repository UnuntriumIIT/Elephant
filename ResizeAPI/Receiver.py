import pika
import io
import uuid
import signal
import psycopg2
import PIL.Image as Image

signal.signal(signal.SIGINT, signal.SIG_DFL)

connection = pika.BlockingConnection(pika.ConnectionParameters('127.0.0.1'))
channel = connection.channel()

channel.queue_declare(queue='resizequeue' , durable=True)

print('\nWaiting for messages. To exit press CTRL+C\n');

def callback(ch, method, properties, body):
    params = body.decode('utf-8').split(';')
    id = params[0]
    if (id == '00000000-0000-0000-0000-000000000000'):
        print('it is zero uuid')
    else:
        conn = psycopg2.connect(user="postgres",
                                password="admin",
                                host="127.0.0.1",
                                port="5432",
                                database="elephant")
        cur = conn.cursor()
        
        
        
        cur.execute('select "Image" from public."Img" where "Id"=\''+id+'\'')
        image = cur.fetchone()[0]
        
        newId = str(uuid.uuid4())
        newImage = resizeImage(image, params[1], params[2])
        img_byte_arr = io.BytesIO()
        newImage.save(img_byte_arr, "JPEG")
        imgByteArr = psycopg2.Binary(img_byte_arr.getvalue())
        
        cur.execute(f'INSERT INTO public."Img" VALUES (\'{newId}\', {imgByteArr}, \'resized\', {params[1]}, {params[2]}, \'00000000-0000-0000-0000-000000000000\')')
        cur.execute(f'UPDATE public."Img" SET "ParentId" = \'{newId}\' WHERE "Id" =  \'{id}\'')
        conn.commit()
        cur.close()
        conn.close()
        
        print("I got ID: " + id+"\nNew ID is: "+str(newId))
        
        ch.basic_ack(delivery_tag = method.delivery_tag)
    
def resizeImage(img, w, h):
    image = Image.open(io.BytesIO(img))
    newSize = (int(w), int(h))
    return image.resize(newSize, Image.ANTIALIAS)

channel.basic_consume(queue='resizequeue', on_message_callback=callback, auto_ack=False)

channel.start_consuming()