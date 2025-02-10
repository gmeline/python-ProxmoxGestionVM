📌 Proxmox Gestion VM

🚀 Description

Ce projet est une application web développée avec Django permettant la gestion des machines virtuelles (VM) sur un serveur Proxmox. L'application propose une interface intuitive pour :

✅ Lister les machines virtuelles présentes sur un serveur Proxmox.

✅ Créer, lire, mettre à jour et supprimer des systèmes d'exploitation (CRUD OS).

✅ Gérer l'authentification des utilisateurs pour sécuriser l'accès.

_____________
🛠️ Technologies utilisées

Python (Django) – Framework backend

Proxmox API – Interaction avec le serveur Proxmox

SQLite / PostgreSQL / MySQL – Base de données (au choix)

HTML, CSS, JavaScript – Interface utilisateur
_____________
📌 Fonctionnalités

🔹 Authentification utilisateur (connexion et gestion des comptes)

🔹 Affichage de la liste des machines virtuelles avec leurs détails

🔹 Gestion des systèmes d'exploitation disponibles (CRUD OS)

🔹 Connexion à un serveur Proxmox via l'API REST pour récupérer les VM
_____________
🚀 Installation et utilisation

1️⃣ Prérequis

Assurez-vous d'avoir :

Python 3.8+ installé

Un serveur Proxmox accessible via l'API

Django et les dépendances du projet

2️⃣ Installation

Clonez le projet :

git clone https://github.com/gmeline/python-ProxmoxGestionVM.git

cd python-ProxmoxGestionVM

Installez les dépendances :

pip install -r requirements.txt

Appliquez les migrations de la base de données :

python manage.py migrate

3️⃣ Configuration

Modifiez les paramètres de connexion à Proxmox dans le fichier settings.py :

PROXMOX_HOST = "IP_DU_SERVEUR"

PROXMOX_USER = "root@pam"

PROXMOX_PASSWORD = "VOTRE_MOT_DE_PASSE"

4️⃣ Lancement du serveur Django

Démarrez l'application avec :

python manage.py runserver

L'application sera accessible à l'adresse http://127.0.0.1:8000/
_____________
🛠️ API Proxmox

Le projet utilise l'API REST de Proxmox pour récupérer et gérer les VM.
_____________
📜 Licence

Ce projet est fait par Godefroy Méline.

