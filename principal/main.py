from telegram.ext import ConversationHandler, CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from estoque import config

class Main():

    END, CHOOSING = [f"main{x}" for x in map(chr,range(2))]

    def __init__(self) -> None:

        # setting parent_state and parent_methods
        for module in config.modules:
            module.set_parent_method(self.show_menu)
            module.set_parent_state(self.CHOOSING)

        # setting module states and conversation handlers
        module_states={}
        for module in config.modules:
            module_states[module.module_name] = [module.conversation_handler]

        states_dict = {self.CHOOSING: [CallbackQueryHandler(self.get_menu_choice)]} | module_states

        self.conversation_handler = ConversationHandler(
            entry_points=[
                CommandHandler("start", self.show_menu)
            ],
            states=states_dict,
            fallbacks=[
                # CommandHandler('sair', )
            ]
        )


    # get conversation handler

    def get_conversation_handler(self):
            return self.conversation_handler

    # callback functions

    def show_menu(self, update, context):
        buttons=[]
        for module in config.modules:
            buttons.append(
                [InlineKeyboardButton(text=f"{module.module_name}", callback_data=f"{module.module_name}")]
            )
        keyboard = InlineKeyboardMarkup(buttons)
        if update.callback_query:
            update.callback_query.answer()
            update.callback_query.edit_message_text("Por favor escolha uma das opções abaixo:", reply_markup=keyboard)
        else:
            update.message.reply_text("Por favor escolha uma das opções abaixo:", reply_markup=keyboard)
        return self.CHOOSING

    def get_menu_choice(self, update, context):
        print("oi")
        query_data = update.callback_query.data
        for module in config.modules:
            if query_data == module.module_name:
                module.show_menu(update, context)  # chamar a funcao de apresentacao do submenu (pegar atraves do config) e depois retornar o conversation handler
                return module.module_name
