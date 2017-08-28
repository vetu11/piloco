# coding=utf-8

import json

with open("usuarios") as f:

    usuarios = json.load(f)


for usuario in usuarios:

    with open("%s.piuser" % usuario) as usu:
        old = json.load(usu)

    new = old
    new["id_ultimo_mensaje"] = None

    with open("%s.piuser" % usuario, "w") as usu:
        json.dump(new, usu, indent=2)