from lxml import etree

def readCedict():    
    #читает файл словаря   
    dic = {}
    with open('cedict_ts.u8', 'r', encoding='utf8') as cedict:
        for line in cedict:
            if line.startswith('#') == False:
                wordsInLine = line.split('\t') #пробелы между колонками предварительно заменены знаками табуляции
                dic[wordsInLine[1]] = wordsInLine[2:]
        cedict.close()
    return dic

dic = readCedict()
punct = ['“', '”', '。', '，','！', '？', '：', '-', '‘', '、', '…', '；', ' ']

def segment(text):
    #делит строку на сегменты, разделённые знаками препинания
    clauses = []
    clause = ''
    for char in text:        
        if char not in punct:
            clause += char
        else:
            clauses.append(clause)
            clause = ''
            clauses.append(char)
    return clauses
            
def findTokens(string, List, initial): 
    if string in dic: #если вся последовательность иероглифов есть в словаре
        found = string
        List.append(found) #записывает токен
        
        if  len(found) != len(initial): #если кроме найденного токена ещё есть иероглифы
            rest = initial.replace(found, '', 1) #убирает из строки найдённый токен
            findTokens(rest, List, rest) #ищет токены в оставшейся подстроке            
    else:
        findTokens(string[:-1], List, initial) #если последовательности нет, уменьшает строку на иероглиф, ищет токены
        
    return List

def process(f):
    
    xml = f.read()
    data = etree.fromstring(xml)
    
    #просматривает вcё дерево
    for tag in data.iter(): 
        allTokens = []
        tokensInSegment = []
        token = ''

        #ищет в теге текст
        if tag.tag == 'se': 
            if 'lang' not in tag.attrib:
                segments = segment(tag.text)
                
                for seg in segments:

                    if seg not in punct and seg not in ['ａ', '', ' ']:
                        tokensInSegment = findTokens(seg, tokensInSegment, seg)

                        for tIS in tokensInSegment:
                            allTokens.append(tIS)
                            
                    if seg in punct:
                        allTokens.append(seg)
                
            #редактирует тег <se>              
            tag.text = ''
            for t in allTokens:
                if t not in punct and t not in ['ａ', '', ' ']:
                    W = etree.Element('w')

                    ANA = etree.Element('ana')
                    ANA.attrib['lex'] = t
                    ANA.attrib['transcr'] = dic[t][0]
                    ANA.attrib['sem'] = dic[t][1]

                    W.append(ANA)
                    W.text = t
                    
                    tag.append(W)
                    
                if t in punct:
                    PUNCT = etree.Element('punct')
                    PUNCT.text = t
                    tag.append(PUNCT)

    toPrint = etree.tounicode(data)
                    
    with open('output.xml', 'w', encoding='utf8') as output:
        output.write(str(toPrint))
        
if __name__ == "__main__":
    with open('stal.xml', 'r', encoding='utf8') as stal:
        process(stal)
