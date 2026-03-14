import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk
from utils.window_helpers import set_window_icon
from automation.login import Login
from ui.main_window import MainWindow
import threading
import time
import json
import os
import sys

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CREDENTIALS_FILE = os.path.join(BASE_DIR, "credentials.json")

# Configuración de CustomTkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")



def guardar_credenciales(user, password):
    """Guarda las credenciales en un archivo JSON"""
    try:
        with open(CREDENTIALS_FILE, "w", encoding="utf-8") as f:
            json.dump(
                {"user": user, "pass": password},
                f,
                ensure_ascii=False,
                indent=2
            )
    except Exception as e:
        print(f"Error guardando credenciales: {e}")


def cargar_credenciales():
    """Carga las credenciales desde el archivo JSON"""
    if not os.path.exists(CREDENTIALS_FILE):
        return "", ""

    try:
        with open(CREDENTIALS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get("user", ""), data.get("pass", "")
    except Exception as e:
        print(f"Error cargando credenciales: {e}")
        return "", ""



class LoginWindow:
    def __init__(self):
        self.root = ctk.CTk()
         # Establecer ícono
        set_window_icon(self.root)

        
        self.root.title("Selene 2.0 – Inicio de sesión")
        self.root.geometry("450x700")
        self.root.resizable(True, True)

        self._centrar_ventana()
        self.root.mainloop()

    def _centrar_ventana(self):

        """Centra la ventana en la pantalla"""
        self.root.update_idletasks()

        # Obtener dimensiones de la pantalla
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Obtener dimensiones de la ventana
        window_width = self.root.winfo_width()
        window_height = self.root.winfo_height()

        # Calcular posición centrada
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)

        self.root.geometry(f"+{x}+{y}")
        
        # Colores Synthwave
        self.bg_color = "#0a0e27"
        self.primary_color = "#ff006e"  # Rosa neón
        self.secondary_color = "#8338ec"  # Púrpura
        self.accent_color = "#3a86ff"  # Azul eléctrico
        self.neon_pink = "#ff006e"
        self.neon_purple = "#b967ff"
        self.neon_cyan = "#05d9e8"
        
        # Configurar color de fondo
        self.root.configure(fg_color=self.bg_color)

        # Cargar la imagen del logo
        self.logo_image = self._cargar_logo()

        self._crear_widgets()
        self.root.mainloop()
    
    def _cargar_logo(self):
        """Carga y procesa la imagen del logo"""
        try:
            # Ajusta la ruta según donde guardaste tu imagen
            img_path = os.path.join(BASE_DIR, "..", "assets", "wow.png")

            # Cargar y redimensionar
            img = Image.open(img_path)
            img = img.resize((150, 150), Image.Resampling.LANCZOS)

            return ctk.CTkImage(
                light_image=img,
                dark_image=img,
                size=(150, 150)
            )
        except Exception as e:
            print(f"Error cargando logo: {e}")
            return None
    
    def _crear_widgets(self):
        # Frame principal con padding
        main_frame = ctk.CTkFrame(
            self.root,
            fg_color=self.bg_color,
            corner_radius=0
        )
        main_frame.pack(fill="both", expand=True, padx=30, pady=30)
        
        # Logo circular
        if self.logo_image:
            logo_label = ctk.CTkLabel( main_frame,
            image=self.logo_image,text="")
            logo_label.pack(pady=(0, 15))

        # Título debajo del logo
        titulo = ctk.CTkLabel(
        main_frame,
        text="Selene 2.0",
        font=("Orbitron", 36, "bold"),
        text_color=self.neon_pink
        )
        titulo.pack(pady=(0, 10))

        
        # Subtítulo
        subtitulo = ctk.CTkLabel(
            main_frame,
            text="Sistema de Gestión Educativa",
            font=("Rajdhani", 16),
            text_color=self.neon_cyan
        )
        subtitulo.pack(pady=(0, 40))
        
        # Frame para inputs con fondo oscuro
        input_frame = ctk.CTkFrame(
            main_frame,
            fg_color="#1a1d35",
            corner_radius=20,
            border_width=2,
            border_color=self.neon_purple
        )
        input_frame.pack(fill="x", pady=20)
        
        # Label Usuario
        label_usuario = ctk.CTkLabel(
            input_frame,
            text="Usuario CiDi",
            font=("Rajdhani", 18, "bold"),
            text_color=self.neon_cyan
        )
        label_usuario.pack(pady=(25, 5), padx=20, anchor="w")
        
        # Entry Usuario
        self.entry_usuario = ctk.CTkEntry(
            input_frame,
            width=350,
            height=45,
            font=("Rajdhani", 16),
            fg_color="#0d1128",
            text_color="#ffffff",
            border_color=self.neon_purple,
            border_width=2,
            corner_radius=10,
            placeholder_text="Ingresa tu CUIL",
            placeholder_text_color="#666d8f"
        )
        self.entry_usuario.pack(pady=(0, 20), padx=20)
        
        # Label Contraseña
        label_password = ctk.CTkLabel(
            input_frame,
            text="Contraseña CiDi",
            font=("Rajdhani", 18, "bold"),
            text_color=self.neon_cyan
        )
        label_password.pack(pady=(5, 5), padx=20, anchor="w")
        
        # Entry Contraseña
        self.entry_password = ctk.CTkEntry(
            input_frame,
            width=350,
            height=45,
            font=("Rajdhani", 16),
            fg_color="#0d1128",
            text_color="#ffffff",
            border_color=self.neon_purple,
            border_width=2,
            corner_radius=10,
            show="●",
            placeholder_text="Ingresa tu contraseña",
            placeholder_text_color="#666d8f"
        )
        self.entry_password.pack(pady=(0, 25), padx=20)
        
        # Cargar credenciales guardadas
        user, password = cargar_credenciales()
        if user:
            self.entry_usuario.insert(0, user)
        if password:
            self.entry_password.insert(0, password)
        
        # Botón de login con efecto hover
        self.btn_login = ctk.CTkButton(
            main_frame,
            text="INICIAR SESIÓN AUTOMATIZADA",
            font=("Orbitron", 18, "bold"),
            width=350,
            height=55,
            fg_color=self.neon_pink,
            hover_color=self.neon_purple,
            text_color="#ffffff",
            corner_radius=15,
            border_width=2,
            border_color=self.neon_cyan,
            command=self.iniciar_sesion
        )
        self.btn_login.pack(pady=(20, 0))
        
        # Decoración inferior
        footer = ctk.CTkLabel(
            main_frame,
            text="━━━━━━━━━━━━━━━━━━━━",
            font=("Courier", 14),
            text_color=self.neon_purple
        )
        footer.pack(pady=(30, 5))
        
        version = ctk.CTkLabel(
            main_frame,
            text="v2.0 • Synthwave Edition",
            font=("Rajdhani", 12),
            text_color=self.accent_color
        )
        version.pack()

    def iniciar_sesion(self):
        # Deshabilitar botón durante el proceso
        self.btn_login.configure(state="disabled", text="CONECTANDO...")
        
        threading.Thread(
            target=self._login_thread,
            daemon=True
        ).start()

    def _login_thread(self):
        user = self.entry_usuario.get()
        password = self.entry_password.get()

        if not user or not password:
            self.root.after(0, lambda: self.btn_login.configure(
                state="normal", text="INICIAR SESIÓN"
            ))
            messagebox.showerror("Error", "Completar usuario y contraseña")
            return
        
        guardar_credenciales(user, password)
        
        driver = None
        try:
            login = Login()
            driver = login.start_login()

            wait = WebDriverWait(driver, 20)

            # botón ingresar (abre formulario)
            wait.until(
                EC.element_to_be_clickable((
                    By.XPATH,
                    "/html/body/app-root/app-navbar/div/mat-toolbar/div/div[3]/button"
                ))
            ).click()

            # esperar modal
            wait.until(
                EC.presence_of_element_located((By.TAG_NAME, "mat-dialog-container"))
            )

            # usuario
            wait.until(
                EC.presence_of_element_located((By.XPATH, "//*[@id='cuil']"))
            ).send_keys(user)

            # contraseña
            wait.until(
                EC.presence_of_element_located((By.XPATH, "//*[@id='password']"))
            ).send_keys(password)

            # ingresar final - MÚLTIPLES ESTRATEGIAS
            boton_encontrado = False
            estrategias = [
                "//app-login//button[.//span[normalize-space()='INGRESAR']]",
                "//input[@id='password']/following::button[contains(., 'INGRESAR')][1]",
                "/html/body/div/div[2]/div/mat-dialog-container/div/div/app-login/div/div/div[1]/button[1]/span[2]",
                "/html/body/div[2]/div[2]/div/mat-dialog-container/div/div/app-login/div/div/app-login/div/div/div[1]/button[1]"
            ]

            for xpath in estrategias:
                try:
                    wait.until(EC.element_to_be_clickable((By.XPATH, xpath))).click()
                    boton_encontrado = True
                    print(f"✅ Botón INGRESAR encontrado con: {xpath}")
                    break
                except:
                    continue
                
            if not boton_encontrado:
                raise Exception("No se pudo hacer click en el botón INGRESAR final")

            time.sleep(5)
            
            try:
                driver.current_url
                self.root.after(0, lambda: messagebox.showinfo(
                    "Éxito", "Sesión iniciada correctamente"
                ))
            except:
                raise WebDriverException("El navegador se cerró inesperadamente")

        except TimeoutException as e:
            self.root.after(0, lambda: self.btn_login.configure(
                state="normal", text="INICIAR SESIÓN"
            ))
            messagebox.showerror(
                "Error de tiempo",
                "Tiempo de espera agotado durante el login.\nEl navegador permanecerá abierto."
            )
            return

        except WebDriverException as e:
            self.root.after(0, lambda: self.btn_login.configure(
                state="normal", text="INICIAR SESIÓN"
            ))
            messagebox.showerror(
                "Error del navegador",
                f"Error en la conexión con el navegador.\n{str(e)}"
            )
            return

        except Exception as e:
            self.root.after(0, lambda: self.btn_login.configure(
                state="normal", text="INICIAR SESIÓN"
            ))
            messagebox.showerror(
                "Error",
                f"No se pudo iniciar sesión en CiDi.\n{str(e)}"
            )
            return

        self.root.after(0, lambda: self._abrir_main_window(driver))

    def _abrir_main_window(self, driver):
        """Abre MainWindow y cierra LoginWindow en el hilo principal"""
        self.root.quit()      # ← CAMBIA destroy() por quit()
        self.root.destroy()   # ← Ahora sí destruye

        main_win = MainWindow(driver)
        main_win.root.mainloop()