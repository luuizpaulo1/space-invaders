from PPlay.window import *
from PPlay.sprite import *
from PPlay.gameimage import *
from PPlay.mouse import *
from PPlay.keyboard import *

def menu(): #MENU
    global janela
    global teclado 
    global fundo
    global clique
    global start
    global dificul
    global rking
    global exitt
    global pipi
    flag = True
   
    while True:
    
        if clique.is_over_object(start): #START
            #pipi.set_position(start.x -  50,start.y)
            if clique.is_button_pressed(1):
                jogo()
        
        if clique.is_over_object(dificul):#DIFICULDADE
            #pipi.set_position(dificul.x -  50,dificul.y)
            if clique.is_button_pressed(1):
                dificuldade()
        
        if clique.is_over_object(rking): #RANKING
            #pipi.set_position(rking.x -  50,rking.y)
            if clique.is_button_pressed(1):
                ranking()
        
        #if clique.is_over_object(exitt): 
            #pipi.set_position(exitt.x -  50,exitt.y)
        
        if clique.is_over_object(exitt) and clique.is_button_pressed(1): #SAI DO JOGO
            break
        
        if clique.is_over_object(start) or clique.is_over_object(dificul) or clique.is_over_object(rking) or clique.is_over_object(exitt): #aparece o negocinho do lado pra indicar o botao q vc vai apertar
            
            flag = False
        else:
            flag = True


        start.set_position((janela.width/2) - (start.width/2),100)
        dificul.set_position((janela.width/2) - (dificul.width/2),250)
        rking.set_position((janela.width/2) - (rking.width/2),400)
        exitt.set_position((janela.width/2) - (exitt.width/2),550)
    
        fundo.draw()
       # if flag == False: #SE O MOUSE ESTIVER SOBRE O BOTAO APARECE O SPRITE
            #pipi.draw()
        dificul.draw()
        rking.draw()
        exitt.draw()
        start.draw()
        janela.update()

def jogo(): #JOGO
    global janela
    global teclado 
    global fundo
    global clique
    janela1 = Window(700,700)
    while True:
        janela1.update()
    
        if teclado.key_pressed("q"):
            menu() 

        fundo.draw()
        janela1.update() 
    
    return 0
    
def ranking(): #RANKING
    
    global teclado 
    global fundo
    global clique
    janela4 = Window(700,700)
    while True:
        janela4.update()
        if teclado.key_pressed("q"):
            menu() 

        fundo.draw()
        janela4.update() 
    return 0

def dificuldade(): #DIFICULDADE
    
    global teclado 
    global fundo
    global clique
    global pipi
    facil = Sprite("FACIL.png")
    medio = Sprite("MEDIO.png")
    dificil = Sprite("DIFICIL.png")
    flag = True 
    janela2 = Window(700,700)
    
    while True:
        
        janela2.update()
        if teclado.key_pressed("q"): #sai do jogo
            menu()  
        
        if clique.is_over_object(facil): #muda a dificulade
           # pipi.set_position(facil.x - 50,facil.y)
            if clique.is_button_pressed(1):
                menu()
        
        if clique.is_over_object(medio): #muda a dificulade
            #pipi.set_position(medio.x - 50,medio.y)
            if clique.is_button_pressed(1):
                menu()
        
        if clique.is_over_object(dificil): #muda a dificulade
            #pipi.set_position(dificil.x - 50,dificil.y)
            if clique.is_button_pressed(1):
                menu()
        
        facil.set_position((janela.width/2) - (facil.width/2),200) #ajusta as posições
        medio.set_position((janela.width/2) - (medio.width/2),350)
        dificil.set_position((janela.width/2) - (dificil.width/2),500)

        if clique.is_over_object(facil) or clique.is_over_object(medio) or clique.is_over_object(dificil):
             flag = False
        else:
            flag = True

        fundo.draw()
        #if flag == False: #SE O MOUSE ESTIVER SOBRE O BOTAO APARECE O SPRITE
            #pipi.draw()
        facil.draw()
        medio.draw()
        dificil.draw()
        janela2.update()
    return 0

#MAIN


janela = Window(700,700)
teclado = Keyboard()
fundo = GameImage("espaço.png")
clique = Mouse()
start = Sprite("START.png")
dificul = Sprite("DIFICULDADE.png")
rking = Sprite("RANKING.png")
exitt = Sprite("SAIR.png")
pipi = Sprite("bicho.png")

menu()

