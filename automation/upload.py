import re
import pandas as pd
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    UnexpectedAlertPresentException,
    NoAlertPresentException)
class Upload:

    def __init__(self, driver, df):
        self.driver = driver
        self.df = df
        


    

    def subir_notas(self, col_inicio, col_fin):
        # Cambiar a la pestaña del formulario
        ventanas = self.driver.window_handles
        self.driver.switch_to.window(ventanas[-1])  # Cambia a la última pestaña abierta

        columnas = list(self.df.columns)

        try:
            idx_inicio = columnas.index(col_inicio)
            idx_fin = columnas.index(col_fin)
        except ValueError:
            print("Columnas seleccionadas no existen en el CSV.")
            return

        if idx_inicio > idx_fin:
            print("El rango de columnas es inválido.")
            return

        columnas_a_procesar = columnas[idx_inicio:idx_fin + 1]

        

        match = re.search(r"\d+", col_inicio)
        if not match:
            print("No se pudo determinar el número de evaluación.")
            return

        eval_num = match.group()   # "8"

        def columna_valida(col, eval_num):
            col = col.strip()

            # excluir EVAL i (con o sin espacio)
            if col == f"EVAL{eval_num}" or col == f"EVAL {eval_num}":
                return False

            # aceptar SOLO estas
            if col == f"NE{eval_num}":
                return True

            if col == f"E{eval_num}R1":
                return True

            if col == f"E{eval_num}R2":
                return True

            # todo lo demás se descarta
            return False

        
        columnas_a_procesar = [
        col for col in columnas_a_procesar
        if columna_valida(col, eval_num)
        ]

        for col in columnas_a_procesar:

            if col == "Estudiante":
                continue

            print(f"Procesando columna: {col}")

            for i in range(len(self.df)):

                calif = self.df.at[i, col]

                if pd.isna(calif):
                    continue

                calif = str(calif).strip()

                if not calif or '@value="0"' in calif:
                    continue

                try:
                    print(f"  → fila {i}, columna {col}")

                    nota_option = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, calif))
                    )
                    nota_option.click()
                    time.sleep(0.5)
                    

                except UnexpectedAlertPresentException:
                    try:
                        alert = self.driver.switch_to.alert
                        alert.accept()
                    except NoAlertPresentException:
                        pass
                    continue

                except TimeoutException:
                    print(f"  ✗ timeout en fila {i}, columna {col}")
                    continue

                except Exception as e:
                    print(f"Error en fila {i}, columna {col}: {e}")
                    continue


