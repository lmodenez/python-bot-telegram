from telegram.ext import ConversationHandler, CallbackQueryHandler, MessageHandler, Filters
from telegram import InlineKeyboardMarkup, InlineKeyboardButton


class Estoque():

    END, CHOOSING, WRITING_ITEM = [f"estoque{x}" for x in map(chr, range(3))]

    module_name = "estoque"

    def __init__(self, parent_state=None, parent_method=None):
        self.parent_state = parent_state
        self.parent_method = parent_method
        self._conversation_handler = None

    # properties

    @property
    def conversation_handler(self):
        if not self._conversation_handler:
            self._instantiate_conversation_handler()
        return self._conversation_handler 


    # conversation handler definition 
    def _instantiate_conversation_handler(self):
        if self.parent_method and self.parent_method:
            self._conversation_handler = ConversationHandler(
                entry_points= [
                    CallbackQueryHandler(self.ask_for_item, pattern=f'^item$'),
                    CallbackQueryHandler(self.return_to_parent_menu, pattern=f'^voltar$')
                ],
                states = {
                    self.CHOOSING: [
                        CallbackQueryHandler(self.ask_for_item, pattern=f'^item$'),
                        CallbackQueryHandler(self.return_to_parent_menu, pattern=f'^voltar$'),
                    ],
                    self.WRITING_ITEM: [MessageHandler(Filters.text & ~Filters.command, self.get_item)]
                },
                fallbacks = [

                ],
                map_to_parent = {
                    self.END: self.parent_state
                }
            )
            return 
        raise Exception("error parent_state or parent_method isn't defined.")



    # callback methods
    def show_menu(self, update, context):
        buttons=[
            [InlineKeyboardButton(text="Busca por Item", callback_data="item")],
            [InlineKeyboardButton(text="Voltar", callback_data="voltar")]
        ]
        keyboard = InlineKeyboardMarkup(buttons)
        update.callback_query.answer()
        update.callback_query.edit_message_text(text="Você escolheu: Consulta Estoque\nPor favor escolha uma das opções abaixo:", reply_markup=keyboard)
        return self.CHOOSING

    def ask_for_item(self, update, context):
        query_data = update.callback_query.data
        update.callback_query.answer()
        update.callback_query.edit_message_text(text="Digite o item desejado:")
        return self.WRITING_ITEM

    def return_to_parent_menu(self, update, context):
        self.parent_method(update, context)
        return self.END
        
    def get_item(self, update, context):
        pass # TODO: Falta implementar




