from .main import Main


def init_app(updater):
    updater.dispatcher.add_handler(Main().conversation_handler)
    return
        