# Juego de damas mejorado con captura, saltos múltiples y coronación
from colorama import Fore, Style, init
init(autoreset=True)

import pygame
# Inicializar pygame
pygame.mixer.init()

# Cargar sonidos con manejo de errores
try:
    sonido_movimiento = pygame.mixer.Sound('sounds/483600__raclure__cursor.wav')
    sonido_captura = pygame.mixer.Sound('sounds/445884__lauracarolina09__48-blood.wav')
    sonido_movimiento_no_valido = pygame.mixer.Sound('sounds/363920__samsterbirdies__8-bit-error.wav')
    sonido_coronacion = pygame.mixer.Sound('sounds/721208__ahhh.wav')
    sonidos_habilitados = True
except pygame.error:
    print("No se pudieron cargar los sonidos. El juego continuará sin audio.")
    sonidos_habilitados = False

# Función helper para reproducir sonidos
def reproducir_sonido(sonido):
    if sonidos_habilitados:
        sonido.play()

def color_ficha(ficha):
    if ficha.lower() == 'x':
        return Fore.RED + ficha + Style.RESET_ALL
    elif ficha.lower() == 'o':
        return Fore.BLUE + ficha + Style.RESET_ALL
    return ficha

def inicializar_tablero():
    tablero = [[' ' for _ in range(8)] for _ in range(8)]
    for fila in range(3):
        for col in range(8):
            if (fila + col) % 2 == 1:
                tablero[fila][col] = 'x'
    for fila in range(5, 8):
        for col in range(8):
            if (fila + col) % 2 == 1:
                tablero[fila][col] = 'o'
    return tablero

def mostrar_tablero(tablero):
    print("    " + "   ".join(str(i) for i in range(8)))
    print("  ┌" + ("───┬" * 7) + "───┐")
    for i, fila in enumerate(tablero):
        fila_str = f"{i} │"
        for j, celda in enumerate(fila):
            if (i + j) % 2 == 1:
                # Casilla negra
                ficha_coloreada = color_ficha(celda)
                if celda == ' ':
                    ficha_coloreada = Fore.WHITE + '·' + Style.RESET_ALL
                fila_str += f" {ficha_coloreada} │"
            else:
                # Casilla blanca
                fila_str += "   │"
        print(fila_str)
        if i < 7:
            print("  ├" + ("───┼" * 7) + "───┤")
    print("  └" + ("───┴" * 7) + "───┘")

def es_dama(ficha):
    return ficha in ('X', 'O')

def direccion(jugador):
    return 1 if jugador == 'x' else -1

def movimiento_valido(tablero, origen, destino, jugador):
    fx, cx = origen
    fy, cy = destino
    if not (0 <= fx < 8 and 0 <= cx < 8 and 0 <= fy < 8 and 0 <= cy < 8):
        return False, None
    ficha = tablero[fx][cx]
    if ficha.lower() != jugador:
        return False, None
    if tablero[fy][cy] != ' ':
        return False, None
    dx = fy - fx
    dy = cy - cx
    dir_jugador = direccion(jugador)

    # Movimiento normal
    if abs(dx) == 1 and abs(dy) == 1:
        if ficha.islower() and dx != dir_jugador:
            return False, None
        return True, None

    # Captura
    if abs(dx) == 2 and abs(dy) == 2:
        midx = (fx + fy) // 2
        midy = (cx + cy) // 2
        ficha_media = tablero[midx][midy]
        if ficha_media.lower() not in ('x', 'o') or ficha_media.lower() == jugador:
            return False, None
        if ficha.islower() and dx != 2 * dir_jugador:
            return False, None
        return True, (midx, midy)

    return False, None

def mover_ficha(tablero, origen, destino, captura):
    fx, cx = origen
    fy, cy = destino
    ficha = tablero[fx][cx]
    tablero[fy][cy] = ficha
    tablero[fx][cx] = ' '
    if captura:
        mx, my = captura
        tablero[mx][my] = ' '
        reproducir_sonido(sonido_captura)
    else: 
        reproducir_sonido(sonido_movimiento)
    # Coronación
    if ficha == 'x' and fy == 7:
        tablero[fy][cy] = 'X'
        reproducir_sonido(sonido_coronacion)
    elif ficha == 'o' and fy == 0:
        tablero[fy][cy] = 'O'
        reproducir_sonido(sonido_coronacion)
    return tablero[fy][cy]

def puede_capturar(tablero, origen, jugador):
    fx, cx = origen
    ficha = tablero[fx][cx]
    saltos = [(-2, -2), (-2, 2), (2, -2), (2, 2)]
    for dx, dy in saltos:
        fy, cy = fx + dx, cx + dy
        if 0 <= fy < 8 and 0 <= cy < 8:
            valido, captura = movimiento_valido(tablero, (fx, cx), (fy, cy), jugador)
            if valido and captura:
                return True
    return False

