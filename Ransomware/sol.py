import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes

def cargar_llave_privada(ruta_llave_privada):
    with open(ruta_llave_privada, "rb") as f:
        return serialization.load_pem_private_key(
            f.read(),
            password=None  # Cambia esto si la llave está cifrada
        )

def descifrar_archivo(ruta_archivo_enc, llave_privada):
    with open(ruta_archivo_enc, "rb") as f:
        iv = f.read(16)  # Lee el IV
        llave_cifrada = f.read(256)  # Lee la llave cifrada (2048 bits)
        datos_cifrados = f.read()  # Lee los datos cifrados

    llave_aes = llave_privada.decrypt(
        llave_cifrada,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    cipher = AES.new(llave_aes, AES.MODE_CBC, iv)
    datos_descifrados = unpad(cipher.decrypt(datos_cifrados), AES.block_size)

    ruta_archivo_descifrado = ruta_archivo_enc[:-4]  # Remover la extensión .enc
    with open(ruta_archivo_descifrado, 'wb') as f:
        f.write(datos_descifrados)

def descifrar_todos_los_archivos(directorio, llave_privada):
    for archivo in os.listdir(directorio):
        if archivo.endswith('.enc'):
            ruta_archivo_enc = os.path.join(directorio, archivo)
            descifrar_archivo(ruta_archivo_enc, llave_privada)

if __name__ == "__main__":
    ruta_llave_privada = "llave_privada.pem"
    llave_privada = cargar_llave_privada(ruta_llave_privada)

    # Obtener la ruta de la carpeta de Documentos del usuario
    directorio_documentos = os.path.join(os.path.expanduser('~'), 'Documents')
    descifrar_todos_los_archivos(directorio_documentos, llave_privada)
