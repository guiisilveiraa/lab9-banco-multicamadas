from decimal import Decimal, InvalidOperation

from model import Cliente, Conta


class BancoService:
    def __init__(self, banco):
        self.banco = banco

    def converter_valor(self, texto):
        try:
            valor = Decimal(str(texto).replace(",", "."))

            if not valor.is_finite():
                raise ValueError

            if valor != valor.quantize(Decimal("0.01")):
                raise ValueError

            return valor

        except (InvalidOperation, ValueError):
            raise ValueError(
                "Informe um valor válido com até duas casas decimais."
            )

    def criar_conta(self, nome, cpf, saldo_texto):
        nome = nome.strip()
        cpf = cpf.strip()

        if not nome or not cpf:
            raise ValueError("Preencha nome e CPF.")

        saldo = self.converter_valor(saldo_texto)

        if saldo < 0:
            raise ValueError("O saldo inicial não pode ser negativo.")

        cliente = Cliente(nome, cpf)

        conta = Conta(
            numero=self.banco.proximo_numero(),
            cliente=cliente,
            saldo=saldo,
        )

        conta.historico.append(
            f"Abertura da conta: R$ {saldo:.2f}"
        )

        self.banco.salvar(conta)
        return conta

    def consultar_conta(self, numero_texto):
        try:
            numero = int(numero_texto)
        except (ValueError, TypeError):
            raise ValueError("Informe um número de conta válido.")

        conta = self.banco.buscar(numero)

        if conta is None:
            raise ValueError("Conta não encontrada.")

        return conta

    def depositar(self, numero, valor_texto):
        conta = self.consultar_conta(numero)
        valor = self.converter_valor(valor_texto)

        if valor <= 0:
            raise ValueError("O depósito deve ser maior que zero.")

        conta.saldo += valor
        conta.historico.append(f"Depósito: +R$ {valor:.2f}")

        self.banco.salvar(conta)
        return conta

    def sacar(self, numero, valor_texto):
        conta = self.consultar_conta(numero)
        valor = self.converter_valor(valor_texto)

        if valor <= 0:
            raise ValueError("O saque deve ser maior que zero.")

        if valor > conta.saldo:
            raise ValueError("Saldo insuficiente.")

        conta.saldo -= valor
        conta.historico.append(f"Saque: -R$ {valor:.2f}")

        self.banco.salvar(conta)
        return conta

    def consultar_historico(self, numero):
        conta = self.consultar_conta(numero)
        return list(conta.historico)