def contar_fichas(tablero):
    x = o = X = O = 0
    for fila in tablero:
        for celda in fila:
            if celda == 'x': x += 1
            elif celda == 'o': o += 1
            elif celda == 'X': X += 1
            elif celda == 'O': O += 1
    return x, o, X, O

def hay_ganador(tablero):
    x, o, X, O = contar_fichas(tablero)
    if x + X == 0:
        return 'o'
    if o + O == 0:
        return 'x'
    return None

def movimientos_posibles(tablero, jugador):
    moves = []
    for fx in range(8):
        for cx in range(8):
            ficha = tablero[fx][cx]
            if ficha.lower() == jugador:
                for dx in [-1, 1, -2, 2]:
                    for dy in [-1, 1, -2, 2]:
                        fy, cy = fx + dx, cx + dy
                        if 0 <= fy < 8 and 0 <= cy < 8:
                            valido, captura = movimiento_valido(tablero, (fx, cx), (fy, cy), jugador)
                            if valido:
                                moves.append(((fx, cx), (fy, cy)))
    return moves

def sugerir_movimientos(tablero, origen, jugador):
    sugerencias = []
    fx, cx = origen
    for dx in [-1, 1, -2, 2]:
        for dy in [-1, 1, -2, 2]:
            fy, cy = fx + dx, cx + dy
            if 0 <= fy < 8 and 0 <= cy < 8:
                valido, captura = movimiento_valido(tablero, (fx, cx), (fy, cy), jugador)
                if valido:
                    sugerencias.append((fy, cy))
    return sugerencias

import random

def jugar():
    tablero = inicializar_tablero()
    turno = 'x'
    modo_vs_cpu = input("¿Quieres jugar contra la computadora? (s/n): ").strip().lower() == 's'
    cpu_jugador = 'o' if modo_vs_cpu else None
    while True:
        mostrar_tablero(tablero)
        x, o, X, O = contar_fichas(tablero)
        print(f"Fichas x: {x} | X: {X}   o: {o} | O: {O}")
        ganador = hay_ganador(tablero)
        if ganador:
            print(f"¡El jugador '{ganador}' ha ganado!")
            break
        print(f"Turno del jugador '{turno}'")
        if modo_vs_cpu and turno == cpu_jugador:
            # Turno de la computadora
            posibles = movimientos_posibles(tablero, cpu_jugador)
            if not posibles:
                print("La computadora no puede mover. ¡Ganas tú!")
                break
            origen, destino = random.choice(posibles)
            print(f"La computadora mueve de {origen} a {destino}")
            valido, captura = movimiento_valido(tablero, origen, destino, cpu_jugador)
            nueva_ficha = mover_ficha(tablero, origen, destino, captura)
            while captura and puede_capturar(tablero, destino, cpu_jugador):
                mostrar_tablero(tablero)
                print(f"¡Captura extra para la computadora!")
                origen = destino
                posibles_saltos = [((origen), (fx, fy)) for (o, (fx, fy)) in movimientos_posibles(tablero, cpu_jugador) if o == origen]
                if posibles_saltos:
                    _, destino = random.choice(posibles_saltos)
                    print(f"La computadora salta a {destino}")
                    valido, captura = movimiento_valido(tablero, origen, destino, cpu_jugador)
                    nueva_ficha = mover_ficha(tablero, origen, destino, captura)
                else:
                    break
            turno = 'o' if turno == 'x' else 'x'
        else:
            try:
                origen = tuple(map(int, input("Ficha a mover (fila col): ").split()))
                if tablero[origen[0]][origen[1]].lower() == turno:
                    sugerencias = sugerir_movimientos(tablero, origen, turno)
                    if sugerencias:
                        print("Movimientos posibles desde esa ficha:", sugerencias)
                destino = tuple(map(int, input("Destino (fila col): ").split()))
            except ValueError:
                print("Entrada inválida. Intenta de nuevo.")
                continue
            valido, captura = movimiento_valido(tablero, origen, destino, turno)
            if valido:
                nueva_ficha = mover_ficha(tablero, origen, destino, captura)
                while captura and puede_capturar(tablero, destino, turno):
                    mostrar_tablero(tablero)
                    print(f"¡Captura extra disponible para '{turno}'!")
                    origen = destino
                    try:
                        destino = tuple(map(int, input("Siguiente salto (fila col): ").split()))
                    except ValueError:
                        break
                    valido, captura = movimiento_valido(tablero, origen, destino, turno)
                    if valido and captura:
                        nueva_ficha = mover_ficha(tablero, origen, destino, captura)
                    else:
                        break
                turno = 'o' if turno == 'x' else 'x'
            else:
                reproducir_sonido(sonido_movimiento_no_valido)
                print("Movimiento no válido. Intenta de nuevo.")

if __name__ == "__main__":
    jugar()
