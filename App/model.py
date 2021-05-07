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
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
assert cf


# Construccion de modelos


def newAnalyzer():
    """ Inicializa el analizador

    Retorna el analizador inicializado.
    """
    analyzer = {'events': None,
                'artists': None,
                'tracks': None,
                'instrumentalness': None,
                'acousticness': None,
                'liveness': None,
                'speechiness': None,
                'energy': None,
                'danceability': None,
                'valence': None,
                'tempo': None,
                'created_at': None,
                'hashtags': None,
                'vaders': None
                }

    analyzer['events'] = lt.newList(datastructure='ARRAY_LIST')
    analyzer['artists'] = mp.newMap(maptype='PROBING')
    analyzer['tracks'] = mp.newMap(maptype='PROBING')
    analyzer['instrumentalness'] = om.newMap(omaptype='RBT')
    analyzer['acousticness'] = om.newMap(omaptype='RBT')
    analyzer['liveness'] = om.newMap(omaptype='RBT')
    analyzer['speechiness'] = om.newMap(omaptype='RBT')
    analyzer['energy'] = om.newMap(omaptype='RBT')
    analyzer['danceability'] = om.newMap(omaptype='RBT')
    analyzer['valence'] = om.newMap(omaptype='RBT')
    analyzer['tempo'] = om.newMap(omaptype='RBT')
    analyzer['created_at'] = om.newMap(omaptype='RBT')
    analyzer['hashtags'] = mp.newMap(maptype='PROBING')
    analyzer['vaders'] = mp.newMap(maptype='PROBING')

    return analyzer


# Funciones para agregar informacion al catalogo

def addEvent(analyzer, event):
    '''
    Agrega individualmente el evento al analyzer, en
    cada uno de sus mapas
    '''
    lt.addLast(analyzer['events'], event)
    mp.put(analyzer['artists'], event['artist_id'], 0)
    mp.put(analyzer['tracks'], event['track_id'], 0)
    addEventOnOrderedRBTMap(
        analyzer, float(event['instrumentalness']),
        event, 'instrumentalness')
    addEventOnOrderedRBTMap(
        analyzer, float(event['acousticness']),
        event, 'acousticness')
    addEventOnOrderedRBTMap(
        analyzer, float(event['liveness']),
        event, 'liveness')
    addEventOnOrderedRBTMap(
        analyzer, float(event['speechiness']),
        event, 'speechiness')
    addEventOnOrderedRBTMap(
        analyzer, float(event['energy']),
        event, 'energy')
    addEventOnOrderedRBTMap(
        analyzer, float(event['danceability']),
        event, 'danceability')
    addEventOnOrderedRBTMap(
        analyzer, float(event['valence']),
        event, 'valence')
    addEventOnOrderedRBTMap(
        analyzer, float(event['tempo']),
        event, 'tempo')
    addTimedEvent(
        analyzer, event['created_at'], event, 'created_at')


def addOnMap(analyzer, event, key, map_name):
    '''
    Agrega los hashtags y los vaders a sus mapas individuales
    '''
    mp.put(analyzer[map_name], key, event)




def addEventOnOrderedRBTMap(analyzer, int_input, event, map_key):
    """
    La función de addEventOnOrderedRBTMap() adiciona el video al árbol
    tipo RBT que se ha seleccionado.
    Args:
        analyzer: Analizador de eventos
        int_input: Llave a analizar
        video: Video a añadir
        map_key: Especifica cuál mapa
    """
    selected_map = analyzer[map_key]
    entry = om.get(selected_map, int_input)
    if entry is not None:
        value = me.getValue(entry)
    else:
        value = newDataEntry()
        om.put(selected_map, int_input, value)
    lt.addLast(value['events'], event)


def addTimedEvent(analyzer, int_input, event, map_key):
    '''
    Adiciona un evento a un árbol tipo RBT usando el
    tiempo de creación del evento, con los segundos como
    llave
    '''
    time = int_input.split(" ")
    time = time[1].split(':')
    time = int(time[0])*3600 + int(time[1])*60 + int(time[2])
    addEventOnOrderedRBTMap(
        analyzer, time,
        event, map_key)




def newDataEntry():
    entry = {'events': None}
    entry['events'] = lt.newList('ARRAY_LIST')
    return entry


# Funciones de consulta


def eventsSize(analyzer):
    '''
    Retorna el tamaño de la lista de eventos
    '''
    return lt.size(analyzer['events'])


def artistsSize(analyzer):
    '''
    Retorna el tamaño del mapa de artistas,
    para saber los artistas únicos cargados
    '''
    return mp.size(analyzer['artists'])


def tracksSize(analyzer):
    '''
    Retorna el tamaño del mapa de tracks, para
    saber los tracks únicos cargados
    '''
    return mp.size(analyzer['tracks'])


def getEventsByRange(analyzer, criteria, initial, final):
    '''
    Retorna los varias características de los
    eventos dado un criterio y rango en el mismo,
    buscándolos en un árbol
    Args:
        analyzer: Analizador de eventos
        criteria: Llave del analyzer a analizar
        initial: Inicio del rango
        final: Fin del rango
    '''
    lst = om.values(analyzer[criteria], initial, final)
    events = 0
    artists = mp.newMap(maptype='PROBING')
    tracks = mp.newMap(maptype='PROBING')

    for lstevents in lt.iterator(lst):
        events += lt.size(lstevents['events'])
        for soundtrackyourtimeline in lt.iterator(lstevents['events']):
            mp.put(artists, soundtrackyourtimeline['artist_id'], 1)
            mp.put(tracks, soundtrackyourtimeline['track_id'], 1)

    artists_size = mp.size(artists)
    tracks_size = mp.size(tracks)

    return events, artists_size, tracks_size, artists, tracks





def getTrcForTwoCriteria(analyzer, criteria1range, str1, criteria2range, str2):
    '''
    Retorna los varias características de los
    eventos dado dos criterios y rangos en el mismo,
    buscándolos en ambos árboles. El retorno son los eventos
    que cumplen con ambas características
    Args:
        analyzer: Analizador de eventos
        criteria1range: Rango del criterio 1
        str1: Llave del analyzer del criterio 1
        criteria2range: Rango del criterio 2
        str2: Llave del analyzer del criterio 2
    '''
    criteria1 = om.values(analyzer[str1], criteria1range[0], criteria1range[1])
    submap = {'events': None}
    submap[str2] = om.newMap(omaptype='RBT')
    for eventO in lt.iterator(criteria1):
        for event0 in lt.iterator(eventO['events']):
            addEventOnOrderedRBTMap(submap, float(event0[str2]), event0, str2)
    result = om.values(submap[str2], criteria2range[0], criteria2range[1])
    artists = mp.newMap(maptype='PROBING')
    tracks = mp.newMap(maptype='PROBING')
    for event1 in lt.iterator(result):
        for eventi in lt.iterator(event1['events']):
            mp.put(artists, eventi['artist_id'], 1)
            mp.put(
                tracks, eventi['track_id'],
                (eventi[str1], eventi[str2]))
    return (mp.size(artists), mp.size(tracks), tracks)

