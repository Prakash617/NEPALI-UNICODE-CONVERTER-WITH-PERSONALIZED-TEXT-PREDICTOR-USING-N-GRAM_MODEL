import re
w={ 
    'c':'क',
    'q':'क',
    'k':'क',
    'g':'ग',
    'x':'छ',
    'j':'ज',
    'z':'ज',
    'p':'प',
    'f':'फ',
    'v':'भ',
    'm':'म',
    'y':'य',
    'r':'र',
    'l':'ल',
    'w':'व',
    'h':'ह',
    
    'kh':'ख',
    'gh':'घ',
    'ch':'च',
    'jh':'झ',
    'ph':'फ',
    'bh':'भ',
    'sh':'श',
    'jn':'ज्ञ',
    'gy':'ज्ञ',
    
    'chh':'छ',
    'ksh':'क्ष',
    'gny':'ज्ञ',
    
    'b':'ब',
    's':'स',
    'sh':'श',
    'Sh':'ष',
    't':'ट',
    'T':'त',
    'Th':'थ',
    'th':'ठ',
    'd':'ड',
    'D':'द',
    'dh':'ढ',
    'Dh':'ध',
    'n':'न',
    'ng':'ङ',
    'yn':'ञ',
    'N':'ण'
  }

vo={
    'a':' ',
    'A':'ा',
    'aa':'ा',
    'i':'ि',
    'I':'ी',
    'ee':'ी',
    'u':'ु',
    'U':'ू',
    'oo':'ू',
    'e':'े',
    'ai':'ै',
    'o':'ो',
    'au':'ौ',
    '^':'ृ'
}

a={
    'a':'अ',
    'A':'आ',
    'aa':'आ',
    'i':'इ',
    'I':'ई',
    'ee':'ई',
    'u':'उ',
    'U':'ऊ',
    'oo':'ऊ',
    'e':'ए',
    'ai':'ऐ',
    'o':'ओ',
    'au':'औ',

    '\\':'्',
    '*':'ं',
    '**':'ँ',
    '|':'‍',
    '||':'‌',
    ':':'ः',
    '.':'।',
    '1':'१',
    '2':'२',
    '3':'३',
    '4':'४',
    '5':'५',
    '6':'६',
    '7':'७',
    '8': '८',
    '9':'९',
    '0':'०'
}

def choose(t):
    print(t)
    x=int(input("Sel Index: "))
    return t[x]

def select1(dic,unit):
    t=dic.get(unit)
    if isinstance(t,list): 
        return choose(t)
    else: return t

def select(unit,next_two_letters):
    v=select1(a,unit)
    l=0
    if not v:
        v=select1(w,unit)
        if v:
            if next_two_letters:
                t=select1(vo,next_two_letters)
                l=len(next_two_letters)
                nxt1=next_two_letters[:1]
                if not t and nxt1:
                    t=select1(vo,nxt1)
                    l=1

                if t:
                    if t==' ':t=''
                    v=v+t
                else:
                    v=v+'्'
                    l=0
    return v,l

def get_nepali(text):
    out=''
    while True:
        offset=3
        for i in range(3):
            t=text[:offset]
            if not t:break
            tt=select(t,text[offset:offset+2])
            if tt[0]: break
            offset-=1 
        if offset==0:
            text=text[1:]
            continue
        if not t: break
        text=text[offset+tt[1]:]
        out+=tt[0] if tt[0] else t
    return out

def lower_lowerables(text):
    v=[(m.start(0), m.end(0)) for m in re.finditer('(Sh)|A|T|(Th)|D|(Dh)|N|I|U', text)]
    t=''
    j=0
    for i in v:
        t=t+text[j:i[0]].lower()+text[i[0]:i[1]]
        j=i[1]
    t+=text[j:len(text)].lower()
    return t


def make_new_nepali(text):
    return([get_nepali(lower_lowerables(text))])


if __name__=='__main__':
    text='Gharoli'
    print(make_new_nepali(text))