import socket
import sys
import uuid
import json
import re

def registrar_dron(file_name, registration_entry):
    with open(file_name, 'a') as f:
                print("Escribiendo en registro...")
                f.write(registration_entry)

def modificar_alias(file_name, alias_antiguo, nuevo_alias):
    # Leer todas las líneas del archivo
    with open(file_name, 'r') as f:
        lineas = f.readlines()

    alias_modificado = False

    # Crear una nueva lista de líneas con el alias modificado
    lineas_actualizadas = []
    for linea in lineas:
        if f'Alias: {alias_antiguo}' in linea:
            # Extraer el UID antiguo de la línea
            uid_antiguo = linea.split(',')[0].split(': ')[1].strip()
            # Crear una nueva línea con el UID y el nuevo alias
            nueva_linea = f'UID: {uid_antiguo}, Alias: {nuevo_alias}\n'
            lineas_actualizadas.append(nueva_linea)
            alias_modificado = True
        else:
            lineas_actualizadas.append(linea)

    # Si no se modificó el alias, mostrar un mensaje de error
    if not alias_modificado:
        print(f"No se encontró el dron con el alias antiguo '{alias_antiguo}'.")
    else:
        # Escribir las líneas actualizadas en el archivo
        with open(file_name, 'w') as f:
            f.writelines(lineas_actualizadas)
            alias_modificado = True

    if alias_modificado:
        print(f"Alias modificado exitosamente: {alias_antiguo} -> {nuevo_alias}")



def dar_de_baja(file_name, alias_a_dar_de_baja):
    # Leer todas las líneas del archivo
    with open(file_name, 'r') as f:
        lineas = f.readlines()

    dron_dado_de_baja = False

    # Crear una nueva lista de líneas sin la línea del dron a dar de baja
    lineas_actualizadas = [linea for linea in lineas if f'Alias: {alias_a_dar_de_baja}' not in linea]

    # Si el dron no se encontró en el registro, mostrar un mensaje de error
    if len(lineas) == len(lineas_actualizadas):
        print(f"No se encontró el dron con el alias '{alias_a_dar_de_baja}' para dar de baja.")
    else:
        # Escribir las líneas actualizadas en el archivo
        with open(file_name, 'w') as f:
            f.writelines(lineas_actualizadas)
            dron_dado_de_baja = True

    if dron_dado_de_baja:
        print(f"Dron con alias '{alias_a_dar_de_baja}' dado de baja exitosamente.")

    


def main():

    if len(sys.argv) != 3:
        print("Uso: python AD_Registry.py <puerto> <nombre_archivo>")
        return

    host = '0.0.0.0'  # Escucha en todas las interfaces
    port = int(sys.argv[1])  # Puerto de escucha proporcionado como argumento
    file_name = sys.argv[2]  # Nombre del archivo de registro proporcionado como argumento

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)  # Escucha hasta 5 conexiones simultáneas

    print(f'AD_Registry en espera en el puerto {port}')
    print(f'Registro de drones se guardará en {file_name}')

    try:
        while True:
            client_socket, addr = server_socket.accept()
            print(f'Conexión entrante desde {addr}')
            
            # Genera un UID único para el dron
            drone_uid = generar_uid_unico(file_name)
            
            # Recibe los datos del dron como una cadena JSON
            datos_dron = client_socket.recv(1024).decode('utf-8')
            
            # Convierte los datos en un diccionario JSON
            datos_dron_dict = json.loads(datos_dron)
            
            # Obtiene la opción y el alias del diccionario
            opcion = datos_dron_dict.get("opcion")
            alias = datos_dron_dict.get("alias")

            # Combina el UID y el alias para el registro
            registration_entry = f'UID: {drone_uid}, Alias: {alias}\n'

            if opcion == 0:
                # Realiza la operación de registro
                registrar_dron(file_name, registration_entry)
                print("Dron registrado exitosamente.")
            elif opcion == 1:
                # Realiza la operación de modificar el alias
                nuevo_alias = datos_dron_dict.get("nuevo_alias")
                modificar_alias(file_name, alias, nuevo_alias)
                print("Alias modificado exitosamente.")
            elif opcion == 2:
                # Realiza la operación de dar de baja el dron
                dar_de_baja(file_name, alias)
                print("Dron dado de baja exitosamente")
            
            client_socket.close()  # Cierra el socket del cliente
            

            client_socket.close()  # Cierra el socket del cliente

    except KeyboardInterrupt:
        print("AD_Registry se ha detenido manualmente.")
    finally:
        server_socket.close()  # Cierra el socket del servidor

import uuid
import os

def generar_uid_unico(file_name):
    # Genera un UID único
    uid = str(uuid.uuid4())

    # Verifica si el archivo de registro existe y no está vacío
    if os.path.isfile(file_name) and os.path.getsize(file_name) > 0:
        with open(file_name, 'r') as f:
            # Leer todas las líneas del archivo y comprobar si alguna contiene el UID
            for linea in f:
                if fr'UID: {uid}' in linea:
                    # Si el UID ya existe en el registro, genera uno nuevo y vuelve a verificar
                    return generar_uid_unico(file_name)

    # Si no se encontró el UID en el registro o el archivo está vacío, se devuelve como único
    return uid

        
            
        

if __name__ == '__main__':
    main()
