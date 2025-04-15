# -*- coding: utf-8 -*-
"""
Juego de Reflejos para Raspberry Pi
Proyecto de ciencias para niños de 12 años

Este programa crea un juego simple para medir los reflejos de un jugador.
Funciona en pantalla completa en Raspberry Pi o en entornos virtualizados.
"""

import pygame
import sys
import time
import random
import json
import os
from pygame.locals import *

# Inicialización de Pygame
pygame.init()

# Constantes del juego
TIEMPO_REACCION_MEDIA = 250 # milisegundos para una persona media (valor de referencia)
NOMBRE_ESCUELA = "CEIP Ría do Burgo"
CREDITOS = "Creado por Gael Matas y Pablo Alonso"

# Colores (formato RGB)
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)
AZUL = (0, 0, 255)
VERDE = (0, 255, 0)
AMARILLO = (255, 255, 0)
GRIS = (100, 100, 100)
AZUL_CLARO = (100, 180, 255)

# Configuración de la pantalla en modo pantalla completa
info = pygame.display.Info()
ANCHO = info.current_w
ALTO = info.current_h
pantalla = pygame.display.set_mode((ANCHO, ALTO), pygame.FULLSCREEN)
pygame.display.set_caption('Juego de reflejos')
reloj = pygame.time.Clock()  # Para controlar la velocidad de actualización

# División de la pantalla - mitad izquierda para el juego, mitad derecha para el histograma
ANCHO_IZQUIERDA = ANCHO // 2
ANCHO_DERECHA = ANCHO - ANCHO_IZQUIERDA

# Fuentes para texto
fuente_grande = pygame.font.Font(None, 72)
fuente_mediana = pygame.font.Font(None, 48)
fuente_pequena = pygame.font.Font(None, 32)
fuente_muy_pequena = pygame.font.Font(None, 24)  # Para los créditos

# Archivo para guardar los datos de los jugadores
ARCHIVO_JUGADORES = 'jugadores.json'

def cargar_datos():
    """
    Carga los datos de los jugadores desde el archivo JSON.
    Si el archivo no existe o está corrupto, crea una estructura de datos vacía.
    """
    if os.path.exists(ARCHIVO_JUGADORES):
        try:
            with open(ARCHIVO_JUGADORES, 'r') as archivo:
                return json.load(archivo)
        except:
            print("Error al cargar el archivo de jugadores. Creando nuevo archivo.")
            return {'jugadores': []}
    else:
        return {'jugadores': []}

def guardar_datos(datos):
    """
    Guarda los datos de los jugadores en el archivo JSON.
    """
    with open(ARCHIVO_JUGADORES, 'w') as archivo:
        json.dump(datos, archivo)

def obtener_mejores_jugadores(datos, numero=5):
    """
    Devuelve una lista con los mejores jugadores ordenados por tiempo (menor es mejor).
    
    Args:
        datos: Diccionario con los datos de los jugadores
        numero: Número de mejores jugadores a devolver
        
    Returns:
        Lista de diccionarios con los mejores jugadores
    """
    # Ordenar por tiempo de reacción (menor es mejor)
    jugadores_ordenados = sorted(datos['jugadores'], key=lambda x: x['tiempo'])
    return jugadores_ordenados[:numero]

def calcular_media(datos):
    """
    Calcula el tiempo medio de reacción de todos los jugadores.
    
    Args:
        datos: Diccionario con los datos de los jugadores
        
    Returns:
        Tiempo medio en milisegundos, o 0 si no hay jugadores
    """
    if not datos['jugadores']:
        return 0
    
    total = sum(jugador['tiempo'] for jugador in datos['jugadores'])
    return total / len(datos['jugadores'])

def obtener_mejor_tiempo(datos):
    """
    Obtiene el mejor tiempo de reacción registrado.
    
    Args:
        datos: Diccionario con los datos de los jugadores
        
    Returns:
        Mejor tiempo en milisegundos, o 0 si no hay jugadores
    """
    if not datos['jugadores']:
        return 0
    
    return min(jugador['tiempo'] for jugador in datos['jugadores'])

