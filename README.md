# AutoClickBoard

AutoClickBoard est un logiciel conçu pour enregistrer des clics de souris et des frappes de clavier afin d'automatiser les tâches répétitives. Avec AutoClickBoard, vous pouvez libérer du temps en automatisant des actions courantes sur votre ordinateur.

## Fonctionnalités

- Enregistrement des clics de souris
- Enregistrement des frappes de clavier
- Personnalisation des délais entre les actions
- Options de personnalisation du curseur
- Gestion des boucles et pauses

## Prérequis

Avant de lancer l'application, assurez-vous que vous avez [Python 3.11](https://www.python.org/downloads/) installé sur votre machine.

## Installation

1. Clonez ce dépôt sur votre machine locale :

    ```bash
    git clone https://github.com/Remi13Git/AutoClickBoard.git
    ```

2. Accédez au répertoire du projet :

    ```bash
    cd AutoClickBoard
    ```

3. (Optionnel) Créez un environnement virtuel et activez-le :

    ```bash
    python -m venv venv
    source venv/bin/activate  # Sur Windows : venv\Scripts\activate
    ```

4. Installez les dépendances nécessaires :

    ```bash
    pip install -r requirements.txt
    ```

## Lancer l'Application

Pour démarrer l'application, utilisez la commande suivante :

```bash
python3.11 server.py
