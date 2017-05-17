# coding=utf-8

import logging
from telegram.ext import Updater, MessageHandler, CommandHandler, CallbackQueryHandler, Filters
from bin import TOKEN, HandlersPiloco, Conversations

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


def stop_bot(updater):
    logging.info("Apagando bot...")
    updater.stop()
    logging.info("Bot apagado")


def main():
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
    a_h(CallbackQueryHandler(HandlersPiloco.proximamente_clb))
    a_h(MessageHandler(Filters.all, HandlersPiloco.mensaje))

    updater.start_polling()

    # CONSOLA
    while True:
        input = raw_input()
        input_C = input.split()[0]
        args = input.split()[1:]
        strig = ""

        for e in args:
            strig = strig + " " + e

        if input_C == "stop":
            stop_bot(updater)
            break

        else:
            print "Comando desconocido"


if __name__ == '__main__':
    main()
