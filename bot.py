# coding=utf-8

import logging
from telegram.ext import Updater, MessageHandler, CommandHandler, CallbackQueryHandler, Filters, RegexHandler
from bin import TOKEN, HandlersPiloco, Conversations, TelegramDonation
from bin.usuarios import Usuarios
from bin.mensaje import MensajesClasica, MensajesEnRevision

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def guardar(bot=None, update=None, from_telegram=True):
    if from_telegram:
        if update.message.from_user.id == 254234845:
            try:
                MensajesClasica.guardar()
                MensajesEnRevision.guardar()
                update.message.reply_text("Guardado correctamente")
            except:
                update.message.reply_text("Ha ocurrido un error 😬")
    else:
        MensajesClasica.guardar()
        MensajesEnRevision.guardar()


def stop_bot(updater):
    logging.info("Apagando bot...")
    for u in Usuarios.activos:
        usuario = Usuarios.activos.pop(0)
        try:
            if usuario.partida:
                updater.bot.send_message(chat_id=usuario.id,
                                         text="El bot se ha reiniciado y se ha cerrado tu partida, usa /start para continuar.")
            elif usuario.editando_mensaje:
                updater.bot.send_message(chat_id=usuario.id,
                                         text="El bot se ha reiniciado y tu mensaje se ha perdido 😭 usa /start para continuar.")
        except: print "Imposible enviar mensaje a %s" % usuario.id
    guardar(from_telegram=False)

    updater.stop()
    logging.info("Bot apagado")


def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"' % (update, error))


def main():

    updater = Updater(TOKEN)
    dp = updater.dispatcher
    a_h = dp.add_handler

    a_h(CommandHandler('start', HandlersPiloco.comando_start))
    a_h(CommandHandler('guardar', guardar))
    a_h(Conversations.add_players)
    a_h(Conversations.add_message)
    a_h(CallbackQueryHandler(HandlersPiloco.menu_info, pattern="^mp_info$"))
    a_h(CallbackQueryHandler(HandlersPiloco.menu_principal, pattern="^mp$"))
    a_h(CallbackQueryHandler(HandlersPiloco.menu_mensajes, pattern="^mp_mensajes$"))
    a_h(CallbackQueryHandler(HandlersPiloco.menu_partidaClasica, pattern="^mp_newGame$"))
    a_h(CallbackQueryHandler(HandlersPiloco.partida_clasica_picante_info, pattern="^mpc_picante_info$"))
    a_h(CallbackQueryHandler(HandlersPiloco.partida_clasica_mas_picante, pattern="^mpc_mas_picante$"))
    a_h(CallbackQueryHandler(HandlersPiloco.partida_clasica_menos_picante, pattern="^mpc_menos_picante$"))
    a_h(CallbackQueryHandler(HandlersPiloco.partida_clasica_emparejador, pattern="^mpc_emparejador$"))
    a_h(CallbackQueryHandler(HandlersPiloco.next_mesagge, pattern="^pc_next$"))
    a_h(CallbackQueryHandler(HandlersPiloco.partida_clasica_vote_up, pattern="^pc_vote_up$"))
    a_h(CallbackQueryHandler(HandlersPiloco.partida_clasica_vote_down, pattern="^pc_vote_down$"))
    a_h(CallbackQueryHandler(HandlersPiloco.ajustes_partida_clasica, pattern="^pc_ajustes$"))
    a_h(CallbackQueryHandler(HandlersPiloco.partida_clasica_volver, pattern="^apc_volver$"))
    a_h(CallbackQueryHandler(HandlersPiloco.partida_clasica_salir, pattern="^apc_salir$"))
    a_h(CallbackQueryHandler(HandlersPiloco.ajustes_mas_picante, pattern="^apc_mas_picante$"))
    a_h(CallbackQueryHandler(HandlersPiloco.ajustes_menos_picante, pattern="^apc_menos_picante$"))
    # a_h(CallbackQueryHandler(HandlersPiloco.delete_player_in_game, pattern="apc_delete_player$"))
    # a_h(CallbackQueryHandler(HandlersPiloco))
    a_h(CallbackQueryHandler(HandlersPiloco.revisar_mensajes, pattern="^ms_rev$"))
    a_h(CallbackQueryHandler(HandlersPiloco.revisar_actualizar_valor, pattern="^revisar_valor_"))
    a_h(CallbackQueryHandler(HandlersPiloco.revisar_actualizar_picante, pattern="^revisar_picante_"))
    a_h(CallbackQueryHandler(TelegramDonation.mostrar_donacion, pattern="^donation_new-\d*"))
    a_h(CallbackQueryHandler(HandlersPiloco.add_message, pattern="^ms_new$"))
    a_h(CommandHandler('restart', HandlersPiloco.restart_bot))
    a_h(CommandHandler('announcement', HandlersPiloco.announcement))
    a_h(CommandHandler('backend', HandlersPiloco.open_backend))
    a_h(CommandHandler('revisiones',HandlersPiloco.comando_revisiones, pass_args=True))
    a_h(RegexHandler("^/", HandlersPiloco.comandos_no_soportados))
    a_h(CallbackQueryHandler(HandlersPiloco.proximamente_clb))
    a_h(MessageHandler(Filters.all, HandlersPiloco.mensaje))
    # a_h(CallbackQueryHandler(HandlersPiloco.start_vote_partida_clasica, pattern="^pc_votar$"))  # todo: DEPRECATED

    dp.add_error_handler(error)

    updater.start_polling()

    # CONSOLA
    while True:
        inp = raw_input()
        if inp:
            input_c = inp.split()[0]
            args = inp.split()[1:]
            strig = ""

            for e in args:
                strig = strig + " " + e

            if input_c == "stop":
                stop_bot(updater)
                break

            elif input_c == "comprobar":
                Usuarios.imprimir_estado()

            elif input_c == "guardar":
                guardar(from_telegram=False)

            else:
                print "Comando desconocido"


if __name__ == '__main__':
    main()
