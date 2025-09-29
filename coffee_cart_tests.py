import os
import time
import tkinter as tk
from tkinter import simpledialog
from tkinter import messagebox
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# ==== CONFIGURACIÓN SELENIUM ====
URL = "https://coffee-cart.app/"
driver = webdriver.Chrome()
wait = WebDriverWait(driver, 5)


# ==== FUNCIONES AUXILIARES ====
def crear_carpeta(caso):
    ruta = os.path.join("capturas", f"caso_{caso}")
    os.makedirs(ruta, exist_ok=True)
    return ruta

def capturar(driver, carpeta, paso):
    archivo = os.path.join(carpeta, f"paso_{paso}.png")
    driver.save_screenshot(archivo)
    print(f"[✔] Captura guardada: {archivo}")

# ==== PRUEBAS ====
def prueba_1(carpeta):
    """Agregar item al carrito usando data-cy con confirmación"""
    driver.get(URL)
    capturar(driver, carpeta, "1_inicio")

    # Click en el Espresso
    cafe = driver.find_element(By.CSS_SELECTOR, "[data-cy='Espresso']")
    cafe.click()
    capturar(driver, carpeta, "2_click_espresso")
 # Seleccionar el elemento "Total"
    total = driver.find_element(By.CLASS_NAME, "pay")

    # Hover con ActionChains
    actions = ActionChains(driver)
    actions.move_to_element(total).perform()

    capturar(driver, carpeta, "3_hover_total")
   # Hacer click en "View Cart"
    cart_link = driver.find_element(By.CSS_SELECTOR, "a[href='/cart']")
    cart_link.click()
    capturar(driver, carpeta, "4_view_cart")
def prueba_2(carpeta):
    """Agregar item al carrito usando data-cy con confirmación""" 
    driver.get(URL)
    capturar(driver, carpeta, "1_inicio")
    # Click en el Espresso
    cafe = driver.find_element(By.CSS_SELECTOR, "[data-cy='Espresso']")
    cafe.click()
    cafe.click()
    cafe.click()
    capturar(driver, carpeta, "2_click_espresso")
    root = tk.Tk()
    root.withdraw()
    respuesta = messagebox.askyesno("Confirmación", "¿Quieres hacer click en 'Yes, of course!'?")
    root.destroy()

    if respuesta:
        try:
            yes_btn = wait.until(
                EC.element_to_be_clickable((By.CLASS_NAME, "yes"))
            )
            yes_btn.click()
            capturar(driver, carpeta, "3_yes_click")
            print("[✔] Se hizo click en 'Yes, of course!'")
        except Exception as e:
            print(f"[ERROR] No encontré el botón Yes: {e}")
    else:
        print("[ℹ] El usuario eligió no hacer click en 'Yes, of course!'")
 # Seleccionar el elemento "Total"
    total = driver.find_element(By.CLASS_NAME, "pay")

    # Hover con ActionChains
    actions = ActionChains(driver)
    actions.move_to_element(total).perform()

    capturar(driver, carpeta, "3_hover_total")
   # Hacer click en "View Cart"
    cart_link = driver.find_element(By.CSS_SELECTOR, "a[href='/cart']")
    cart_link.click()
    capturar(driver, carpeta, "4_view_cart")
def prueba_3(carpeta):
    driver.get(URL)
    capturar(driver, carpeta, "1_inicio")

    # Localizar el Espresso
    cafe = driver.find_element(By.CSS_SELECTOR, "[data-cy='Espresso']")

    # Click derecho con ActionChains
    actions = ActionChains(driver)
    actions.context_click(cafe).perform()
    capturar(driver, carpeta, "2_click_derecho")

    # ==== Tkinter con botones Sí / No ====
    root = tk.Tk()
    root.withdraw()  # Oculta la ventana principal
    respuesta = messagebox.askyesno("Confirmación", "¿Quieres agregar Espresso al carrito?")
    root.destroy()

    # ==== Según la opción seleccionada en Tkinter ====
    if respuesta:  # True si eligió Sí
        driver.find_element(By.XPATH, "//button[text()='Yes']").click()
        capturar(driver, carpeta, "3_yes")
    else:
        driver.find_element(By.XPATH, "//button[text()='No']").click()
        capturar(driver, carpeta, "3_no")

    # Hover en total
    total = driver.find_element(By.CLASS_NAME, "pay")
    actions.move_to_element(total).perform()
    capturar(driver, carpeta, "4_hover_total")

    # Click en "View Cart"
    cart_link = driver.find_element(By.CSS_SELECTOR, "a[href='/cart']")
    cart_link.click()
    capturar(driver, carpeta, "5_view_cart") 
def prueba_4(carpeta):
    """Agregar item al carrito usando data-cy con confirmación"""
    driver.get(URL)
    capturar(driver, carpeta, "1_inicio")

    # Click en el Espresso
    cafe = driver.find_element(By.CSS_SELECTOR, "[data-cy='Espresso']")
    cafe.click()
    capturar(driver, carpeta, "2_click_espresso")
 # Seleccionar el elemento "Total"
    total = driver.find_element(By.CLASS_NAME, "pay")

    # Hover con ActionChains
    actions = ActionChains(driver)
    actions.move_to_element(total).perform()

    capturar(driver, carpeta, "3_hover_total")
   # Hacer click en "View Cart"
    cart_link = driver.find_element(By.CSS_SELECTOR, "a[href='/cart']")
    cart_link.click()
    capturar(driver, carpeta, "4_view_cart")
    #hacer click en +
    #hacer click en -
# ==== MAPA DE PRUEBAS ====
PRUEBAS = {
    1: prueba_1, 2: prueba_2, 3: prueba_3, 4: prueba_4
}

# ==== TKINTER ====
root = tk.Tk(); root.withdraw()
caso = simpledialog.askinteger("Caso de prueba", "Ingrese el número de caso (1-4):")

if caso in PRUEBAS:
    carpeta = crear_carpeta(caso)
    PRUEBAS[caso](carpeta)
    print(f"[✔] Caso {caso} ejecutado con capturas en {carpeta}")
else:
    print("❌ Número de caso inválido.")

driver.quit()
