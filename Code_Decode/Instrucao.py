from abc import ABC, abstractmethod


class InstrucaoMIPS(ABC):
    """
    Classe abstrata base para representar instruções MIPS.

    A classe define a interface para as representações binária, hexadecimal
    e assembly de uma instrução.
    """
    def __init__(self, nome: str, tipo: str):
        """
        Inicializa os atributos comuns de todas as instruções MIPS.

        :param nome: Nome da instrução (ex: 'add', 'lw', 'j').
        :param tipo: Tipo da instrução ('R', 'I' ou 'J').
        """
        self.nome = nome
        self.tipo = tipo

    @abstractmethod
    def binary_format(self) -> str:
        """
        Método abstrato que deve retornar a representação binária da instrução.
        """
        pass

    def hexa_format(self) -> str:
        """
        Converte a representação binária da instrução para hexadecimal.

        :return: String hexadecimal com 8 caracteres.
        """
        return hex(int(self.binary_format(), 2))[2:].zfill(8)

    def asm_format(self) -> str:
        """
        Retorna a representação da instrução no formato assembly.
        Deve ser sobrescrito nas subclasses.
        """
        pass

    def __str__(self):
        """
        Representação legível da instrução.

        :return: Nome e tipo da instrução.
        """
        return f'Função: {self.nome} Tipo: {self.tipo}'


# ---------------------- Tipo R ----------------------

class InstrucaoTipoR(InstrucaoMIPS):
    """
    Classe que representa instruções do tipo R no formato MIPS.
    """
    def __init__(self, nome, rs, rt, rd, shamt, funct):
        """
        Inicializa os campos de uma instrução tipo R.

        :param nome: Nome da instrução.
        :param rs: Registrador fonte.
        :param rt: Registrador destino.
        :param rd: Registrador de destino do resultado.
        :param shamt: Quantidade de deslocamento (shift amount).
        :param funct: Código da função (funct).
        """
        super().__init__(nome, 'R')
        self.opcode = "000000"
        self.rs = rs
        self.rt = rt
        self.rd = rd
        self.shamt = shamt
        self.funct = funct

    def binary_format(self) -> str:
        """
        Gera o código binário da instrução tipo R.

        :return: String binária de 32 bits.
        """
        return f"{self.opcode}{self.rt:05b}{self.rd:05b}{self.rs:05b}{self.shamt:05b}{self.funct:06b}"

    def asm_format(self) -> str:
        """
        Formato legível em assembly.

        :return: String no formato 'funct rd, rs, rt'.
        """
        return f'{self.funct} {self.rd}, {self.rs}, {self.rt}'

    def __str__(self):
        """
        Retorna todos os campos da instrução para depuração.

        :return: Detalhes da instrução tipo R.
        """
        return f'NOME: {self.nome} OPCODE: {self.opcode}; RS: {self.rs}; RT: {self.rt}; RD {self.rd} SHAMPT: {self.shamt} FUNCT {self.funct}'


# ---------------------- Tipo I ----------------------

class InstrucaoTipoI(InstrucaoMIPS):
    """
    Classe que representa instruções do tipo I no formato MIPS.
    """
    def __init__(self, nome, opcode, rt, rs, immediate):
        """
        Inicializa os campos de uma instrução tipo I.

        :param nome: Nome da instrução.
        :param opcode: Código da operação.
        :param rt: Registrador destino.
        :param rs: Registrador fonte.
        :param immediate: Valor imediato (16 bits, pode ser negativo).
        """
        super().__init__(nome, 'I')
        self.nome = nome
        self.opcode = opcode
        self.rs = rs
        self.rt = rt
        self.immediate = immediate

    def binary_format(self) -> str:
        """
        Gera a codificação binária da instrução tipo I, incluindo
        o tratamento de números negativos em complemento de dois.

        :return: String binária de 32 bits.
        """
        if self.immediate < 0:
            imm_val = (1 << 16) + self.immediate
        else:
            imm_val = self.immediate
        imm_bin = f"{imm_val:016b}"

        return f"{self.opcode:06b}{self.rt:05b}{self.rs:05b}{imm_bin}"

    def asm_format(self) -> str:
        """
        Retorna o formato assembly da instrução tipo I.

        :return: String como 'nome rt, rs, immediate' ou 'nome rt, offset(rs)' para lw/sw.
        """
        if self.opcode == 'lw' or self.opcode == 'sw':
            return f'{self.opcode} {self.rt}, {self.immediate}({self.rs})'
        return f'{self.opcode} {self.rt}, {self.rs}, {self.immediate}'

    def __str__(self):
        """
        Detalhes completos da instrução tipo I para depuração.

        :return: Campos da instrução tipo I.
        """
        return f'NOME: {self.nome} OPCODE: {self.opcode}; RS: {self.rs}; RT: {self.rt}; IMEDIATE: {self.immediate}'


# ---------------------- Tipo J ----------------------

class InstrucaoTipoJ(InstrucaoMIPS):
    """
    Classe que representa instruções do tipo J no formato MIPS.
    """
    def __init__(self, nome, opcode, address):
        """
        Inicializa os campos de uma instrução tipo J.

        :param nome: Nome da instrução.
        :param opcode: Código da operação.
        :param address: Endereço de destino.
        """
        super().__init__(nome, 'J')
        self.opcode = opcode
        self.address = address

    def binary_format(self) -> str:
        """
        Constrói o código binário da instrução tipo J, com ajuste
        de base para 0x00400000 e extração de 26 bits.

        :return: String binária de 32 bits.
        """
        adress = self.address + 0x00400000
        adress = f'{adress:032b}'
        adress = adress[4:30]
        return f"{self.opcode:06b}{adress}"

    def asm_format(self) -> str:
        """
        Formato assembly da instrução J.

        :return: String no formato 'nome address'.
        """
        return f'{self.opcode} {self.address}'

    def __str__(self):
        """
        Detalhes completos da instrução tipo J.

        :return: Campos da instrução tipo J.
        """
        return f'NOME: {self.nome} OPCODE: {self.opcode}; ADDRESS: {self.address}'
