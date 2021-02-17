from . import config, estoque


def init_app():
    config.modules.append(estoque.Estoque())
    return