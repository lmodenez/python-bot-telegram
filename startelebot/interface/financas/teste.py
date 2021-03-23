#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pyboleto
from pyboleto.bank.bradesco import BoletoBradesco
from pyboleto.pdf import BoletoPDF
import datetime

def print_bradesco():
    listaDadosBradesco = []
    for i in range(1):
        d = BoletoBradesco()
        d.carteira = '06'  # Contrato firmado com o Banco Bradesco
        d.cedente = 'Empresa ACME LTDA'
        d.cedente_documento = "102.323.777-01"
        d.cedente_endereco = ("Rua Acme, 123 - Centro - Sao Paulo/SP - " +
                              "CEP: 12345-678")
        d.agencia_cedente = '0278-0'
        d.conta_cedente = '43905-3'

        d.data_vencimento = datetime.date(2011, 1, 25)
        d.data_documento = datetime.date(2010, 2, 12)
        d.data_processamento = datetime.date(2010, 2, 12)

        d.instrucoes = [
            "- Linha 1",
            "- Sr Caixa, cobrar multa de 2% após o vencimento",
            "- Receber até 10 dias após o vencimento",
        ]
        d.demonstrativo = [
            "- Serviço Teste R$ 5,00",
            "- Total R$ 5,00",
        ]
        d.valor_documento = 2158.41

        d.nosso_numero = "1112011668"
        d.numero_documento = "1112011668"
        d.sacado = [
            "Cliente Teste %d" % (i + 1),
            "Rua Desconhecida, 00/0000 - Não Sei - Cidade - Cep. 00000-000",
            ""
        ]
        listaDadosBradesco.append(d)

    # Bradesco Formato normal - uma pagina por folha A4
    boleto = BoletoPDF('boleto-bradesco-formato-normal-teste.pdf')
    for i in range(len(listaDadosBradesco)):
        boleto.drawBoleto(listaDadosBradesco[i])
        boleto.nextPage()
    boleto.save()

def print_all():
    print("Pyboleto version: %s" % pyboleto.__version__)
    print("----------------------------------")
    print("     Printing Example Boletos     ")
    print("----------------------------------")

    print("Bradesco")
    print_bradesco()


    print("----------------------------------")
    print("Ok")


if __name__ == "__main__":
    print_all()
