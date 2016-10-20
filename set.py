import random
class Jeu_de_set():
    def __init__(self):
        self.paquet=[]

    def creer_paquet(self):
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    for l in range(3):
                        self.paquet.append((i,j,k,l))
        self.l=len(self.paquet)
        self.melanger()

    def tirer_carte(self,n):
        d=self.paquet[:n]
        self.paquet=self.paquet[n:]
        self.l=len(self.paquet)
        return d
    def is_a_set(self,l):
        r=False
        if len(l)==3:
            a,b,c=l
            r=True
            i=0
            while i< 4 and r:
                r= (r and ((a[i]+b[i]+c[i])% 3 ==0))
                i+=1
        return r

    def nb_set(self,l):
        n=len(l)
        nb_set=0
        ex=(0,0,0)
        for i in range(n-2):
            for j in range(i+1,n-1):
                for k in range(j+1,n):
                    if self.is_a_set((l[i],l[j],l[k])):
                        nb_set+=1
                        ex=(i,j,k)
        return nb_set,ex

    def melanger(self):
        for i in range(self.l):
            j=random.randrange(self.l)
            self.paquet[i],self.paquet[j]=self.paquet[j],self.paquet[i]

#nb=0
#for i in range (1000):
#    j=Jeu_de_set()
#    for k in range(6):
#        p=j.tirer_carte(12)
#        if j.nb_set(p)==0:
#            nb+=1
#print(nb)
#print(6000/(1.*nb))
