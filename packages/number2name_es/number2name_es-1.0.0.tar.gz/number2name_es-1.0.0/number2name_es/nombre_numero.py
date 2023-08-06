# -*- coding: utf-8 -*-

__author__ = 'david'
import math
import os
import sys

class Nombre_Numero:

    "Almacena las caracteristicas de un numero"

    #numero
    #levels niveles
    #L_nr numero de caracteres
    #N_dicc numero por niveles
    #nombre nombre
    #Nom_levels nombres por nivel
    #Nom_value_level nombres de valor por nivel

    def __init__(self, numero):
        self.numero = numero
        self.N_dicc = {}
        self.nombre = {}
        self.Nom_levels = {}
        self.Nom_value_level={}
        self.Name_Total = ''
        self.get_names()
        
    def get_names(self):
        self.getLevels()
        self.getNum_by_level()
        self.getLevelNames()
        self.getValuesName()
        self.numero
        self.N_dicc
        self.Nom_levels
        self.Nom_value_level
        self.getName_Total()   

    def getLevels(self):
        self.str_nr = str(self.numero)
        self.L_nr = len(self.str_nr)
        self.levels = int(math.ceil(float(self.L_nr)/3))

    def getNum_by_level(self):
        levels = self.levels
        L_nr = self.L_nr
        N_dicc = {}
        for i in range(0,levels):
            a = L_nr -3*(i+1)
            b = L_nr - 3*i
            if ( a < 0):
                a = 0
            N_dicc.update({i:int(self.str_nr[a:b])})
        self.N_dicc.update(N_dicc)

    def getLevelNames(self):

        levels = self.levels

        if levels == 2:
            self.Nom_levels.update({1: "mil"})

        elif levels == 3:
            self.Nom_levels.update({1: "mil"})

            if   self.N_dicc[2] == 1:
                self.Nom_levels.update({2:"millón"})
            elif self.N_dicc[2] > 1:
                self.Nom_levels.update({2:"millones"})

        elif levels == 4:

            self.Nom_levels.update({1: "mil"})

            if   self.N_dicc[2] == 1:
                self.Nom_levels.update({2:"millón"})
            elif self.N_dicc[2] > 1:
                self.Nom_levels.update({2:"millones"})

            if   self.N_dicc[3] == 1:
                self.Nom_levels.update({3:"billón"})
            elif self.N_dicc[3] > 1:
                self.Nom_levels.update({3:"billones"})


    def getValuesName(self):
        #3 character value
        Numeric_Names = {
            0: 'cero',
            1: 'uno',
            2: 'dos',
            3: 'tres',
            4: 'cuatro',
            5: 'cinco',
            6: 'seis',
            7: 'siete',
            8: 'ocho',
            9: 'nueve',
            10: 'diez',
            11: 'once',
            12: 'doce',
            13: 'trece',
            14: 'catorce',
            15: 'quince',
            16: 'dieciseis',
            17: 'diecisiete',
            18: 'dieciocho',
            19: 'diecinueve',
            20: 'veinte',
            21: 'veintiuno',
            22: 'veintidos',
            23: 'veintitres',
            24: 'veinticuatro',
            25: 'veinticinco',
            26: 'veintiseis',
            27: 'veintisiete',
            28: 'veintiocho',
            29: 'veintinueve',
            30: 'treinta',
            40: 'cuarenta',
            50: 'cincuenta',
            60: 'sesenta',
            70: 'setenta',
            80: 'ochenta',
            90: 'noventa',
            100: 'ciento',
            200: 'doscientos',
            300: 'trescientos',
            400: 'cuatrocientos',
            500: 'quinientos',
            600: 'seiscientos',
            700: 'setecientos',
            800: 'ochocientos',
            900: 'novecientos',
        }
        Lv = self.levels
        for i in range(0,Lv):
            unidad = 0
            decena = 0
            centena = 0
            decena_unidad=0
            centenas=0
            nombre_centena_decena_unidad= ''
            str_nr_i=''
        #obtengo string de numero por nivel y lo giro
            str_nr_i = str(self.N_dicc[i])[::-1]
        #largo del string
            l_nr_i   = len(str_nr_i)
        #separar cada caracter
            for j in range(0,l_nr_i):
                if j == 0:
                    unidad = int(str_nr_i[0])
                elif j == 1:
                    decena = int(str_nr_i[1])
                elif j == 2:
                    centena = int(str_nr_i[2])
        #en caso de ser menor segundo caracter a 2
                decena_unidad = decena*10 + unidad
                centenas = centena*100
        #unir el segundo y tercero para obtener el nombre
            if  decena_unidad <= 30:
                nombre_decena_unidad = Numeric_Names[decena_unidad]
        #si es superior se une a un 0, para obtener la decenas
        #poner 'y' valor de unidad
            elif decena_unidad > 30:
                nombre_decena_unidad = Numeric_Names[int(decena)*10]+" y "+Numeric_Names[int(unidad)]
        #si existe primer caracter, ponerle 00 y obtener los cientos
        #luego juntar con valores de decenas
            #Centenas
            if centena == 0:
                nombre_centena_decena_unidad = nombre_decena_unidad
            elif centenas  == 100 and decena_unidad == 0:
                nombre_centena_decena_unidad = "cien"
        #retornar el nombre completo del valor
            elif centenas >= 100 and decena_unidad > 0:
                nombre_centena_decena_unidad = Numeric_Names[centenas]+" "+nombre_decena_unidad

        #Poner nombre a cada valor de nivel
            self.Nom_value_level.update({ i: nombre_centena_decena_unidad})

#Unificar los nombres, para nivel 1 si es 'uno' omitir
#si hay solo 'cero' en niveles inferiroes omitir

    def getName_Total(self):
        Lv = self.levels
        N_dicc = self.N_dicc
        Name_Level = self.Nom_levels
        Value_Name_Level = self.Nom_value_level
        Name_Total=''
        a_name = ''
        b_name = ''
        c_name = ''

        for i in range(0,Lv):
            if i == 0:
                if Lv == 1  and N_dicc[i] == 0:
                    a_name = Value_Name_Level[i]
                elif Lv > 1 and N_dicc[i] == 0:
                    a_name = ''
                elif Lv >= 1 and N_dicc[i] > 0:
                    a_name = Value_Name_Level[i]
                self.nombre.update({i:a_name})
            elif i == 1:
                if Lv >= 2 and N_dicc[i] == 0:
                    b_name = ''
                elif  Lv >= 2 and N_dicc[i] ==  1 :
                    b_name = Name_Level[i]
                elif   Lv >= 2 and N_dicc[i] >  1 :
                    b_name = Value_Name_Level[i]+" "+Name_Level[i]
                self.nombre.update({i:b_name})
            elif i >= 2:
                if Lv >= 3 and N_dicc[i] == 0 :
                    c_name = ''
                elif Lv >= 3 and N_dicc[i] ==  1 :
                    c_name = "un " + Name_Level[i]
                elif Lv >= 3  and N_dicc[i] >  1 :
                    c_name = Value_Name_Level[i]+" "+Name_Level[i]
                self.nombre.update({i:c_name})

        for j in list(reversed(list(self.nombre.keys()))):
            Name_Total += self.nombre[j]+" "
        self.Name_Total=Name_Total.rstrip()
        self.Name_Total=self.Name_Total[0].upper()+self.Name_Total[1:]