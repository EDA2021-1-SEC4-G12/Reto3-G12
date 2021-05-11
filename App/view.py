"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
import sys
import controller
from DISClib.ADT import list as lt
assert cf
import os
import random
from DISClib.ADT import map as mp
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me

"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

analyzer = None

events_analysis_file = 'context_content_features-small.csv'
sentiment_values = 'sentiment_values.csv'
hashtag_file = 'user_track_hashtag_timestamp-small.csv'

genre = {
    'reggae': (60, 90),
    'down-tempo': (70, 100),
    'chill-out': (90, 120),
    'hip-hop': (85, 115),
    'jazz and funk': (120, 125),
    'pop': (100, 130),
    'r&b': (60, 80),
    'rock': (110, 140),
    'metal': (100, 160)}




def printMenu():
    print("Bienvenido")
    print("1- Inizializar y Cargar información en el catálogo ")
    print("2- Conocer Reproducciones con una característica específica de contenido y un rango determinado")
    print("3- Encontrar música para festejar")
    print("4- Encontrar música para estudiar")
    print("5- Encontrar música por género")
    print("6- Encontrar género más escuchado en un tiempo dado")
    print("7- Salir")
cont = None

def printRandom5(mapa, str1, str2):
    '''
    Imprime 5 eventos random dentro del mapa
    '''
    lista = mp.keySet(mapa)
    listsize = lt.size(lista)
    sample = random.sample(range(listsize), 5)
    n = 0
    for num in sample:
        n += 1
        element = lt.getElement(lista, num)
        thing = mp.get(mapa, element)
        value = me.getValue(thing)
        print(
            "Track ", n, ':', str(element),
            str1, ':', value[0], str2, ':', value[1])

def print10Artists(mapa, genero):
    '''
    Imprime primeros 10 artistas dentro del mapa
    '''
    lista = mp.keySet(mapa)
    n = 0
    print('--- Algunos artistas para ' + genero + ' ---')
    for num in range(10):
        n += 1
        element = lt.getElement(lista, num)
        thing = mp.get(mapa, element)
        value = me.getValue(thing)
        print(
            "Artist", n, ':', str(element))


        
def printTopGenres(mapa):
    '''
    '''
    n = 0
    print('================= ' + 'GENEROS ORDENADOS POR REPRODUCCIONES' + ' =================')
    for elems in mapa:
        n += 1
        print(
            "TOP", n, ': ', str(elems[0]) + ' con ' + str(elems[1]) + ' reproducciones')


