import pygame
import sys
import random
from damas import JuegoDamas

# Constantes visuales
ANCHO, ALTO = 640, 640
TAM_CASILLA = ANCHO // 8
COLOR_BLANCO = (240, 217, 181)
COLOR_NEGRO = (181, 136, 99)
COLOR_ROJO = (220, 20, 60)
COLOR_AZUL = (30, 144, 255)
COLOR_DAMA = (255, 215, 0)

# Inicializar pygame
pygame.init()
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption('Damas - Versión Gráfica')

# Sonidos
try:
    sonido_movimiento = pygame.mixer.Sound('sounds/483600__raclure__cursor.wav')
    sonido_captura = pygame.mixer.Sound('sounds/445884__lauracarolina09__48-blood.wav')
    sonido_movimiento_no_valido = pygame.mixer.Sound('sounds/363920__samsterbirdies__8-bit-error.wav')
    sonido_coronacion = pygame.mixer.Sound('sounds/721208__ahhh.wav')
    sonidos_habilitados = True
except pygame.error:
    print("No se pudieron cargar los sonidos. El juego continuará sin audio.")
    sonidos_habilitados = False

def reproducir_sonido(sonido):
    if sonidos_habilitados:
        sonido.play()

# Dibujo
def contar_fichas(tablero):
    x = o = X = O = 0
    for fila in tablero:
        for celda in fila:
            if celda == 'x': x += 1
            elif celda == 'o': o += 1
            elif celda == 'X': X += 1
            elif celda == 'O': O += 1
    return x, o, X, O

def sugerir_movimientos(tablero, origen, jugador):
    from damas import JuegoDamas
    juego_tmp = JuegoDamas()
    juego_tmp.tablero = [row[:] for row in tablero]
    sugerencias = []
    fx, cx = origen
    for dx in [-1, 1, -2, 2]:
        for dy in [-1, 1, -2, 2]:
            fy, cy = fx + dx, cx + dy
            if 0 <= fy < juego_tmp.size and 0 <= cy < juego_tmp.size:
                valido, captura = juego_tmp.movimiento_valido((fx, cx), (fy, cy), jugador)
                if valido:
                    sugerencias.append((fy, cy))
    return sugerencias

def es_dama(ficha):
    return ficha in ('X', 'O')

