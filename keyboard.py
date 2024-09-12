import tkinter as tk

def key_press(key):
    print(f"Key pressed: {key}")

# Création de la fenêtre principale
root = tk.Tk()
root.title("Clavier Virtuel")

# Liste des touches du clavier
keys = [
    'a', 'z', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p',
    'q', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm',
    'w', 'x', 'c', 'v', 'b', 'n'
]

# Création des boutons pour chaque touche
for key in keys:
    button = tk.Button(root, text=key, command=lambda k=key: key_press(k), width=4, height=2)
    button.grid(row=keys.index(key) // 10, column=keys.index(key) % 10)

# Exécution de la boucle principale
root.mainloop()