"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')

    if int(inputs[0]) == 1:
        analyzer = controller.init()
        print("Cargando información de los archivos ....")
        answer = controller.loadData(
            analyzer, events_analysis_file, hashtag_file, sentiment_values)
        print('Registro de eventos Cargados: ' + str(controller.eventsSize(
            analyzer)))
        print('Artistas únicos Cargados: ' + str(controller.artistsSize(
            analyzer)))
        print('Pistas únicas Cargados: ' + str(controller.tracksSize(
            analyzer)))
              
        print('\n')
        print(
            "Tiempo [ms]: ",
            f"{answer[0]:.3f}", "  ||  ",
            "Memoria [kB]: ",
            f"{answer[1]:.3f}")
        

    elif int(inputs[0]) == 2:
        criteria = input("Ingrese el criterio a evaluar: ")
        initial = float(input("Ingrese el límite inferior: "))
        final = float(input("Ingrese el límite superior: "))
        print("Buscando en la base de datos ....")
        result = controller.getEventsByRange(
            analyzer, criteria, initial, final)
        print('Registro de eventos Cargados: ' + str(result[0][0]))
        print('Artistas únicos Cargados: ' + str(result[0][1]))
        print(
            "Tiempo [ms]: ",
            f"{result[1]:.3f}", "  ||  ",
            "Memoria [kB]: ",
            f"{result[2]:.3f}")


    elif int(inputs[0]) == 3:
        initialenergy = float(input(
            "Ingrese el límite inferior para la energía: "))
        finalenergy = float(input(
            "Ingrese el límite superior para la energía: "))
        energyrange = (initialenergy, finalenergy)
        initialdanceability = float(input(
            "Ingrese el límite inferior para la capacidad de baile: "))
        finaldanceability = float(input(
            "Ingrese el límite superior para la capacidad de baile: "))
        danceabilityrange = (initialdanceability, finaldanceability)
        print("Buscando en la base de datos ....")
        result = controller.getMusicToParty(
            analyzer, energyrange, danceabilityrange)
        print('Artistas únicos Cargados:', str(result[0][0]))
        print('Tracks únicas Cargadas:', str(result[0][1]))
        printRandom5(result[0][2], 'energy', 'danceability')
        print(
            "Tiempo [ms]: ",
            f"{result[1]:.3f}", "  ||  ",
            "Memoria [kB]: ",
            f"{result[2]:.3f}")


    elif int(inputs[0]) == 4:
        initialinstrumentalness = float(input(
            "Ingrese el límite inferior para la instrumentalidad: "))
        finalinstrumentalness = float(input(
            "Ingrese el límite superior para la instrumentalidad: "))
        instrumentalnessrange = (initialinstrumentalness, finalinstrumentalness)
        initialtempo = float(input(
            "Ingrese el límite inferior para el tempo: "))
        finaltempo = float(input(
            "Ingrese el límite superior para el tempo: "))
        temporange = (initialtempo, finaltempo)
        print("Buscando en la base de datos ....")
        result = controller.getMusicToStudy(
            analyzer, instrumentalnessrange, temporange)
        print('Artistas únicos Cargados:', str(result[0][0]))
        print('Tracks únicas Cargadas:', str(result[0][1]))
        printRandom5(result[0][2], 'instrumentalness', 'tempo')
        print(
            "Tiempo [ms]: ",
            f"{result[1]:.3f}", "  ||  ",
            "Memoria [kB]: ",
            f"{result[2]:.3f}")


    elif int(inputs[0]) == 5:
        ifadd = int(input(
            "Especifique si quiere añadir un nuevo genero músical (1=Sí, 0=No) : "))
        while ifadd == 1:
            addgenre = str(input(
                "Ingrese el nombre del genero : "))
            addLoTempo = float(input(
                    "Ingrese el límite inferior para el tempo : "))
            addHiTempo = float(input(
                    "Ingrese el límite superior para el tempo : "))
            if genre.has_key(addgenre.lower()):
                print('Este genero ya está creado')
            else:
                genre[addgenre] = (addLoTempo, addHiTempo)
                print('Genero musical ' + addgenre + ' añadido.')
            ifadd = int(input(
                "Especifique si quiere añadir un nuevo genero músical (1=Sí, 0=No) : "))

        genre_list = str(input(
            "Especifique los generos musicales que desea buscar, separados con coma (sin espacios) : "))
        genre_list = genre_list.lower()
        genre_list = genre_list.split(',')
        total_e = 0
        for genre_i in genre_list:
            bounds_i = genre[genre_i]
            result = controller.getEventsByRange(
                    analyzer, 'tempo', bounds_i[0], bounds_i[1])
            total_e += result[0][0]
            print('\n========== ' + str(genre_i.upper()) + ' ==========')
            print('El tempo de ' + str(genre_i) + ' esta entre ' + str(bounds_i[0]) + ' y ' + str(bounds_i[1]) + ' BPM')
            print('Registro de eventos Cargados: ' + str(result[0][0]))
            print('Artistas únicos Cargados: ' + str(result[0][1]))
            print10Artists(result[0][4], genre_i)
            print(
                "Tiempo [ms]: ",
                f"{result[1]:.3f}", "  ||  ",
                "Memoria [kB]: ",
                f"{result[2]:.3f}")

        print('\nTotal de reproducciones: ' + str(total_e))


    elif int(inputs[0]) == 6:

        lo_time = str(input(
                "Ingrese el límite inferior para el tiempo : "))
        hi_time = str(input(
                "Ingrese el límite superior para el tiempo : "))

        hi_time_sec = hi_time.split(':'); hi_time_sec = int(hi_time_sec[0])*3600 + int(hi_time_sec[1])*60 + int(hi_time_sec[2])
        lo_time_sec = lo_time.split(':'); lo_time_sec = int(lo_time_sec[0])*3600 + int(lo_time_sec[1])*60 + int(lo_time_sec[2])
        
        dict_genres_reps = {}
        total_e = 0
        for genre_i in genre.keys():
            bounds_i = genre[genre_i]
            result = controller.getEventsByTimeRangeGenre(
                    analyzer, bounds_i, (lo_time_sec,hi_time_sec))
            total_e += result[2]
            dict_genres_reps[genre_i] = result[2]
        
        sorted_genred_reps = sorted(dict_genres_reps.items(), key=lambda x: x[1], reverse=True)
        printTopGenres(sorted_genred_reps)
        print('----------------------------------------------------------')
        print('\nTotal de reproducciones entre {} y {}: {}'.format(lo_time,hi_time,total_e))
        top_k, top_v = sorted_genred_reps[0][0], sorted_genred_reps[0][1]
        # top_k, top_v = list(sorted_genred_reps.keys()), list(sorted_genred_reps.values())
        print('El genero TOP es {} con {} reproducciones...'.forma(top_k, top_v))



            
        #     print('El tempo de ' + str(genre_i) + ' esta entre ' + str(bounds_i[0]) + ' y ' + str(bounds_i[1]) + ' BPM')
        #     print('Registro de eventos Cargados: ' + str(result[0][0]))
        #     print('Artistas únicos Cargados: ' + str(result[0][1]))
        #     print10Artists(result[0][4], genre_i)
        #     print(
        #         "Tiempo [ms]: ",
        #         f"{result[1]:.3f}", "  ||  ",
        #         "Memoria [kB]: ",
        #         f"{result[2]:.3f}")

        # print('\nTotal de reproducciones: ' + str(total_e))


    else:
        sys.exit(0)
sys.exit(0)
