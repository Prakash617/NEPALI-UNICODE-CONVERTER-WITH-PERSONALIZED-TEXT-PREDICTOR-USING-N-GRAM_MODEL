import json
import re

with open(r'map\map.json') as mp:
    mapping = json.load(mp)

d={
    'aa':'a',
    'z':'j',
    'sh':'s',
    'f':'ph',
    'v':'bh',
    'ee':'i',
    'oo':'u',
    'w':'b'
}

def modify_for_mapping(text):
    v=[(m.start(0), m.end(0)) for m in re.finditer('(aa)|z|sh|f|v|(oo)|(ee)|(w)', text)]
    l=text[:]
    for i in v:
        key=text[i[0]:i[1]]
        l=l.replace(key,d[key],1)
    return l

with open(r'map\map_stop.json') as fi:
    kk = json.load(fi)

vv=mapping

t="|".join(i for i in sorted(list(kk.keys()),key=lambda x:len(x),reverse=True))

def get_possible_nepali(word):
    r =word
    g = vv.get(modify_for_mapping(word),None)
    if g: return [i[0] for i in g]
    for i in range(2):
        v=[(m.start(0), m.end(0)) for m in re.finditer(t, r)]
        mid=''
        if v and v[-1][1]==len(r):
            if len(v)>1 and r[v[-2][0]:v[-2][1]] in ('haru','antargat'):
                prefix = r[:v[-2][0]]
                mid=kk[r[v[-2][0]:v[-2][1]]][0][0]
            else:
                prefix = r[:v[-1][0]]
            suffix = r[v[-1][0]:]
#             print(prefix,mid,suffix)
            prefix_conv2=vv.get(modify_for_mapping(prefix),None)
            suffix_conv=kk[suffix]
            tmp1=[]
            tmp2=[]
            if prefix and prefix[-1]=='a' and prefix[-1]:
                prefix_conv1=vv.get(modify_for_mapping(prefix[:-1]),None)
                if prefix_conv1:
                    
                    for i in range(len(prefix_conv1)):
                        tmp1.append(prefix_conv1[i][0]+mid+suffix_conv[0][0])
            if prefix_conv2: 
                
                for i in range(len(prefix_conv2)):
                        tmp2.append(prefix_conv2[i][0]+mid+suffix_conv[0][0])
            tmp=tmp1+tmp2
            if tmp: return tmp
        g=vv.get(modify_for_mapping(r),None)
        if not g and r[-1]=='a':
            r=word[:-1]
            continue
        else:
            if g:
                tmp=[]
                for i in range(len(g)):
                    tmp.append(g[i][0])
                return tmp
            else: return g

if __name__=="__main__":
    print(get_possible_nepali('mayale'))
    print(vv.get('may'))