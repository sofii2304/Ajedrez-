import tkinter as tk

class GameState():
    def __init__(self):
        self.piezas = [
            ["TorreNegra", "CaballoNegro", "AlfilNegro", "DamaNegra", "ReyNegro", "AlfilNegro", "CaballoNegro", "TorreNegra"],
            ["PeonNegro", "PeonNegro", "PeonNegro", "PeonNegro", "PeonNegro", "PeonNegro", "PeonNegro", "PeonNegro"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["PeonBlanco", "PeonBlanco", "PeonBlanco", "PeonBlanco", "PeonBlanco", "PeonBlanco", "PeonBlanco", "PeonBlanco"],
            ["TorreBlanca", "CaballoBlanco", "AlfilBlanco", "DamaBlanca", "ReyBlanco",  "AlfilBlanco", "CaballoBlanco", "TorreBlanca"]
        ]

    def imprimirTablero(self):
        for fila in self.piezas:
            print(" ".join(fila))

    def mover_ficha(self, fila_origen, columna_origen, fila_destino, columna_destino):
        pieza = self.piezas[fila_origen][columna_origen]
        self.piezas[fila_origen][columna_origen] = "--"
        self.piezas[fila_destino][columna_destino] = pieza


class App():
    def __init__(self, L_QUADRADO):
        self.gs = GameState()
        self.L_QUADRADO = L_QUADRADO
        self.imagenes = {}

        self.ventana = tk.Tk()
        self.ventana.title("Motor de Ajedrez")
        self.ventana.iconbitmap("ajedrez.ico")
        self.ventana.geometry(f"{str(L_QUADRADO*8)}x{str(L_QUADRADO*8)}")
        self.ventana.resizable(0, 0)

        self.interfaz = tk.Canvas(self.ventana)
        self.interfaz.pack(fill="both", expand=True)

        self.cargarImagenes()

        self.dibujarTablero()
        self.mostrarPiezas()

        self.pieza_seleccionada = None
        self.ultima_posicion = None

        self.interfaz.bind("<Button-1>", self.click)
        self.interfaz.bind("<B1-Motion>", self.movimiento)
        self.interfaz.bind("<ButtonRelease-1>", self.soltar)

    def cargarImagenes(self):
        piezas = ["PeonNegro", "TorreNegra", "CaballoNegro", "AlfilNegro", "DamaNegra", 
                  "ReyNegro", "PeonBlanco", "TorreBlanca", "CaballoBlanco", "AlfilBlanco", 
                  "DamaBlanca", "ReyBlanco"]
        for pieza in piezas:
            ruta = "./img/" + pieza + ".png"
            print("Ruta de imagen:", ruta)
            imagen = tk.PhotoImage(file=ruta)
            # Redimensionar la imagen al tamaño del cuadrado del tablero
            imagen = imagen.subsample(4, 4)
            self.imagenes[pieza.lower()] = imagen

    def __call__(self):
        self.ventana.mainloop()

    def dibujarTablero(self):
        for i in range(8):
            for j in range(8):
                if (i+j) % 2 == 0:
                    self.interfaz.create_rectangle(j*self.L_QUADRADO, i*self.L_QUADRADO,
                                                   (j+1)*self.L_QUADRADO, (i+1)*self.L_QUADRADO,
                                                   fill="#dfc07f")
                else:
                    self.interfaz.create_rectangle(j*self.L_QUADRADO, i*self.L_QUADRADO,
                                                   (j+1)*self.L_QUADRADO, (i+1)*self.L_QUADRADO,
                                                   fill="#7a4f37")

    def mostrarPiezas(self):
        for indice_i, i in enumerate(self.gs.piezas):
            for indice_j, j in enumerate(i):
                if j != "--":
                    self.interfaz.create_image(indice_j*self.L_QUADRADO, indice_i*self.L_QUADRADO,
                                               image=self.imagenes[j.lower()], anchor="nw")

    def click(self, event):
        columna = event.x // self.L_QUADRADO
        fila = event.y // self.L_QUADRADO
        pieza = self.gs.piezas[fila][columna]
        if pieza != "--":
            self.pieza_seleccionada = (fila, columna)
            self.ultima_posicion = (event.x, event.y)

    def movimiento(self, event):
        if self.pieza_seleccionada:
            dx = event.x - self.ultima_posicion[0]
            dy = event.y - self.ultima_posicion[1]
            self.interfaz.move("pieza_seleccionada", dx, dy)
            self.ultima_posicion = (event.x, event.y)

    def soltar(self, event):
        if self.pieza_seleccionada:
            columna = event.x // self.L_QUADRADO
            fila = event.y // self.L_QUADRADO
            destino = (fila, columna)
            self.gs.mover_ficha(*self.pieza_seleccionada, *destino)
            self.pieza_seleccionada = None
            self.ultima_posicion = None
            self.dibujarTablero()
            self.mostrarPiezas()


# Instanciar la aplicación
MotordeAjedrez = App(70)

# Llamar a la función __call__() para iniciar el bucle de eventos
MotordeAjedrez()
