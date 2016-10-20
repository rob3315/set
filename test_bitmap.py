import Image
import Tkinter as Tk
import ImageTk
v=1
im=Image.new('1',(10,10))
def creer_image(n,e,r):
    l=[]
    for i in range(n):
        for j in range(n):
            if ((i+j)%n)<e:
                l.append(v)
            else:
                l.append(0)
    return l
def main():
    l=creer_image(10,4,5)
    #print(l)
    im.putdata(l)
    #print(list(im.getdata()))
    #return(ImageTk.BitmapImage(im))
main()
im.save('test.xbm')
