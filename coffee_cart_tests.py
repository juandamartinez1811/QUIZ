import os
import time
import tkinter as tk
from tkinter import simpledialog, messagebox
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    ElementClickInterceptedException,
    WebDriverException,
)

# ==== CONFIGURACIÓN SELENIUM ====
URL = "https://coffee-cart.app/"
driver = webdriver.Chrome()
wait = WebDriverWait(driver, 12)


# ==== FUNCIONES AUXILIARES ====
def crear_carpeta(caso):
    """Crea carpeta relativa capturas/caso_X y la devuelve."""
    ruta = os.path.join("capturas", f"caso_{caso}")
    os.makedirs(ruta, exist_ok=True)
    return ruta

def capturar(driver, carpeta, paso):
    """Guarda screenshot en la carpeta dada con el nombre paso_{paso}.png"""
    try:
        archivo = os.path.join(carpeta, f"paso_{paso}.png")
        driver.save_screenshot(archivo)
        print(f"[✔] Captura guardada: {archivo}")
    except WebDriverException as e:
        print(f"[ERROR] No pude guardar captura {paso}: {e}")

def js_click(el):
    """Forzar click por JS (evita overlays que interceptan clicks)."""
    try:
        driver.execute_script("arguments[0].click();", el)
    except Exception as e:
        raise

def wait_for_success_message(carpeta, timeout=18):
    """
    Intenta localizar el mensaje de éxito tras el pago.
    Si lo encuentra guarda captura y devuelve el elemento; si no, guarda evidencia y devuelve None.
    """
    end = time.time() + timeout
    xpaths = [
        "//*[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'thanks for your purchase')]",
        "//*[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'please check your email')]",
        "//div[contains(@class,'toast') or contains(@class,'notification') or contains(@class,'success') or @role='alert']",
        "//div[contains(.,'Thanks for your purchase. Please check your email for payment.')]",
        "//div[contains(.,'Thanks for your purchase')]",
        "//p[contains(.,'Thanks for your purchase')]",
    ]
    while time.time() < end:
        for xp in xpaths:
            try:
                el = driver.find_element(By.XPATH, xp)
                if el.is_displayed():
                    capturar(driver, carpeta, "mensaje_exito_detectado")
                    return el
            except Exception:
                continue
        time.sleep(0.5)
    # no encontrado
    capturar(driver, carpeta, "mensaje_exito_no_detectado")
    return None


# ==== PRUEBAS ====
def prueba_1(carpeta):
    driver.get(URL)
    capturar(driver, carpeta, "1_inicio")

    cafe = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-cy='Espresso']")))
    cafe.click()
    capturar(driver, carpeta, "2_click_espresso")

    # hover sobre total (si existe) y captura
    try:
        total = driver.find_element(By.CLASS_NAME, "pay")
        ActionChains(driver).move_to_element(total).perform()
    except Exception:
        pass
    capturar(driver, carpeta, "3_hover_total")

    # ver carrito
    try:
        cart_link = driver.find_element(By.CSS_SELECTOR, "a[href='/cart']")
        cart_link.click()
    except Exception:
        # fallback: cualquier enlace que contenga 'cart'
        try:
            cart_link = driver.find_element(By.XPATH, "//a[contains(@href,'cart') or contains(.,'Cart') or contains(.,'carrito')]")
            cart_link.click()
        except Exception:
            print("[WARN] No pude abrir link directo al carrito en prueba_1")
    capturar(driver, carpeta, "4_view_cart")


def prueba_2(carpeta):
    driver.get(URL)
    capturar(driver, carpeta, "1_inicio")

    cafe = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-cy='Espresso']")))
    cafe.click(); cafe.click(); cafe.click()
    capturar(driver, carpeta, "2_click_espresso")

    root = tk.Tk(); root.withdraw()
    respuesta = messagebox.askyesno("Confirmación", "¿Quieres hacer click en 'Yes, of course!'?")
    root.destroy()

    if respuesta:
        try:
            yes_btn = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "yes")))
            try:
                yes_btn.click()
            except ElementClickInterceptedException:
                js_click(yes_btn)
            capturar(driver, carpeta, "3_yes_click")
        except Exception as e:
            print(f"[ERROR] No encontré el botón Yes: {e}")
    else:
        print("[ℹ] El usuario eligió no hacer click en 'Yes, of course!'")

    # hover y ver carrito
    try:
        total = driver.find_element(By.CLASS_NAME, "pay")
        ActionChains(driver).move_to_element(total).perform()
    except Exception:
        pass
    capturar(driver, carpeta, "4_hover_total")

    try:
        cart_link = driver.find_element(By.CSS_SELECTOR, "a[href='/cart']")
        cart_link.click()
    except Exception:
        try:
            cart_link = driver.find_element(By.XPATH, "//a[contains(@href,'cart') or contains(.,'Cart') or contains(.,'carrito')]")
            cart_link.click()
        except Exception:
            print("[WARN] No pude abrir link directo al carrito en prueba_2")
    capturar(driver, carpeta, "5_view_cart")


