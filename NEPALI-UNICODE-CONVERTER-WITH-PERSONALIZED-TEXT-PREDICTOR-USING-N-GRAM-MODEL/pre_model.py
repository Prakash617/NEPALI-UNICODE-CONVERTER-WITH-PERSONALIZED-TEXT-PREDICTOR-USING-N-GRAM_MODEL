import json
with open(r'map\pre_model.json','r',encoding='utf-8') as f:
    prediction_list_pre=json.load(f)

def pre_make(start):
    a=start.strip().split()
    l=len(a)
    l=l if l<5 else 4
    trunc=a[-4:]
    start=' '.join(trunc)
    # print(start)
    out=[]
    p = None
    while(not p and l>0):
        p=prediction_list_pre[l-1].get(start)
        l-=1
        trunc=trunc[1:]
        start=' '.join(trunc)
    if p:
        v=[n[0] for n in p]
        out=v  #select one of v  
     
    return out 

if __name__=="__main__":
    print(make('के हो यो के'))