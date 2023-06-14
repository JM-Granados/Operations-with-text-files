from easygui import *
import os.path
import os
#-------------------------------------------------------------------------------------------------------------------------------
def archivos():
    """
    Programa que permita hacer diferentes operaciones sobre archivos de texto.
    Ya sea imprimir las estadísticas del archivo (Nombre, cantidad de líneas, cantidad de carácteres, top 10 de 
    palabras más utilizadas.), busqueda textual y reemplazar texto. 
    Entradas y restricciones:
    - nombre de archivo: debe existir, str.
    - 1, 2 o 3: Operación escogida
    """
    # Pantallas para solicitar info y verificar si el archivo existe o abre ---------------------------------------------------
    mensaje = "Ingrese el nombre del archivo"
    titulo = "Archivos de texto"
    espacios = ["Nombre del archivo"]
    nombre = multenterbox(mensaje, titulo, espacios)
    # Restricciones------------------------------------------------------------------------------------------------------------
    while nombre[0] == '':
        mensaje = "No ingresó ningún nombre, por favor, ingrese el nombre del archivo"
        nombre = multenterbox(mensaje, titulo, espacios)
    nombre = nombre[0]
    try:
        archivo = open(nombre, "r")
    except Exception: 
        mensaje = "Error al abrir el archivo. \n Puede que esté mal escrito o no exista."
        error = msgbox(mensaje, titulo)
        return
    menu(archivo, nombre)
# Pantalla de menú para seleccionar operación ----------------------------------------------------------------------------------
def menu(archivo, nombre):
    """
    Función que presenta una ventana con las diferentes opciones de operación a elegir.
    """
    msgM = "Indique qué operación desea realizar:"
    titM = "Menú de operaciones"
    botones = []
    boton1 = "Estadísticas de archivo"
    boton2 = "Búsqueda textual"
    boton3 = "Reemplazar texto"
    botones.append(boton1)
    botones.append(boton2)
    botones.append(boton3)
    opcion = buttonbox(msgM, titM, botones)
    if opcion == "Estadísticas de archivo":
        estadistica(archivo, nombre)
        return
    if opcion == "Búsqueda textual":
        busqueda(archivo)
        return
    else:
        reemplazar(nombre, archivo)
        return
#Operaciones--------------------------------------------------------------------------------------------------------------------
def estadistica(archivo, nombre): #Archivo es el abierto y nombre es el que no
    """
    Función que calcula las estadísticas de un archivo de texto: nombre, ruta completa, cantidad de líneas, 
    cantidad de carácteres y top 10 de palabras más utilizadas.
    """
    ruta = os.path.abspath(nombre)
    lineas = 0
    caracteres = 0
    cuenta= {}
    for linea in archivo:
        lineas += 1
        caracteres += len(linea)
        for palabra in palabras(linea):
            if palabra in cuenta:
                cuenta[palabra] += 1
            else:
                cuenta[palabra] = 1
    archivo.close()
    top = generarTop(cuenta)
    msg = "Estadisticas"
    titulo = "Estadisticas de archivo"
    texto = [f"Ruta: {ruta} \n", f"Nombre: {nombre} \n", f"Cantidad de líneas: {lineas} \n", f"Cantidad de caracteres: {caracteres} \n", "Top 10 de palabras más utilizadas:"]
    for numero, (palabra, cantidad) in enumerate(top, start = 1):
        texto.append(f"\n{numero}. {palabra} ({cantidad}) \n")
    salida = textbox(msg, titulo, texto)
def palabras(texto):
    """
    Función que recibe un str y retorna una lista de las palabras.
    """
    texto = texto.lower()
    nuevoTexto = ""
    for c in texto:
        if c.isalpha():
            nuevoTexto += c
        else:
            nuevoTexto += " "
    return nuevoTexto.split()
def generarTop(dic):
    """
    Función que ordena el diccionario en descendente dependiendo de las veces en las que una 
    palabra apareció.
    """
    top = list(dic.items())
    top.sort(key = lambda t : t[1], reverse = True)
    return top[:10]
#-------------------------------------------------------------------------------------------------------------------------------
def busqueda(archivo):
    """
    Función que recibe el nombre de un archivo y un texto a buscar e imprime las líneas donde se encontró
    el texto y la cantidad de veces.
    Entradas y restricciones:
    - Nombre de archivo: str con el archivo a procesar.
    - Texto: str con el texto a buscar.
    Salida: 
    Los números de línea y la línea completa donde el texto fue encontrado. Cantidad total de coincidencias.
    """
    msg = "Ingrese el texto que desee buscar"
    titulo = "Búsqueda textual"
    texto = enterbox(msg, titulo)
    while texto[0] == '':
        mensaje = "No ingresó ningún texto, por favor, ingrese el texto a buscar"
        error = multenterbox(mensaje, titulo, texto)
    texto = texto.lower()
    coincidencias = 0
    msg = []
    for n, linea in enumerate(archivo, start = 1):
        if texto in linea.lower():
            coincidencias += 1
            msg.append(f"Línea {n}: {linea} \n")
    archivo.close() 
    if coincidencias == 0:
        m = "No se encontraron coincidencias"
        salida = msgbox(m, titulo)
    else:
        msg.append(f"\n Se encontraron {coincidencias} coincidencias.")
        mensaje = "Búsqueda"
        texto = textbox(mensaje, titulo, msg)
#-------------------------------------------------------------------------------------------------------------------------------
def reemplazar(archivo, archabierto):
    """
    Función que realiza un reemplazo de texto en un archivo.
    Entradas y restrcciones:
    - Archivo: el nombre del archivo a procesar.
    - texto: str con el texto a reemplazar.
    - reemplazo: str con el texto de reemplazo.
    Salidas:
    En el archivo original se sustituyen todas las apariciones del texto por el texto de reemplazo.
    """
    archabierto.close()
    msg = "Ingrese el texto que desee buscar para reemplazar y el reemplazo"
    titulo = "Reemplazar texto"
    nombres = ["Reemplazo", "A reemplazar"]
    nombres = multenterbox(msg, titulo, nombres)
    while nombres[0] == '' or nombres[1] == '': #0 es el reemplazo y 1 es el que se desea reemplazar
        mensaje = "No ingresó ningún texto, por favor, ingrese un texto válido"
        nombres = multenterbox(mensaje, titulo, nombres)
    with open(archivo, "r") as entrada, open(archivo + ".temp", "w") as salida:
        for linea in entrada:
            linea = linea.replace(nombres[1], nombres[0])
            salida.write(linea)
    m = "El reemplazo fue exitoso."
    P = msgbox(m, titulo)
    os.remove(archivo)
    os.rename(archivo + ".temp", archivo)
archivos()
