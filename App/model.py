"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as m
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import orderedmap as om
from DISClib.Algorithms.Sorting import shellsort as sa
import datetime
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos

def newAnalyzer():
    """ Inicializa el analizador

    Crea una lista vacia para guardar todos los crimenes
    Se crean indices (Maps) por los siguientes criterios:
    -Fechas

    Retorna el analizador inicializado.
    """
    analyzer = {'events': None,
                'dateIndex': None
                }

    analyzer['events'] = lt.newList('SINGLE_LINKED', compareIds)
    analyzer['dateIndex'] = om.newMap(omaptype='RBT',
                                      comparefunction=compareDates)                         
    return analyzer

# Funciones para agregar informacion al catalogo

def addEvent(analyzer, event):
    """
    """
    lt.addLast(analyzer['events'], event)
    updateDateIndex(analyzer['dateIndex'], event)
    return analyzer


# Funciones para creacion de datos

def updateDateIndex(map, event):
    """
    Se toma la fecha del evento y se busca si ya existe en el arbol
    dicha fecha.  Si es asi, se adiciona a su lista de eventos
    y se actualiza el indice de tipos de eventos.

    Si no se encuentra creado un nodo para esa fecha en el arbol
    se crea y se actualiza el indice de tipos de eventos
    """
    occurreddate = event['created_at']
    eventdate = datetime.datetime.strptime(occurreddate, '%Y-%m-%d %H:%M:%S')
    entry = om.get(map, eventdate.date())
    if entry is None:
        datentry = newDataEntry(event)
        om.put(map, eventdate.date(), datentry)
    else:
        datentry = me.getValue(entry)
    # addDateIndex(datentry, event)
    return map

# def addDateIndex(datentry, event):
#     """
#     Actualiza un indice de tipo de eventos.  Este indice tiene una lista
#     de eventos y una tabla de hash cuya llave es el tipo de crimen y
#     el valor es una lista con los eventos de dicho tipo en la fecha que
#     se está consultando (dada por el nodo del arbol)
#     """
#     lst = datentry['lstevents']
#     lt.addLast(lst, event)
#     track_id = datentry['trackID']
#     offentry = m.get(track_id, event['track_id'])
#     if (offentry is None):
#         entry = newOffenseEntry(event['track_id'], event)
#         lt.addLast(entry['lstoffenses'], event)
#         m.put(track_id, event['track_id'], entry)
#     else:
#         entry = me.getValue(offentry)
#         lt.addLast(entry['lstoffenses'], crime)
#     return datentry


def newDataEntry(event):
    """
    Crea una entrada en el indice por fechas, es decir en el arbol
    binario.
    """
    entry = {'trackID': None,
             'lstevents': None}
    entry['trackID'] = m.newMap(numelements=30,
                                     maptype='PROBING',
                                     comparefunction=compareIds)
    entry['lstevents'] = lt.newList('SINGLE_LINKED', compareDates)
    return entry

# Funciones de consulta

def eventsSize(analyzer):
    """
    Número de crimenes
    """
    return lt.size(analyzer['events'])


def indexHeight(analyzer):
    """
    Altura del arbol
    """
    return om.height(analyzer['dateIndex'])


def indexSize(analyzer):
    """
    Numero de elementos en el indice
    """
    return om.size(analyzer['dateIndex'])


def minKey(analyzer):
    """
    Llave mas pequena
    """
    return om.minKey(analyzer['dateIndex'])


def maxKey(analyzer):
    """
    Llave mas grande
    """
    return om.maxKey(analyzer['dateIndex'])

# Funciones utilizadas para comparar elementos dentro de una lista

# Funciones de ordenamiento

def compareIds(id1, id2):
    """
    Compara dos ids
    """
    if (int(id1) == int(id2)):
        return 0
    elif (int(id1) > int(id2)):
        return 1
    else:
        return -1


def compareDates(date1, date2):
    """
    Compara dos fechas
    """
    if (date1 == date2):
        return 0
    elif (date1 > date2):
        return 1
    else:
        return -1