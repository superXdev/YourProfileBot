import menu
import logging  
from telegram import (
        InlineKeyboardButton, 
        InlineKeyboardMarkup,
        Update, 
        ReplyKeyboardRemove, 
        ReplyKeyboardMarkup,
        InlineKeyboardButton, 
        InlineKeyboardMarkup
    )
from telegram.ext import (
        Updater,
        CommandHandler, 
        CallbackQueryHandler, 
        MessageHandler, 
        Filters, 
        ConversationHandler,
        CallbackContext
    )

# Menampung inputan user
GENDER = range(1)

# Aktifkan logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

'''
Semua tombol menu keyboard
'''
# Untuk kembali ke menu utama
def return_menu_keyboard():
    keyboard = [ [InlineKeyboardButton('Menu utama', callback_data='main_menu')] ]
    return InlineKeyboardMarkup(keyboard)

# Semua menu utama
def main_menu_keyboard():
    keyboard = [[InlineKeyboardButton('Profile kamu', callback_data='profile')],
              [InlineKeyboardButton('About', callback_data='about')]]
    return InlineKeyboardMarkup(keyboard)

'''
 Semua menu bot ada disini
'''
# Ketika pertama kali memulai bot
def start(update: Update, context: CallbackContext) -> int:
    # Kirim pilih jenis kelamin ketika memulai bot
    reply_keyboard = [['Cowok', 'Cewek', 'Lainnya']]

    update.message.reply_text(
        'Selamat datang di YourProfile Bot. \n\n'
        'Apa jenis kelamin kamu?',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
    )

    return GENDER

# Menanyakan jenis kelamin user
def gender(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("Jenis kelamin dari %s: %s", user.first_name, update.message.text)
    update.message.reply_text("Pilih menu", reply_markup=main_menu_keyboard())

# Menampilkan tentang bot
def about_menu(update: Update, context: CallbackContext) -> int:
    update.callback_query.message.edit_text("About bot.", reply_markup=return_menu_keyboard())

# Menampilkan menu utama
def main_menu(update: Update, context: CallbackContext) -> int:
    update.callback_query.message.edit_text("Menu utama.", reply_markup=main_menu_keyboard())

# Menampilkan informasi user
def profile_menu(update: Update, context: CallbackContext) -> int:
    user = update.callback_query.message.chat
    full_name = user.first_name + ' '+ user.last_name
    username = user.username
    update.callback_query.message.edit_text('*Your Profile*\nFull Name: {}\nUsername: {}'.format(full_name, username), reply_markup=return_menu_keyboard(), parse_mode='MarkdownV2')

# Membatalkan perintah bot
def cancel(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("Pengguna %s menekan batal.", user.first_name)
    update.message.reply_text(
        'Percakapan diakhiri.', reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END

# Ketika ada error tampilkan pada terminal
def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)

''' 
Bagian untuk menjalankan keseluruhan bot telegram
'''
def main():
    # Masukkan token bot disini
    updater = Updater("TOKEN", use_context=True)

    # Daftarkan dispatcher handler
    dp = updater.dispatcher

    dp.add_handler(ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states = {
            GENDER: [MessageHandler(Filters.regex('^(Cowok|Cewek|Lainnya)$'), gender)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    ))

    # Perintah yang ada di bot
    dp.add_handler(CallbackQueryHandler(main_menu, pattern='main_menu'))
    dp.add_handler(CallbackQueryHandler(about_menu, pattern='about'))
    dp.add_handler(CallbackQueryHandler(profile_menu, pattern='profile'))

    # log semua error
    dp.add_error_handler(menu.error)

    # Memulai bot
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()