from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time

start_url = "https://www.expansion.com/mercados/cotizaciones/indices/ibex35_I.IB.html"

with webdriver.Firefox() as driver:
    wait = WebDriverWait(driver, 10)
    driver.get(start_url)

    # Esperar hasta que la ventana emergente de cookies aparezca
    popup = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".didomi-popup-container")))

    # Hacer clic en el botón "Aceptar y continuar"
    accept_button = driver.find_element_by_id("ue-accept-notice-button")
    accept_button.click()

    time.sleep(1)

    #recuperamos listado de acciones
    commodities = driver.find_elements_by_xpath("/html/body/main/section/div/div/div/ul/li/div/section/div/article/section[2]/ul[2]/li[1]/div/section/table/tbody/tr")

    for stock in commodities:
        #recuperamos la información de cada acción
        values = stock.find_elements_by_xpath("td")        
        list_of_values = [x.text for x in values]
        for value in range(len(list_of_values)-1):
            if value != (len(list_of_values)-2):
                #eliminamos el punto de millar y cambiamos la coma decimal
                v = list_of_values[value].replace('.','')
                v = v.replace(',','.')
                print(v,end=",")
            else:
                print(list_of_values[value])
