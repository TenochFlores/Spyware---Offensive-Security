#!/bin/bash

# Obtén la dirección IP local y extrae los primeros tres octetos
IP_PREFIX=$(hostname -I | cut -d' ' -f1 | cut -d'.' -f1-3)

echo "Realizando Network Sweep en la red: $IP_PREFIX.0/24"

# Itera a través del rango de posibles direcciones IP en el último octeto
for i in {1..254}; do
  # Construye la dirección IP completa
  IP="$IP_PREFIX.$i"

  # Realiza un ping rápido a la dirección IP
  ping -c 1 -W 1 $IP &> /dev/null

  # Comprueba el resultado del último comando e imprime true o false
  if [ $? -eq 0 ]; then
    echo "$IP is up - true"
  else
    echo "$IP is down - false"
  fi
done
