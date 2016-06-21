import csv, re

def balanceSize(corp):
    balanced = []
    for line in corp:
        if 'none' not in line['words']:
            wordcount = int(line['words'])            
            if 'none' not in line['words'] and wordcount > 75000:    
                if wordcount > 100000:
                    oneThird = wordcount // 3
                    ratio = (oneThird, oneThird, wordcount - oneThird*2)
                else:
                    oneHalf = wordcount // 2
                    ratio = (oneHalf, wordcount - oneHalf)
                for i in ratio:
                    line['path'] = line['path'] + 'part'
                    line['words'] = i
                    balanced.append(line)
            else:
                balanced.append(line)
    return balanced

def balanceSphere(cor):
    line = ''
    balanced = []
    
    fiction = 0
    memoirs = 0
    science = 0
    journal = 0
    official = 0
    church = 0
    correspondence = 0
    tech = 0
    ads = 0
    
    for line in cor:       
        
        if 'художественная' in line['sphere']:
            fiction += int(line['words'])
            if fiction < 40000000:
                balanced.append(line)
        elif 'мемуары' in line['sphere']:
            memoirs += int(line['words'])
            if fiction < 11000000:
                balanced.append(line)
        elif 'учебно-научная' in line['sphere']:
            science += int(line['words'])
            if science < 12000000:
                balanced.append(line)
        elif 'публицистика' in line['sphere']:
            journal += int(line['words'])
            if journal < 29000000:
                balanced.append(line)
        elif 'официально-деловая' in line['sphere']:
            official += int(line['words'])
            if official < 1500000:
                balanced.append(line)
        elif 'церковно-богословская' in line['sphere']:
            church += int(line['words'])
            if church < 1500000:
                balanced.append(line)
        elif 'бытовая' in line['sphere'] or 'электронная' in line['sphere']:
            correspondence += int(line['words'])
            if correspondence < 3600000:
                balanced.append(line)
        elif 'техника|производство' in line['sphere']:
            tech += int(line['words'])
            if tech < 900000:
                balanced.append(line)
        elif 'реклама' in line['sphere']:
            ads += int(line['words'])
            if ads < 500000:
                balanced.append(line)
    return balanced         
        
if __name__ == '__main__':
    with open('source_post1950_wordcount.csv', 'r', encoding='windows-1251') as source:
        allTexts = csv.DictReader(source, delimiter=";")

        corpus = []
        for i, line in enumerate(allTexts):
            if re.search('[0-9]{4}', line['created']) != None:
                if int(re.search('[0-9]{4}', line['created']).group()) >= 1950: 
                    corpus.append(line)
                    
        corpus = balanceSize(corpus)
        corpus = balanceSphere(corpus)
        
        toWrite = []
        
        for entry in corpus:
            fields = {'path': entry['path'],
                      'author': entry['author'],
                      'sex': entry['sex'],
                      'birthday': entry['birthday'],
                      'header': entry['header'],
                      'created': entry['created'],
                      'sphere': entry['sphere'],
                      'genre_fi': entry['genre_fi'],
                      'type': entry['type'],
                      'topic': entry['topic'],
                      'chronotop': entry['chronotop'],
                      'style': entry['style'],
                      'audience_age': entry['audience_age'],
                      'audience_level': entry['audience_level'],
                      'audience_size': entry['audience_size'],
                      'source': entry['source'],
                      'publication': entry['publication'],
                      'publisher': entry['publisher'],
                      'publ_year': entry['publ_year'],
                      'medium': entry['medium'],
                      'subcorpus': entry['subcorpus'],
                      'tagging': entry['tagging'],
                      'words': entry['words']}
            toWrite.append(fields)
      

        with open('corpus1950.csv', 'w', encoding='utf-8') as newCorp:
            header = ('path','author','sex','birthday','header','created','sphere','genre_fi','type','topic','chronotop','style','audience_age',
                      'audience_level','audience_size','source','publication','publisher','publ_year','medium','subcorpus','tagging','words')
            writer = csv.DictWriter(newCorp, header, delimiter=";")
            writer.writeheader()
            writer.writerows(toWrite)
        print('Done')
