import json as J,os,sys,urllib.request as R,urllib.error as E
U=os.environ.get("MAKEFUN_ENV_URL") or sys.exit(1)
def P(p,b):
 q=R.Request(U+p,data=J.dumps(b).encode(),headers={"content-type":"application/json"})
 try:
  with R.urlopen(q) as x:return J.load(x)
 except E.HTTPError as e:sys.exit(1)
V=[0,100,320,330,500,900,20000]
NO=[-33,-31,-18,-14,14,18,31,33]
KO=[-17,-16,-15,-1,1,15,16,17]
BO=[-17,-15,15,17]
RO=[-16,-1,1,16]
def F(f):
 p=f.split();b=[0]*128;k=[0,0];r=7;n=0
 for c in p[0]:
  if c=="/":r-=1;n=0
  elif c.isdigit():n+=int(c)
  else:
   v="PNBRQKpnbrqk".index(c);v=v%6+1 if v<6 else -(v%6+1);s=r*16+n;b[s]=v
   if abs(v)==6:k[0 if v>0 else 1]=s
   n+=1
 t=1 if p[1]=="w" else -1;c=0
 if len(p)>2:
  c=("K" in p[2])*1+("Q" in p[2])*2+("k" in p[2])*4+("q" in p[2])*8
 e=-1
 if len(p)>3 and p[3]!="-":e=ord(p[3][0])-97+(int(p[3][1])-1)*16
 return [b,t,c,e,k]
def A(B,s,y):
 d=-16 if y>0 else 16
 for f in (-1,1):
  q=s+d+f
  if not q&0x88 and B[q]==y:return 1
 for o in NO:
  q=s+o
  if not q&0x88 and B[q]==y*2:return 1
 for o in KO:
  q=s+o
  if not q&0x88 and B[q]==y*6:return 1
 for O,Z in ((BO,(3,5)),(RO,(4,5))):
  for o in O:
   q=s+o
   while not q&0x88:
    v=B[q]
    if v:
     if v*y>0 and abs(v) in Z:return 1
     break
    q+=o
 return 0
def G(S,cap=0):
 B,t,c,e,k=S;O=[]
 for s in range(128):
  if s&0x88:continue
  v=B[s]
  if v*t<=0:continue
  a=abs(v)
  if a==1:
   d=16 if t>0 else -16;st=1 if t>0 else 6;la=6 if t>0 else 1;o=s+d
   if not o&0x88 and B[o]==0:
    if o>>4==la:
     for r in (5,4,3,2):O.append((s,o,r))
    else:
     O.append((s,o,0))
     if s>>4==st:
      w=s+2*d
      if B[w]==0:O.append((s,w,0))
   for f in (-1,1):
    q=s+d+f
    if q&0x88:continue
    w=B[q]
    if w*t<0 or q==e:
     if q>>4==la:
      for r in (5,4,3,2):O.append((s,q,r))
     else:O.append((s,q,0))
  elif a==2:
   for o in NO:
    q=s+o
    if not q&0x88 and B[q]*t<=0:O.append((s,q,0))
  elif a==6:
   for o in KO:
    q=s+o
    if not q&0x88 and B[q]*t<=0:O.append((s,q,0))
   if t>0 and s==4:
    if c&1 and B[5]==0 and B[6]==0 and B[7]==4 and not A(B,4,-1) and not A(B,5,-1) and not A(B,6,-1):O.append((4,6,0))
    if c&2 and B[3]==0 and B[2]==0 and B[1]==0 and B[0]==4 and not A(B,4,-1) and not A(B,3,-1) and not A(B,2,-1):O.append((4,2,0))
   elif t<0 and s==116:
    if c&4 and B[117]==0 and B[118]==0 and B[119]==4 and not A(B,116,1) and not A(B,117,1) and not A(B,118,1):O.append((116,118,0))
    if c&8 and B[115]==0 and B[114]==0 and B[113]==0 and B[112]==4 and not A(B,116,1) and not A(B,115,1) and not A(B,114,1):O.append((116,114,0))
  else:
   O2=BO if a==3 else RO if a==4 else BO+RO
   for o in O2:
    q=s+o
    while not q&0x88:
     w=B[q]
     if w==0:O.append((s,q,0))
     else:
      if w*t<0:O.append((s,q,0))
      break
     q+=o
 if cap:O=[m for m in O if B[m[1]]!=0 or m[1]==e]
 return O
