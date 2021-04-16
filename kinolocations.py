from urllib.request import urlopen
from bs4 import BeautifulSoup
from bs4 import NavigableString
from scrapy import linkextractors
import re
import scrapy
import json

# f = open('locations_from_kinolocation.json', 'w')
# f.write("[")
with open("locations_from_kinolocation.json", "w", encoding='utf8') as write_file:

    d = dict.fromkeys(['Link', 'Title', 'Description', 'Photo', 'Address'])

    html = urlopen("http://kinolocation.ru")
    bsObj = BeautifulSoup(html.read(), "html.parser")

    # contacts = bsObj.find('div', {'class': 'textwidget'})

    pages = bsObj.find('a', {'class': 'last'})
    pages = str(pages)
    pages = int((re.findall('\d+', pages))[0])
    # f.write(str(pages))
    # f.write("\n")

    for place in bsObj.find_all('h2', {'class': 'title'}):
        # f.write("{")
        # f.write("\n")
        link = place.find('a', href=True)
        if link is None:
            continue
        # f.write('"Link":')
        # f.write(link['href'])
        # f.write("\n")
        d['Link'] = link['href']

        place_html = urlopen(link['href'])
        place_soup = BeautifulSoup(place_html.read(), 'html.parser')

        title = place_soup.find('h2', {'class': 'title'})
        # f.write(title.getText())
        # f.write("\n")
        d['Title'] = title.getText()

        description = place_soup.find('meta', {'name': 'description'}, content=True)
        # f.write(description['content'])
        # f.write("\n")
        d['Description'] = description['content']

        images = place_soup.find('ul', {'class': 'wp-block-gallery columns-3 is-cropped'})
        images = images.find_all('li', {'class': 'blocks-gallery-item'})
        images_string = ""
        for image in images:
            image_link = image.find('a', href=True)
            images_string += image_link['href']
            images_string += " "
            # f.write(image_link['href'])
            # f.write("\n")
        d['Photo'] = images_string

        # for contact in contacts.find_all('p'):
        #    f.write(contact.getText())
        #    f.write("\n")

        #f.write("\n")

        json.dump(d, write_file, ensure_ascii=False)

    for page in range(2, pages + 1):
        next_page = "http://kinolocation.ru/page/" + str(page) + "/"

        html = urlopen(next_page)
        bsObj = BeautifulSoup(html.read(), "html.parser")
        # d = dict(Link="", Title="", Description="", Photo="", Address="")

        for place in bsObj.find_all('h2', {'class': 'title'}):
            link = place.find('a', href=True)
            if link is None:
                continue
            # f.write(link['href'])
            # f.write("\n")
            d['Link'] = link['href']

            place_html = urlopen(link['href'])
            place_soup = BeautifulSoup(place_html.read(), 'html.parser')

            title = place_soup.find('h2', {'class': 'title'})
            # f.write(title.getText())
            # f.write("\n")
            d['Title'] = title.getText()

            description = place_soup.find('meta', {'name': 'description'}, content=True)
            # f.write(description['content'])
            # f.write("\n")
            d['Description'] = description['content']

            images = place_soup.find_all('li', {'class': 'blocks-gallery-item'})
            images_string = ""
            for image in images:
                image_link = image.find('a', href=True)
                images_string += image_link['href']
                images_string += " "
                # f.write(image_link['href'])
                # f.write("\n")
            d['Photo'] = images_string

            if images_string == "":
                images = place_soup.find_all('figure', {'class': 'gallery-item'})
                images_string = ""
                for image in images:
                    image_link = image.find('a', href=True)
                    images_string += image_link['href']
                    images_string += " "
                    # f.write(image_link['href'])
                    # f.write("\n")
                d['Photo'] = images_string

            json.dump(d, write_file, ensure_ascii=False)

            # for contact in contacts.find_all('p'):
            #    f.write(contact.getText())
            #    f.write("\n")

            #f.write("\n")
    # f.write("]")
    # f.close()
