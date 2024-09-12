import pyautogui
import time
import json
import os
import random
from pynput import keyboard

def load_parameters():
    try:
        # Charger les paramètres à partir du fichier de configuration JSON
        with open('config.json', 'r') as file:
            params = json.load(file)
            
    except FileNotFoundError:
        # Créer un fichier avec les valeurs par défaut si le fichier n'existe pas
        params = {
            'delayStart': 0,
            'pauseClicks': 0.1,
            'pauseKeyPress': 0.1,
            'pauseLoops': 0,
            'numberLoops': 5,
            'showCursor': True,
            'cursorSpeed': 1.5,
            'cursorStyle': pyautogui.easeOutQuad,
            'cursorRandomize': False,
            'reverseScroll': 1
        }
        with open('config.json', 'w') as file:
            json.dump(params, file)
    return params

def start_loop():
    global is_rotating
    is_rotating = True
    # Ajoutez le code pour démarrer la boucle ici
    return 'Loop started'

def main():
    # Charger les paramètres
    params = load_parameters()

    # Utiliser les paramètres
    delayStart = params.get('delayStart', 0)
    pauseClicks = params.get('pauseClicks', 0.1)
    pauseKeyPress = params.get('pauseKeyPress', 0.1)
    pauseLoops = params.get('pauseLoops', 0)
    numberLoops = params.get('numberLoops', 5)
    showCursor = params.get('showCursor', True)
    cursorSpeed = params.get('cursorSpeed', 1.5)
    cursorStyle = params.get('cursorStyle', pyautogui.easeOutQuad)
    cursorRandomize = params.get('cursorRandomize', False)
    reverseScroll = params.get('reverseScroll', 1)


    # Retourner les paramètres
    return delayStart, pauseClicks, pauseKeyPress, pauseLoops, numberLoops, showCursor, cursorSpeed, cursorStyle, cursorRandomize, reverseScroll


# Définir une variable pour indiquer si la touche "Echap" a été pressée
esc_pressed = False

# Fonction callback pour gérer la pression de la touche "Echap"
def on_key_press(key):
    global esc_pressed
    if key == keyboard.Key.esc:
        esc_pressed = True

# Installer le gestionnaire d'événements pour la touche "Echap"
listener = keyboard.Listener(on_press=on_key_press)
listener.start()



# Chemin absolu vers le fichier recordings.json
file_path = '/Users/remi/Documents/auto-clickboard/recordings/recordings.json'

def read_recordings(file_path):
    # Lire les enregistrements depuis le fichier JSON
    with open(file_path, 'r') as file:
        return json.load(file)
    
def simulate_key_press(key):
    pyautogui.press(key)
    

def convert_recordings_to_actions(recordings, showCursor):
    actions = []
    for record in recordings:
        if record["type"] == "mouse_click":
            # Convertir l'enregistrement de clic de souris en action
            position = tuple(record["position"])
            if showCursor:
                actions.append(("moveTo", position))
            actions.append(("click", position))
        elif record["type"] == "key_press":
            # Convertir l'enregistrement de pression de touche en action
            if record["value"] == "Key.shift":
                actions.append(("keyDown", record["value"]))
            else:
                actions.append(("write", record["value"]))
        elif record["type"] == "key_release":
            # Convertir l'enregistrement de relâchement de touche en action
            actions.append(("keyUp", record["value"]))
        elif record["type"] == "scroll":
            # Ajouter l'enregistrement de défilement en tant qu'action
            actions.append(("scroll", record["delta"][1]))
        elif record["type"] == "key_write":
            # Ajouter l'enregistrement de défilement en tant qu'action
            actions.append(("write", record["value"]))
    return actions


if __name__ == '__main__':
    # Appeler main() pour obtenir les valeurs des paramètres
    delayStart, pauseClicks, pauseKeyPress, pauseLoops, numberLoops, showCursor, cursorSpeed, cursorStyle, cursorRandomize, reverseScroll = main()


# Vérifier si le fichier existe
if os.path.exists(file_path):
    # Lire les enregistrements depuis le fichier
    recordings = read_recordings(file_path)

    # Convertir les enregistrements en actions
    actions = convert_recordings_to_actions(recordings, showCursor)


    # Nombre de répétitions
    nombre_repetitions = numberLoops

    # Attendre quelques secondes avant de commencer
    time.sleep(delayStart)

# Boucle pour reproduire les actions avec délais
for _ in range(nombre_repetitions):
    for action in actions:
        # Vérifier si la touche "Echap" a été pressée
        if esc_pressed:
            print("Boucle interrompue par l'utilisateur.")
            listener.stop()  # Arrêter le gestionnaire d'événements
            exit()  # Terminer le script complètement

        if isinstance(action, tuple):
            # Action de souris ou de clavier
            action_type, param = action
            if action_type == "click":
                x, y = param
                if showCursor:
                    if cursorRandomize:
                        # Ajouter une valeur aléatoire à partir de la position d'origine
                        x += random.randint(-5, 5)
                        y += random.randint(-5, 5)

                    # Définir la fonction associée à cursorStyle
                    cursor_style_function = getattr(pyautogui, cursorStyle, None)
                    if cursor_style_function:
                        pyautogui.moveTo(x, y, cursorSpeed, cursor_style_function)
                    else:
                        print(f"La fonction {cursorStyle} n'est pas prise en charge par PyAutoGUI.")
                        # Vous pouvez ajouter une gestion d'erreur ou utiliser une fonction par défaut ici
                pyautogui.click(x, y, interval=pauseClicks)
            elif action_type == "scroll":
                pyautogui.scroll(action[1] * reverseScroll)
            elif action_type == "write":
                pyautogui.keyDown('shift')
                pyautogui.write(action, interval=pauseKeyPress)
                pyautogui.keyUp('shift')

    # Délai entre chaque répétition
    time.sleep(pauseLoops)

    print("Boucle terminée")
else:
    print(f"Fin du script.")

