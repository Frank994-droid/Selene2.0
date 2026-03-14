# Selene 2.0 🤖

> **[English](#english) | [Español](#español)**

---

<a name="english"></a>
## 🇬🇧 English

### About the Project

**Selene 2.0** is a desktop automation app built for Argentine high school teachers. It automates the manual and repetitive process of uploading student grades and IEFs (Formative Evaluation Reports) to **CiDi** — the official educational platform of the Province of Córdoba, Argentina.

Instead of entering data one by one through the web interface, teachers simply export their spreadsheets from Google Sheets as `.csv` files, and Selene handles the rest: it reads the data with **pandas** and uses **Selenium WebDriver** to automatically navigate and fill in the platform.

![Demo](assets/Selene2.0Lanzamiento.gif)
---

### ✨ Features

- 📂 Reads student data from `.csv` files exported from Google Sheets
- 🌐 Automates browser interaction with CiDi using Selenium
- 🖥️ Desktop GUI built with Python (Tkinter / PyQt)
- ⚡ Uploads grades and IEFs without manual input
- 🔐 Secure login handling via local credentials file

---

### 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core language |
| Selenium WebDriver | Browser automation |
| pandas | CSV parsing and data handling |
| Tkinter / PyQt | Desktop GUI |
| GeckoDriver | Firefox WebDriver |

---

### 🚀 Getting Started

#### Prerequisites

- Python 3.8+
- Firefox browser installed
- GeckoDriver (included in `/drivers`)

#### Installation

```bash
# Clone the repository
git clone https://github.com/Frank994-droid/Selene2.0.git
cd Selene2.0

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

#### Configuration

Create a `credentials.json` file in the root directory with your CiDi login:

```json
{
  "username": "your_username",
  "password": "your_password"
}
```

> ⚠️ Never share or upload this file. It is already listed in `.gitignore`.

#### Run the app

```bash
python main.py
```

---

### 📁 Project Structure

```
Selene2.0/
├── assets/         # Images and icons
├── automation/     # Selenium automation logic
├── config/         # App configuration
├── data/           # CSV input files
├── drivers/        # GeckoDriver executable
├── reports/        # Upload result reports
├── ui/             # GUI windows and components
├── utils/          # Helper functions
└── main.py         # App entry point
```

---

### 📌 Status

🚧 **Beta** — Core features are functional. Currently being tested with real users.

---

### 🗺️ Roadmap

The following features are planned for future versions, depending on adoption and user growth:

- [ ] **Google Sheets API integration** — Connect directly to cloud spreadsheets, eliminating the need to manually export and attach CSV files
- [ ] **Support for other educational platforms** — Expand beyond CiDi (Córdoba) to cover similar platforms used in other Argentine provinces
- [ ] Multi-school / multi-user support
- [ ] Upload progress dashboard and detailed error reporting

---

### 📬 Contact

Franco Brondo — francobrondo@gmail.com

---

---

<a name="español"></a>
## 🇦🇷 Español

### Sobre el Proyecto

**Selene 2.0** es una aplicación de escritorio pensada para docentes de secundaria de Argentina. Automatiza el proceso manual y repetitivo de cargar notas e IEFs (Informes de Evaluación Formativa) en **CiDi** — la plataforma educativa oficial de la Provincia de Córdoba.

En lugar de cargar los datos uno por uno desde el navegador, el docente simplemente exporta su planilla desde Google Sheets en formato `.csv`, y Selene hace el resto: lee los datos con **pandas** y usa **Selenium WebDriver** para navegar y completar la plataforma de forma automática.

![Demo](assets/Selene2.0Lanzamiento.gif)
---

### ✨ Funcionalidades

- 📂 Lee datos de alumnos desde archivos `.csv` exportados de Google Sheets
- 🌐 Automatiza la interacción con CiDi mediante Selenium
- 🖥️ Interfaz gráfica de escritorio construida en Python
- ⚡ Carga notas e IEFs sin intervención manual
- 🔐 Manejo seguro del login mediante archivo de credenciales local

---

### 🛠️ Tecnologías utilizadas

| Tecnología | Uso |
|---|---|
| Python | Lenguaje principal |
| Selenium WebDriver | Automatización del navegador |
| pandas | Lectura y procesamiento de CSV |
| Tkinter / PyQt | Interfaz gráfica de escritorio |
| GeckoDriver | WebDriver para Firefox |

---

### 🚀 Instalación

#### Requisitos previos

- Python 3.8+
- Firefox instalado
- GeckoDriver (incluido en `/drivers`)

#### Pasos

```bash
# Clonar el repositorio
git clone https://github.com/Frank994-droid/Selene2.0.git
cd Selene2.0

# Crear y activar entorno virtual
python -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

#### Configuración

Crear un archivo `credentials.json` en la raíz del proyecto con las credenciales de CiDi:

```json
{
  "username": "tu_usuario",
  "password": "tu_contraseña"
}
```

> ⚠️ Nunca compartas ni subas este archivo. Ya está incluido en `.gitignore`.

#### Ejecutar la app

```bash
python main.py
```

---

### 📁 Estructura del proyecto

```
Selene2.0/
├── assets/         # Imágenes e íconos
├── automation/     # Lógica de automatización con Selenium
├── config/         # Configuración de la app
├── data/           # Archivos CSV de entrada
├── drivers/        # Ejecutable de GeckoDriver
├── reports/        # Reportes de carga
├── ui/             # Ventanas y componentes de la GUI
├── utils/          # Funciones auxiliares
└── main.py         # Punto de entrada de la app
```

---

### 📌 Estado del proyecto

🚧 **Beta** — Las funcionalidades principales están operativas. Actualmente en pruebas con usuarios reales.

---

### 🗺️ Roadmap

Las siguientes funcionalidades están previstas para versiones futuras, según la adopción y crecimiento de usuarios:

- [ ] **Integración con la API de Google Sheets** — Conectar la app directamente con las planillas en la nube, eliminando la necesidad de exportar y adjuntar archivos CSV manualmente
- [ ] **Soporte para otras plataformas educativas** — Expandir la app más allá del CiDi (Córdoba) para cubrir plataformas similares utilizadas en otras provincias de Argentina
- [ ] Soporte multi-escuela / multi-usuario
- [ ] Panel de progreso de carga y reporte detallado de errores

---

### 📬 Contacto

Franco Brondo — francobrondo@gmail.com



