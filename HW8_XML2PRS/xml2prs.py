import sys, csv
from lxml import etree

def prs2xml(source, target):
    with open(source, 'r', encoding='utf-8') as prs:
        read = csv.DictReader(prs, delimiter="\t")

        body = etree.Element('body')

        sentno = 0
        wordno = 0

        for i, line in enumerate(read):
            if i > 10:
                #создаём новый тег <se> каждый раз, когда значение поля sentno увеличивается
                if int(line['#sentno']) > sentno:
                    se = etree.SubElement(body, 'se')
                    sentno += 1
                #создаём новый тег <w> каждый раз, когда значение поля wordno увеличивается  
                if int(line['#wordno']) >wordno:
                    w = etree.SubElement(se, 'w')
                    sentno += 1
                    
                    ana = etree.SubElement(w, 'ana')
                    ana.set('lang', line['#lang'])
                    ana.set('word', line['#word'])
                    ana.set('indexword', line['#indexword'])            
                    ana.set('lem', line['#lem'])
                    ana.set('trans', line['#trans'])            
                    ana.set('trans_ru', line['#trans_ru'])

                    #в тег <gr> записываем содержимое полей lex и gram
                    gr = line['#lex']+ ',' + line['#gram']
                    ana.set('gr', gr)
                    
                    ana.set('morph', line['#flex'])
                    ana.set('punctl', line['#punctl'])

                    ana.tail = line['#word']
                    w.tail = line['#punctl']
            
        with open(target, 'w', encoding='utf-8') as xml:
            xml.write(etree.tounicode(body, pretty_print = False))

        print('Complete')

def xml2prs(source, target):
    with open(source, 'r', encoding='utf-8') as xml:
        tree = etree.fromstring(xml.read())
        
        sentno = 0
        toWrite = [] #для записи строк будущей таблицы prs

        for se in tree.iter('se'):
            sentno += 1 #считаем предложения
            wordno = 0
            
            for w in se.iter('w'):
                wordno += 1 #считаем слова в предложении
                nvar = 0
                nlems = set()

                #определяем место в предложении
                if wordno == len(list(se.iter('w'))):
                    sent_pos = 'eos'
                elif wordno == 1:
                    sent_pos = 'bos'
                else:
                    sent_pos = ''

                for ana in w.iter('ana'):
                    nvar += 1 #считаем варианты
                    graph = ''

                    #ищем заглавную букву
                    try:
                        if ana.tail.strip(' \n')[0].isupper() == True:
                            graph = 'cap'
                    except:
                        pass

                    #для подсчёта количества лемм собираем их в множество
                    nlems.add(ana.attrib['lex'])

                    #выделяем часть речи из тега <gr>
                    lex = ana.attrib['gr'].split(',')[0]

                    #отделяем пробелами грамматические теги в теге <gr>
                    gram = ' '.join(ana.attrib['gr'].split(',')[1:])

                    #в файле example.xml эти поля пусты, в каких-нибудь других файлах в них может быть информация
                    tags = {}
                    for tag in ['lang', 'indexword', 'trans_ru', 'punctl']:
                        if tag in ana.attrib:
                            tags[tag] = ana.attrib[tag]
                        else:
                            tags[tag] = ''

                    fields = {
                            '#sentno': sentno, '#wordno': wordno,'#lang': tags['lang'], '#graph': graph,
                            '#word': ana.tail.strip(' \n'), '#indexword': tags['indexword'],'#nvars': len(list(w.iter('ana'))),
                            '#nlems': len(nlems), '#nvar': nvar,'#lem': ana.attrib['lex'], '#trans': ana.attrib['trans'],
                            '#trans_ru': tags['trans_ru'], '#lex': lex,'#gram': gram.upper(),'#flex': ana.get('morph'),
                            '#punctl': tags['punctl'], '#punctr': w.tail.strip(' \n'), '#sent_pos': sent_pos
                            }
                    toWrite.append(fields)

    with open(target, 'w', encoding='utf-8') as prs:
        header = ('#sentno', '#wordno', '#lang', '#graph', '#word', '#indexword', '#nvars', '#nlems', '#nvar',
                      '#lem', '#trans', '#trans_ru', '#lex', '#gram', '#flex', '#punctl', '#punctr', '#sent_pos')
        writer = csv.DictWriter(prs, header, delimiter="\t")
        writer.writeheader()
        writer.writerows(toWrite)
        
    print('Complete')

def options(argv):
    """
    Instructions:
    python xml2prs.py source_file target_file
    """
    
    if len(argv) == 3:
        print(argv[1])
        if argv[1].endswith('.prs') and argv[2].endswith('.xml'):
            prs2xml(argv[1], argv[2])  
        elif argv[1].endswith('.xml') and argv[2].endswith('.prs'):
            xml2prs(argv[1], argv[2])
        else:
            print('Invalid filename extensions')
    else: 
        print(options.__doc__) 

if __name__=='__main__':
    options(sys.argv)
