from Tkinter import *
from random import randrange
import set
class Carte(Frame):
    def __init__(self,fen,val,largeur,hauteur,maincolor,id,**kwargs):
        Frame.__init__(self,fen,width=largeur,height=hauteur)
        self.val=val
        self.id=id
        self.maincolor=maincolor
        self.height=hauteur
        self.width=largeur
        self.canvas=Canvas(self,width=largeur,height=hauteur,bg=self.maincolor,**kwargs)
        self.figure=self.dessin()
        self.canvas.pack()

    def dessin(self):
        couleur=['red','purple','green']
        forme=[self.losange,self.ovale,self.vague]
        remplissage=self.get_remplissage(couleur[self.val[0]])
        x= int(self.width/2)
        y=int(self.height/6)
        if self.val[3]==0:
            return(forme[self.val[1]]((x,3*y),x-10,y-10,**remplissage),)
        elif self.val[3]==1:
            return(forme[self.val[1]]((x,2*y),x-10,y-10,**remplissage),forme[self.val[1]]((x,4*y),x-10,y-10,**remplissage))
        else:
            return(forme[self.val[1]]((x,1*y),x-10,y-10,**remplissage),forme[self.val[1]]((x,3*y),x-10,y-10,**remplissage),forme[self.val[1]]((x,5*y),x-10,y-10,**remplissage))

    def get_remplissage(self,color):
        dic=[{'fill':color,'outline':''},{'outline':color,'fill':self.maincolor,'width':4},{'stipple':'@test.xbm','outline':color,'fill':color}]
        return dic[self.val[2]]

    def losange(self,c,lar,haut,**remplissage):
        """trace un losange centre en c de demi largeur,demi hauteur et couleur donne"""
        x,y=c
        los=self.canvas.create_polygon(x-lar,y,x,y+haut,x+lar,y,x,y-haut,**remplissage)
        return los

    def ovale(self,c,lar,haut,**remplissage):
        x,y=c
        ov=self.canvas.create_oval(x-lar,y-haut,x+lar,y+haut,**remplissage)
        return ov

    def vague(self,c,lar,haut,**remplissage):
        x,y=c
        l1=int(1./3.*lar)
        h1=int(haut/2)
        vague= self.canvas.create_polygon(x-lar,y+h1,x-l1,y+haut,x+l1,y,x+lar,y+h1,x+lar,y-h1,x+l1,y-haut,x-l1,y,x-lar,y-h1,smooth=1,**remplissage)
        return vague
    def redimensionne(self):
        self.canvas.configure(width=self.width)
        self.update()
    def update(self):
        self.canvas.delete('all')
        self.canvas.configure(bg=self.maincolor)
        self.figure=self.dessin()
        self.canvas.update()

class Fenetre(Tk):
    def __init__(self,maincolor):
        Tk.__init__(self)
        self.w=self.winfo_screenwidth()-10
        self.jeu=set.Jeu_de_set()
        self.h=self.winfo_screenheight()-100
        self.maincolor=maincolor
        self.lst_cart=[]
        self.selected=[]
        self.nbh=0 #nombre d'aide demande
        self.title("jeu de set")
    def link_everyone(self):
        self.button_help=Button(self,text='aide',command=self.help)
        self.button_help.grid(row=3,column=0)
        self.button_update=Button(self,text='update',command=self.update)
        self.button_update.grid(row=3,column=1)
        self.label=Label(self )
        self.det_nb_set()
        self.label.grid(row=3,column=2)
        self.bind('<1>',self.select)
        self.bind('<3>',self.deselect)
        self.bind('h',self.helpb)
        self.bind('u',self.updateb)

    def is_a_set(self):
        l=map( lambda x : self.id_to_card(x),self.selected)
        #if self.jeu.is_a_set(map(lambda x: x.val,l)):
    def update(self):
        for c in self.lst_cart:
            c.canvas.configure(bg=self.maincolor)
            c.canvas.update()
        self.selected=[]
        self.nbh=0

    def updateb(self,event):
        self.update()

    def help(self):
        if self.nbh>2:
            print('vous vous moquez du monde')
            self.nbh=0
        else:
            i=self.ex[self.nbh]
            (self.lst_cart)[i].canvas.configure(bg='yellow')
            (self.lst_cart)[i].canvas.update()
            self.nbh+=1
    def helpb(self,event):
        """appel help sans l'event"""
        self.help()
    def add(self,event):
        self.no_set()
    def no_set(self):
        pass
    def det_nb_set(self):
        self.nb_set,self.ex=self.jeu.nb_set(map(lambda x : x.val, self.lst_cart))
        self.label.configure(text=('il y a %d sets')% (self.nb_set))
        self.label.update()
        if self.nb_set==0:
            self.no_set()

    def select(self,event):
        if len(self.selected)<3 and (event.widget.master.__class__.__name__=="Carte") and (event.widget.master.id not in self.selected ):
            event.widget.configure(bg='blue')
            self.selected.append(event.widget.master.id)
            self.is_a_set()
        else :
            pass

    def deselect(self,event):
        for k in range(len(self.selected)):
            if (self.selected)[k] == event.widget.master.id:
                event.widget.configure(bg=self.maincolor)
                event.widget.update()
                del (self.selected)[k]
                break

class Game(Fenetre):
    def __init__(self,maincolor):
        Fenetre.__init__(self,maincolor)
        self.start_game()

    def start_game(self):
        self.jeu.creer_paquet()
        l=self.jeu.tirer_carte(12)
        for j in range(4):
            for i in range(3):
                c=Carte(self,l[i+3*j],self.w/4,self.h/3,maincolor,(i,j))
                self.lst_cart.append(c)
                c.grid(row=i, column=j)
        self.bind('a',self.add)
        self.link_everyone()

    def is_a_set(self):
        l=map( lambda x : self.id_to_card(x),self.selected)
        if self.jeu.is_a_set(map(lambda x: x.val,l)):
            if len(self.lst_cart)==12:
                nv_val=self.jeu.tirer_carte(3)
                for i in range(3):
                    l[i].val=nv_val[i]
                    l[i].update()
            else:
                n=len(self.lst_cart)/3 -1 # nb de colonnes -1
                for ii in range(3):
                    i,j=l[ii].id
                    self.lst_cart[i+3*j],self.lst_cart[ii+3*n]=self.lst_cart[ii+3*n], self.lst_cart[i+3*j]# on transfert les cartes de place
                    (self.lst_cart)[i+3*j].id=(i,j)
                    (self.lst_cart)[ii+3*n].id=(ii,n)
                for ii in range(3):
                    l[ii].destroy()
                    del self.lst_cart[-1]
                for j in range(n):
                    for i in range(3):
                        (self.lst_cart)[i+3*j].width=self.w/n
                        (self.lst_cart)[i+3*j].redimensionne()
                        (self.lst_cart)[i+3*j].grid(row=i,column=j)
            self.selected=[]
            self.nbh=0
            self.det_nb_set()
    def no_set(self):
        """ajoute une colonne et redimensionne tout"""
        nv_val=self.jeu.tirer_carte(3)
        n=1+ len(self.lst_cart)/3
        for c in self.lst_cart:
            c.width=self.w/n
            c.redimensionne()
        for i in range(3):
            c=Carte(self,nv_val[i],self.w/n,self.h/3,self.maincolor,(i,n-1))
            self.lst_cart.append(c)
            c.grid(row=i,column=n)
        self.det_nb_set()
    def id_to_card(self,id):
        i,j=id
        return self.lst_cart[i+3*j]







maincolor='white'
fen1=Game(maincolor)
fen1.mainloop()