def prueba_3(carpeta):
    driver.get(URL)
    capturar(driver, carpeta, "1_inicio")

    cafe = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-cy='Espresso']")))
    ActionChains(driver).context_click(cafe).perform()
    capturar(driver, carpeta, "2_click_derecho")

    root = tk.Tk(); root.withdraw()
    respuesta = messagebox.askyesno("Confirmación", "¿Quieres agregar Espresso al carrito?")
    root.destroy()

    if respuesta:
        try:
            btn_yes = driver.find_element(By.XPATH, "//button[text()='Yes']")
            try:
                btn_yes.click()
            except ElementClickInterceptedException:
                js_click(btn_yes)
            capturar(driver, carpeta, "3_yes")
        except Exception:
            print("[WARN] No encontré botón 'Yes' en prueba_3")
    else:
        try:
            btn_no = driver.find_element(By.XPATH, "//button[text()='No']")
            try:
                btn_no.click()
            except ElementClickInterceptedException:
                js_click(btn_no)
            capturar(driver, carpeta, "3_no")
        except Exception:
            print("[WARN] No encontré botón 'No' en prueba_3")

    try:
        total = driver.find_element(By.CLASS_NAME, "pay")
        ActionChains(driver).move_to_element(total).perform()
    except Exception:
        pass
    capturar(driver, carpeta, "4_hover_total")

    try:
        cart_link = driver.find_element(By.CSS_SELECTOR, "a[href='/cart']")
        cart_link.click()
    except Exception:
        try:
            cart_link = driver.find_element(By.XPATH, "//a[contains(@href,'cart') or contains(.,'Cart') or contains(.,'carrito')]")
            cart_link.click()
        except Exception:
            print("[WARN] No pude abrir link directo al carrito en prueba_3")
    capturar(driver, carpeta, "5_view_cart")


def prueba_4(carpeta):
    """
    Prueba 4:
    - Seleccionar Espresso (igual que prueba_1)
    - Abrir carrito
    - Checkout (clic forzado si hace falta)
    - Rellenar nombre/email
    - Confirmar pago (clic forzado si hace falta)
    - Esperar mensaje de éxito y mostrar messagebox
    - Guardar capturas en cada paso
    """
    driver.get(URL)
    capturar(driver, carpeta, "1_inicio")

    # 1) Seleccionar Espresso (igual visual que prueba_1)
    try:
        espresso = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-cy='Espresso']")))
        espresso.click()
        capturar(driver, carpeta, "2_click_espresso")
    except Exception as e:
        print("[ERROR] No se pudo seleccionar Espresso en prueba_4:", e)
        capturar(driver, carpeta, "2_error_no_espresso")
        return

    # Hover total
    try:
        total = driver.find_element(By.CLASS_NAME, "pay")
        ActionChains(driver).move_to_element(total).perform()
    except Exception:
        pass
    capturar(driver, carpeta, "3_hover_total")

    # 2) Abrir carrito
    opened = False
    try:
        cart_anchor = driver.find_element(By.CSS_SELECTOR, "a[href='/cart']")
        cart_anchor.click()
        opened = True
    except Exception:
        # fallback: intentar click en total/pay
        try:
            pay_el = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "pay")))
            try:
                pay_el.click()
            except ElementClickInterceptedException:
                js_click(pay_el)
            opened = True
        except Exception:
            opened = False

    if not opened:
        try:
            cart_fb = driver.find_element(By.XPATH, "//a[contains(@href,'cart') or contains(.,'Cart') or contains(.,'carrito')]")
            js_click(cart_fb)
            opened = True
        except Exception:
            opened = False

    if not opened:
        print("[ERROR] No pude abrir el carrito en prueba_4.")
        capturar(driver, carpeta, "4_error_no_cart")
        return

    capturar(driver, carpeta, "4_view_cart")
    time.sleep(0.5)

    # 3) Checkout / Proceed to pay (varias opciones)
    checkout_found = False
    checkout_candidates = [
        (By.CLASS_NAME, "pay"),
        (By.CSS_SELECTOR, "button[data-test='checkout']"),
        (By.XPATH, "//button[contains(.,'Checkout') or contains(.,'Pay') or contains(.,'Pagar')]"),
        (By.XPATH, "//button[contains(.,'Total') or contains(.,'$')]"),
    ]
    for by, sel in checkout_candidates:
        try:
            el = driver.find_element(by, sel)
            try:
                el.click()
            except ElementClickInterceptedException:
                js_click(el)
            checkout_found = True
            break
        except Exception:
            continue

    if not checkout_found:
        print("[ERROR] No encontré botón de checkout/pagar en prueba_4.")
        capturar(driver, carpeta, "5_error_no_checkout")
        return

    capturar(driver, carpeta, "5_click_checkout")
    time.sleep(0.6)

    # 4) Llenar nombre y email
    name_selectors = [(By.ID, "name"), (By.NAME, "name"), (By.CSS_SELECTOR, "input[placeholder*='name']")]
    email_selectors = [(By.ID, "email"), (By.NAME, "email"), (By.CSS_SELECTOR, "input[placeholder*='email']"), (By.CSS_SELECTOR, "input[type='email']")]

    name_field = None
    email_field = None
    for by, sel in name_selectors:
        try:
            name_field = driver.find_element(by, sel)
            break
        except Exception:
            name_field = None
    for by, sel in email_selectors:
        try:
            email_field = driver.find_element(by, sel)
            break
        except Exception:
            email_field = None

    # fallback: primeros inputs visibles si no se detectaron
    if not name_field or not email_field:
        inputs = driver.find_elements(By.XPATH, "//input[not(@type='hidden') and (contains(@type,'text') or contains(@type,'email'))]")
        if len(inputs) >= 2:
            if not name_field:
                name_field = inputs[0]
            if not email_field:
                email_field = inputs[1]

    if not name_field or not email_field:
        print("[ERROR] No pude localizar campos nombre/email en prueba_4.")
        capturar(driver, carpeta, "6_error_no_inputs")
        return

    try:
        name_field.clear()
        name_field.send_keys("Luisa Rojas")
        email_field.clear()
        email_field.send_keys("luisa@test.com")
        capturar(driver, carpeta, "6_datos_ingresados")
    except Exception as e:
        print("[ERROR] Error al escribir datos en prueba_4:", e)
        capturar(driver, carpeta, "6_error_writing_inputs")
        return

    time.sleep(0.4)

    # 5) Confirmar / Pagar (buscar botón confirm y hacer click)
    confirm_found = False
    confirm_selectors = [
        (By.XPATH, "//button[contains(.,'Confirm') or contains(.,'Place order') or contains(.,'Pagar') or contains(.,'Pay') or contains(.,'Checkout')]"),
        (By.CSS_SELECTOR, "button[type='submit']"),
        (By.CSS_SELECTOR, "button[data-test='confirm']"),
        (By.CLASS_NAME, "pay"),
    ]
    for by, sel in confirm_selectors:
        try:
            btn = driver.find_element(by, sel)
            try:
                btn.click()
            except ElementClickInterceptedException:
                js_click(btn)
            confirm_found = True
            break
        except Exception:
            continue

    if not confirm_found:
        print("[ERROR] No encontré botón de confirmación en prueba_4.")
        capturar(driver, carpeta, "7_error_no_confirm")
        return

    capturar(driver, carpeta, "7_click_confirm")
    time.sleep(0.7)

    # 6) Esperar y validar mensaje de éxito
    success_el = wait_for_success_message(carpeta, timeout=10)
    if success_el:
        text = success_el.text if hasattr(success_el, "text") else str(success_el)
        print("[✔] Mensaje de éxito detectado:", text)
        # mostrar messagebox para evidenciar al usuario
        try:
            messagebox.showinfo("Compra exitosa", "Compra realizada con éxito.\n" + (text[:200] if text else ""))
        except Exception:
            pass
    else:
        print("[⚠] No apareció mensaje de éxito en prueba_4; revisa capturas para diagnóstico.")

