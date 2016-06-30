from flask import Flask, request
import pika
import os

app = Flask(__name__)

@app.route('/',methods=['POST'])
def image():
	params = pika.URLParameters(os.getenv('AMQP_URL', 'amqp://localhost'))
	params.socket_timeout = os.getenv('SOCKET_TIMEOUT', 5)
	connection = pika.BlockingConnection(params)
	channel = connection.channel()
	channel.queue_declare(queue=os.getenv('CHANNEL_NAME', 'channel'))
	channel.basic_publish(exchange='', routing_key=os.getenv('CHANNEL_NAME', 'channel'), body=request.data)
	connection.close()
	return 'ok'

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=80)