import tkinter as tk

from dados import BancoDados
from negocios import BancoService
from view import BancoView


def main():
    banco = BancoDados()
    servico = BancoService(banco)

    janela = tk.Tk()
    view = BancoView(janela, servico)

    janela.mainloop()


if __name__ == "__main__":
    main()