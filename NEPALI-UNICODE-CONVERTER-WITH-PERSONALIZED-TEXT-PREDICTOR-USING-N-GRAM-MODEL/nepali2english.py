vowel = {
    'अ':'a','आ':'a','इ':'i','ई':'i','उ':'u','ऊ':'u','ए':'ye','ऐ':'ai','ओ':'o','औ':'au','ऋ':'ri'
}

consonant = {
    'क':'k','ख':'kh','ग':'g','घ':'gh','ज':'j','झ':'jh','प':'p','फ':'ph','भ':'bh','म':'m','य':'y','र':'r','ल':'l','ह':'h','ज्ञ':'gy'
}

n = { 'न':'n','ङ':'n','ञ':'n','ण':'n'}

t={'ट':'t','त':'t'}
th={'ठ':'th','थ':'th'}

d={'ड':'d','द':'d'}
dh={'ढ':'dh','ध':'dh'}

s={'स':'s','श':'s','ष':'s'}
b={'ब':'b'}
w={'व':'b'}

ch={'च':'ch','छ':'chh'}
ksh={'क्ष':'ksh'}


def mergedict(*args):
    output = {}
    for arg in args:
        output.update(arg)
    return output


consonant=mergedict(consonant,n,t,th,d,dh,s,b,w,ch,ksh)

diacritic={'ा':'a','ि':'i', 'ी':'i', 'ु':'u', 'ू':'u',
 'े': 'e', 'ै':'ai', 'ो':'o', 'ौ':'au','ृ':'ri','ः':'ah'}

additive={'ं':'n','ँ':'n'}

def get_text_array(text):
    length=len(text)
    i=0
    text_arr=[]
    while (i<length):
        if text[i] in ("क","ज") and i+2 < length:
            if text[i:i+3] in ('ज्ञ','क्ष'):
                text_arr.append(text[i:i+3])
                i+=3
                continue
#         if text[i]!="ँ":pass
        text_arr+=text[i]
        i+=1
    return text_arr


def get_english(text):
    out=""
    text_arr = get_text_array(text)
    skip= True
    for letter in text_arr:
        if letter in (" ",",","!","।","-"):
            out+=letter
            skip= True
            continue
        if (not skip): 
                if letter in diacritic:
                    out+=diacritic[letter]
                    skip=True 
                    continue
                elif letter != '्':
                    out+='a'
                elif letter == '्':
                    skip=True
                    continue
        if  letter in consonant:
            out+=consonant[letter]
            if(skip): 
                skip=False

        elif letter in vowel:
            out+=vowel[letter]
            skip=True
        elif letter in additive:
            out+=additive[letter]
            skip=True
        else:
            out+=letter
    return out
        