def dibujar_tablero(tablero, seleccionada=None, sugerencias=None, fichas=None):
    for fila in range(8):
        for col in range(8):
            color = COLOR_BLANCO if (fila + col) % 2 == 0 else COLOR_NEGRO
            rect = pygame.Rect(col * TAM_CASILLA, fila * TAM_CASILLA, TAM_CASILLA, TAM_CASILLA)
            pygame.draw.rect(ventana, color, rect)
            if seleccionada == (fila, col):
                pygame.draw.rect(ventana, (255, 255, 0), rect, 4)
            if sugerencias and (fila, col) in sugerencias:
                pygame.draw.rect(ventana, (0, 255, 0), rect, 4)
            ficha = tablero[fila][col]
            if ficha != ' ':
                if ficha.lower() == 'x':
                    color_ficha = COLOR_ROJO
                else:
                    color_ficha = COLOR_AZUL
                pygame.draw.circle(ventana, color_ficha, rect.center, TAM_CASILLA // 2 - 8)
                if es_dama(ficha):
                    pygame.draw.circle(ventana, COLOR_DAMA, rect.center, TAM_CASILLA // 2 - 20)
    # Mostrar contador de fichas
    if fichas:
        font = pygame.font.SysFont(None, 32)
        x, o, X, O = fichas
        texto = f"x: {x} | X: {X}    o: {o} | O: {O}"
        text = font.render(texto, True, (0, 0, 0))
        ventana.blit(text, (10, 10))

def hay_captura_obligatoria(juego, jugador):
    for fx in range(8):
        for cx in range(8):
            ficha = juego.tablero[fx][cx]
            if ficha.lower() == jugador:
                if juego.puede_capturar((fx, cx), jugador):
                    return True
    return False

def obtener_capturas(juego, jugador):
    capturas = []
    for fx in range(8):
        for cx in range(8):
            ficha = juego.tablero[fx][cx]
            if ficha.lower() == jugador:
                for dx in [-2, 2]:
                    for dy in [-2, 2]:
                        fy, cy = fx + dx, cx + dy
                        if 0 <= fy < 8 and 0 <= cy < 8:
                            valido, captura = juego.movimiento_valido((fx, cx), (fy, cy), jugador)
                            if valido and captura:
                                capturas.append(((fx, cx), (fy, cy)))
    return capturas

def pantalla_inicio():
    font_titulo = pygame.font.SysFont(None, 80)
    font_boton = pygame.font.SysFont(None, 48)
    font_creditos = pygame.font.SysFont(None, 24)
    titulo = font_titulo.render('Damas', True, (30, 144, 255))
    boton = font_boton.render('Jugar', True, (255, 255, 255))
    boton_rect = pygame.Rect(ANCHO//2 - 100, ALTO//2, 200, 60)
    creditos = font_creditos.render('por Cristian', True, (100, 100, 100))
    while True:
        ventana.fill((240, 217, 181))
        ventana.blit(titulo, (ANCHO//2 - titulo.get_width()//2, ALTO//3 - 60))
        pygame.draw.rect(ventana, (30, 144, 255), boton_rect, border_radius=12)
        ventana.blit(boton, (boton_rect.x + boton_rect.width//2 - boton.get_width()//2, boton_rect.y + 10))
        ventana.blit(creditos, (ANCHO//2 - creditos.get_width()//2, ALTO - 40))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if boton_rect.collidepoint(event.pos):
                    return

def animar_movimiento(tablero, origen, destino, color_ficha, es_dama_ficha):
    frames = 12
    fx, fy = origen[1] * TAM_CASILLA + TAM_CASILLA // 2, origen[0] * TAM_CASILLA + TAM_CASILLA // 2
    tx, ty = destino[1] * TAM_CASILLA + TAM_CASILLA // 2, destino[0] * TAM_CASILLA + TAM_CASILLA // 2
    for i in range(1, frames + 1):
        ventana.fill((0, 0, 0))
        fichas = contar_fichas(tablero)
        dibujar_tablero(tablero, fichas=fichas)
        # Interpolación
        x = fx + (tx - fx) * i // frames
        y = fy + (ty - fy) * i // frames
        pygame.draw.circle(ventana, color_ficha, (x, y), TAM_CASILLA // 2 - 8)
        if es_dama_ficha:
            pygame.draw.circle(ventana, COLOR_DAMA, (x, y), TAM_CASILLA // 2 - 20)
        pygame.display.flip()
        pygame.time.delay(18)

def main():
    pantalla_inicio()
    juego = JuegoDamas()
    turno = 'x'
    seleccion = None
    mensaje = ''
    sugerencias = []
    modo_vs_cpu = False
    cpu_jugador = None
    historial = []
    # Preguntar al usuario si quiere jugar contra la computadora
    font = pygame.font.SysFont(None, 36)
    pregunta = font.render('¿Jugar contra la computadora? (Clic izquierdo: Sí, derecho: No)', True, (0,0,0))
    ventana.fill((255,255,255))
    ventana.blit(pregunta, (30, ALTO//2 - 20))
    pygame.display.flip()
    esperando = True
    while esperando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    modo_vs_cpu = True
                    cpu_jugador = 'o'
                    esperando = False
                elif event.button == 3:
                    modo_vs_cpu = False
                    cpu_jugador = None
                    esperando = False
    while True:
        if modo_vs_cpu and turno == cpu_jugador:
            pygame.time.wait(500)
            # --- CAPTURA OBLIGATORIA CPU ---
            if hay_captura_obligatoria(juego, cpu_jugador):
                posibles = obtener_capturas(juego, cpu_jugador)
            else:
                posibles = juego.movimientos_posibles(cpu_jugador)
            if not posibles:
                mensaje = '¡Ganas tú!'
                break
            origen, destino = random.choice(posibles)
            ficha = juego.tablero[origen[0]][origen[1]]
            color_ficha = COLOR_ROJO if ficha.lower() == 'x' else COLOR_AZUL
            es_dama_ficha = es_dama(ficha)
            animar_movimiento(juego.tablero, origen, destino, color_ficha, es_dama_ficha)
            valido, captura = juego.movimiento_valido(origen, destino, cpu_jugador)
            juego.mover_ficha(origen, destino, captura)
            historial.append(([[c for c in f] for f in juego.tablero], turno))
            if captura:
                reproducir_sonido(sonido_captura)
            elif juego.tablero[destino[0]][destino[1]] in ('X', 'O'):
                reproducir_sonido(sonido_coronacion)
            else:
                reproducir_sonido(sonido_movimiento)
            if captura and juego.puede_capturar(destino, cpu_jugador):
                while captura and juego.puede_capturar(destino, cpu_jugador):
                    pygame.time.wait(500)
                    saltos = [((o),(d)) for (o,d) in juego.movimientos_posibles(cpu_jugador) if o == destino]
                    if saltos:
                        _, destino2 = random.choice(saltos)
                        valido, captura = juego.movimiento_valido(destino, destino2, cpu_jugador)
                        juego.mover_ficha(destino, destino2, captura)
                        destino = destino2
                        reproducir_sonido(sonido_captura)
                    else:
                        break
            else:
                turno = 'o' if turno == 'x' else 'x'
            seleccion = None
            sugerencias = []
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_u and historial:
                        # Deshacer movimiento
                        estado, turno_prev = historial.pop()
                        juego.tablero = [[c for c in f] for f in estado]
                        turno = turno_prev
                        seleccion = None
                        sugerencias = []
                        mensaje = 'Deshacer'
                        continue
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    fila, col = y // TAM_CASILLA, x // TAM_CASILLA
                    if seleccion is None:
                        if juego.tablero[fila][col].lower() == turno:
                            # --- CAPTURA OBLIGATORIA JUGADOR ---
                            if hay_captura_obligatoria(juego, turno):
                                capturas = obtener_capturas(juego, turno)
                                if not any((fila, col) == o for o, _ in capturas):
                                    mensaje = '¡Debes capturar!'
                                    continue
                            seleccion = (fila, col)
                            sugerencias = sugerir_movimientos(juego.tablero, seleccion, turno)
                    else:
                        origen = seleccion
                        destino = (fila, col)
                        # Si hay captura obligatoria, solo permite movimientos de captura
                        if hay_captura_obligatoria(juego, turno):
                            capturas = obtener_capturas(juego, turno)
                            if (origen, destino) not in capturas:
                                mensaje = '¡Debes capturar!'
                                seleccion = None
                                sugerencias = []
                                reproducir_sonido(sonido_movimiento_no_valido)
                                continue
                        valido, captura = juego.movimiento_valido(origen, destino, turno)
                        if valido:
                            ficha = juego.tablero[origen[0]][origen[1]]
                            color_ficha = COLOR_ROJO if ficha.lower() == 'x' else COLOR_AZUL
                            es_dama_ficha = es_dama(ficha)
                            animar_movimiento(juego.tablero, origen, destino, color_ficha, es_dama_ficha)
                            historial.append(([[c for c in f] for f in juego.tablero], turno))
                            juego.mover_ficha(origen, destino, captura)
                            if captura:
                                reproducir_sonido(sonido_captura)
                            elif juego.tablero[destino[0]][destino[1]] in ('X', 'O'):
                                reproducir_sonido(sonido_coronacion)
                            else:
                                reproducir_sonido(sonido_movimiento)
                            seleccion = None
                            sugerencias = []
                            if captura and juego.puede_capturar(destino, turno):
                                seleccion = destino
                                sugerencias = sugerir_movimientos(juego.tablero, seleccion, turno)
                            else:
                                turno = 'o' if turno == 'x' else 'x'
                            mensaje = ''
                        else:
                            reproducir_sonido(sonido_movimiento_no_valido)
                            mensaje = 'Movimiento no válido'
                            seleccion = None
                            sugerencias = []
        ventana.fill((0, 0, 0))
        fichas = juego.contar_fichas()
        dibujar_tablero(juego.tablero, seleccion, sugerencias, fichas)
        if mensaje:
            font = pygame.font.SysFont(None, 36)
            text = font.render(mensaje, True, (255, 0, 0))
            ventana.blit(text, (20, ANCHO - 40))
        font = pygame.font.SysFont(None, 32)
        turno_text = font.render(f"Turno: {turno}  (Deshacer: U)", True, (0, 0, 0))
        ventana.blit(turno_text, (ANCHO - 260, 10))
        pygame.display.flip()
        ganador = juego.hay_ganador()
        if ganador:
            font = pygame.font.SysFont(None, 48)
            text = font.render(f'¡El jugador {ganador} ha ganado!', True, (0, 128, 0))
            ventana.blit(text, (ANCHO // 2 - 180, ALTO // 2 - 24))
            pygame.display.flip()
            pygame.time.wait(2500)
            break
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
