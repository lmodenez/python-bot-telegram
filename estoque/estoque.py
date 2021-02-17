from telegram.ext import ConversationHandler, CallbackQueryHandler, MessageHandler, Filters
from telegram import InlineKeyboardMarkup, InlineKeyboardButton

class Estoque():

    END, CHOOSING, WRITING_ITEM = [f"estoque{x}" for x in map(chr,range(3))]

    module_name = "estoque"

    def __init__(self, parent_state=None, parent_method=None):
        self.parent_state = parent_state
        self.parent_method = parent_method
        self.__conversation_handler = None

        


    # set parent_state and parent_methods

    def set_parent_state(self, parent_state):
        self.parent_state = parent_state
        return

    def set_parent_method(self, parent_method):
        self.parent_method = parent_method
        return 

    # properties
    @property
    def conversation_handler(self):
        if not self.__conversation_handler:
            self._instantiate_conversation_handler()
        return self.__conversation_handler

    # get conversation handler
    def _instantiate_conversation_handler(self):
        if self.parent_state and self.parent_method:
            self.__conversation_handler = ConversationHandler(
                entry_points=[
                    CallbackQueryHandler(self.get_menu_choice)
                ],
                states={
                    self.CHOOSING: [CallbackQueryHandler(self.get_menu_choice)],
                    self.WRITING_ITEM: [MessageHandler(Filters.text, self.get_item)]
                },
                fallbacks=[
                    # CommandHandler("sair", self.return_to_parent)
                ],
                map_to_parent={
                    self.END: self.parent_state
                }
            )
            return 
        raise Exception("error parent_state or parent_method isn't defined.")

    # callback functions
    def show_menu(self, update, context):
        buttons=[
            [InlineKeyboardButton(text="Busca por Item", callback_data="item")],
            [InlineKeyboardButton(text="Voltar", callback_data="voltar")]
        ]
        keyboard = InlineKeyboardMarkup(buttons)
        update.callback_query.answer()
        update.callback_query.edit_message_text(text="Você escolheu: Consulta Estoque\nFavor escolher uma das opções abaixo:", reply_markup=keyboard)
        return self.CHOOSING

    def get_menu_choice(self, update, context):
        query_data = update.callback_query.data
        if query_data == "item":
            update.callback_query.answer()
            update.callback_query.edit_message_text("Favor informar o item.")
            return self.WRITING_ITEM
        elif query_data == "voltar":
            self.parent_method(update, context)
            return self.END
        return 

    def get_item(self, update, context):
        pass

    def return_to_parent(self, update, context):
        self.parent_method(update, context)
        return self.END
    