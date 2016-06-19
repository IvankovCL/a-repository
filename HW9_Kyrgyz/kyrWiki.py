import os, re

def getWiki(path1): #скачивание википедии
    os.system("C:\\Python27\\python.exe C:\\Users\\Ivankov\\Desktop\\HW_KGZ\\wikiextractor-master\\WikiExtractor1.py -o " /
              + path1 + " -b 3M C:\\Users\\Ivankov\\Desktop\\HW_KGZ\\kywiki-20160601-pages-meta-current.xml") 
    

def wordsToVoc(file): #извлечение слов из всех скачанных файлов
    with open(file, 'r', encoding='utf-8') as toParse:
        words = []
        for line in toParse:
            wordsInLine = line.split()
            words += wordsInLine

        clean = []            

        for word in words:
            if re.search('^(<doc|</doc|id=|url=|title=)', word) == None and re.search('[0-9%A-z]', word) == None:
                word = word.strip('«»,:;.!?\"\"\'\\()[]{}/><”')
                clean.append(word)           
            
        return clean

def walk(path2): #обход скачанных файлов
    fullVoc = []
    for d, dirs, files in os.walk(path2):
        for filename in files:
            wiki = os.path.join(d,filename)
            print(wiki)
            fullVoc += wordsToVoc(wiki)
            
    with open('words.txt', 'w', encoding='utf-8') as toWrite:
        for one in fullVoc:
            toWrite.write(one + '\n')

if __name__ == '__main__':
    """
     Скачивает дамп киргизской википедии
     """    
    output = '.\\wikiFiles'
    getWiki(output)
    walk(output)
    print('Done')
