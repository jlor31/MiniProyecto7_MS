#Juan Lorthiois
#Elder Guzman
#MiniProyecto 7

from tkinter import *
import time
import numpy as np


# Definiendo las funciones que componen el mecanismo de fuzzyficación
def f1(x):#Funcion representativa de 'poco' o 'leve'

    if (x<=10):

        return 1

    if (10<x<=25):

        return -x/15+(5/3)
    else:
        return 0

def f2(x): #Funcion representativa de 'promedio'

    if (10<x<25):

        return (1/15)*x -(2/3)

    if (25<=x<50):
        return (-1/25)*x + 2

    else:
        return 0

def f3(x): #Funcion representativa de 'mucho' o 'fuerte'

    if (25<= x < 50):

        return (1/25)*x -1
    if (x>=50):
        return 1
    else:
        return 0


def fuzzificar(d):  #Utilizando las funciones anteriores, establecemos la funcion para la fuzzificacion

    a,b,c = f1(d), f2(d), f3(d)

    return (np.round(a,2),np.round(b,2),np.round(c,2))

def desfuzzificar(tripla): #Esta funcion sirve para desfuzzificar y es literalmente el proceso inverso al anteiror

    a = tripla[0]
    b = tripla[1]
    c = tripla[2]

    if c == 0:

        if (a == 1):

            return 10
        else:
            return 15*(5/3 - a)

    else:

        if (c == 1):

            return 50

        else:
            return 25*(c+1)




def mover_jugador(tripla_fuzzy):  #Esta funcion se encarrga de mover el jugador basnadoase en la distanica a la que se encuetra de la pelota

    d = desfuzzificar(tripla_fuzzy)  #ingresa la distancia fuzzy y se desfuzzifica a una distancia azimuth en pixeles
    p = 0

    while p != d :
        p += 1
        coords_jugador = canvas.coords(jugador)  #obtener las coordenadas del jugador
        print(coords_jugador) #imprimir las coordenadas del jugador
        x_Vel_jugador = p / d * (canvas.coords(pelota)[0] - canvas.coords(jugador)[0])  #parametrizacion del desplazamiento que se le debe imponer al jugador en funcion de la distancia hasta la pelota
        y_Vel_jugador = p / d * (canvas.coords(pelota)[1] - canvas.coords(jugador)[1])


        canvas.move(jugador, x_Vel_jugador, y_Vel_jugador)  #mover el jugador
        window.update()
        time.sleep(0.05)

def mover_pelota(tripla_fuzzy):  #esta funcion procede de la misma manera que la otra pero mueve la pelota después de que el jugador la patee
    #La cantidad de pixeles que debe desplazarse la pelota depende de su distancia en pixeles de la porteria.

    d = desfuzzificar(tripla_fuzzy)
    p = 0  #parametro

    while p != d :
        p += 1
        x_Vel_pelota = p / d * (468 - canvas.coords(pelota)[0]) #Parametrizacion de la posicion de la pelota en funcion de la distancia
        y_Vel_pelota = p / d * (302 - canvas.coords(pelota)[1])

        canvas.move(pelota, x_Vel_pelota, y_Vel_pelota)
        window.update()
        time.sleep(0.02)



###### Graficas y animaciones de la simulacione


WIDTH = 468  #ancho del canvas
HEIGHT = 605  #Longitud



window = Tk()

canvas = Canvas(window, width = WIDTH, height= HEIGHT)  #crear el canvas

canvas.pack()

img_campo = PhotoImage(file='campo.png')  #agregar la imgen del campo de football
campo = canvas.create_image(0, 0, image=img_campo, anchor=NW)

img_jugador = PhotoImage(file='15x15.png')
jugador = canvas.create_image(np.random.randint(0,WIDTH), np.random.randint(0,HEIGHT), image=img_jugador, anchor=NW)  #jugador

img_pelota = PhotoImage(file='10x10.png')
pelota = canvas.create_image(np.random.randint(0,WIDTH), np.random.randint(0,HEIGHT), image=img_pelota, anchor=NW)  #pelota


d_pelota_porteria = np.round(np.linalg.norm(np.array([468, 302]) - np.array(canvas.coords(pelota))))  #Estimar la distnacia entre la pelota y la porteria en su formato CRISP (distancia euclidiana)


while d_pelota_porteria != 0:  #Correr al simulacion

    d_new = np.round(np.linalg.norm(np.array(canvas.coords(jugador)) - np.array(canvas.coords(pelota))))

    tripla_fuzzy = fuzzificar(d_new)  #conversion de CRISP a FUZZY

    mover_jugador(tripla_fuzzy)



    if (d_new == 0):  #Si el jugador esta sobre la pelota, entonces movemos la pelota

        d_pelota_porteria = np.round(np.linalg.norm(np.array([468, 302]) - np.array(canvas.coords(pelota))))
        tripla_fuzzy = fuzzificar(d_pelota_porteria)  #pasamos de CRISP a FUZZY la distancia entre la pelota y la porteria

        mover_pelota(tripla_fuzzy)


img_GOL = PhotoImage(file='GOOOL!.png')  # Cuando termina el programa porque la pelota llego a la portería se muestra un mensaje de GOOOL!
GOL = canvas.create_image(100, 100, image=img_GOL, anchor=NW)
print('GOOOOOOOOl!!!')





window.mainloop()

