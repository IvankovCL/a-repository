import vk, time, os, re

def meta():
    with open('meta.csv', 'w', encoding='utf-8') as meta:
        meta.write('id'+'\t'+'sex'+'\t'+'bdate'+'\t'+'education'+'\t'+'occupation'+'\t'+'langs'+'\n')

def fetchPosts(people):
    for user in range(1,len(people)):
        uid = users[user]['uid']

        inf = api.users.get(user_ids = uid, fields = ['sex', 'bdate', 'education' 'occupation', 'personal'])

        if 'bdate' in inf[0] and re.search('[0-9]{4}', inf[0]['bdate']) != None:
            bdate = inf[0]['bdate'][-4:]
        else:
            bdate = 0
        if 'sex' in inf[0]:
            sex = inf[0]['sex']
        else:
            sex = ''
        if 'education' in inf[0]:
            education = inf[0]['education']['type']
        else:
            education = ''
        if 'occupation' in inf[0]:
            occupation = inf[0]['occupation']['type']
        else:
            occupation = ''
        if 'personal' in inf[0] and 'langs' in inf[0]['personal']:
            langs = inf[0]['personal']['langs']
        else:
            langs = ''   

        with open('meta.csv', 'a', encoding='utf-8') as metadata:
            metadata.write(str(uid)+'\t'+str(sex)+'\t'+str(bdate)+'\t'+str(education)+'\t'+str(occupation)+'\t'+str(langs)+'\n')

        wall = api.wall.get(owner_id=uid, count=100)

        for post in range(1,len(wall)):
            if wall[post]['post_type'] == 'post':
                if wall[post]['text']:
                    text = wall[post]['text']
                
                    os.makedirs('..\\HW5_API\\texts2\\'+str(bdate), exist_ok=True)

                    with open('..\\HW5_API\\texts2\\'+str(bdate)+'\\'+str(uid)+'.txt', 'a', encoding='utf8') as forPosts:
                        forPosts.write(text + '\n')
                        
        time.sleep(0.6)
        
if __name__ == "__main__":    
    meta()
    session = vk.Session(access_token='')
    api = vk.API(session)
    users = api.users.search(hometown="Щёкино", count=1000)
    fetchPosts(users)
