import os

for d, dirs, files in os.walk('C:\\search\\corpora'):
    for filename in files:
        path = os.path.join(d,filename)
        os.makedirs(d.replace('corpora', 'MyStemmed'), exist_ok = True)
        os.system('C:\\search\\mystem.exe -icd ' + path + ' ' + path.replace('.txt', '_MyStemmed.txt').replace('corpora', 'MyStemmed'))
        os.makedirs(d.replace('corpora', 'xml'), exist_ok = True)
        os.system('C:\\search\\mystem.exe -icd --format xml ' + path + ' ' + path.replace('.txt', '_MyStemmed.xml').replace('corpora', 'xml'))


