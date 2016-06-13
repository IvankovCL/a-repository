import os

def getWiki(path1): #скачивание википедии
    os.system("C:\\Python27\\python.exe C:\\hw_python\\wikiextractor-master\\WikiExtractor1.py -o " + output + " -b 3M C:\\hw_python\\maltese_wiki.xml")

def walk(path2): #обход скачанных файлов
    fullVoc = []
    for d, dirs, files in os.walk(path2):
        for filename in files:
            wiki = os.path.join(d,filename)
            fullVoc += wordsToVoc(wiki)
    freqDict(fullVoc)

def wordsToVoc(file): #извлечение слов из всех скачанных файлов
    f = open(file, 'r', encoding='utf-8')
    words = []
    for line in f:
        wordsInLine = line.split()
        words += wordsInLine
    f.close()
    return words

def freqDict(voc):
    #подсчёт частотности
    freqs = {}
    for word in voc:
        word = word.lower()
        word = word.strip(',:;.!?\"\"\'\\()[]{}/><')
        if word.isalpha() == True:
            if word in freqs:
                freqs[word] += 1
            else:
                freqs[word] = 1

    #сортировка по убыванию частотности
    items = [(value, key) for key, value in freqs.items()]
    items.sort()
    items.reverse()

    #запись словаря в файл
    f2 = open('MalteseDict.tsv', 'w', encoding='utf-8')
    for item in items:
        f2.write(str(item[1]) + '\t' + str(item[0]) + '\n')

output = 'C:\\hw_python\\wikiFiles'
getWiki(output)
walk(output)