def generar_datos_histograma(datos):
    """
    Genera los datos para el histograma de tiempos de reacción.
    
    Args:
        datos: Diccionario con los datos de los jugadores
        
    Returns:
        Lista de 10 elementos con el conteo de jugadores por rango de tiempo
    """
# Definir los rangos específicos
    rangos_limites = [0, 200, 220, 240, 260, 280, 300, 320, 340, 360, 380]
    
    # Inicializar contadores para cada rango
    rangos_conteo = [0] * 10
    
    # Contar jugadores en cada rango
    for jugador in datos['jugadores']:
        tiempo = jugador['tiempo']
        
        # Ubicar el tiempo en el rango correspondiente
        for i in range(10):
            if rangos_limites[i] <= tiempo < rangos_limites[i+1]:
                rangos_conteo[i] += 1
                break
    
    return rangos_conteo

def dibujar_histograma(datos):
    """
    Dibuja un histograma de distribución de tiempos de reacción en la parte derecha de la pantalla.
    
    Args:
        datos: Diccionario con los datos de los jugadores
    """
    # Área para el histograma
    area_x = ANCHO_IZQUIERDA + 50
    area_y = 150
    area_ancho = ANCHO_DERECHA - 100
    area_alto = ALTO - 300
    
    # Dibujar título
    titulo = fuente_mediana.render("Distribución de tiempos de reacción", True, BLANCO)
    pantalla.blit(titulo, (ANCHO_IZQUIERDA + (ANCHO_DERECHA // 2) - titulo.get_width() // 2, 80))
    
    # Dibujar ejes
    pygame.draw.line(pantalla, BLANCO, (area_x, area_y), (area_x, area_y + area_alto), 2)  # Eje Y
    pygame.draw.line(pantalla, BLANCO, (area_x, area_y + area_alto), (area_x + area_ancho, area_y + area_alto), 2)  # Eje X
    
    # Obtener datos para el histograma
    conteos = generar_datos_histograma(datos)
    
    # Encontrar el valor máximo para escalar las barras
    max_conteo = max(conteos) if max(conteos) > 0 else 1
    
    # Dibujar etiquetas del eje X (tiempos)
    rangos_etiquetas = ["0-199", "200-219", "220-239", "240-259", "260-279", 
                        "280-299", "300-319", "320-339", "340-359", "360-380"]
    for i in range(10):
        etiqueta = fuente_muy_pequena.render(rangos_etiquetas[i], True, BLANCO)
        x_pos = area_x + (i * area_ancho // 10) + (area_ancho // 20)
        pantalla.blit(etiqueta, (x_pos - etiqueta.get_width() // 2, area_y + area_alto + 5))
    
    # Dibujar etiquetas del eje Y (número de jugadores)
    for i in range(5):
        valor = i * (max_conteo // 4 + 1)
        if i == 4:  # Para la etiqueta superior
            valor = max_conteo
        etiqueta = fuente_muy_pequena.render(str(valor), True, BLANCO)
        y_pos = area_y + area_alto - (i * area_alto // 4)
        pantalla.blit(etiqueta, (area_x - etiqueta.get_width() - 5, y_pos - etiqueta.get_height() // 2))
    
    # Dibujar barras
    ancho_barra = (area_ancho) // 10 - 10
    for i, conteo in enumerate(conteos):
        if max_conteo > 0:
            altura_barra = (conteo / max_conteo) * area_alto
        else:
            altura_barra = 0
        
        x = area_x + 5 + (i * area_ancho // 10)
        y = area_y + area_alto - altura_barra
        
        # Alternar colores para mejor visibilidad
        color = VERDE if i % 2 == 0 else AZUL_CLARO
        
        pygame.draw.rect(pantalla, color, (x, y, ancho_barra, altura_barra))
    
    # Dibujar etiqueta de eje X
    etiqueta_x = fuente_pequena.render("Tiempo (ms)", True, BLANCO)
    pantalla.blit(etiqueta_x, (area_x + area_ancho // 2 - etiqueta_x.get_width() // 2, area_y + area_alto + 30))
    
    # Dibujar etiqueta de eje Y
    etiqueta_y = fuente_pequena.render("Jugadores", True, BLANCO)
    # Rotar texto para eje Y
    etiqueta_y_rotada = pygame.transform.rotate(etiqueta_y, 90)
    pantalla.blit(etiqueta_y_rotada, (area_x - 40, area_y + area_alto // 2 - etiqueta_y_rotada.get_height() // 2))

def dibujar_boton_salir():
    """
    Dibuja un pequeño botón X para salir del juego en la esquina superior derecha.
    
    Returns:
        Rect: Objeto rectángulo que representa el área del botón
    """
    # Dibujar un pequeño botón de salida en la esquina superior derecha
    tamano_boton = 30
    margen = 10
    pygame.draw.rect(pantalla, NEGRO, (ANCHO - tamano_boton - margen, margen, tamano_boton, tamano_boton))
    pygame.draw.rect(pantalla, BLANCO, (ANCHO - tamano_boton - margen, margen, tamano_boton, tamano_boton), 2)
    
    # Dibujar una X
    x = fuente_pequena.render("X", True, BLANCO)
    pantalla.blit(x, (ANCHO - tamano_boton - margen + tamano_boton//2 - x.get_width()//2, 
                      margen + tamano_boton//2 - x.get_height()//2))
    
    return pygame.Rect(ANCHO - tamano_boton - margen, margen, tamano_boton, tamano_boton)

def pantalla_bienvenida():
    """
    Muestra la pantalla de bienvenida con la entrada del nombre del jugador.
    También muestra los mejores jugadores y estadísticas.
    
    Returns:
        str: Nombre del jugador ingresado
    """
    # Cargar datos de jugadores
    datos = cargar_datos()
    mejores = obtener_mejores_jugadores(datos)
    tiempo_medio = calcular_media(datos)
    nombre = ""
    cursor_visible = True
    ultimo_cambio = time.time()
    
    # Longitud máxima del nombre
    LONGITUD_MAXIMA_NOMBRE = 20
    
    # Calcular altura total del contenido para centrado vertical en la parte izquierda
    altura_total = 0
    altura_total += 80  # Título escuela
    altura_total += 80  # Título juego
    altura_total += 60  # Subtítulo mejores jugadores
    altura_total += (len(mejores) if mejores else 1) * 40  # Lista de jugadores
    altura_total += 40  # Tiempo medio
    altura_total += 40  # Tiempo referencia
    altura_total += 60  # Instrucción nombre
    altura_total += 50  # Campo de texto
    altura_total += 70  # Botón jugar
    altura_total += 40  # Créditos
    
    # Calcular posición inicial para centrado vertical
    y_inicio = (ALTO - altura_total) // 2
    
    while True:
        pantalla.fill(NEGRO)
        
        # Dibujar línea divisoria vertical
        pygame.draw.line(pantalla, BLANCO, (ANCHO_IZQUIERDA, 0), (ANCHO_IZQUIERDA, ALTO), 2)
        
        # Nombre de la escuela en la parte superior izquierda
        escuela = fuente_mediana.render(NOMBRE_ESCUELA, True, BLANCO)
        pantalla.blit(escuela, (ANCHO_IZQUIERDA//2 - escuela.get_width()//2, 20))
        
        # Posición vertical actual (empezando desde el centrado)
        y_pos = y_inicio
        
        # Título
        titulo = fuente_grande.render("COMPRUEBA TUS REFLEJOS", True, BLANCO)
        pantalla.blit(titulo, (ANCHO_IZQUIERDA//2 - titulo.get_width()//2, y_pos))
        y_pos += 80
        
        # Mejores jugadores
        subtitulo = fuente_mediana.render("Mejores Jugadores:", True, BLANCO)
        pantalla.blit(subtitulo, (ANCHO_IZQUIERDA//2 - subtitulo.get_width()//2, y_pos))
        y_pos += 60
        
        if mejores:
            for i, jugador in enumerate(mejores):
                texto = f"{i+1}. {jugador['nombre']}: {jugador['tiempo']} ms"
                render = fuente_pequena.render(texto, True, BLANCO)
                pantalla.blit(render, (ANCHO_IZQUIERDA//2 - render.get_width()//2, y_pos))
                y_pos += 40
        else:
            texto = "Aún no hay registros"
            render = fuente_pequena.render(texto, True, BLANCO)
            pantalla.blit(render, (ANCHO_IZQUIERDA//2 - render.get_width()//2, y_pos))
            y_pos += 40
        
        # Tiempo medio de los jugadores
        if tiempo_medio > 0:
            texto = f"Tiempo medio de nuestros jugadores: {int(tiempo_medio)} ms"
            render = fuente_pequena.render(texto, True, AMARILLO)
            pantalla.blit(render, (ANCHO_IZQUIERDA//2 - render.get_width()//2, y_pos))
        y_pos += 40
        
        # Tiempo medio de referencia
        texto = f"Tiempo medio de la poblacion: {TIEMPO_REACCION_MEDIA} ms"
        render = fuente_pequena.render(texto, True, AMARILLO)
        pantalla.blit(render, (ANCHO_IZQUIERDA//2 - render.get_width()//2, y_pos))
        y_pos += 60
        
        # Entrada de nombre
        instruccion = fuente_mediana.render("Ingresa tu nombre:", True, BLANCO)
        pantalla.blit(instruccion, (ANCHO_IZQUIERDA//2 - instruccion.get_width()//2, y_pos))
        y_pos += 50
        
        # Actualizar el cursor parpadeante cada 0.5 segundos
        if time.time() - ultimo_cambio > 0.5:
            cursor_visible = not cursor_visible
            ultimo_cambio = time.time()
        
        # Mostrar el campo de texto con cursor
        if cursor_visible:
            texto_input = fuente_mediana.render(nombre + "|", True, BLANCO)
        else:
            texto_input = fuente_mediana.render(nombre + " ", True, BLANCO)
        
        pantalla.blit(texto_input, (ANCHO_IZQUIERDA//2 - texto_input.get_width()//2, y_pos))
        y_pos += 70
        
        # Botón de jugar
        pygame.draw.rect(pantalla, VERDE, (ANCHO_IZQUIERDA//2 - 100, y_pos, 200, 50))
        texto_boton = fuente_mediana.render("JUGAR", True, NEGRO)
        pantalla.blit(texto_boton, (ANCHO_IZQUIERDA//2 - texto_boton.get_width()//2, y_pos + 10))
        
        # Área de clic para el botón jugar
        rect_boton_jugar = pygame.Rect(ANCHO_IZQUIERDA//2 - 100, y_pos, 200, 50)
        
        # Créditos en la parte inferior
        creditos = fuente_muy_pequena.render(CREDITOS, True, BLANCO)
        pantalla.blit(creditos, (ANCHO_IZQUIERDA//2 - creditos.get_width()//2, ALTO - 40))
        
        # Dibujar histograma en la parte derecha
        dibujar_histograma(datos)
        
        # Botón de salir
        boton_salir = dibujar_boton_salir()
        
        pygame.display.flip()
        
        for evento in pygame.event.get():
            if evento.type == QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == KEYDOWN:
                if evento.key == K_RETURN and nombre.strip():
                    # Si el usuario presiona Enter y el nombre no está vacío
                    return nombre
                elif evento.key == K_BACKSPACE:
                    # Borrar el último carácter
                    nombre = nombre[:-1]
                # Permitir letras, números y espacio, y limitar a LONGITUD_MAXIMA_NOMBRE caracteres
                elif (evento.unicode.isalnum() or evento.unicode == ' ') and len(nombre) < LONGITUD_MAXIMA_NOMBRE:
                    nombre += evento.unicode
            elif evento.type == MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                # Verificar si hizo clic en el botón de jugar
                if rect_boton_jugar.collidepoint(mouse_pos):
                    if nombre.strip():  # Verificar que el nombre no esté vacío
                        return nombre
                # Verificar si hizo clic en el botón de salir
                if boton_salir.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()
        
        reloj.tick(30)  # 30 FPS

def pantalla_espera():
    """
    Muestra la pantalla de "estate atento" durante un tiempo aleatorio.
    
    Returns:
        bool: True si el tiempo de espera terminó normalmente, 
              False si el jugador pulsó una tecla antes de tiempo
    """
    tiempo_espera = random.uniform(3, 10)  # Tiempo aleatorio entre 3 y 10 segundos
    tiempo_inicio = time.time()
    
    # Cargar datos para el histograma
    datos = cargar_datos()
    
    while True:
        tiempo_actual = time.time() - tiempo_inicio
        
        if tiempo_actual >= tiempo_espera:
            # El tiempo de espera ha terminado, pasar a la siguiente pantalla
            return True
        
        pantalla.fill(NEGRO)
        
        # Dibujar línea divisoria vertical
        pygame.draw.line(pantalla, BLANCO, (ANCHO_IZQUIERDA, 0), (ANCHO_IZQUIERDA, ALTO), 2)
        
        # Contenido en la parte izquierda
        texto = fuente_grande.render("ESTATE ATENTO", True, BLANCO)
        pantalla.blit(texto, (ANCHO_IZQUIERDA//2 - texto.get_width()//2, ALTO//2 - 50))
        
        instruccion = fuente_mediana.render("Cuando te diga debes pulsar una tecla", True, BLANCO)
        pantalla.blit(instruccion, (ANCHO_IZQUIERDA//2 - instruccion.get_width()//2, ALTO//2 + 30))
        
        # Dibujar histograma en la parte derecha
        dibujar_histograma(datos)
        
        pygame.display.flip()
        
        for evento in pygame.event.get():
            if evento.type == QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == KEYDOWN:
                # El jugador pulsó una tecla antes de tiempo
                return False
        
        reloj.tick(30)

def pantalla_reaccion():
    """
    Muestra la pantalla roja "¡¡¡Pulsa ya!!!" y mide el tiempo de reacción.
    
    Returns:
        int o None: Tiempo de reacción en milisegundos, 
                  o None si el jugador no reaccionó a tiempo
    """
    tiempo_inicio = time.time()
    tiempo_limite = tiempo_inicio + 10  # 10 segundos para reaccionar
    
    # Cargar datos para el histograma
    datos = cargar_datos()
    
    while True:
        tiempo_actual = time.time()
        
        if tiempo_actual >= tiempo_limite:
            # Se acabó el tiempo sin que el jugador pulsara
            return None
        
        # La parte izquierda es roja, la derecha sigue siendo negra con el histograma
        pantalla.fill(NEGRO)
        pygame.draw.rect(pantalla, ROJO, (0, 0, ANCHO_IZQUIERDA, ALTO))
        
        # Dibujar línea divisoria vertical
        pygame.draw.line(pantalla, BLANCO, (ANCHO_IZQUIERDA, 0), (ANCHO_IZQUIERDA, ALTO), 2)
        
        # Texto en la parte izquierda
        texto = fuente_grande.render("¡¡¡Pulsa ya!!!", True, BLANCO)
        pantalla.blit(texto, (ANCHO_IZQUIERDA//2 - texto.get_width()//2, ALTO//2))
        
        # Dibujar histograma en la parte derecha
        dibujar_histograma(datos)
        
        pygame.display.flip()
        
        for evento in pygame.event.get():
            if evento.type == QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == KEYDOWN:
                # Calcular tiempo de reacción en milisegundos
                tiempo_reaccion = int((time.time() - tiempo_inicio) * 1000)
                return tiempo_reaccion
        
        reloj.tick(30)

def pantalla_perdida(mensaje="No has pulsado nada y has perdido"):
    """
    Muestra una pantalla de derrota con un mensaje personalizable.
    
    Args:
        mensaje: Texto que se mostrará al jugador
    """
    tiempo_inicio = time.time()
    
    # Cargar datos para el histograma
    datos = cargar_datos()
    
    while True:
        tiempo_actual = time.time() - tiempo_inicio
        
        if tiempo_actual >= 6:  # Mostrar por 6 segundos
            return
        
        pantalla.fill(NEGRO)
        
        # Dibujar línea divisoria vertical
        pygame.draw.line(pantalla, BLANCO, (ANCHO_IZQUIERDA, 0), (ANCHO_IZQUIERDA, ALTO), 2)
        
        # Dividir el mensaje en dos líneas si es necesario (parte izquierda)
        if len(mensaje) > 30:
            partes = mensaje.split(" y ")
            if len(partes) == 2:
                texto1 = fuente_grande.render(partes[0], True, BLANCO)
                texto2 = fuente_grande.render("y " + partes[1], True, BLANCO)
                
                pantalla.blit(texto1, (ANCHO_IZQUIERDA//2 - texto1.get_width()//2, ALTO//2 - 50))
                pantalla.blit(texto2, (ANCHO_IZQUIERDA//2 - texto2.get_width()//2, ALTO//2 + 30))
            else:
                palabras = mensaje.split()
                mitad = len(palabras) // 2
                texto1 = fuente_grande.render(" ".join(palabras[:mitad]), True, BLANCO)
                texto2 = fuente_grande.render(" ".join(palabras[mitad:]), True, BLANCO)
                
                pantalla.blit(texto1, (ANCHO_IZQUIERDA//2 - texto1.get_width()//2, ALTO//2 - 50))
                pantalla.blit(texto2, (ANCHO_IZQUIERDA//2 - texto2.get_width()//2, ALTO//2 + 30))
        else:
            texto = fuente_grande.render(mensaje, True, BLANCO)
            pantalla.blit(texto, (ANCHO_IZQUIERDA//2 - texto.get_width()//2, ALTO//2))
        
        # Dibujar histograma en la parte derecha
        dibujar_histograma(datos)
        
        pygame.display.flip()
        
        for evento in pygame.event.get():
            if evento.type == QUIT:
                pygame.quit()
                sys.exit()
        
        reloj.tick(30)

def pantalla_resultados(nombre, tiempo_reaccion):
    """
    Muestra los resultados del jugador y las estadísticas comparativas.
    Si el jugador completó el juego, guarda su puntuación.
    
    Args:
        nombre: Nombre del jugador
        tiempo_reaccion: Tiempo de reacción en ms, o None si perdió
    """
    datos = cargar_datos()
    
    # Guardar el nuevo resultado solo si el jugador completó el juego
    if tiempo_reaccion is not None:
        datos['jugadores'].append({
            'nombre': nombre,
            'tiempo': tiempo_reaccion
        })
        guardar_datos(datos)
    
    # Calcular estadísticas
    mejor_tiempo = obtener_mejor_tiempo(datos)
    tiempo_medio = calcular_media(datos)
    
    while True:
        pantalla.fill(NEGRO)
        
        # Dibujar línea divisoria vertical
        pygame.draw.line(pantalla, BLANCO, (ANCHO_IZQUIERDA, 0), (ANCHO_IZQUIERDA, ALTO), 2)
        
        # Título según el resultado (parte izquierda)
        if tiempo_reaccion is None:
            titulo = fuente_grande.render("¡Has perdido!", True, ROJO)
        else:
            titulo = fuente_grande.render("¡Resultados!", True, VERDE)
        
        pantalla.blit(titulo, (ANCHO_IZQUIERDA//2 - titulo.get_width()//2, 50))
        
        # Calcular altura total del contenido para centrado vertical
        altura_total = 0
        if tiempo_reaccion is not None:
            altura_total += 60  # Tiempo del jugador
        altura_total += 60  # Tiempo persona media
        altura_total += 60  # Mejor tiempo (si existe)
        altura_total += 60  # Tiempo promedio (si existe)
        altura_total += 40  # Instrucción final
        
        # Calcular posición inicial para centrado vertical
        y_pos = max(150, (ALTO - altura_total) // 2)
        
        if tiempo_reaccion is not None:
            # Mostrar tiempo de reacción del jugador
            texto = f"Tu tiempo de reacción: {tiempo_reaccion} ms"
            render = fuente_mediana.render(texto, True, BLANCO)
            pantalla.blit(render, (ANCHO_IZQUIERDA//2 - render.get_width()//2, y_pos))
            y_pos += 60
        
        # Mostrar tiempo de reacción promedio de referencia
        texto = f"Tiempo de una persona media: {TIEMPO_REACCION_MEDIA} ms"
        render = fuente_mediana.render(texto, True, BLANCO)
        pantalla.blit(render, (ANCHO_IZQUIERDA//2 - render.get_width()//2, y_pos))
        y_pos += 60
        
        # Mostrar mejor tiempo
        if mejor_tiempo > 0:
            texto = f"Mejor tiempo: {mejor_tiempo} ms"
            render = fuente_mediana.render(texto, True, BLANCO)
            pantalla.blit(render, (ANCHO_IZQUIERDA//2 - render.get_width()//2, y_pos))
            y_pos += 60
        
        # Mostrar tiempo promedio de todos los jugadores
        if tiempo_medio > 0:
            texto = f"Tiempo promedio: {int(tiempo_medio)} ms"
            render = fuente_mediana.render(texto, True, BLANCO)
            pantalla.blit(render, (ANCHO_IZQUIERDA//2 - render.get_width()//2, y_pos))
            y_pos += 60
        
 # Instrucción final
        instruccion = fuente_pequena.render("Pulsa cualquier tecla para continuar", True, BLANCO)
        pantalla.blit(instruccion, (ANCHO_IZQUIERDA//2 - instruccion.get_width()//2, y_pos))
        
        # Mostrar créditos en la parte inferior
        creditos = fuente_muy_pequena.render(CREDITOS, True, BLANCO)
        pantalla.blit(creditos, (ANCHO_IZQUIERDA//2 - creditos.get_width()//2, ALTO - 40))
        
        # Dibujar el histograma en la parte derecha
        dibujar_histograma(datos)
        
        pygame.display.flip()
        
        for evento in pygame.event.get():
            if evento.type == QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == KEYDOWN:
                return
        
        reloj.tick(30)

def main():
    """
    Función principal que controla el flujo del juego.
    """
    while True:
        try:
            # Pantalla 1: Bienvenida y entrada de nombre
            nombre = pantalla_bienvenida()
            
            # Pantalla 2: Espera con instrucciones
            espera_completada = pantalla_espera()
            
            if not espera_completada:
                # Pantalla 4.5: Perdida por presionar antes de tiempo
                pantalla_perdida("Has pulsado antes de tiempo y has perdido")
                continue
                
            # Pantalla 3: Reacción (pantalla roja)
            tiempo_reaccion = pantalla_reaccion()
            
            # Pantalla 4: Perdida (si no reaccionó a tiempo)
            if tiempo_reaccion is None:
                pantalla_perdida()
            else:
                # Pantalla 5: Resultados
                pantalla_resultados(nombre, tiempo_reaccion)
        except Exception as e:
            # Capturar excepciones para evitar que el programa se cierre inesperadamente
            print(f"Error en el juego: {e}")
            pygame.quit()
            sys.exit()

# Punto de entrada del programa
if __name__ == "__main__":
    main()
