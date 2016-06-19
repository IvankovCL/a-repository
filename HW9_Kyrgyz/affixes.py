#отрезает от слова все возможные куски,
#среди них должна быть грамматичная цепочка аффиксов
def findVariants(words):
    variants = {}
    for i, word in enumerate(words): 
        if i < 300000: #иначе MemoryError        
            if len(word) > 2:
                for border in range(3,len(word)-1):
                    variant = word[border:]
                    if variant in variants:
                        variants[variant] += 1
                    else:
                        variants[variant] = 1

    with open('pseudos.txt', 'w', encoding='utf-8') as affFile:
        for variant in variants:
            #берёт самые частотные цепочки
            if variants[variant] > 100:
                affFile.write(variant + ' ' + str(variants[variant]) + '\n')
                
    return variants

#смотрит, чтобы предполагаемая цепочка аффиксов
#делилась на аффиксы из двух-трёх букв
def parse(aff, short):
    for border in range(3, len(aff)-1):            
        end = aff[-border:]
        begin = aff[:-border]    
        if end in short:
            if begin in short:                
                return True
            else:
                if parse(begin, short) == True:
                    return True
                else:
                    return False
                

def findAffixes(name):
    with open(name, 'r', encoding='utf-8') as affFile:
        mostLikely = []
        for line in affFile:
            mostLikely.append(line.split()[0].strip('\n'))       
        
        short = []
        fourletter = []
        long = []
        realAffixes = []
        #пытается разобрать длинные цепочки аффиксов
        for one in mostLikely:
            if len(one) > 1 and len(one) < 5:
                short.append(one)
                realAffixes.append(one)
            else:
                long.append(one)

        #добавляет все двух-трёхбуквенные
        one = ''
        for one in long:            
            if parse(one, short) == True:
                realAffixes.append(one)
                
        return realAffixes

              
if __name__ == '__main__':
    """
    Находит киргизские аффиксы
    """
    #берёт все слова из википедии
    tokens = [] 
    with open('words.txt', 'r', encoding='utf-8') as toRead:
        for line in toRead:
            tokens.append(line.strip('\n'))
            
    #оставляет уникальные
    tokens = set(tokens)

    pseudos = findVariants(tokens)

    affixes = findAffixes('pseudos.txt')
    
    with open('affixes.txt', 'w', encoding='utf-8') as affFile:
        for affix in affixes:
            affFile.write(affix+'\n')
