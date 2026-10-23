from dataclasses import dataclass, field
from decimal import Decimal


@dataclass
class Cliente:
    nome: str
    cpf: str


@dataclass
class Conta:
    numero: int
    cliente: Cliente
    saldo: Decimal
    historico: list = field(default_factory=list)