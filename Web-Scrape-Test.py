#Libraries
from googletrans import Translator
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



# configure webdriver
options = Options()
options.headless = True  # hide GUI
options.add_argument("--window-size=1920,11880")  # set window size to native GUI size
options.add_argument("start-maximized")  # ensure window is full-screen

#Website URL to Scrape
url = "https://www.classcentral.com/"
driver = webdriver.Chrome(options=options)
driver.get(url)

# wait for page to load
element = WebDriverWait(driver=driver, timeout=150).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, 'div[class=main-nav-dropdown__index]'))
)

#Putting the Page source on a variable
page = driver.page_source

soup = BeautifulSoup(page, 'html.parser')



#Creating an HTML File with our Scrapped Page Source
file_html = open("index.html", "w", encoding='utf-8')
file_html.write(str(soup))
file_html.close()
soup = BeautifulSoup(page, 'html.parser')
#Adding the website URL to Local Images and scripts in order for them to be visible
for el in soup.select("[srcset]"):

    if not el.attrs['srcset'].startswith('https://'):
        with open(r'index.html', 'r', encoding='utf-8') as file:
            data = file.read()

            data = data.replace(el.attrs['srcset'], "https://www.classcentral.com/images/illustrations/homepage-discover-01-small.webp 900w, https://www.classcentral.com/images/illustrations/homepage-discover-01-med.webp 1500w, https://www.classcentral.com/images/illustrations/homepage-discover-01-large.webp 2400w")
        with open(r'index.html', 'w', encoding='utf-8') as file:
            file.write(data)

for el in soup.select("[src]"):

    if   el.attrs['src'].startswith('images/'):
        with open(r'index.html', 'r', encoding='utf-8') as file:
            data = file.read()

            data = data.replace(el.attrs['src'], "https://www.classcentral.com/images/illustrations/homepage-discover-01-large.webp")
        with open(r'index.html', 'w', encoding='utf-8') as file:
            file.write(data)

    elif  el.attrs['src'].startswith('/webpack') :
        with open(r'index.html', 'r', encoding='utf-8') as file:
            data = file.read()

            data = data.replace(el.attrs['src'], "https://www.classcentral.com/"+el.attrs['src'])
        with open(r'index.html', 'w', encoding='utf-8') as file:
            file.write(data)


#Setting up translator
translator = Translator(service_urls=['translate.google.com'])
translator.raise_Exception = True

#Translating main page to Hindi

for tags in soup.find_all():   
    
    if not tags.name == 'script' and  not tags.name == 'style' and not tags.name == 'meta'  and not tags.text  == '\n':
        ScrappedText = tags.string
        if not ScrappedText == None:

            Hinditext = translator.translate(ScrappedText, src='en', dest='hi')
            with open(r'index.html', 'r', encoding='utf-8') as file:
                    data = file.read()
                    finder = '>'+tags.text+'<'
                    data = data.replace(finder, '>'+Hinditext.text+'<')
            with open(r'index.html', 'w', encoding='utf-8') as file:
                file.write(data)
print("main page translated")

#Getting all the URLS on the main site to scrape them
for links in soup.find_all('a'):
    urls = links.get('href')
    drivers = webdriver.Chrome(options=options)

    #Giving a name to our 1 level depth URL sites for the HTML files

    #Adding the website URL to Local urls to be able to scrape them as well
    if urls.startswith('/'):
        if urls == '/':
            name = links.find('span').text
        else:
            name = urls.split("/")
            name = (name[-1])
        urls = "https://classcentral.com"+urls
        
    #Making sure the socialmedia sites are also included    
    elif urls == 'https://www.facebook.com/classcentral':
        name = "facebookclasscentral"
    elif urls == 'https://www.twitter.com/classcentral':
        name = "twitter-classcentral"
    elif urls == 'https://www.linkedin.com/company/classcentral':
        name = "linkedin-classcentral"
    elif urls == 'https://www.youtube.com/classcentral':
        name = "youtube-classcentral"
    elif urls == 'http://www.facebook.com/sharer.php?u=https%3A%2F%2Fwww.classcentral.com%2F':
        name = "facebook-share-classcentral"
    elif urls == 'https://twitter.com/intent/tweet?url=https%3A%2F%2Fwww.classcentral.com%2F&text=&via=classcentral':
        name = "tweetclasscentral"
    elif urls == 'mailto:?subject=&body=%20https%3A%2F%2Fwww.classcentral.com%2F':
        name = "mailto-classcentral"

    #Removing the ending backslash to URLs to avoid the /.html error
    else:
        if urls.endswith('/'):
            urls = urls.rstrip('/')
            name = urls.split("/")
            name = (name[-1])
        else:
            name = urls.split("/")
            name = (name[-1])

    #Calling our drivers to scrape all the URLs on the main site        
    drivers.get(urls)
        # wait for page to load
    elements = WebDriverWait(driver=driver, timeout=150).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'div[class=main-nav-dropdown__index]'))
    )
    pages = drivers.page_source
    soups = BeautifulSoup(pages, 'lxml')
    
    name = name+".html"
    #Creating all the new HTML Files
    file_html = open(name, "w", encoding='utf-8')
    file_html.write(str(soups))
    file_html.close()

    #Making it not possible to go more than 1 level depth
    for refs in soups.find_all('a'):
        file = open(name, "r", encoding='utf-8')
        data = file.read()
        data = data.replace("href="+'"'+refs.get('href')+'"',"href="+'""')
        file = open(name, "w", encoding='utf-8')
        file.write(data)


    #Translating 1 level depth pages, Im commenting this part because it would take my laptop
    # like 8 hours to translate it all and its really difficult for me
    '''
    for tags in soups.find_all():      
        if not tags.name == 'script' and  not tags.name == 'style' and not tags.name == 'meta'  and not tags.text  == '\n':
            
            if not tags.string is None:
                Hindi = translator.translate(tags.string, src='en', dest='hi')
                file = open(name, 'r', encoding='utf-8')
                data = file.read()
                finder = '>'+tags.text+'<'
                data = data.replace(finder, '>'+Hindi.text+'<')
                file = open(name, 'w', encoding='utf-8')
                file.write(data)
    print(name+" translated")            
    '''
    #Pointing URls in index.html to their new HTML file
    with open(r'index.html', 'r', encoding='utf-8') as file:
            data = file.read()
            data = data.replace("href="+'"'+links.get('href')+'"',"href="+'"'+ name+".html"+'"')
    with open(r'index.html', 'w', encoding='utf-8') as file:
            file.write(data)


