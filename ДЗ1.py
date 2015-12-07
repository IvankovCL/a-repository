import re

g = []
rules = open('rules.csv', 'r', encoding = 'UTF-8')
for line in rules:
    g.append(line[0])
rules.close()

ipa = []
rules = open('rules.csv', 'r', encoding = 'UTF-8')
for l in rules:
    m = re.search("[a-zɛɔʒʁʃχʰ'ʼ]+", l)
    ipa.append(m.group(0))
rules.close()

gToIPA = ''
text = open('text.txt', 'r', encoding = 'UTF-8')
gText = text.read()
for symbol in gText:
    if symbol in g:
        for i in range(len(g)):
            if g[i] == symbol:
                m = ipa[i]
                gToIPA += m
    else:
        gToIPA += symbol 

IPAtext = open('IPAtext.txt', 'w', encoding = 'UTF-8')
IPAtext.write(gToIPA)
IPAtext.close()

print("Done.")
    
