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
    '1- reggae': (60, 90),
    '2- down-tempo': (70, 100),
    '3- chill-out': (90, 120),
    '4- hip-hop': (85, 115),
    '5- jazz and funk': (120, 125),
    '6- pop': (100, 130),
    '7- r&b': (60, 80),
    '8- rock': (110, 140),
    '9- metal': (100, 160)}




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
            "Track:", n, str(element),
            str1, ':', value[0], str2, ':', value[1])

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


    else:
        sys.exit(0)
sys.exit(0)
