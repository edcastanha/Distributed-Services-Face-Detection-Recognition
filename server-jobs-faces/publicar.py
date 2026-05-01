import pika
import json
import logging
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class Publisher:
    def __init__(self):
        self.rabbitmq_host = os.environ.get('RABBITMQ_HOST', 'localhost')
        self.rabbitmq_port = int(os.environ.get('RABBITMQ_PORT', 5672))
        self.rabbitmq_user = os.environ.get('RABBITMQ_USER', 'guest')
        self.rabbitmq_pass = os.environ.get('RABBITMQ_PASS', 'guest')
        self.exchange = 'secedu'
        self.routing_key = 'path'

    def publish(self, payload: dict) -> bool:
        """
        Publica o payload na exchange secedu.
        Em caso de AMQPConnectionError, faz fallback para log sem quebrar o sistema.
        """
        credentials = pika.PlainCredentials(self.rabbitmq_user, self.rabbitmq_pass)
        parameters = pika.ConnectionParameters(
            host=self.rabbitmq_host,
            port=self.rabbitmq_port,
            credentials=credentials
        )
        
        try:
            connection = pika.BlockingConnection(parameters)
            channel = connection.channel()
            
            # Garante a existência da exchange
            channel.exchange_declare(exchange=self.exchange, exchange_type='direct', durable=True)
            
            message_body = json.dumps(payload)
            
            channel.basic_publish(
                exchange=self.exchange,
                routing_key=self.routing_key,
                body=message_body,
                properties=pika.BasicProperties(
                    delivery_mode=2,  # Tornar mensagem persistente
                )
            )
            
            logger.info(f"Publicado na exchange {self.exchange} com routing_key {self.routing_key}: {payload.get('path')}")
            connection.close()
            return True
            
        except pika.exceptions.AMQPConnectionError as e:
            logger.error(f"AMQPConnectionError: Nao foi possivel conectar ao RabbitMQ. Detalhes: {e}")
            return False
        except Exception as e:
            logger.error(f"Erro generico ao publicar mensagem: {e}")
            return False