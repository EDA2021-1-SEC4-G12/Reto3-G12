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
from DISClib.ADT import map as mp
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
                'artistIDs': None,
                'trackIDs': None,
                }

    analyzer['events'] = lt.newList('SINGLE_LINKED', compareDates)
    analyzer['artistIDs'] = om.newMap(omaptype='RBT',
                                      comparefunction=compareIds)
    analyzer['trackIDs'] = om.newMap(omaptype='RBT',
                                      comparefunction=compareIds)                         
    return analyzer

# Funciones para agregar informacion al catalogo

def addEvent(analyzer, event):
    """
    """
    lt.addLast(analyzer['events'], event)
    updateDateTrackID(analyzer['trackIDs'], event)
    return analyzer


# Funciones para creacion de datos

def updateDateTrackID(map, event):
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
        datentry = newTrackEntry(event)
        om.put(map, eventdate.date(), datentry)
    else:
        datentry = me.getValue(entry)
    addDateTrack(datentry, event)
    return map

def addDateTrack(datentry, event):
    """
    Actualiza un indice de tipo de eventos.  Este indice tiene una lista
    de eventos y una tabla de hash cuya llave es el tipo de crimen y
    el valor es una lista con los eventos de dicho tipo en la fecha que
    se está consultando (dada por el nodo del arbol)
    """
    lst = datentry['lstevents']
    lt.addLast(lst, event)
    track_id = datentry['trackID']
    offentry = mp.get(track_id, crime['OFFENSE_CODE_GROUP'])
    if (offentry is None):
        entry = newOffenseEntry(crime['OFFENSE_CODE_GROUP'], crime)
        lt.addLast(entry['lstoffenses'], crime)
        m.put(track_id, crime['OFFENSE_CODE_GROUP'], entry)
    else:
        entry = me.getValue(offentry)
        lt.addLast(entry['lstoffenses'], crime)
    return datentry


def updateDateIndex(map, crime):
    """
    Se toma la fecha del crimen y se busca si ya existe en el arbol
    dicha fecha.  Si es asi, se adiciona a su lista de crimenes
    y se actualiza el indice de tipos de crimenes.

    Si no se encuentra creado un nodo para esa fecha en el arbol
    se crea y se actualiza el indice de tipos de crimenes
    """
    occurreddate = crime['OCCURRED_ON_DATE']
    crimedate = datetime.datetime.strptime(occurreddate, '%Y-%m-%d %H:%M:%S')
    entry = om.get(map, crimedate.date())
    if entry is None:
        datentry = newDataEntry(crime)
        om.put(map, crimedate.date(), datentry)
    else:
        datentry = me.getValue(entry)
    addDateIndex(datentry, crime)
    return map

def newTrackEntry(event):
    """
    Crea una entrada en el indice por fechas, es decir en el arbol
    binario.
    """
    entry = {'trackID': None,
             'lstevents': None}
    entry['trackID'] = mp.newMap(numelements=30,
                                     maptype='PROBING',
                                     comparefunction=compareIds)
    entry['lstevents'] = lt.newList('SINGLE_LINKED', compareDates)
    return entry

def newOffenseEntry(offensegrp, crime):
    """
    Crea una entrada en el indice por tipo de crimen, es decir en
    la tabla de hash, que se encuentra en cada nodo del arbol.
    """
    ofentry = {'offense': None, 'lstoffenses': None}
    ofentry['offense'] = offensegrp
    ofentry['lstoffenses'] = lt.newList('SINGLELINKED', compareIds)
    return ofentry
# Funciones de consulta

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