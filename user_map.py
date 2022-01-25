import json
import re
updated=0
usermap={}

def prepare(word):
    word = re.sub(r'[|]|\\', "",word)
    word = re.sub('\*\*|\*','n',word)
    word = re.sub('\^','ri',word)
    return word.lower()

def save_new_word(word,new_word):
    word=prepare(word)
    # h = modify_for_mapping(word)
    # z=mapping.get(h,None)

    global usermap
    # if not z:
    #     new_word=make_new_nepali(myword)[0]
    try:
        with open(r'map\user.json','r') as f:
            usermap=json.load(f)
    except FileNotFoundError:
        pass

    x=usermap.get(word)
    if x:
        if new_word not in x:
            x[new_word]=0
        x[new_word]+=1
        usermap[word]=x
    else:
        usermap[word]={new_word:1}
    with open(r'map\user.json','w') as f:   
        json.dump(usermap,f)
    
def get_user_suggestions(word):
    global usermap
    if not usermap:
        try:
            with open(r'map\user.json','r') as f:
                usermap=json.load(f)
        except FileNotFoundError:
            return []
    if usermap.get(word):
        return [i[0] for i in sorted(usermap.get(word).items(),key=lambda x: x[1],reverse=True)]
    else: return []

if __name__=='__main__':
    print(get_user_suggestions('mayale'))
    print(prepare(r'k^Shna'))