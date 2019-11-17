from bs4 import BeautifulSoup
import requests
import re

url = 'https://irecommend.ru/content/prekrasnyi-otdykh-za-nebolshuyu-tsenu'
#p1 полож
#m1 отриц
#zero нейтр
tonality = "p1"

timeTxt = ''

arr = url.split('/')

nameTxt=arr[4]
print(arr[4])

#filename = "eto-samaya-uzhasnaya-poezdka-v-moei-zhizni.txt"
filename = nameTxt+".txt"

page = requests.get(url)
#Код вернул нам статус код '200', значит это, что мы успешно подключены и все в полном порядке.
print(page.status_code)

new_data = []
new_news = []
new_news2 = []
new_news3 = []

data = []
data2 = []
news = []
news2 = []
news3 = []

#Самое время воспользоваться
# BeautifulSoup4 и скормить ему наш page, указав в кавычках как он нам поможет 'html.parcer

soup = BeautifulSoup(page.text, "html.parser")
#Нам вылезет весь html-код нашей страницы.
#print(soup)

#Теперь воспользуемся функцией поиска в BeautifulSoup4:
#В ранее созданный список 'news' , сохраняем все с тэгом 'а' и классом 'news'.
# Если попросим вывести в консоль все, что он нашел, он покажет нам все новости, что были на странице:
data = soup.findAll('span', class_='dtreviewed')
news = soup.findAll('h2', class_='reviewTitle')
news2 = soup.findAll('div', class_='description hasinlineimage')
news3 = soup.findAll('div', class_='fivestarWidgetStatic fivestarWidgetStatic-vote fivestarWidgetStatic-5')

#Тут мы в цикле for перебираем весь наш список новостей. Если в новости под индексом [i] мы находим тэг 'span' и
#класc 'time2 time3', то сохраняем текст из этой новости в новый список 'new_news'.
#description hasinlineimage

#str = 0
#for a in range(len(news3)):
    #if news3[a].find('div', class_='star') is not None:
        #if news3[a].find('div', class_='on') is not None:
            #str = str + 1
         #   new_news3.append(news3[a])
            #print(str)

        #for a in range(len(new_news3)):
         #   print(new_news3[a])
           # print(str)

#Перед началом обучения тексты прошли процедуру предварительной обработки:
#приведение к нижнему регистру;
#замена «ё» на «е»;
#замена ссылок на токен «URL»;
#замена упоминания пользователя на токен «USER»;
#удаление знаков пунктуации.
def preprocess_text(text):
    text = text.lower().replace("ё", "е")
    text = text.lower().replace("\n", " ")
    text = re.sub('((www\.[^\s]+)|(https?://[^\s]+))', 'URL', text)
    text = re.sub('@[^\s]+', 'USER', text)
    text = re.sub('[^a-zA-Zа-яА-Я1-9]+', ' ', text)
    text = re.sub(' +', ' ', text)
    return text.strip()


#data = [preprocess_text(t) for t in raw_data]

def addTextInFile(text):
    # -*- coding: utf-8 -*-
    my_file = open('zero.txt', 'w')

    #text_for_file = 'Some text here...'
    my_file.write(text)

    my_file.close()

def addTextInFileTwo(L):
    # -*- coding: utf-8 -*-
    F = open(filename, 'w', encoding='utf-8')

    for i in L:
        F.write(str(i) + " ")

    F.close()


#------------------------------------------------------------------------------------------------------------------
for i in range(len(data)):
    if data[i].find('meta') is not None:
        #print(data[i].attrs('content'))
        if data[i].find('meta').has_attr('content'):
           # new_data.append(['content'])
            timeText = data[i].find('meta').attrs['content']
            #print(data[i].find('meta').attrs['content'])

        arr2 = timeText.split('T')
        timeTxt = arr2[0]
        #print(arr2[0])

#----------------------------------------------------------------------------------------------------------------
def addTextInFileJson():
    print(timeTxt)
    # -*- coding: utf-8 -*-
    F = open('AVSafeeva.json', 'a')
    text = '{'+"\n"'"student_name": "Safeeva Nastya",'+ "\n"'"student_group": 651,'+ "\n"'"student_number": 3,'+ "\n"'"date": "'+timeTxt+'",'+ "\n"'"Data source": "'+url+'",'+ "\n"'"tonality": "'+tonality+'",'+ "\n"'"filename":"'+filename+'"'+ "\n"'},'+"\n"
    F.write(text)
    F.close()


#-----------------------------------------------------------------------------------------------------------------
for i in range(len(news)):
    if news[i].find('a', class_='review-summary active') is not None:
        new_news.append(news[i].text)
        #new_news.append(preprocess_text(news[i].text))

        #for i in range(len(new_news)):
            #print(new_news[i])
            #print(preprocess_text(new_news[i]))
            #addTextInFile(preprocess_text(new_news[i]))

for j in range(len(news2)):
    if news2[j].find('p') is not None:
         new_news.append(news2[j].text)
         #new_news.append(preprocess_text(news2[j].text))
         addTextInFileTwo(new_news)
         addTextInFileJson()
         for j in range(len(new_news)):
                print(new_news[j])
                #print(preprocess_text(new_news[j]))