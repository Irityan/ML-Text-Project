# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
import re
import os

def countFiles(folder):
    file_count = len([name for name in os.listdir(folder) if os.path.isfile(os.path.join(folder, name))])
    return file_count

def addTextToFile(text):
    file = open(os.path.join(tonality, filename), 'w',encoding='utf-8')

    for i in text:
        file.write(str(i) + "\n")

def addToJSON():
    jsonFile = open(jsonPath, 'a', encoding='utf-8')
    text = '{' + "\n"'"student_name": "Курасов Илья",' + "\n"'"student_group": 651,' + "\n"'"student_number": 16,' + "\n"'"date": "' + timeTxt + '",' + "\n"'"Data source": "' + url + '",' + "\n"'"tonality": "' + tonality + '",' + "\n"'"filename": "' + tonality + '//' + filename + '"' + "\n"'},' + "\n"
    jsonFile.write(text)
    jsonFile.close()

jsonPath = "newElements.json"

try:
    while True:
        print("CTRL+C чтобы выйти")
        counts = [countFiles("m1"), countFiles("zero"), countFiles("p1")]
        print("Кол-во файлов: {}".format(sum(counts)))
        print("Из них: m1 - {}, zero - {}, p1 - {}".format(counts[0], counts[1], counts[2]))
        print("Процент сбора: {0:.2f}%".format(sum(counts)/250 * 100))
        url = input("URL: ").strip()
        tonality = input("Tonality (m1/zero/p1): ").strip()

        arr = url.split('/')
        nameTxt = arr[-1]
        filename = "{}.txt".format(nameTxt)

        page = requests.get(url)
        if page.status_code != 200:
            print("Не удалось получить данные с сайта!\n")
            input()
            os.system('cls')
            continue

        soup = BeautifulSoup(page.text, "html.parser")
        data = soup.findAll('span', class_='dtreviewed')
        titles = soup.findAll('h2', class_='reviewTitle')
        reviewBodies = soup.findAll('div', class_="description hasinlineimage")

        newReview = []

        for i in range(len(data)):
            if data[i].find('meta') is not None:
                if data[i].find('meta').has_attr('content'):
                    timeText = data[i].find('meta').attrs['content']

                arr2 = timeText.split('T')
                timeTxt = arr2[0]

        for i in range(len(titles)):
            if titles[i].find('a', class_='review-summary active') is not None:
                newReview.append(titles[i].text)

        for j in range(len(reviewBodies)):
            if reviewBodies[j].find('p') is not None:
                newReview.append(reviewBodies[j].text)
                addTextToFile(newReview)
                addToJSON()

        # os.system('cls')
except Exception:
    print('\nЗакончен сбор данных!')
