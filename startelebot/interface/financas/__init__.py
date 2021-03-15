from .financas import Financas
from startelebot.infrastructure.config import settings


def init_app():
    submenu_modules = settings.submenu_modules
    submenu_modules.append(Financas())
    settings.submenu_modules = submenu_modules
    return