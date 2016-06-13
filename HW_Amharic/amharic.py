def getSyllables():
    with open('alphabet.csv', 'r', encoding='UTF-8') as alphabet:

        lines = []
        syllables = {}
        vowels = []
        cons = []
        
        for line in alphabet:
            lines.append(line.split())
        for i in range(6):
            vowels.append(lines[0][i])
        for j in range(33):
            cons.append(lines[j+1][0])
        for k in range(33):
            for m in range(6):
                syllables[lines[k+1][m+1]] = cons[k] + vowels[m]
    return syllables
            
def translit(syllabs):
    with open('text.txt', 'r', encoding='UTF-8') as input:
        text = input.read()

    textToIPA = ''
    for char in text:
        if char in syllabs:
            textToIPA += syllabs[char]
        else:
            textToIPA += char
        
    with open('output.txt', 'w', encoding='UTF-8') as output:
        output.write(textToIPA)

if __name__ == "__main__":    
    translit(getSyllables())
