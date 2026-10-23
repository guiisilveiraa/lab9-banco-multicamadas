class BancoDados:
    def __init__(self):
        self.contas = []

    def salvar(self, conta):
        for indice, existente in enumerate(self.contas):
            if existente.numero == conta.numero:
                self.contas[indice] = conta
                return

        self.contas.append(conta)

    def buscar(self, numero):
        for conta in self.contas:
            if conta.numero == numero:
                return conta

        return None

    def proximo_numero(self):
        return len(self.contas) + 1