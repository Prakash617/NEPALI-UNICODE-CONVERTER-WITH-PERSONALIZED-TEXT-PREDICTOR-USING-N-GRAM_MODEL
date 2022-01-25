# from static_conversion import suggest

from english2nepali import get_possible_nepali
from user_map import get_user_suggestions
from rule_conversion import make_new_nepali
import json
with open(r'map\agantuk.json','r',encoding='utf-8') as f:
    agantuk=json.load(f)

def get_three_suggestions(word):
    user_defined_suggestions=get_user_suggestions(word.lower())
    pre_sugg = get_possible_nepali(word.lower())
    z=[i for i in pre_sugg] if pre_sugg else []
    z=user_defined_suggestions+[x for x in z if x not in user_defined_suggestions]
    if word in agantuk:
        agantuk[word][0]
        z.append(agantuk[word][0])
    if len(z)<3: 
        rsugg=make_new_nepali(word)[0]
        if rsugg not in z: z.append(rsugg)
       
    return z
    
if __name__=='__main__':
    print(get_three_suggestions('mayale'))