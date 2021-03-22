"""
A silly service intended to return a random insult

"""
import json
import logging
import random

import pika

LOGGER = logging.getLogger(__name__)


_INSULTS = [
    "You're so dumb it took you 2 hours to watch 60 minutes.",
    "I'm jealous of all the people that haven't met you.",
    "I bet your brain feels as good as new, seeing that you never use it.",
    "You bring everyone a lot of joy, when you leave the room.",
    "You're as bright as a black hole, and twice as dense.",
    "Two wrongs don't make a right, take your parents as an example.",
    "You're the reason the gene pool needs a lifeguard.",
    "You have two brains cells, one is lost and the other is out looking for it.",
    "You shouldn't play hide and seek, no one would look for you.",
    "Some drink from the fountain of knowledge; you only gargled.",
    "If I gave you a penny for your thoughts, I'd get change.",
    "I can explain it to you, but I can't understand it for you.",
    "If you spoke your mind, you'd be speechless.",
    "I'll never forget the first time we met, although I'll keep trying."
]


def on_request(ch, method, props, body):
    decoded_body = json.loads(body.decode('utf-8'))

    response = {"hurt_em": ", ".join([decoded_body["name"], 
                _INSULTS[random.randint(0, len(_INSULTS) - 1)]])}

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id),
                     body=json.dumps(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)


if __name__ == "__main__":

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))

    channel = connection.channel()

    channel.queue_declare(queue='insults')

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='insults', on_message_callback=on_request)

    LOGGER.info("Consuming on insult queue")
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.stop_consuming()
