import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.widgets import Slider
import numpy as np
import math

from check_arg import *

def laplacien(i,j,tab,dx,dy):
    return((tab[i+1][j]+tab[i-1][j]-2*tab[i][j])/(dy**2)+(tab[i][j+1]+tab[i][j-1]-2*tab[i][j])/(dx**2))

def f(i,j,n,m):
    ii=i*1./(n-1)
    jj=j*1./(m-1)
    return(max(4*(jj*(jj-1.))*math.sin(ii*3*math.pi),0))

def main(n,m,mat,tm,dt,D,tauximage):
    t=0
    dx=1./n
    at=mat[-1]
    dy=1./m
    ci=0
    while t<tm:
        tab=np.copy(at)
        for i in range(1,n-1):
            for j in range (1,m-1):
                tab[i][j]=tab[i][j]+dt*(laplacien(i,j,at,dx,dy)/D)
        t=t+dt
        at=tab
        ci+=1
        if ci==tauximage:
            mat.append(tab)
            ci=0
    return(mat)

n=20
m=20
dt=10**(-5)
D=1
ns=5000
mati=np.zeros((n,m))
for i in range(n):
    for j in range(m):
        mati[i,j]=f(i,j,n,m)

print mati
res=main(n,m,[mati],ns*dt,dt,D,10)
print('calcul ok')
X = np.arange(0, n)
Y = np.arange(0, m)
X, Y = np.meshgrid(X, Y)
Z=res[0]
fig = plt.figure()

ax2=plt.axes([0.15, 0.05, 0.75, 0.03])
simage=Slider(ax2,'image',0.,1*len(res),valinit=0)

ax = fig.gca(projection='3d')
surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap='hot', linewidth=0, antialiased=False)
ax.set_zlim(-0.01, 1.01)
fig.colorbar(surf, shrink=0.5, aspect=5)

@check_arg(pause=False)
def update(val):
    im=int(simage.val)
    plt.cla()
    surf = ax.plot_surface(X, Y,res[im] , rstride=1, cstride=1, cmap='hot', linewidth=0, antialiased=False)
    ax.set_zlim(-0.01, 1.01)
    plt.draw()
    print('done')
#    fig.canvas.draw_idle()

simage.on_changed(update)
plt.show()