def M(S,m):
 f,t,r=m;B=S[0];p=B[f];z=B[t];y=-1
 if abs(p)==1 and t==S[3] and z==0:
  y=t-(16 if S[1]>0 else -16);z=B[y];B[y]=0
 o=None
 if abs(p)==6 and abs(t-f)==2:
  o=(f+3,f+1) if t>f else (f-4,f-1);B[o[1]]=B[o[0]];B[o[0]]=0
 B[t]=r*S[1] if r else p;B[f]=0
 if abs(p)==6:S[4][0 if S[1]>0 else 1]=t
 C=S[2]
 if f==4 or t==4:S[2]&=~1
 if f==0 or t==0:S[2]&=~2
 if f==7 or t==7:S[2]&=~1
 if f==116 or t==116:S[2]&=~4
 if f==112 or t==112:S[2]&=~8
 if f==119 or t==119:S[2]&=~4
 X=S[3];S[3]=-1
 if abs(p)==1 and abs(t-f)==32:S[3]=(f+t)//2
 S[1]=-S[1]
 return (f,t,r,p,z,y,o,C,X)
def Z(S,u):
 f,t,r,p,z,y,o,C,X=u;B=S[0];S[1]=-S[1];S[3]=X;S[2]=C
 if o:B[o[0]]=B[o[1]];B[o[1]]=0
 B[f]=p;B[t]=0
 if y>=0:B[y]=z
 else:B[t]=z
 if abs(p)==6:S[4][0 if S[1]>0 else 1]=f
def L(S):
 O=[]
 for m in G(S):
  u=M(S,m)
  if not A(S[0],S[4][0 if S[1]<0 else 1],S[1]):O.append(m)
  Z(S,u)
 return O
def W(S):
 B=S[0];s=0;qn=0;mn=0
 for x in range(128):
  if x&0x88:continue
  v=B[x]
  if v:
   a=abs(v)
   if a==5:qn+=1
   elif a in (2,3):mn+=1
 eg=qn==0 or (qn==2 and mn<=2)
 for x in range(128):
  if x&0x88:continue
  v=B[x]
  if not v:continue
  a=abs(v);r=x>>4;n=x&7;i=r*8+n
  t=PT[a][i] if v>0 else PT[a][(7-r)*8+n]
  if a==6 and eg:t=KT[i] if v>0 else KT[(7-r)*8+n]
  s+=(V[a]+t) if v>0 else -(V[a]+t)
 wb=sum(1 for x in range(128) if not x&0x88 and B[x]==3)
 bb=sum(1 for x in range(128) if not x&0x88 and B[x]==-3)
 if wb>=2:s+=30
 if bb>=2:s-=30
 return s if S[1]>0 else -s
# piece-square tables (a1=0..h8=63), white perspective
PT={1:[0,0,0,0,0,0,0,0,5,10,10,-20,-20,10,10,5,5,-5,-10,0,0,-10,-5,5,0,0,0,20,20,0,0,0,5,5,10,25,25,10,5,5,10,10,20,30,30,20,10,10,50,50,50,50,50,50,50,50,0,0,0,0,0,0,0,0],2:[-50,-40,-30,-30,-30,-30,-40,-50,-40,-20,0,5,5,0,-20,-40,-30,5,10,15,15,10,5,-30,-30,0,15,20,20,15,0,-30,-30,5,15,20,20,15,5,-30,-30,0,10,15,15,10,0,-30,-40,-20,0,0,0,0,-20,-40,-50,-40,-30,-30,-30,-30,-40,-50],3:[-20,-10,-10,-10,-10,-10,-10,-20,-10,5,0,0,0,0,5,-10,-10,10,10,10,10,10,10,-10,-10,0,10,10,10,10,0,-10,-10,5,5,10,10,5,5,-10,-10,0,5,10,10,5,0,-10,-10,0,0,0,0,0,0,-10,-20,-10,-10,-10,-10,-10,-10,-20],4:[0,0,0,5,5,0,0,0,-5,0,0,0,0,0,0,-5,-5,0,0,0,0,0,0,-5,-5,0,0,0,0,0,0,-5,-5,0,0,0,0,0,0,-5,-5,0,0,0,0,0,0,-5,5,10,10,10,10,10,10,5,0,0,0,0,0,0,0,0],5:[-20,-10,-10,-5,-5,-10,-10,-20,-10,0,5,0,0,0,0,-10,-10,5,5,5,5,5,0,-10,0,0,5,5,5,5,0,-5,-5,0,5,5,5,5,0,-5,-10,0,5,5,5,5,0,-10,-10,0,0,0,0,0,0,-10,-20,-10,-10,-5,-5,-10,-10,-20],6:[20,30,10,0,0,10,30,20,20,20,0,0,0,0,20,20,-10,-20,-20,-20,-20,-20,-20,-10,-20,-30,-30,-40,-40,-30,-30,-20,-30,-40,-40,-50,-50,-40,-40,-30,-30,-40,-40,-50,-50,-40,-40,-30,-30,-40,-40,-50,-50,-40,-40,-30,20,30,10,0,0,10,30,20]}
KT=[-50,-30,-30,-30,-30,-30,-30,-50,-30,-30,0,0,0,0,-30,-30,-30,-10,20,30,30,20,-10,-30,-30,-10,30,40,40,30,-10,-30,-30,-10,30,40,40,30,-10,-30,-30,-10,20,30,30,20,-10,-30,-30,-30,0,0,0,0,-30,-30,-50,-30,-30,-30,-30,-30,-30,-50]
TT={};KI={};ND=[0];LM=[20000]
def O(S,mv,tm,pl):
 Z=[]
 for m in mv:
  s=0
  if m==tm:s=1000000
  else:
   v=S[0][m[1]]
   if v!=0 or m[1]==S[3]:s=10000+abs(v)*10-abs(S[0][m[0]])
   elif KI.get(pl)==m:s=5000
   elif m[2]:s=9000+m[2]
  Z.append((-s,m))
 Z.sort();return [m for _,m in Z]
