"""
Modulo damas: lógica de juego de damas como clase reutilizable.
"""
from typing import List, Tuple, Optional

class JuegoDamas:
    def __init__(self, size: int = 8):
        self.size = size
        self.tablero = self.inicializar_tablero()

    def inicializar_tablero(self) -> List[List[str]]:
        tablero = [[' ' for _ in range(self.size)] for _ in range(self.size)]
        for fila in range(3):
            for col in range(self.size):
                if (fila + col) % 2 == 1:
                    tablero[fila][col] = 'x'
        for fila in range(self.size - 3, self.size):
            for col in range(self.size):
                if (fila + col) % 2 == 1:
                    tablero[fila][col] = 'o'
        return tablero

    @staticmethod
    def es_dama(ficha: str) -> bool:
        return ficha in ('X', 'O')

    @staticmethod
    def direccion(jugador: str) -> int:
        return 1 if jugador == 'x' else -1

    def movimiento_valido(self, origen: Tuple[int, int], destino: Tuple[int, int], jugador: str) -> Tuple[bool, Optional[Tuple[int, int]]]:
        fx, cx = origen
        fy, cy = destino
        if not (0 <= fx < self.size and 0 <= cx < self.size and 0 <= fy < self.size and 0 <= cy < self.size):
            return False, None
        ficha = self.tablero[fx][cx]
        if ficha.lower() != jugador:
            return False, None
        if self.tablero[fy][cy] != ' ':
            return False, None
        dx = fy - fx
        dy = cy - cx
        dir_jugador = self.direccion(jugador)
        # Movimiento normal
        if abs(dx) == 1 and abs(dy) == 1:
            if ficha.islower() and dx != dir_jugador:
                return False, None
            return True, None
        # Captura
        if abs(dx) == 2 and abs(dy) == 2:
            midx = (fx + fy) // 2
            midy = (cx + cy) // 2
            ficha_media = self.tablero[midx][midy]
            if ficha_media.lower() not in ('x', 'o') or ficha_media.lower() == jugador:
                return False, None
            if ficha.islower() and dx != 2 * dir_jugador:
                return False, None
            return True, (midx, midy)
        return False, None

    def mover_ficha(self, origen: Tuple[int, int], destino: Tuple[int, int], captura: Optional[Tuple[int, int]]) -> str:
        fx, cx = origen
        fy, cy = destino
        ficha = self.tablero[fx][cx]
        self.tablero[fy][cy] = ficha
        self.tablero[fx][cx] = ' '
        if captura:
            mx, my = captura
            self.tablero[mx][my] = ' '
        # Coronación
        if ficha == 'x' and fy == self.size - 1:
            self.tablero[fy][cy] = 'X'
        elif ficha == 'o' and fy == 0:
            self.tablero[fy][cy] = 'O'
        return self.tablero[fy][cy]

    def puede_capturar(self, origen: Tuple[int, int], jugador: str) -> bool:
        fx, cx = origen
        saltos = [(-2, -2), (-2, 2), (2, -2), (2, 2)]
        for dx, dy in saltos:
            fy, cy = fx + dx, cx + dy
            if 0 <= fy < self.size and 0 <= cy < self.size:
                valido, captura = self.movimiento_valido((fx, cx), (fy, cy), jugador)
                if valido and captura:
                    return True
        return False

    def hay_ganador(self) -> Optional[str]:
        x = o = X = O = 0
        for fila in self.tablero:
            for celda in fila:
                if celda == 'x': x += 1
                elif celda == 'o': o += 1
                elif celda == 'X': X += 1
                elif celda == 'O': O += 1
        if x + X == 0:
            return 'o'
        if o + O == 0:
            return 'x'
        return None

    def movimientos_posibles(self, jugador: str) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
        moves = []
        for fx in range(self.size):
            for cx in range(self.size):
                ficha = self.tablero[fx][cx]
                if ficha.lower() == jugador:
                    for dx in [-1, 1, -2, 2]:
                        for dy in [-1, 1, -2, 2]:
                            fy, cy = fx + dx, cx + dy
                            if 0 <= fy < self.size and 0 <= cy < self.size:
                                valido, captura = self.movimiento_valido((fx, cx), (fy, cy), jugador)
                                if valido:
                                    moves.append(((fx, cx), (fy, cy)))
        return moves

    def contar_fichas(self) -> Tuple[int, int, int, int]:
        x = o = X = O = 0
        for fila in self.tablero:
            for celda in fila:
                if celda == 'x': x += 1
                elif celda == 'o': o += 1
                elif celda == 'X': X += 1
                elif celda == 'O': O += 1
        return x, o, X, O
