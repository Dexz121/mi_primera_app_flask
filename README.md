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


Aplicación web mínima en Flask que cumple los checkpoints: landing, login/registro, sesión persistente, página inicial con contenido dinámico y base de datos relacional (SQLite). Incluye control de versiones (Git/GitHub) y carpeta Entregables.

Estructura
.
├─ app.py
├─ models.py
├─ auth.py
├─ main.py
├─ requirements.txt
├─ .gitignore
├─ templates/
│  ├─ base.html
│  ├─ index.html
│  ├─ dashboard.html
│  ├─ login.html
│  └─ register.html
├─ static/
│  └─ styles.css
├─ documentation/
│  └─ db/
│     └─ er.md
└─ Entregables/

Requisitos

Python 3.10+ (en WSL2/Ubuntu o Linux)

pip y venv

Git

Instalación
# 1) Clonar y entrar
git clone https://github.com/<TU-USUARIO>/<TU-REPO>.git
cd <TU-REPO>

# 2) Entorno virtual
python3 -m venv venv
source venv/bin/activate

# 3) Dependencias
pip install -r requirements.txt

Variables de entorno (opcional)

Crea un archivo .env en la raíz si deseas personalizar claves/DB:

SECRET_KEY=dev-secret
DATABASE_URL=sqlite:///app.db

Migraciones y base de datos
# Indicar el factory de la app a Flask-Migrate
export FLASK_APP=app:create_app

flask db init
flask db migrate -m "initial"
flask db upgrade

(Opcional) Crear un usuario de prueba
python3 - << 'PY'
from app import create_app, db
from models import User
app = create_app()
with app.app_context():
    u = User(name="Demo", email="demo@example.com")
    u.set_password("demo123")
    db.session.add(u); db.session.commit()
    print("Usuario creado:", u.email)
PY

Ejecutar
# Opción recomendada (auto-reload y debugger)
flask --app app:create_app run --debug
# Navegar a: http://127.0.0.1:5000

Paqueterías usadas
Flask
Flask-Login
Flask-SQLAlchemy
Flask-Migrate
python-dotenv


Si necesitas regenerar requirements.txt:

pip freeze > requirements.txt

Checkpoints (cómo se cumplen)

CP1: Repositorio público con README.md, requirements.txt y estructura base (listo).

CP2: Esquema ER en documentation/db/er.md (Mermaid).

CP3: Vistas implementadas y navegables:

Landing (sin sesión): / → templates/index.html

Inicio con sesión: /dashboard → templates/dashboard.html

Login: /auth/login

Registro: /auth/register

CP4: Autenticación y sesión persistente con Flask-Login (flujo registro/login/logout).

CP5: Página inicial dinámica (/dashboard) que muestra preguntas según usuario autenticado.

Entregables

Agrega capturas y videos en la carpeta Entregables/ (no comprimir).

Sube el ER y diagramas a documentation/db/ y a la raíz según pida la plataforma.

Notas

DB por defecto: SQLite (sqlite:///app.db).

Para producción, cambia DATABASE_URL (e.g., Postgres) y configura SECRET_KEY.

No subas venv/, __pycache__/ ni .env (ya cubierto en .gitignore).

# Tkinter To-Do (GUI)

Aplicación de Lista de Tareas con **Tkinter** que demuestra: uso de componentes, layout **grid** responsive, eventos (Enter, Supr, Ctrl+N, doble clic), y buenas prácticas (modelo–vista–controlador). Persistencia en `tasks.json`.

## Requisitos
- Python 3.10+
- Tkinter (Linux/WSL): `sudo apt install -y python3-tk`

## Ejecutar
```bash
python3 tk_todo/tk_todo.py
