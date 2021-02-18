from telegram.ext import Updater
import estoque
import principal


def create_app():

    # create bot
    token = "1670031977:AAHT9urvoMRj741IJ1_9BQtrH-0cr4uuVtk"
    updater = Updater(token=token, use_context=True)

    # initiating extensions
    estoque.init_app()
    principal.init_app(updater)

    # initiating handles

    # start app
    updater.start_polling()


if __name__ == '__main__':
    create_app()
