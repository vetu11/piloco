import json

def buscarIDsLibres(listaDeMensajes):
    with open("pilocuras.json") as f:
        data = json.load(f)

    listaID = []
    for e in listaDeMensajes:
        listaID.append(int(e["id"]))
    ultima = max(listaID)
    idLibres = []
    idRepetidas = []
    posicion = 0
    while posicion <= ultima:
        if posicion not in listaID:
            idLibres.append(posicion)
        if listaID.count(posicion) > 1:
            idRepetidas.append(posicion)
        posicion = posicion + 1
    print "Las ids libres son las siguientes:\n", idLibres,"\nID mas alta: ",ultima,"\nLas id repetidas son las siguientes:\n",idRepetidas,"\nHay un total de ",len(listaDeMensajes)," mensajes."

    if len(idLibres):
        return idLibres[0]
    else:
        return ultima + 1