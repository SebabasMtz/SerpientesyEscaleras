import tkinter as tk
from tkinter import messagebox
import random

class SerpientesEscalerasGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Serpientes y Escaleras")
        self.root.geometry("600x600")
        
        self.mostrar_menu_inicio()

    def mostrar_menu_inicio(self):
        """Muestra un menú inicial con las reglas y un botón para iniciar el juego."""
        self.menu_frame = tk.Frame(self.root)
        self.menu_frame.pack(fill="both", expand=True)

        titulo = tk.Label(self.menu_frame, text="¡Bienvenido a Serpientes y Escaleras!", font=("Arial", 18, "bold"))
        titulo.pack(pady=20)

        reglas = (
            "Reglas del Juego:\n"
            "- El tablero tiene casillas numeradas del 1 al 100.\n"
            "- Si caes en una escalera, subes a una posición más alta.\n"
            "- Si caes en una serpiente, bajas a una posición más baja.\n"
            "- Gana quien llegue primero a la casilla 100.\n\n"
            "Colores de los jugadores:\n"
            "- Tú (Jugador): Rojo\n"
            "- IA (Computadora): Azul"
        )

        reglas_label = tk.Label(self.menu_frame, text=reglas, font=("Arial", 12), justify="left")
        reglas_label.pack(pady=20)

        boton_iniciar = tk.Button(self.menu_frame, text="Iniciar Juego", font=("Arial", 14), command=self.iniciar_juego)
        boton_iniciar.pack(pady=10)

    def iniciar_juego(self):
        self.menu_frame.destroy()
        self.configurar_juego()

    def configurar_juego(self):
        # Configuración inicial del tablero y jugadores
        self.max_pos = 100
        self.serpientes = {17: 7, 54: 34, 62: 19, 87: 24, 98: 79}
        self.escaleras = {3: 38, 14: 31, 27: 84, 40: 59, 72: 91}
        self.jugadores = {"Jugador": 1, "IA": 1}  # Los jugadores comienzan en la casilla 1
        self.turno_actual = "Jugador"
        
        # Cargar imágenes
        self.imagen_serpiente = tk.PhotoImage(file="serpiente.png")
        self.imagen_escalera = tk.PhotoImage(file="escalera.png")
        
        # Crear elementos gráficos
        self.crear_interfaz()
        self.actualizar_tablero()

    def crear_interfaz(self):
        # Tablero
        self.tablero = tk.Canvas(self.root, width=450, height=450, bg="lightblue")
        self.tablero.pack(pady=20)
        self.dibujar_tablero()

        # Botones e información
        self.info_turno = tk.Label(self.root, text="Turno: Jugador", font=("Arial", 14))
        self.info_turno.pack(pady=10)

        self.boton_lanzar = tk.Button(self.root, text="Lanzar Dado", command=self.lanzar_dado)
        self.boton_lanzar.pack(pady=10)

    def dibujar_tablero(self):
        size = 45  # Tamaño de cada celda
        for i in range(10):
            for j in range(10):
                x0 = j * size
                y0 = i * size
                x1 = x0 + size
                y1 = y0 + size
                pos = (9 - i) * 10 + (j + 1) if (9 - i) % 2 == 0 else (9 - i) * 10 + (10 - j)
                self.tablero.create_rectangle(x0, y0, x1, y1, fill="white", outline="black")
                self.tablero.create_text(x0 + 20, y0 + 20, text=str(pos))

                # Colocar imágenes de serpientes y escaleras y mostrar su destino
                if pos in self.serpientes:
                    self.tablero.create_image(x0 + 20, y0 + 10, image=self.imagen_serpiente, tags="serpientes")
                    self.tablero.create_text(x0 + 20, y0 + 35, text=f"Baja a {self.serpientes[pos]}", fill="red", font=("Arial", 8))
                elif pos in self.escaleras:
                    self.tablero.create_image(x0 + 20, y0 + 10, image=self.imagen_escalera, tags="escaleras")
                    self.tablero.create_text(x0 + 20, y0 + 35, text=f"Sube a {self.escaleras[pos]}", fill="green", font=("Arial", 8))

    def lanzar_dado(self):
        dado = random.randint(1, 6)
        messagebox.showinfo("Dado", f"Obtuviste un {dado}")
        self.mover_jugador(self.turno_actual, dado)

    def mover_jugador(self, jugador, dado):
        nueva_pos = self.jugadores[jugador] + dado

        if nueva_pos > self.max_pos:
            messagebox.showinfo("Turno perdido", f"{jugador} necesita un número exacto para ganar.")
        else:
            if nueva_pos in self.serpientes:
                nueva_pos = self.serpientes[nueva_pos]
                messagebox.showinfo("Serpiente", f"{jugador} cayó en una serpiente. Baja a {nueva_pos}.")
            elif nueva_pos in self.escaleras:
                nueva_pos = self.escaleras[nueva_pos]
                messagebox.showinfo("Escalera", f"{jugador} subió por una escalera. Sube a {nueva_pos}.")

            self.jugadores[jugador] = nueva_pos
            self.actualizar_tablero()

            if nueva_pos == self.max_pos:
                messagebox.showinfo("¡Ganador!", f"¡{jugador} ha ganado el juego!")
                self.root.quit()

        self.cambiar_turno()

    def actualizar_tablero(self):
        self.tablero.delete("fichas")
        colores = {"Jugador": "red", "IA": "blue"}
        size = 45  # Tamaño de cada casilla en el tablero

        # El cálculo de la posición de la ficha ahora está corregido
        for jugador, pos in self.jugadores.items():
            fila = (pos - 1) // 10
            col = (pos - 1) % 10
            if fila % 2 == 1:  # Invertir las columnas en filas impares
                col = 9 - col
            x = col * size + size / 2  # Centramos la ficha dentro de la casilla
            y = (9 - fila) * size + size / 2  # Centramos la ficha dentro de la casilla
            self.tablero.create_oval(x - 10, y - 10, x + 10, y + 10, fill=colores[jugador], tags="fichas")

    def cambiar_turno(self):
        if self.turno_actual == "Jugador":
            self.turno_actual = "IA"
            self.info_turno.config(text="Turno: IA")
            self.root.after(1000, self.turno_ia)  # Esperar 1 segundo antes de jugar el turno de la IA
        else:
            self.turno_actual = "Jugador"
            self.info_turno.config(text="Turno: Jugador")

    def turno_ia(self):
        dado = random.randint(1, 6)
        messagebox.showinfo("Dado IA", f"La IA obtuvo un {dado}")
        self.mover_jugador("IA", dado)


# Ejecutar el juego
if __name__ == "__main__":
    root = tk.Tk()
    juego = SerpientesEscalerasGUI(root)
    root.mainloop()


