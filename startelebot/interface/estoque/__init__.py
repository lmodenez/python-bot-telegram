from .estoque import Estoque
from startelebot.infrastructure.config import settings


def init_app():
    submenu_modules = settings.submenu_modules
    submenu_modules.append(Estoque())
    settings.submenu_modules = submenu_modules
    return
