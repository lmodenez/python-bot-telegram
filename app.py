from telegram.ext import Updater
import estoque, principal


def create_app():

    # create bot
    token = "1537564807:AAEJnfoye2C4dYcSqukYKtBrZAxn_Vt8UJY"
    updater = Updater(token=token, use_context=True)


    #initiating extensions
    estoque.init_app()
    principal.init_app(updater)


    # initiating handles



    #start app
    updater.start_polling()

if __name__ == '__main__':
    create_app()