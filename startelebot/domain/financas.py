from datetime import date
from startelebot.infrastructure.dbservice import DbService

class Financa(): 

    def __init__(self):
        self.db_service = DbService()
    
    def get_client_name(self, document):
        try:
            client_data = self.db_service.get_client_data(document)
            return client_data.get('name')
        except:
            pass
    
    def get_unpaid_invoices(self, document):
        try:
            client_code =  self.db_service.get_client_data(document).get("client_code")
           
            result = self.db_service.get_unpaid_invoices(client_code)

            invoices = []
            for invoice in result:
                invoice_number = invoice.get("invoice_number")
                invoice_series = invoice.get("invoice_series")
                invoices.append(f"{invoice_number} - {invoice_series}" )
            return invoices
        except:
            pass

    def get_client_tickets(self, client_document, invoice):
        try:
            result = self.db_service.get_unpaid_ticket(client_document, invoice)
            
            tickets = []

            for ticket in result:
                ticket = ticket.get("DATA_VENCIMENTO")
                tickets.append(f"{ticket}" )
            return tickets
        except:
            pass