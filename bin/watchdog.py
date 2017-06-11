# coding=utf-8

import threading
from telegram import Bot
from .token import TOKEN

bot = Bot(TOKEN)

class Watchdog:

    def __init__(self):

        self.success = False
        t = threading.Timer(15, self.countdown)
        t.start()

    def countdown(self):

        if not self.success:
            self.error()

    def error(self):

        print "Ha ocurrido un error"

    def succesfull(self):

        self.success = True


class TelegramWatchdog(Watchdog):

    def __init__(self, idTelegram):

        self.user = idTelegram
        Watchdog.__init__(self)

    def error(self):

        bot.send_message(self.user,
                         text="Parece que ha ocurrido un error grave. Usa /restart y si ves que el bot no responde por "
                              "favor habla con @PilocoSupportbot e informa del problema cuanto antes, muchas gracias.")