def Q(S,al,be):
 ND[0]+=1
 if ND[0]>=LM[0]:return W(S)
 ck=A(S[0],S[4][0 if S[1]>0 else 1],-S[1])
 if ck:
  mv=L(S)
  if not mv:return -20000
  bs=-30000
  for m in O(S,mv,None,0):
   u=M(S,m);sc=-Q(S,-be,-al);Z(S,u)
   if sc>bs:bs=sc
   if sc>=be:return be
   if sc>al:al=sc
   if ND[0]>=LM[0]:break
  return al if bs==-30000 else max(al,bs)
 st=W(S)
 if st>=be:return be
 if st>al:al=st
 for m in O(S,G(S,1),None,0):
  u=M(S,m)
  if A(S[0],S[4][0 if S[1]<0 else 1],S[1]):Z(S,u);continue
  sc=-Q(S,-be,-al);Z(S,u)
  if sc>=be:return be
  if sc>al:al=sc
  if ND[0]>=LM[0]:break
 return al
def S_(S,d,al,be,pl):
 if d<=0:return Q(S,al,be)
 ND[0]+=1
 if ND[0]>=LM[0]:return W(S)
 mv=O(S,L(S),None,pl)
 if not mv:
  return -20000+pl if A(S[0],S[4][0 if S[1]>0 else 1],-S[1]) else 0
 bs=-30000;bm=mv[0];a=al
 for m in mv:
  u=M(S,m);sc=-S_(S,d-1,-be,-a,pl+1);Z(S,u)
  if sc>bs:bs=sc;bm=m
  if sc>a:a=sc
  if a>=be:
   if S[0][m[1]]==0:KI[pl]=m
   break
  if ND[0]>=LM[0]:break
 return bs
def BM(S,lg,nn):
 if not lg:return None
 ND[0]=0;LM[0]=nn;be=lg[0]
 for d in range(1,10):
  ND[0]=0
  best=-30000;bm=lg[0]
  for m in O(S,lg,None,0):
   u=M(S,m);sc=-S_(S,d-1,-30000,30000,1);Z(S,u)
   if sc>best:best=sc;bm=m
   if ND[0]>=nn:break
  be=bm
  if ND[0]>=nn:break
 return be
def C(m):
 return "abcdefgh"[m[0]&7]+str((m[0]>>4)+1)+"abcdefgh"[m[1]&7]+str((m[1]>>4)+1)+(" nbrq"[m[2]] if m[2] else "")
while True:
 g=P("/game",{})
 if g["status"]=="done":break
 while g["status"]=="your_move":
  S=F(g["fen"]);lg=L(S)
  if not lg:break
  g=P("/move",{"game":g["game"],"move":C(BM(S,lg,25000))})
 print("game",g["game"],g["outcome"],g["reason"],file=sys.stderr)
print("done",g.get("wins"),g.get("draws"),g.get("losses"),file=sys.stderr)
