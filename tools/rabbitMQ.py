import pika
import json
from tools.ReadConfig import ReadConfig

host, user, password, virtual_host, exchange, port = ReadConfig.read_mq_info()


class MQHandler():
    def __init__(self):
        credentials = pika.PlainCredentials(user, password)
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=host, port=port, virtual_host=virtual_host, credentials=credentials))
        self.connection = connection

    def channel_cr(self):
        channel = self.connection.channel()
        channel.exchange_declare(exchange=exchange, durable=True, exchange_type='direct')
        return channel

    def push(self, routing_key, message):
        if isinstance(message, (list, dict)):
            message = json.dumps(message)
        channel = self.channel_cr()
        channel.basic_publish(exchange=exchange, routing_key=routing_key, body=message,
                              properties=pika.BasicProperties(delivery_mode=2))
        self.connection.close()

    def consume(self, queue, routing_key, callback):
        channel = self.channel_cr()
        queue_obj = channel.queue_declare(queue=queue, durable=True)
        channel.queue_bind(exchange=exchange, queue=queue_obj.method.queue, routing_key=routing_key)
        channel.basic_consume(queue_obj.method.queue, callback, auto_ack=False)
        channel.start_consuming()


if __name__ == "__main__":
    def callback(channel, method, properties, body):
        channel.basic_ack(delivery_tag=method.delivery_tag)
        print(body.decode())


    mq = MQHandler()
    mq.consume("report_p", "key", callback=callback)

