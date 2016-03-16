import urllib.request, requests, re, os, lxml.html
import urllib.parse 
from pymystem3 import Mystem

def lemma(text):
    m = Mystem()
    lemmas = m.lemmatize(text)
    titleStemmed = ''.join(lemmas)
    return titleStemmed

def wordToDigit(wordForMonth):
    calendar = {'января':'01', 'февраля':'02', 'марта':'03', 'апреля':'04', 
                'мая':'05', 'июня':'06', 'июля':'07', 'августа':'08', 'сентября':'09',
                'октября':'10', 'ноября':'11', 'декабря':'12'}
    digitForMonth = calendar[wordForMonth]
    return digitForMonth

def crawl(response, usedLinks, curLink):
    
    """page = con.read()
    page = page.decode(encoding='utf-8')"""
    
    #получаем текущую страницу
    page = response.text
    tree = lxml.html.fromstring(page)   
  
    #анализируем текущую страницу  
       
    if 'news/' in curLink:
    
        #находим заголовок
        title = tree.findtext('.//title')
            #print(title)
        
        #генерируем имя файла 
        filename = curLink.replace('/', '-')+'.txt'
                
        #находим дату, месяц и год
        date = tree.xpath('.//div[@class="news-item-additional"]/text()')

        d = re.search('[0-9]{2}', str(date))
        day = d.group(0)
        
        m = re.search('([А-Яа-я]+)', str(date))
        month = m.group(0)
        month = wordToDigit(month) 
        y = re.search('[0-9]{4}', str(date))
        year = y.group(0)     
        #находим текст       
        text = tree.xpath('.//p[@style="text-align: justify;"]/text()')
        if not text:
            text = tree.xpath('.//span[@style="font-size:9.5pt;font-family:&quot;Arial&quot;,&quot;sans-serif&quot;"]/text()')
        if not text:
            text = tree.xpath('.//p/text()')
        if not text:
            text = tree.xpath('.//div[@style="text-align: justify;"]/text()')
                  
        #очищаем от мусора
        for e in range(len(text)):
            if '\r\n\t' in text[e]:
                text[e] = text[e].replace('\r\n\t','')
                
        #создаём папки по годам и месяцам
        os.makedirs('C:\\search\\corpora\\' + year + '\\' + month + '\\', exist_ok = True)
               
        #записываем метаданные
        f1 = open('meta.csv', 'a', encoding='utf-8')
        f1.write('C:\\search\\corpora\\' + year + '\\' + month + '\\'+'\t'+''+'\t'+''+'\t'+''+'\t'+str(title)+'\t'+day+'.'+month+'.'+year+'.'+'\t'  
                 'публицистика'+'\t'+''+'\t'+''+'\t'+''+'\t'+''+'\t'+'нейтральный'+'\t'+'н-возраст'+'\t'+
                 'н-уровень'+'\t'+'городская'+'\t'+'http://ulpravda.ru/'+curLink+'\t'+'Ульяновская правда'+'\t'+''+'\t'+
                 year+'\t'+'газета'+'\t'+'Россия'+'\t'+'Ульяновская область'+'\t'+'ru'+'\t'+lemma(title)+'\n')
        f1.close()
        
        #записываем текст
        f2 = open('corpora\\' + year + '\\' + month + '\\' + filename, 'w', encoding='utf-8')
        f2.write('@au ' + 'NoName' + '\n' + '@ti ' +  str(title) + '\n' + '@da '+day+'.'+month+'.'+year + '\n' +
                 '@topic ' + 'NoTopic' + '\n' + '@url ' + 'http://ulpravda.ru/'+curLink+ '\n' + str(text))
        f2.close()
    

    
    #собираем ссылки с текущей страницы, нужны ссылки, содержащие subrubric, interview или district (оттуда можно добраться до любой новости в одной из подрубрик)
    #а чтобы найти новость, нужно в теге <a> найти строку news-item-more,  ссылка со строкой subrubric/pobeda не нужна
    links = [] 
    for a in tree.iter('a'):
        if a.get('class') != None:
            if 'subrubric' in a.get('href') and 'pobeda' not in a.get('href') or 'news-item-more' in a.get('class') or 'interview' in a.get('href') or 'district' in a.get('href'):
                links.append(a.get('href'))
                
    #заходим на каждую страницу в списке           
    for link in links:
        #проверяем, не было ли ещё этой ссылки
        if link in usedLinks:
            continue
        else:                      
            print('http://ulpravda.ru/'+link)
            #на странице подрубрики есть ссылка "Посмотреть всё", которая ведёт 
            #на страницу со всеми новостями в подрубрике, нужно передать параметр page=0
            if 'subrubric' in link:
                data = {}
                data["page"] = "0"
                url_values = urllib.parse.urlencode(data)
                q = urllib.parse.quote(link)
                curResponse = requests.get('http://ulpravda.ru/'+ q + "?" + url_values)
            else:
                q = urllib.parse.quote(link)
                curResponse = requests.get('http://ulpravda.ru/'+ q)
            used.append(link) #добавляем текущую страницу в использованные
            print(str(len(used)))
            crawl(curResponse, used, link) #переходим на новую  
         
# таблица с метаданными        
f1 = open('meta.csv', 'w', encoding='utf-8')
f1.write('path'+'\t'+'author'+'\t'+'sex'+'\t'+'birthday'+'\t'+'header'+'\t'+'created'+'\t'  
          'sphere'+'\t'+'genre_fi'+'\t'+'type'+'\t'+'topic'+'\t'+'chronotop'+'\t'+'style'+'\t'+'audience_age'+'\t'+
          'audience_level'+'\t'+'audience_size'+'\t'+'source'+'\t'+'publication'+'\t'+'publisher'+'\t'+
          'publ_year'+'\t'+'medium'+'\t'+'country'+'\t'+'	region'+'\t'+'language'+'\n')
f1.close()

firstLink = 'http://ulpravda.ru/'           
firstResponse = requests.get(firstLink)
used = [] #для использованных ссылок

crawl(firstResponse, used, firstLink)
  
print('Done')



    


