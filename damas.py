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
    if ficha == 'x':
        return Fore.RED + Style.BRIGHT + '⛂' + Style.RESET_ALL
    elif ficha == 'X':
        return Fore.RED + Style.BRIGHT + '⛃' + Style.RESET_ALL
    elif ficha == 'o':
        return Fore.BLUE + Style.BRIGHT + '⛀' + Style.RESET_ALL
    elif ficha == 'O':
        return Fore.BLUE + Style.BRIGHT + '⛁' + Style.RESET_ALL
    return ficha

from damas import JuegoDamas

def mostrar_tablero(tablero):
    print("    " + "   ".join(str(i) for i in range(8)))
    print("  ┏" + ("━━━┳" * 7) + "━━━┓")
    for i, fila in enumerate(tablero):
        fila_str = f"{i} ┃"
        for j, celda in enumerate(fila):
            if (i + j) % 2 == 1:
                if celda == 'x':
                    ficha_coloreada = '\033[91m⛂\033[0m'
                elif celda == 'X':
                    ficha_coloreada = '\033[91m⛃\033[0m'
                elif celda == 'o':
                    ficha_coloreada = '\033[94m⛀\033[0m'
                elif celda == 'O':
                    ficha_coloreada = '\033[94m⛁\033[0m'
                elif celda == ' ':
                    ficha_coloreada = '\033[37m·\033[0m'
                else:
                    ficha_coloreada = celda
                fila_str += f" {ficha_coloreada} ┃"
            else:
                fila_str += "   ┃"
        print(fila_str)
        if i < 7:
            print("  ┣" + ("━━━╋" * 7) + "━━━┫")
    print("  ┗" + ("━━━┻" * 7) + "━━━┛")

def contar_fichas(tablero):
    x = o = X = O = 0
    for fila in tablero:
        for celda in fila:
            if celda == 'x': x += 1
            elif celda == 'o': o += 1
            elif celda == 'X': X += 1
            elif celda == 'O': O += 1
    return x, o, X, O

def sugerir_movimientos(juego, origen, jugador):
    sugerencias = []
    fx, cx = origen
    for dx in [-1, 1, -2, 2]:
        for dy in [-1, 1, -2, 2]:
            fy, cy = fx + dx, cx + dy
            if 0 <= fy < juego.size and 0 <= cy < juego.size:
                valido, captura = juego.movimiento_valido((fx, cx), (fy, cy), jugador)
                if valido:
                    sugerencias.append((fy, cy))
    return sugerencias

def jugar():
    juego = JuegoDamas()
    turno = 'x'
    while True:
        mostrar_tablero(juego.tablero)
        x, o, X, O = juego.contar_fichas()
        print(f"Fichas x: {x} | X: {X}   o: {o} | O: {O}")
        ganador = juego.hay_ganador()
        if ganador:
            print(f"¡El jugador '{ganador}' ha ganado!")
            break
        print(f"Turno del jugador '{turno}'")
        try:
            origen = tuple(map(int, input("Ficha a mover (fila col): ").split()))
            if juego.tablero[origen[0]][origen[1]].lower() == turno:
                sugerencias = sugerir_movimientos(juego, origen, turno)
                if sugerencias:
                    print("Movimientos posibles desde esa ficha:", sugerencias)
            destino = tuple(map(int, input("Destino (fila col): ").split()))
        except ValueError:
            print("Entrada inválida. Intenta de nuevo.")
            continue
        valido, captura = juego.movimiento_valido(origen, destino, turno)
        if valido:
            nueva_ficha = juego.mover_ficha(origen, destino, captura)
            while captura and juego.puede_capturar(destino, turno):
                mostrar_tablero(juego.tablero)
                print(f"¡Captura extra disponible para '{turno}'!")
                origen = destino
                try:
                    destino = tuple(map(int, input("Siguiente salto (fila col): ").split()))
                except ValueError:
                    break
                valido, captura = juego.movimiento_valido(origen, destino, turno)
                if valido and captura:
                    nueva_ficha = juego.mover_ficha(origen, destino, captura)
                else:
                    break
            turno = 'o' if turno == 'x' else 'x'
        else:
            print("Movimiento no válido. Intenta de nuevo.");

if __name__ == "__main__":
    jugar()
