from confluent_kafka import Producer, Consumer, KafkaError
import random
import time

# Configuración del productor
producer_config = {
    'bootstrap.servers': 'localhost:9092',  # Reemplaza con la dirección de tu broker Kafka
}

# Configuración del consumidor
consumer_config = {
    'bootstrap.servers': 'localhost:9092',  # Reemplaza con la dirección de tu broker Kafka
    'group.id': 'my_consumer_group',        # Identificador de grupo del consumidor
    'auto.offset.reset': 'earliest'         # Comenzar desde el principio del topic
}

def produce_coordinates():
    producer = Producer(producer_config)
    topic = "Posicion"

    print("Prueba2")
    while True:
        # Genera coordenadas aleatorias
        latitude = random.uniform(-90, 90)
        longitude = random.uniform(-180, 180)
        message = f"{latitude}, {longitude}"

        # Envía las coordenadas al topic
        producer.produce(topic, key="coordenadas", value=message)
        producer.flush()
        print(f"Enviado: {message}")

        # Espera un tiempo antes de generar y enviar la siguiente coordenada
        time.sleep(1)

def consume_coordinates():
    consumer = Consumer(consumer_config)
    topic = "Posicion"

    consumer.subscribe([topic])

    while True:
        message = consumer.poll(1.0)

        if message is None:
            continue

        if message.error():
            if message.error().code() == KafkaError._PARTITION_EOF:
                print(f"Llegó al final de la partición: {message.partition()}")
            else:
                print(f"Error en el mensaje: {message.error()}")
        else:
            print(f"Recibido: {message.value().decode('utf-8')}")

if __name__ == "__main__":
    # Puedes ejecutar el productor y el consumidor en procesos separados
    # o en terminales separadas para simular la interacción entre ambos.
    #produce_coordinates()
    consume_coordinates()
