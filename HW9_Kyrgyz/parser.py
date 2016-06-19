#загружает найденные аффиксы
def loadAffixes():
    with open('affixes.txt', 'r', encoding='utf-8') as affFile:
        affixes = []
        for affLine in affFile:
            affsInLine = affLine.split()
            affixes += affsInLine

        for affix in affixes:
            affix = affix.strip('\n')

        #сортирует в порядке убвания длины, чтобы находить самую длинную цепочку
        affixesSorted = []
        for i in reversed(sorted(affixes, key=len)):
            affixesSorted.append(i)

        return affixesSorted
        
if __name__ == '__main__':

    affixes = loadAffixes()
    
    with open('example.txt', 'r', encoding='utf-8') as example:
        words = []
        for line in example:
            wordsInLine = line.split()
            words += wordsInLine

        parsed = []
        for word in words:
            word = word.strip('«»,:;.!?\"\"\'\\()[]{}/><”')
            for affix in affixes:
                if word.endswith(affix):
                    stem = word.replace(affix, '')
                    parsed.append(stem+'+'+affix)
                    break

        with open('output.txt', 'w', encoding='utf-8') as output:
            for parsedOne in parsed:
                output.write(parsedOne+' ')
