# coding=utf-8

from .token import PAYMENT_PROVIDER_TOKEN
from telegram import (LabeledPrice, InlineKeyboardButton, InlineKeyboardMarkup, ParseMode)
from telegram.ext import (MessageHandler, CallbackQueryHandler, Filters, PreCheckoutQueryHandler, ShippingQueryHandler)
import logging

logger = logging.getLogger(__name__)


class TelegramDonation:

    def manual_cuantity(self, bot, update):

        try:

            return 0 # CONVERSATION.END
        except: pass

    def mostrar_donacion(self, bot, update):
        if update.message:
            pass # TODO

        else:
            donation_amount = int(update.callback_query.data.split("-")[1])

        if donation_amount - 100:
            less = donation_amount - 50
        else:
            less = donation_amount

        more = donation_amount + 50
        eur_num_to_text = ("%s" % (donation_amount / 100.0) + "0").replace(".", ",")

        msg = "_TEST_ actualmente detrás del código de Piloco hay una única persona trabajando para mejorarlo. " \
              "Bla bla bla.\nSi puedes hacer una aportación económica sería de gran ayuda, para mantener los se" \
              "rvidores y para poder dedicar más tiempo a Piloco."
        keyboard = [[InlineKeyboardButton("Cancelar 💔", callback_data="donation_cancel")],
                    [InlineKeyboardButton("➖", callback_data="donation_new-%s" % less),
                     InlineKeyboardButton("%s €" % eur_num_to_text, callback_data="donation_custom"),
                     InlineKeyboardButton("➕", callback_data="donation_new-%s" % more)],
                    [InlineKeyboardButton("Donar %s € ❤️" % eur_num_to_text, callback_data="donate-%s" % donation_amount)]]

        if update.message:
            update.message.reply_text(msg, reply_markup=InlineKeyboardMarkup(keyboard))
        else:
            update.callback_query.message.edit_text(msg, reply_markup=InlineKeyboardMarkup(keyboard))
            update.callback_query.answer()


    def start_without_shipping_callback(self, bot, update):
        chat_id = update.callback_query.message.chat_id
        title = "Donación"
        description = "Aportación económica para el mantenimiento y desarrollo de Pilocobot."
        payload = "Custom-Payload"
        provider_token = PAYMENT_PROVIDER_TOKEN
        start_parameter = "test-payment"
        currency = "EUR"
        price = int(update.callback_query.data.split("-")[1])
        prices = [LabeledPrice("Donacion", price)]

        update.callback_query.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup([]))
        # optionally pass need_name=True, need_phone_number=True,
        # need_email=True, need_shipping_address=True, is_flexible=True
        bot.sendInvoice(chat_id, title, description, payload,
                        provider_token, start_parameter, currency, prices)


    # after (optional) shipping, it's the pre-checkout
    def precheckout_callback(self, bot, update):
        query = update.pre_checkout_query
        # check the payload, is this from your bot?
        if query.invoice_payload != 'Custom-Payload':
            # answer False pre_checkout_query
            bot.answer_pre_checkout_query(pre_checkout_query_id=query.id, ok=False,
                                          error_message="Parece que ha habido un error")
        else:
            bot.answer_pre_checkout_query(pre_checkout_query_id=query.id, ok=True)


    # finally, after contacting to the payment provider...
    def successful_payment_callback(self, bot, update):
        # do something after successful receive of payment
        update.message.reply_text(
            "¡La transacción se ha completado con éxito! Gracias por tu aportación, "
            "has recibido %s puntos reputación." % update.message.successful_payment.total_amount)
TelegramDonation = TelegramDonation()

def main():

    # Optional handler if your product requires shipping
    dp.add_handler(ShippingQueryHandler(shipping_callback))

    # Pre-checkout handler to final check
    dp.add_handler(PreCheckoutQueryHandler(precheckout_callback))

    # Success! Notify your user!
    dp.add_handler(MessageHandler(Filters.successful_payment, successful_payment_callback))
    dp.add_handler(CallbackQueryHandler(mostrar_donacion, pattern="^donation_new-\d*"))
    dp.add_handler(CallbackQueryHandler(start_without_shipping_callback, pattern="^donate-\d*"))

    # Start the Bot
    updater.start_polling()
