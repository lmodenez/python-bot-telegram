from telegram.ext import ConversationHandler, CallbackQueryHandler, MessageHandler, Filters
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from startelebot.domain.financas import Financa

class Financas():

    END, CHOOSING, WRITING_DOCUMENT, CHOOSING_INVOICE = [f"financas{x}" for x in map(chr, range(4))]

    module_name = "financas"

    def __init__(self, parent_state=None, parent_method=None):
        self.parent_state = parent_state
        self.parent_method = parent_method
        self._conversation_handler = None
        self.financas = Financa()

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
                    CallbackQueryHandler(self.ask_for_document, pattern=f'^2_via_boleto$'),
                    CallbackQueryHandler(self.return_to_parent_choice, pattern=f'^voltar$')
                ],
                states = {
                    self.CHOOSING: [
                        CallbackQueryHandler(self.ask_for_document, pattern=f'^2_via_boleto$'),
                        CallbackQueryHandler(self.return_to_parent_choice, pattern=f'^voltar$')
                    ],
                    self.WRITING_DOCUMENT: [
                        MessageHandler(Filters.text & ~Filters.command, self.get_document),
                        CallbackQueryHandler(self.return_to_parent_choice, pattern=f'^voltar$')
                    ],
                    self.CHOOSING_INVOICE: [
                        CallbackQueryHandler(self.show_ticket, pattern=f'^(?!.*voltar).*$'),
                        CallbackQueryHandler(self.return_to_parent_choice, pattern=f'^voltar$')
                    ]
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
            [InlineKeyboardButton(text="2 via de Boleto", callback_data="2_via_boleto")],
            [InlineKeyboardButton(text="Limite de credito", callback_data="limite_credito")],
            [InlineKeyboardButton(text="Pedidos restritos", callback_data="pedidos_restritos")],
            [InlineKeyboardButton(text="Voltar", callback_data="voltar")]
        ]
        keyboard = InlineKeyboardMarkup(buttons)
        update.callback_query.answer()
        update.callback_query.edit_message_text(text="Você escolheu: Financas\nPor favor escolha uma das opcoes abaixo:", reply_markup=keyboard)
        return self.CHOOSING

    def show_invoice(self, update, context):
        document = update.message.text.strip()
        context.user_data["client_document"] = document

        client_name = self.financas.get_client_name(document).strip()
        invoices = self.financas.get_unpaid_invoices(document)

        buttons=[
            [InlineKeyboardButton(text="Voltar", callback_data="voltar")]
        ]
        keyboard = InlineKeyboardMarkup(buttons)

        for invoice in invoices:
            button = [InlineKeyboardButton(text=f"{invoice}", callback_data=f"{invoice}")]
            buttons.insert(0, button)

        update.message.reply_text(text=f"Voce informou o cliente: <strong>{client_name.title()}</strong>\nEssas sao as notas em aberto:", reply_markup=keyboard, parse_mode='HTML')
        return self.CHOOSING_INVOICE

    def show_ticket(self, update, context):
        client_document = context.user_data.get("client_document")
        invoice = update.callback_query.data.split('-')[0].strip()

        buttons=[
            [InlineKeyboardButton(text="Voltar", callback_data="voltar")]
        ]
        keyboard = InlineKeyboardMarkup(buttons)
        
        update.callback_query.answer()
        update.callback_query.edit_message_text(text=f"Voce informou a nota: <strong>{invoice}</strong>\nEsses sao os boletos:", reply_markup=keyboard, parse_mode='HTML')
           
        result = self.financas.get_client_tickets(client_document, invoice)
        print(result)
        return self.END

    def ask_for_document(self, update, context):
        buttons=[
            [InlineKeyboardButton(text="Voltar", callback_data="voltar")]
        ]
        keyboard = InlineKeyboardMarkup(buttons)
        query_data = update.callback_query.data
        update.callback_query.answer()
        update.callback_query.edit_message_text(text="Digite o CNPJ/CPF do cliente ou selecione voltar", reply_markup=keyboard)
        return self.WRITING_DOCUMENT

    def return_to_parent_choice(self, update, context):
        return self.show_menu(update, context)
        
    def get_document(self, update, context):
        document = update.message.text.strip()
        return self.show_invoice(update, context)







