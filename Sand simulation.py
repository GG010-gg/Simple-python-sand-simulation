"""
Il y a probablement des optimisations supplémentaires à effectuer.
Prévenez moi s'il y a des bugs.
En cas d'utilisation (peu probable), précisez la source initiale du code.
"""
import pygame as py
import random
py.init()
SizeX,SizeY=300,200
TPix=2
MAP=[[0 for j in range(SizeX)] for i in range(SizeY)]
MAPVAL=[[[(0,0,0),0,0] for j in range(SizeX)] for i in range(SizeY)]
#couleur, actif ?/ autre, je n'ai pas d'idée
#0: inactif 1 : actif
Actifs=[]
font=py.font.Font(None,15)
screen=py.display.set_mode((min(900,SizeX*TPix+200),min(600,SizeY*TPix+200)))
py.display.set_caption("pygame")
screen.fill((0,0,0))
py.draw.rect(screen,(150,150,150),(0,0,SizeX*TPix+20,SizeY*TPix+20))
py.draw.rect(screen,(0,0,0),(10,10,SizeX*TPix,SizeY*TPix))
running=True
clock=py.time.Clock();fps=0
Actu=[]
#initialiser les caractéristiques
Type=["Air","Sable","Eau","Fumée","Blocky"]
Poids=[0,1,0.5,0.4,10]#le blocky a un poids fort pour ne pas etre déplacé
col=[(0,0,0),(210,180,90),(0,0,200),(100,100,100),(0,255,255)]#couleur sans bruit
Act=[0,0,1,0,0]#si la particule peut etre désactivée, 0
#move sert à ne pas activer les particules non déplacables, car j'ai eu un bug avec le "blocky"
Move=[0,1,1,1,0]
Gravity=[0,1,1,-1,0]#sens de chute
SpawnT=2
Tspawn=2*int(SizeY/25)
def pr():
    #Actu contient toutes les coordonnées à actualiser. On ne scanne pas la grille, car trop lent
    for Px,Py in Actu:
        py.draw.rect(screen,MAPVAL[Py][Px][0],(10+Px*TPix,10+Py*TPix,TPix,TPix))
    #donner les indication : FPS/Nombre de particules traitées / Type de particules créée
    py.draw.rect(screen,(0,0,0),(SizeX*TPix+20,0,200,200))
    screen.blit(font.render(str(fps),True,(255,255,255)),(SizeX*TPix+30,5))
    screen.blit(font.render(str(len(Actifs)),True,(255,255,255)),(SizeX*TPix+30,25))
    screen.blit(font.render(Type[SpawnT],True,(255,255,255)),(SizeX*TPix+30,45))
    py.display.flip()
def simulate():
    #traiter toutes les particules actives.
    global Actifs
    Actu=[]
    for i,Pos in enumerate(Actifs):
        New=Pos
        Ax,Ay=Pos
        Mypoid=Poids[MAP[Ay][Ax]]
        Mygravit=Gravity[MAP[Ay][Ax]]
        #limY correspond à la valeur Y à ne pas dépasser, 0 pour la fumée (car on monte et les axes de notre grille ont le meme sens que notre fenetre, et SizeY-1 pour les autres
        limY=(SizeY-1)*int((Mygravit+1)/2)
        if Ay!=limY:
            #vérifier si peu descendre (monter pour la fumée)
            if Poids[MAP[Ay+Mygravit][Ax]]<Mypoid:
                New=(Ax,Ay+Mygravit)
            #si ne peut pas descendre et que son comportement correspond à celui du sable, regarde ses voisins du dessous/dessus
            elif MAP[New[1]][New[0]]!=2:
                if Ax!=SizeX-1:
                    if Poids[MAP[Ay+Mygravit][Ax+1]]<Mypoid:
                        New=(Ax+1,Ay+Mygravit)
                if Ax!=0:
                    if Poids[MAP[Ay+Mygravit][Ax-1]]<Mypoid:
                        New=(Ax-1,Ay+Mygravit)
        #si c'est de l'eau et que ce ne s'est pas déplacé verticalement, déplacement horizontal
        if New[0]==Ax and MAP[New[1]][New[0]]==2:
            w=2*round(random.random())-1
            #w transorme random() en -1 ou 1 , round(random()) renvoie 0 ou 1 et donc 2*(0 ou 1)-1 renvoie -1 ou 1
            if 0<=New[0]+w<=SizeX-1:
                if Poids[MAP[Ay][Ax+w]]<Mypoid:
                    New=(Ax+w,Ay)
        #New correspond à la nouvelle position
        if Pos!=New:
            #échanger les particules
            MAP[Ay][Ax],MAP[New[1]][New[0]]=MAP[New[1]][New[0]],MAP[Ay][Ax]
            MAPVAL[Ay][Ax],MAPVAL[New[1]][New[0]]=MAPVAL[New[1]][New[0]],MAPVAL[Ay][Ax]
            #changer, au besoin, les coordonnées de actifs
            if MAPVAL[Ay][Ax][1]==0:
                Actifs[i]=New
            #actualiser l'écran
            Actu.append(New)
            Actu.append((Ax,Ay))
            #tester si les particules du dessus/dessous peuvent etre activée
            if Ay!=SizeY-1-limY:
                if Move[MAP[Ay-Mygravit][Ax]]:
                    if MAPVAL[Ay-Mygravit][Ax][1]==0:Actifs.append((Ax,Ay-Mygravit));MAPVAL[Ay-Mygravit][Ax][1]=1
                if Ax>0:
                    if Move[MAP[Ay-Mygravit][Ax-1]]:
                        if MAPVAL[Ay-Mygravit][Ax-1][1]==0:Actifs.append((Ax-1,Ay-Mygravit));MAPVAL[Ay-Mygravit][Ax-1][1]=1
                if Ax<SizeX-1:
                    if Move[MAP[Ay-Mygravit][Ax+1]]:
                        if MAPVAL[Ay-Mygravit][Ax+1][1]==0:Actifs.append((Ax+1,Ay-Mygravit));MAPVAL[Ay-Mygravit][Ax+1][1]=1
        elif Act[MAP[Ay][Ax]]==0:
            #si ne bouge pas et est désacitvable
            if MAPVAL[Ay][Ax][1]==1:
                MAPVAL[Ay][Ax][1]=0
                #désactiver la particule
            Actu.append((Ax,Ay))
    Actifs=[(Ax,Ay) for Ax,Ay in Actifs if MAPVAL[Ay][Ax][1] or Act[MAP[Ay][Ax]]]
    return Actu
