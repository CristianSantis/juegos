# Juego de damas mejorado con captura, saltos múltiples y coronación

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
    print("  " + " ".join(str(i) for i in range(8)))
    for i, fila in enumerate(tablero):
        print(i, " ".join(fila))

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
    # Coronación
    if ficha == 'x' and fy == 7:
        tablero[fy][cy] = 'X'
    elif ficha == 'o' and fy == 0:
        tablero[fy][cy] = 'O'
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

def jugar():
    tablero = inicializar_tablero()
    turno = 'x'
    while True:
        mostrar_tablero(tablero)
        print(f"Turno del jugador '{turno}'")
        try:
            origen = tuple(map(int, input("Ficha a mover (fila col): ").split()))
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
            print("Movimiento no válido. Intenta de nuevo.")

if __name__ == "__main__":
    jugar()
