from ast import alias
import socket
import sys
import json


class Drone:
    def __init__(self):
        self.alias = None
        self.id = None
        self.token = None  # Inicialmente, el token estará en blanco

    def set_id(self, id):
        self.id = id
    
    def set_alias(self, alias):
        self.alias = alias

    def set_token(self, token):
        self.token = token


def enviar_operacion(opcion, alias, ad_registry_host, ad_registry_port, nuevo_alias, drone):
    # Crea un diccionario con la operación y el alias
    datos_operacion = {
        "opcion": opcion,
        "alias": alias
    }

    # Si estamos modificando el alias necesitaremos también pasar el nuevo alias
    if opcion == 1:
        datos_operacion["nuevo_alias"] = nuevo_alias

    # Convierte el diccionario a una cadena JSON
    datos_operacion_json = json.dumps(datos_operacion)

    # Crea un socket de cliente y se conecta al AD_Registry
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(ad_registry_host,ad_registry_port)
    # Se conecta al servidor de registro
    client_socket.connect((ad_registry_host, ad_registry_port))
    print("No")
    # Envía los datos de la operación al servidor AD_Registry
    client_socket.send(datos_operacion_json.encode('utf-8'))

    if opcion == 0:
        # Recibe el id y el token del servidor AD_Registry si la opción es 0
        response = client_socket.recv(1024).decode('utf-8')
        id, token = parse_response(response)
        
    # Cierra la conexión
    client_socket.close()

def parse_response(response):
    # Parsea la respuesta para obtener el id y el token
    # Esta función dependerá de cómo se formatea la respuesta en AD_Registry
    # Supongamos que la respuesta es de la forma "id: <id>, Token: <token>"
    parts = response.split(', ')
    id = parts[0].split(': ')[1]
    token = parts[1].split(': ')[1]
    return id, token

def mostrar_menu():
    print("Menú de opciones:")
    print("1. Modificar Alias del Dron")
    print("2. Dar de Baja el Dron")
    print("3. Unirse al Espectáculo (Sin Implementar)")
    print("4. Salir")


def main():

    

    if len(sys.argv) != 4:
        print("Uso: python AD_Drone.py <puerto_AD_Registry> <alias>")
        return



    ad_registry_port = int(sys.argv[1])
    alias = sys.argv[2]
    ad_registry_host = sys.argv[3]  

    print(ad_registry_host)

    # Imprime el valor del alias para verificar
    print(f"Alias a enviar: {alias}")

    drone = Drone() # Creamos la instancia del Drone sin atributos aún

    enviar_operacion(0, alias, ad_registry_host, ad_registry_port, "", drone)

    while True:
        mostrar_menu()
        opcion = input("Elija una opción: ")
        if opcion == "1":
            nuevo_alias = input("Ingrese el nuevo alias: ")
            enviar_operacion(1, alias, ad_registry_host, ad_registry_port, nuevo_alias, drone)
            drone.set_alias(nuevo_alias)
            print("Alias modificado exitosamente.")
        elif opcion == "2":
            enviar_operacion(2, alias, ad_registry_host, ad_registry_port, "", drone)
            print("Dron dado de baja exitosamente.")
        elif opcion == "3":
            print("Esta opción aún no está implementada.")
        elif opcion == "4":
            print("Saliendo del programa.")
            break
        else:
            print("Opción no válida. Por favor, elija una opción válida.")
    

if __name__ == '__main__':
    main()
