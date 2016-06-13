import pymysql, os, re

def createTables():
    
    """
    В качестве входных данных используются данные, полученные через VK API
    в виде шести csv-таблиц (в папке tables)
    """
    
    for d, dirs, files in os.walk('..\\tables'):
        for filename in files:
            table = filename.replace('.csv', '')
            path = os.path.join(d,filename)

            #читает файл
            lines = []  
            with open(path, 'r', encoding='utf8') as csv:                      
                for line in csv:
                    lines.append(line)

            """
            из первой строки файла берёт названия полей таблицы и
            определяет тип поля для вставки в строку CREATE TABLE
            и названия полей для вставки в строку INSERT
            """
            fields = ' '
            fieldsForInsert = ' '
            for field in lines[0].strip('\n').split('\t'):
                if re.search('^[0-9]$', field):
                    fieldType = 'int'
                else:
                    fieldType = 'varchar(255)'                        
                fields += '`'+field+'` '+ fieldType + ', '
                fieldsForInsert += '`'+field+'` ' + ', '                    
            fieldsForInsert = fieldsForInsert.strip(', ')

            create = 'CREATE TABLE `' + table + '` (' + fields + ' PRIMARY KEY (`uid`)  DEFAULT CHARSET = utf8);'
            cur.execute(create)

            #из остальных строк берёт значения полей для вставки в строку INSERT
            valuesForInsert = ''                
            for i in range(2, len(lines)):
                values = ('\' , \''.join(lines[i].strip('\n').split('\t')))
                values = '\'' + values + '\''
                valuesForInsert += '(' + str(values) + '), '                    
            valuesForInsert = valuesForInsert.strip(', ')
            
            insert = 'INSERT INTO `' + table + '` (' + fieldsForInsert + ') VALUES ' + valuesForInsert + ';'
            cur.execute(insert)

if __name__ == "__main__":                    
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 port=3306,
                                 password='',
                                 db='sys',
                                 charset='utf8',
                                 cursorclass=pymysql.cursors.DictCursor)
    cur = connection.cursor()
    createTables()
    connection.close()
