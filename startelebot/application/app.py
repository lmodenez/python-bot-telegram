from telegram.ext import Updater
from startelebot.interface import estoque, financas, main
from startelebot.infrastructure.config import settings 

def create_app():

    token = settings.bot_token
    updater = Updater(token=token, use_context=True)

    # initiating extensions
    estoque.init_app()
    financas.init_app()

    main.init_app(updater)
    
    # start app
    updater.start_polling()

if __name__ == "__main__":
    create_app()