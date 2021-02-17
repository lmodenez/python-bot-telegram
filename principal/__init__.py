from .main import Main


def init_app(updater):
    updater.dispatcher.add_handler(Main().get_conversation_handler())
    return

    