def prueba_5(carpeta):
    """Agregar item al carrito usando data-cy con confirmación"""
    driver.get(URL)
    capturar(driver, carpeta, "1_inicio")

    # Click en el Espresso
    cafe = driver.find_element(By.CSS_SELECTOR, "[data-cy='Espresso']")
    cafe.click()
    capturar(driver, carpeta, "2.1_click_espresso")
    # Click en la Mocha
    cafe = driver.find_element(By.CSS_SELECTOR, "[data-cy='Mocha']")
    cafe.click()
    capturar(driver, carpeta, "2.2_click_Mocha")
    # Click en la Espresso-Con Panna
    cafe = driver.find_element(By.CSS_SELECTOR, "[data-cy='Espresso-Con Panna']")
    cafe.click()
    capturar(driver, carpeta, "2.3_click_Espresso-Con Panna")
    time.sleep(2)
    #Seleccionar si se quiere la oferta
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

    capturar(driver, carpeta, "4_hover_total")
   # Hacer click en "View Cart"
    cart_link = driver.find_element(By.CSS_SELECTOR, "a[href='/cart']")
    cart_link.click()
    capturar(driver, carpeta, "5_view_cart")
# ==== MAPA DE PRUEBAS ====
PRUEBAS = {1: prueba_1, 2: prueba_2, 3: prueba_3, 4: prueba_4, 5: prueba_5}


# ==== TKINTER ====
root = tk.Tk(); root.withdraw()
caso = simpledialog.askinteger("Caso de prueba", "Ingrese el número de caso (1-5):")
root.destroy()

if caso in PRUEBAS:
    carpeta = crear_carpeta(caso)
    try:
        PRUEBAS[caso](carpeta)
    finally:
        # asegurar guardado y cerrar driver
        time.sleep(0.8)
        try:
            driver.quit()
        except Exception:
            pass
else:
    print("Número de caso inválido.")
    driver.quit()
