# coding=utf-8

import logging
from telegram.ext import Updater, MessageHandler, CommandHandler, CallbackQueryHandler, Filters, RegexHandler
from bin import TOKEN, HandlersPiloco, Conversations
from bin.usuarios import Usuarios


def stop_bot(updater):
    logging.info("Apagando bot...")
    for usuario in Usuarios.activos:
        try:
            if usuario.partida:
                updater.bot.send_message(chat_id=usuario.id,
                                         text="El bot se ha reiniciado y se ha cerrado tu partida, usa /start para continuar.")
            elif usuario.editando_mensaje:
                updater.bot.send_message(chat_id=usuario.id,
                                         text="El bot se ha reiniciado y tu mensaje se ha perdido 😭 usa /start para continuar.")
        except: print "Imposible enviar mensaje a %s" % usuario.id
    updater.stop()
    logging.info("Bot apagado")


def main():
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    a_h = dp.add_handler

    a_h(CommandHandler('start', HandlersPiloco.comando_start))
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
    a_h(CallbackQueryHandler(HandlersPiloco.start_vote_partida_clasica, pattern="^pc_votar$"))
    a_h(CallbackQueryHandler(HandlersPiloco.partida_clasica_vote_up, pattern="^pc_vote_up$"))
    a_h(CallbackQueryHandler(HandlersPiloco.partida_clasica_vote_down, pattern="^pc_vote_down$"))
    a_h(CallbackQueryHandler(HandlersPiloco.ajustes_partida_clasica, pattern="^pc_ajustes$"))
    a_h(CallbackQueryHandler(HandlersPiloco.partida_clasica_volver, pattern="^apc_volver$"))
    a_h(CallbackQueryHandler(HandlersPiloco.partida_clasica_salir, pattern="^apc_salir$"))
    a_h(CallbackQueryHandler(HandlersPiloco.ajustes_mas_picante, pattern="^apc_mas_picante$"))
    a_h(CallbackQueryHandler(HandlersPiloco.ajustes_menos_picante, pattern="^apc_menos_picante$"))
    a_h(CallbackQueryHandler(HandlersPiloco.revisar_mensajes, pattern="^ms_rev$"))
    a_h(CallbackQueryHandler(HandlersPiloco.revisar_actualizar_valor, pattern="^revisar_valor_"))
    a_h(CallbackQueryHandler(HandlersPiloco.revisar_actualizar_picante, pattern="^revisar_picante_"))
    a_h(CallbackQueryHandler(HandlersPiloco.add_message, pattern="^ms_new$"))
    a_h(CommandHandler('restart', HandlersPiloco.restart_bot))
    a_h(RegexHandler("^/", HandlersPiloco.comandos_no_soportados))
    a_h(CallbackQueryHandler(HandlersPiloco.proximamente_clb))
    a_h(MessageHandler(Filters.all, HandlersPiloco.mensaje))

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

            else:
                print "Comando desconocido"


if __name__ == '__main__':
    main()
