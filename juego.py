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
            "- IA Azul: Azul\n"
            "- IA Verde: Verde"
        )

        reglas_label = tk.Label(self.menu_frame, text=reglas, font=("Arial", 12), justify="left")
        reglas_label.pack(pady=20)

        boton_iniciar = tk.Button(self.menu_frame, text="Iniciar Juego", font=("Arial", 14), command=self.iniciar_juego)
        boton_iniciar.pack(pady=10)

    def iniciar_juego(self):
        self.menu_frame.destroy()
        self.configurar_juego()

    def configurar_juego(self):
        self.max_pos = 100
        self.serpientes = {17: 7, 54: 34, 62: 19, 87: 24, 98: 79}
        self.escaleras = {3: 38, 14: 31, 27: 84, 40: 59, 72: 91}
        self.jugadores = {"Jugador": 1, "IA Azul": 1, "IA Verde": 1}
        self.turno_actual = "Jugador"
        self.dados = {"Jugador": 2, "IA Azul": 2, "IA Verde": 2}
        
        self.crear_interfaz()
        self.actualizar_tablero()

    def crear_interfaz(self):
        self.tablero = tk.Canvas(self.root, width=450, height=450, bg="lightblue")
        self.tablero.pack(pady=20)
        self.dibujar_tablero()

        self.info_turno = tk.Label(self.root, text="Turno: Jugador", font=("Arial", 14))
        self.info_turno.pack(pady=10)

        self.boton_dado = tk.Button(self.root, text="Lanzar Dado", command=self.lanzar_dado)
        self.boton_dado.pack(pady=10)

        self.selector_dados = tk.IntVar(value=2)
        tk.Label(self.root, text="Elige el número de dados:", font=("Arial", 12)).pack()
        tk.Radiobutton(self.root, text="1 Dado", variable=self.selector_dados, value=1).pack()
        tk.Radiobutton(self.root, text="2 Dados", variable=self.selector_dados, value=2).pack()

    def dibujar_tablero(self):
        size = 45
        for i in range(10):
            for j in range(10):
                x0 = j * size
                y0 = i * size
                x1 = x0 + size
                y1 = y0 + size
                pos = (9 - i) * 10 + (j + 1) if (9 - i) % 2 == 0 else (9 - i) * 10 + (10 - j)
                self.tablero.create_rectangle(x0, y0, x1, y1, fill="white", outline="black")
                self.tablero.create_text(x0 + 20, y0 + 20, text=str(pos))

                if pos in self.serpientes:
                    self.tablero.create_text(x0 + 20, y0 + 35, text=f"Baja a {self.serpientes[pos]}", fill="red", font=("Arial", 8))
                elif pos in self.escaleras:
                    self.tablero.create_text(x0 + 20, y0 + 35, text=f"Sube a {self.escaleras[pos]}", fill="green", font=("Arial", 8))

    def lanzar_dado(self):
        num_dados = self.selector_dados.get() if self.turno_actual == "Jugador" else self.dados[self.turno_actual]
        dado = sum(random.randint(1, 6) for _ in range(num_dados))
        messagebox.showinfo("Dado", f"Se lanzaron {num_dados} dado(s): Resultado = {dado}")
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
        colores = {"Jugador": "red", "IA Azul": "blue", "IA Verde": "green"}
        size = 45
        for jugador, pos in self.jugadores.items():
            fila = (pos - 1) // 10
            col = (pos - 1) % 10
            if fila % 2 == 1:
                col = 9 - col
            x = col * size + size / 2
            y = (9 - fila) * size + size / 2
            self.tablero.create_oval(x - 10, y - 10, x + 10, y + 10, fill=colores[jugador], tags="fichas")

    def cambiar_turno(self):
        turnos = list(self.jugadores.keys())
        turno_index = turnos.index(self.turno_actual)
        self.turno_actual = turnos[(turno_index + 1) % len(turnos)]
        self.info_turno.config(text=f"Turno: {self.turno_actual}")
        if "IA" in self.turno_actual:
            self.root.after(1000, self.turno_ia)

    def turno_ia(self):
        posicion_actual = self.jugadores[self.turno_actual]
        mejores_dados = 2
        for dados in [1, 2]:
            dado = sum(random.randint(1, 6) for _ in range(dados))
            nueva_pos = posicion_actual + dado
            if nueva_pos in self.escaleras or (nueva_pos not in self.serpientes and nueva_pos <= self.max_pos):
                mejores_dados = dados
                break
        self.dados[self.turno_actual] = mejores_dados
        self.lanzar_dado()

# Ejecutar el juego
if __name__ == "__main__":
    root = tk.Tk()
    juego = SerpientesEscalerasGUI(root)
    root.mainloop()
