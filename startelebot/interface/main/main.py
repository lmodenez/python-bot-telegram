from typing import Dict
from telegram.ext import ConversationHandler, CommandHandler, CallbackQueryHandler, MessageHandler, Filters
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from startelebot.domain.login import Login
from startelebot.infrastructure.config import settings

class Main():

    END, CHOOSING, WRITING_PASSWORD = [f"main{x}" for x in map(chr,range(3))]

    def __init__(self, conversation_handler=None) -> None:
        self._conversation_handler = conversation_handler
        self.login = Login()

    
    # properties

    @property
    def conversation_handler(self):
        if not self._conversation_handler:
            self._instantiate_conversation_handler()
        return self._conversation_handler     

    # auxiliary methods referring to the submenus  

    def _set_up_submodules(self):
        # setting parent_state and parent_methods for each submenu module.        
        for module in settings.submenu_modules:
            module.parent_method = self.show_menu
            module.parent_state = self.CHOOSING

    def _get_submenu_module_states(self) -> Dict:
        module_states = {}
        for module in settings.submenu_modules:
            module_states[module.module_name] = [module.conversation_handler]
        return module_states

    def _get_submenu_keyboard(self) -> InlineKeyboardMarkup:
        buttons = []
        for module in settings.submenu_modules:
            buttons.append(
                [InlineKeyboardButton(text=f"{module.module_name}", callback_data=f"{module.module_name}")]
            )
        return InlineKeyboardMarkup(buttons)

    # conversation handler

    def _instantiate_conversation_handler(self) -> None:
        self._set_up_submodules()
        submenu_states = self._get_submenu_module_states()
        
        # setting module states and conversation handlers
        self._conversation_handler = ConversationHandler(
            entry_points=[
                MessageHandler(Filters.text & ~Filters.command, self.verify_user_is_logged),
                CommandHandler("start", self.verify_user_is_logged)
            ],
            states = {
                self.CHOOSING: [
                    CallbackQueryHandler(
                        self.call_submodule_menu,
                        pattern="|".join([f"^{module.module_name}$" for module in settings.submenu_modules])
                    ),
                ],
                self.WRITING_PASSWORD: [
                    MessageHandler(Filters.text & ~Filters.command, self.validate_password)
                ],
                **submenu_states
            },
            fallbacks=[
            
            ]
        )
        return

    #callback methods
    
    def verify_user_is_logged(self, update, context):
        user = update.effective_user
        if self.login.user_is_logged(user):
            return self.show_menu(update, context)
        else:
            return self.ask_for_password(update, context)

    def ask_for_password(self, update, context):
        user = update.effective_user
        update.message.reply_text(f"Olá {user.first_name}, para continuar a utilizar o bot, por favor me informe sua senha.")
        return self.WRITING_PASSWORD

    def validate_password(self, update, context):
        user = update.effective_user
        password = update.message.text.strip()
        if self.login.verify_user_password(user, password):
            return self.show_menu(update, context)
        return self.ask_for_password(update, context)

    def show_menu(self, update, context):
        keyboard = self._get_submenu_keyboard()
        if update.callback_query:
            update.callback_query.answer()
            update.callback_query.edit_message_text("Por favor escolha uma das opções abaixo:", reply_markup=keyboard)
        else:
            update.message.reply_text("Por favor escolha uma das opções abaixo:", reply_markup=keyboard)
        return self.CHOOSING
    
    def call_submodule_menu(self, update, context):
        query_data = update.callback_query.data
        for module in settings.submenu_modules:
            if query_data == module.module_name:
                module.show_menu(update, context)  # call the submenu's apresentetion method.
                return module.module_name