import os
import sys
import tkinter as tk




def resource_path(relative_path):
    """Obtiene la ruta absoluta del recurso"""
    try:
        base_dir = sys._MEIPASS  # type: ignore[attr-defined]
    except AttributeError:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    full_path = os.path.join(base_dir, relative_path)
    
    if not os.path.exists(full_path):
        print(f"⚠️ Advertencia: No se encontró el recurso en {full_path}")
    
    return full_path

def set_window_icon(window, icon_name="wow.ico"):
    """
    Establece el ícono de una ventana de forma robusta
    
    Args:
        window: Instancia de CTk o Tk
        icon_name: Nombre del archivo de ícono en la carpeta assets
    """
    icon_path = resource_path(os.path.join("assets", icon_name))
    
    # Intentar múltiples métodos
    try:
        window.iconbitmap(icon_path)
    except Exception as e:
        print(f"iconbitmap falló: {e}")
        try:
            window.wm_iconbitmap(icon_path)
        except Exception as e2:
            print(f"wm_iconbitmap falló: {e2}")
    
    # Método adicional con PNG (más compatible)
    try:
        png_path = resource_path(os.path.join("assets", icon_name.replace(".ico", ".png")))
        if os.path.exists(png_path):
            icon_image = tk.PhotoImage(file=png_path)
            window.iconphoto(True, icon_image)
            # Guardar referencia para evitar garbage collection
            window._icon_ref = icon_image
    except Exception as e:
        print(f"iconphoto falló: {e}")