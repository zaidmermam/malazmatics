from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters

token = '6255596860:AAFVu3vCmRW9G7BjujcEnhJiMJCGyFj7joI'
updater = Updater(token, use_context=True)


def start(update: Update, context: CallbackContext):
    update.message.reply_text("مرحبا بك! انا بوت يهدف لمساعدة طلاب سوريا من مختلف الصفوف من خلال توفير ملفات شرح "
                              "الدروس, النماذج الامتحانية, و اوراق العمل من قبل نخبة الاساتذة السوريين. في الوقت "
                              "الحالي, ليست لدينا موارد الا لمادة الرياضيات, لكننا نعمل جاهدين لتوفير ذلك لجميع المواد!")


def helptext(update: Update, context: CallbackContext):
    update.message.reply_text("Your Message")


def main():
    dispatcher = updater.dispatcher
    updater.dispatcher.add_handler(CommandHandler('help',helptext))
    updater.dispatcher.add_handler(CommandHandler('start',start))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
