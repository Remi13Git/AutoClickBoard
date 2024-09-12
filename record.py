from pynput import mouse, keyboard
import time
import json
import os


# Variables Parameters
azertyMode = True
recordingDuration = 3000


print("Répertoire actuel :", os.getcwd())

# Liste pour stocker les enregistrements
recordings = []

#Azerty <--> Qwerty
azerty = "azertyuiop^$qsdfghjklmùwxcvbn,;:!'AZERTYUIOPQSDFGHJKLMWXCVBN"
qwerty = "qwertyuiop[]asdfghjkl;'zxcvbnm,.!ùQWERTYUIOPASDFGHJKL;ZXCVBN"

# join as keys and values
tr = dict(zip(azerty, qwerty))

key_states = {"shift": False}

def translate_azerty_to_qwerty(key):
    """Returns qwerty key or the given key itself if no mapping found"""
    translated_key = "".join([tr.get(char, char) for char in key])
    return translated_key


# Fonction appelée lorsqu'une touche est pressée
def on_press(key):
    try:
        # Récupérer la dernière séquence de frappe
        current_sequence = recordings[-1] if recordings and recordings[-1].get("type") == "key_press" else None

        if current_sequence and current_sequence["value"] == keyboard.Key.backspace:
            # Supprimer la séquence précédente si c'était une suppression
            recordings.pop()

        if key == keyboard.Key.esc:
            stop_recording()

        # Ajouter chaque caractère de la frappe à la liste
        for char in key.char:
            if char.isdigit():
                recordings.append({"type": "key_write", "value": char})  # Utiliser "key_write" pour les chiffres
                print(f"Key write: {char}")
            else:
                key_value = translate_azerty_to_qwerty(char) if azertyMode else char
                recordings.append({"type": "key_press", "value": key_value})
                print(f"Key press: {char}")

        

    except AttributeError:
        # Ajouter l'enregistrement du nom de la touche à la liste
        recordings.append({"type": "key_press", "value": str(key)})
        print(f"Key press: {key}")

# Fonction appelée lorsqu'une touche est relâchée
def on_release(key):
    if str(key).lower() == 'key.shift':
        key_states["shift"] = False
        recordings.append({"type": "key_release", "value": "shift"})  # Enregistrement de "release" pour Shift
        print(f"Key release: Key.shift")

# Fonction appelée lorsqu'un clic de souris est effectué
def on_click(x, y, button, pressed):
    if pressed:
        # Ajouter l'enregistrement du clic à la liste seulement si le bouton est pressé
        action = "Mouse click (pressed)"
        recordings.append({"type": "mouse_click", "position": (x, y), "button": button, "action": action})
        print(f"{action} at ({x}, {y}) with {button}")


def write_to_file():
    # Chemin absolu vers le fichier recordings.json
    file_path = '/Users/remi/Documents/auto-clickboard/recordings/recordings.json'

    # Vérifier si le fichier existe
    if os.path.exists(file_path):
        os.remove(file_path)

    # Convertir les objets Button en chaînes de texte
    for record in recordings:
        if 'button' in record:
            record['button'] = record['button'].name

    # Écrire les enregistrements dans le fichier JSON
    with open(file_path, 'w') as file:
        json.dump(recordings, file, default=str)  # Utiliser default=str pour gérer les types non sérialisables

    # Afficher un message de débogage
    print(f"Enregistrements écrits dans {file_path}")

def on_scroll(x, y, dx, dy):
    print(f'Scrolled at ({x}, {y}) with delta ({dx}, {dy})')
    # Ajouter l'enregistrement du défilement à la liste
    action = {"type": "scroll", "position": (x, y), "delta": (dx, dy)}
    recordings.append(action)


def stop_recording():
    global recording_stopped
    recording_stopped = True

def start_record():
    global is_recording
    is_recording = True
    # Ajoutez le code pour démarrer l'enregistrement ici
    return 'Record started'



# Configurer les écouteurs pour la souris et le clavier
mouse_listener = mouse.Listener(on_click=on_click, on_scroll=on_scroll)
keyboard_listener = keyboard.Listener(on_press=on_press, on_release=on_release)


# Démarrer les écouteurs dans des threads séparés
mouse_listener.start()
keyboard_listener.start()

print("Début de l'enregistrement")

# Attendre X secondes ou jusqu'à ce que la touche Échap soit pressée
recording_stopped = False
for _ in range(recordingDuration): # Default/Max = 300s
    if recording_stopped:
        break
    time.sleep(1)  # Attendez 1 seconde à chaque itération

# Arrêter les écouteurs 
mouse_listener.stop()
keyboard_listener.stop()

# Chemin absolu vers le fichier recordings.json
file_path = '/Users/remi/Documents/auto-clickboard/recordings/recordings.json'

# Vérifier si le fichier existe
if os.path.exists(file_path):
    os.remove(file_path)

# Créer et écrire dans le fichier
write_to_file()

print("Enregistrement terminé")