RUN=0
while running:
    if RUN:
        Actifs=sorted(Actifs,key=lambda p:p[1])
        Actifs.reverse()
        #trie les particules selon leur Y
        #pour une raison inconnue,  key=lambda p:0-p[1], qui est censé remplacer le .reverse(), donne un mauvais résultat. Essayez.
        Actu=simulate()
    xs,ys=py.mouse.get_pos()
    #actualiser la grille
    pr()
    fps=int(clock.get_fps())
    for event in py.event.get():
        if event.type==py.QUIT:running=False
        #modifier le type de particule à placer, si touche 5 pressée, mettre pause/run
        if event.type==py.KEYDOWN:
            for i in range(len(Type)):
                if event.unicode==str(i):SpawnT=i
            if event.unicode==str(len(Type)):RUN=1-RUN
    #ajouter les particules
    if py.mouse.get_pressed()[0]:
        #trouver les coordonnées de placement dans la grille
        xs-=Tspawn;ys-=Tspawn
        Nx,Ny=int((xs-10)//TPix),int((ys-10)//TPix)
        xspawn=max(min(Nx,SizeX-Tspawn),0)
        yspawn=max(min(Ny,SizeY-Tspawn),0)
        if 0<xs<10+SizeX*TPix and 0<ys<10+SizeY*TPix:
            #scanne le carré de placement
            for dx in range(Tspawn):
                for dy in range(Tspawn):
                    #vérifie si doit activer les particules au dessus de nous
                    #bancal mais marche aussi pour la fumée
                    if yspawn+dy!=0:
                        if Move[MAP[yspawn+dy-1][xspawn+dx]]:
                            if MAPVAL[yspawn+dy-1][xspawn+dx][1]==0:Actifs.append((xspawn+dx,yspawn+dy-1));MAPVAL[yspawn+dy-1][xspawn+dx][1]=1
                        if xspawn+dx>0:
                            if Move[MAP[yspawn+dy-1][xspawn+dx-1]]:
                                if MAPVAL[yspawn+dy-1][xspawn+dx-1][1]==0:Actifs.append((xspawn+dx-1,yspawn+dy-1));MAPVAL[yspawn+dy-1][xspawn+dx-1][1]=1
                        if xspawn+dx<SizeX-1:
                            if Move[MAP[yspawn+dy-1][xspawn+dx+1]]:
                                if MAPVAL[yspawn+dy-1][xspawn+dx+1][1]==0 and Move[MAP[yspawn+dy-1][xspawn+dx+1]]==1:Actifs.append((xspawn+dx+1,yspawn+dy-1));MAPVAL[yspawn+dy-1][xspawn+dx+1][1]=1
                    #ajoute les particules si elles sont différentes de celles de la grille, car sinon rend un grésillement
                    if MAP[yspawn+dy][dx+xspawn]!=SpawnT:
                        MAP[yspawn+dy][dx+xspawn]=SpawnT
                        if Move[SpawnT]:
                            #si l'ancienne particule était active, il ne faut pas ajouter ses coordonnées une deuxième fois dans Actifs
                            if MAPVAL[yspawn+dy][xspawn+dx][1]==0:
                                Actifs.append((xspawn+dx,yspawn+dy))
                            #choisir le bruit de la couleur si est activable (eau, sable, fumée)
                            c=col[SpawnT]
                            mod=random.randint(-50,50)
                            C=tuple([max(0,min(c[i]+mod+random.randint(-10,10),255)) for i in range(3)])
                            MAPVAL[yspawn+dy][dx+xspawn]=[C,Move[SpawnT],(0,0)]
                        else:
                            C=col[SpawnT]
                            MAPVAL[yspawn+dy][dx+xspawn]=[C,Move[SpawnT],(0,0)]
                        #actualiser comme ca si pause on voit les modifications
                        py.draw.rect(screen,C,(10+(xspawn+dx)*TPix,10+(yspawn+dy)*TPix,TPix,TPix))
    clock.tick(60)
py.quit()