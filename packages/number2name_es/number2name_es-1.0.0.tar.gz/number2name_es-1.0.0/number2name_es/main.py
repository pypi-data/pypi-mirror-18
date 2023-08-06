# coding=utf-8
__author__ = 'david pineda'

import sys
from nombre_numero import *

"""
Este programa permite pasar un numero desde 0 a 999.999.999.999 a palabras

-Se ingresa un numero como entero

-Verificar que sea número

-Pasar Número a String

-Se obtiene el largo de carácteres para saber el nivel

-Cada nivel corresponde a una posición en un arreglo numero_nivel de tamaño # niveles obtenidas anteriormente

-Pasar numeros string a numeros valor (para eliminar 0 a la izquierda) a string

--Nivel 0: unidades->decenas->cientos
--Nivel 1: unidades->decenas->cientos | miles
--Nivel 2: unidades->decenas->cientos | millones
--Nivel 3: unidades->decenas->cientos | billones

Filtros de nivel

*Caso especial (En nivel 0) 0--> cero
*Caso especial si el numero es 1 en unidad -> se usa singular

-De cada nivel obtener la centena, la decena y la unidad.

--Ver caso de centena:
{
0: no se pone palabra y se analiza decena y unidad solamente
1: es 'cien' si decena=0 y unidad=0, si no es 'ciento'
2: es doscientos
3: es trescientos
4: es cuatrocientos
5: es quinientos
6: es seiscientos
7: es setecientos
8: es ochocientos
9: es novecientos
}
--Ver caso de decenas:
{
0: solo hay unidad
1: once, doce, trece ..... (dependiendo de la unidad)
2: veint{en unidad 0:e,1:iuno,2:idos,3:itres....}
3: treinta y ....
4: idem
5: idem
6: idem
7: idem
8: idem
9: idem
}

--Ver caso de unidad:
{
0: cero
1: uno
2: dos
3: tres_
4: cuatro
5: cinco
6: seis
7: siete
8: ocho
9: nueve
}

"""

#Poner entrada por línea de comando


while True:
    print("Ingresa tu número y te dire su nombre:")
    numero = sys.stdin.readline().rstrip('\n')
    print(numero.isdigit())
    if numero.isdigit():
        numero = int(numero)
        print("Es un número, procesaremos la cifra para entregarte el nombre")
        Num = Nombre_Numero(numero)
        Num.getLevels()
        Num.getNum_by_level()
        Num.getLevelNames()
        Num.getValuesName()
        Num.numero
        Num.N_dicc
        Num.Nom_levels
        Num.Nom_value_level
        Num.getName_Total()
        print(Num.Name_Total)

    else :
        print("No es un número, ingresa un valor que si lo sea")
