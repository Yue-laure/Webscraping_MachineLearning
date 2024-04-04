import time
import csv
from selenium import webdriver
from selenium.common.exceptions import  NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
url = 'https://www.pole-emploi.fr/'
linkAnnounce = url + 'accueil/'
# Métier, entreprise, mot-clé, n° d'offre
emploiNameFind = 'Python'
emploiLieuFind = 'Paris'
# version
# site driver:https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/120.0.6099.71/win64/chromedriver-win64.zip
from selenium.webdriver.common.by import By

driver = webdriver.Chrome(executable_path=r'chromedriver-win64\chromedriver.exe')
driver.get(linkAnnounce)
driver.implicitly_wait(5)

# page home
# refuse cookies
# element = driver.find_element(By.ID, 'footer_tc_privacy_button')
# # element.click()
# driver.switch_to.frame('privacy-iframe')
# element = driver.find_element(By.CSS_SELECTOR, 'button[class="btn refuse-all"]')
# element.click()
# driver.implicitly_wait(5)
# shadow_root = driver.execute_script('return document.querySelector("#shadow-root").shadowRoot')
# inner_element = shadow_root.find_element(By.CSS_SELECTOR, '#pecookies-continue-btn')
# driver.execute_script('arguments[0].click();', inner_element)

# Attendre que la balise <pe-cookies> soit chargée et récupérez-la
pe_cookies = driver.find_element(By.TAG_NAME, "pe-cookies")
# Accéder au shadow root et récupérez le bouton
accept_all_button = driver.execute_script("""
return arguments[0].shadowRoot.querySelector('#pecookies-accept-all');
""", pe_cookies)
# Affichez des informations sur le bouton (si trouvé)
if accept_all_button:
    print("Bouton 'Tout accepter' trouvé.")
    print("Texte du bouton:", accept_all_button.text)
else:
    print("Bouton 'Tout accepter' non trouvé.")
accept_all_button.click()

#accepter announce du site
driver.switch_to.default_content()
element  =driver.find_element(By.CSS_SELECTOR,'div [class="know_button primaryButton know_button-has-background"]')
element.click()
driver.implicitly_wait(5)

# chercher emploi \
element = driver.find_element(By.CSS_SELECTOR, '#keywords-selectized')
element.send_keys(emploiNameFind + '\n')
element.send_keys(Keys.TAB)
if emploiLieuFind:
    element = driver.find_element(By.CSS_SELECTOR, '#location1-selectized')
    element.send_keys(emploiLieuFind)
    first_option = driver.find_element(By.CSS_SELECTOR, 'div .option.active.ng-star-inserted')
    first_option.click()
element = driver.find_element(By.XPATH,
                              '//*[@id="contents"]/app-bandeau-top/div/app-recherche-emploi/div/div/form/div/div/div[3]/span/button')
element.click()

# page apres chercher
for handle in driver.window_handles:
    driver.switch_to.window(handle)
    if "2179 offres d'emploi pour Python - Paris (Dept.) | Pôle emploi" in driver.title:
        break
offres = driver.find_elements(By.CSS_SELECTOR, '#zoneAfficherListeOffres>ul li')
# offres = driver.find_elements_by_class_name('media with-fav')
print(len(offres)) # 20 each page
offreUrls=[]
print(offres)
for i in offres:
    offreUrls.append(i.find_element(By.TAG_NAME, 'a').get_attribute("href"))
print(offreUrls)

header = ['Titre', 'Departement', 'ExperienceRequirements', 'OffreUrl', 'Description']
i = 0
with open("dataDownloadSelenium/announce.csv", mode="w", newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(header)

    for offreUrl in offreUrls:
        #ouvrir lien de announce emploi
        time.sleep(1)
        driver.get(offreUrl)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
        driver.switch_to.window(driver.window_handles[-1])
        titre = None
        departement = None
        experienceRequirements = None
        description = None
        try:
            titre = driver.find_element(By.CSS_SELECTOR, '#labelPopinDetailsOffre > span[itemprop="title"]').text
            time.sleep(1)
            departement = driver.find_element(By.XPATH,
                                              '//*[@id="contents"]/div[1]/div/div[1]/div/div[3]/div/div/div/div/p[1]/span[1]/span[5]').text
            time.sleep(1)
            experienceRequirements = driver.find_element(By.CSS_SELECTOR,
                                                         '#contents > div.container-fluid.gabarit-full-page.with-large-right-column > div > div.panel-center.col-md-8 > div > div.modal-details.modal-details-offre > div > div > div > div > ul:nth-child(7) > li > span > span.skill-name').text
            time.sleep(1)
            description = driver.find_element(By.XPATH,
                                              '//*[@id="contents"]/div[1]/div/div[1]/div/div[3]/div/div/div/div/div[1]/div[1]/p').text
        except NoSuchElementException as e:
            print(f"Element not found: {e}")
        # print(titre, departement, experienceRequirements, offreUrls, description)
        writer.writerow([titre, departement, experienceRequirements, offreUrl, description])
driver.quit()