class UploadIEFs:
    

    

    def __init__(self, driver, df):
        self.driver = driver
        self.df = df

    def subir_iefs(self, col_inicio, col_fin):

        # Cambiar a la pestaña del formulario
        ventanas = self.driver.window_handles
        self.driver.switch_to.window(ventanas[-1])  # Cambia a la última pestaña abierta

        columnas = list(self.df.columns)

        try:
            idx_inicio = columnas.index(col_inicio)
            idx_fin = columnas.index(col_fin)
        except ValueError:
            print("Columnas seleccionadas no existen en el CSV.")
            return

        if idx_inicio > idx_fin:
            print("El rango de columnas es inválido.")
            return
        def filtrar_columnas_aprendizaje(columnas):
            """
            Devuelve solo las columnas 'Aprendizaje X'.
            Excluye cualquier columna que empiece con 'Condición'.
            """
            columnas_filtradas = []

            for col in columnas:
                if col.startswith("Aprendizaje ") and not col.startswith("Condición"):
                    columnas_filtradas.append(col)

            return columnas_filtradas



        columnas_filtradas = filtrar_columnas_aprendizaje(columnas[idx_inicio:idx_fin + 1])
        self.df=self.df.dropna(how="all").reset_index(drop=True)
        for i in range(len(self.df)):

            xpath_estudiante = self.df.at[i, "Xpath_estudiantes_Gestion_aprendizajes"]

            if pd.isna(xpath_estudiante):
                continue
            
            xpath_estudiante = str(xpath_estudiante).strip()
            if not xpath_estudiante:
                continue
            
            try:
                print(f"→ Seleccionando estudiante fila {i}")

                estudiante_element = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, xpath_estudiante))
                )
                estudiante_element.click()
                time.sleep(0.5)

            except TimeoutException:
                print(f"✗ timeout al seleccionar estudiante fila {i}")
                continue
            
            # 🔁 ahora cargás TODOS los aprendizajes de ESE estudiante
            for col in columnas_filtradas:
            
                if col == "Estudiante":
                    continue
                
                ief_value = self.df.at[i, col]

                if pd.isna(ief_value):
                    continue
                
                ief_value = str(ief_value).strip()
                if not ief_value:
                    continue
                
                try:
                    print(f"   → {col}")

                    ief_option = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, ief_value))
                    )
                    ief_option.click()
                    time.sleep(0.5)

                except TimeoutException:
                    print(f"   ✗ timeout en {col}, fila {i}")
                    continue
                
                except Exception as e:
                    print(f"Error en fila {i}, columna {col}: {e}")
                    continue

    def finalizar_etapas(self, n):
        """
        Finaliza las etapas de los primeros n estudiantes.

        Args:
            n: Número máximo de filas a procesar
        """
        # 🔥- Cambiar a la ventana correcta
        ventanas = self.driver.window_handles
        self.driver.switch_to.window(ventanas[-1])

        XPATH_CERRAR_VENTANA = "/html/body/form/div[3]/div[3]/div[1]/div[1]/div[3]/div/div[3]/a"

        self.df = self.df.dropna(how="all").reset_index(drop=True)
        filas = min(n, len(self.df))

        print(f"Procesando {filas} estudiantes...")

        for i in range(filas):
            xpath_estudiante = self.df.at[i, "Xpath_estudiantes_Gestion_aprendizajes"]
            xpath_finalizar = self.df.at[i, "Xpath_finalizar_etapa"]

            if pd.isna(xpath_estudiante) or pd.isna(xpath_finalizar):
                print(f"⊘ Fila {i}: XPaths faltantes, saltando...")
                continue

            xpath_estudiante = str(xpath_estudiante).strip()
            xpath_finalizar = str(xpath_finalizar).strip()

            if not xpath_estudiante or not xpath_finalizar:
                print(f"⊘ Fila {i}: XPaths vacíos, saltando...")
                continue

            try:
                print(f"→ Finalizando etapa del estudiante (fila {i})...", end=" ")

                # 1. Click en estudiante (igual que en subir_iefs)
                estudiante_element = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, xpath_estudiante))
                )
                estudiante_element.click()
                time.sleep(0.5)

                # 2. Buscar el botón finalizar (sin scroll primero, como subir_iefs)
                finalizar_btn = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, xpath_finalizar))
                )
                # 3. AHORA SÍ hacer scroll hacia el botón
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", finalizar_btn)
                time.sleep(0.5)

                # 4. Click en el botón
                finalizar_btn.click()
                time.sleep(2)

                # 5. Cerrar popup
                cerrar_popup = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, XPATH_CERRAR_VENTANA))
                )
                cerrar_popup.click()
                time.sleep(2)

                print("✓")

            except TimeoutException:
                print(f"✗ Timeout")
                print(f"   XPath estudiante: {xpath_estudiante}")
                print(f"   XPath finalizar: {xpath_finalizar}")

            except Exception as e:
                print(f"✗ Error: {type(e).__name__} - {str(e)}")

        print(f"\n✓ Proceso completado. Se procesaron {filas} filas.")


    def cerrar_iefs(self):

        # Cambiar a la pestaña del formulario
        ventanas = self.driver.window_handles
        self.driver.switch_to.window(ventanas[-1])  # Cambia a la última pestaña abierta
        XPATH_CERRAR_VENTANA = "/html/body/form/div[3]/div[3]/div[1]/div[1]/div[3]/div/div[3]/a"

        self.df = self.df.dropna(how="all").reset_index(drop=True)

        for i in range(len(self.df)):

            xpath_estudiante = self.df.at[i, "Xpath_estudiantes_Gestion_aprendizajes"]
            xpath_texto = self.df.at[i, "Xpath_text"]
            texto_ief = self.df.at[i, "Síntesis final IEF"]
            xpath_cerrar = self.df.at[i, "Xpath_cerrar_IEF"]

            if pd.isna(xpath_estudiante) or pd.isna(xpath_cerrar) or pd.isna(texto_ief):
                continue

            xpath_estudiante = str(xpath_estudiante).strip()
            xpath_cerrar = str(xpath_cerrar).strip()
            texto_ief = str(texto_ief).strip()

            if not xpath_estudiante or not xpath_cerrar or not texto_ief:
                continue

            try:
                print(f"→ Cerrando IEF (fila {i})")

                # Click en estudiante
                estudiante_element = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, xpath_estudiante))
                )
                estudiante_element.click()
                time.sleep(2)

                # Buscar input de texto
                input_texto = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, xpath_texto))
                )
                input_texto.click()
                # Scroll hacia el input
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", input_texto)
                time.sleep(0.3)
                # Limpiar en caso de texto previo
                # ✅ TAMBIÉN CORRECTO
                valor_actual = input_texto.get_attribute("value")
                if valor_actual:  # Si tiene contenido
                    input_texto.clear()
                input_texto.send_keys(texto_ief)
                time.sleep(2)

                # Buscar botón cerrar (debería ser diferente xpath que input_texto)
                # NOTA: Aquí usas el mismo xpath para input y botón, verifica esto
                cerrar_btn = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, xpath_cerrar))
                )
                cerrar_btn.click()
                time.sleep(2)

                # Cerrar popup
                cerrar_popup = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, XPATH_CERRAR_VENTANA))
                )
                cerrar_popup.click()
                time.sleep(2)

            except TimeoutException:
                print(f"✗ No se pudo cerrar IEF (fila {i})")
                continue

            except Exception as e:
                print(f"Error en fila {i}: {e}")
                continue