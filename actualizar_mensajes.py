# coding=utf-8

import json

with open("pilocuras.json") as f:
    pilocuras = json.load(f)

with open("newMessages.json") as f:
    new_messages = json.load(f)

new_pilocuras = []
new_new_messages = []

print "Empezemos por los mensajes en revisión, que son menos"

for mensaje in new_messages:
    if mensaje["tipo"] == "normal":
        print "El mensaje es:\n0:%s" % mensaje["text"]
    else:
        print "El mensaje es:\n1:%s\n2:%s" % (mensaje["text0"], mensaje["text1"])

    while True:
        i = raw_input("¿es repetible? (s/n)")

        if i == "s":
            mensaje["repetible"] = True
            new_new_messages.append(mensaje)
            break
        elif i == "n":
            mensaje["repetible"] = False
            new_new_messages.append(mensaje)
            break
        else:
            print "¿qué mierda ha sido eso?"

print "Ahora vamos a los mensajes en juego"

for mensaje in pilocuras:
    if mensaje["tipo"] == "normal":
        print "El mensaje es:\n0:%s" % mensaje["text"]
    else:
        print "El mensaje es:\n1:%s\n2:%s" % (mensaje["text0"], mensaje["text1"])

    while True:
        i = raw_input("¿es repetible? (s/n)")

        if i == "s":
            mensaje["repetible"] = True
            new_pilocuras.append(mensaje)
            break
        elif i == "n":
            mensaje["repetible"] = False
            new_pilocuras.append(mensaje)
            break
        else:
            print "¿qué mierda ha sido eso?"

with open("pilocuras.json", "w") as f:
    json.dump(new_pilocuras, f, indent=2)

with open("newMessages.json", "w") as f:
    json.dump(new_new_messages, f, indent=2)
