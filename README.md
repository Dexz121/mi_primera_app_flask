Mi primera app Flask (WSL)

Proyecto base en Flask ejecutándose en WSL (Ubuntu) con entorno virtual y Git/GitHub.

Requisitos:

WSL2 con Ubuntu

Python 3.10+ y pip

Git

(Opcional) VS Code con “Remote - WSL”

Instalación y preparación:

# Clonar o entrar al proyecto
git clone https://github.com/<TU-USUARIO>/<TU-REPO>.git
cd <TU-REPO>  # o cd ~/mi_primera_app_flask

# Crear y activar entorno virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias (si no hay requirements.txt instalar Flask)
[ -f requirements.txt ] && pip install -r requirements.txt || pip install flask


Ejecución:

# Con Flask CLI
flask --app app run --debug
# o con Python directo
python3 app.py


Abre en el navegador: http://127.0.0.1:5000

Archivo mínimo app.py:

from flask import Flask, jsonify

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False  # evita el escape de emojis en JSON

@app.get("/")
def home():
    return jsonify(ok=True, message="Hola Flask en WSL 🚀")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)


Generar requirements.txt (elige una opción):

# A) Congelar entorno actual
pip freeze > requirements.txt

# B) Solo lo importado en tu código
pip install pipreqs
pipreqs . --encoding=utf-8 --force


Configurar Git y primer push:

git init
git add .
git commit -m "feat: primera versión Flask"
git branch -M main
git remote add origin https://github.com/<TU-USUARIO>/<TU-REPO>.git
git push -u origin main


.gitignore recomendado (créalo en la raíz):

venv/
__pycache__/
*.pyc
*.pyo
*.pyd
.env
.env.*
.vscode/
.idea/
.DS_Store


Solución de problemas habituales:

# Locks/permisos Git
rm -f .git/index.lock
sudo chown -R "$(whoami)":"$(whoami)" .git
chmod -R u+rwX .git
git config --global --add safe.directory "$(pwd)"

# Saltos de línea en WSL
git config --global core.autocrlf input
git config --global core.eol lf

# Puerto 5000 ocupado
lsof -i :5000
kill -9 <PID>