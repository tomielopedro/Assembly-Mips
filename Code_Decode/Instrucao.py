from abc import ABC, abstractmethod


class InstrucaoMIPS(ABC):
    """
    Classe abstrata base para instruções MIPS.
    """
    def __init__(self, nome: str, tipo: str):
        self.nome = nome
        self.tipo = tipo

    @abstractmethod
    def binary_format(self) -> str:
        """
        Retorna a codificação binária da instrução.
        """
        pass

    def hexa_format(self) -> str:
        return hex(int(self.binary_format(), 2))[2:].zfill(8)

    def __str__(self):
        return f'Função: {self.nome} Tipo: {self.tipo}'

# ---------------------- Tipo R ----------------------


class InstrucaoTipoR(InstrucaoMIPS):
    def __init__(self, nome, rs, rt, rd, shamt, funct):
        super().__init__(nome, 'R')
        self.opcode = "000000"
        self.rs = rs
        self.rt = rt
        self.rd = rd
        self.shamt = shamt
        self.funct = funct

    def binary_format(self) -> str:
        return f"{self.opcode}{self.rt:05b}{self.rd:05b}{self.rs:05b}{self.shamt:05b}{self.funct:06b}"

    def __str__(self):
        return f'NOME: {self.nome} OPCODE: {self.opcode}; RS: {self.rs}; RT: {self.rt}; RD {self.rd} SHAMPT: {self.shamt} FUNCT {self.funct}'




# ---------------------- Tipo I ----------------------


class InstrucaoTipoI(InstrucaoMIPS):
    def __init__(self, nome, opcode, rt, rs, immediate):
        super().__init__(nome, 'I')
        self.nome = nome
        self.opcode = opcode
        self.rs = rs
        self.rt = rt
        self.immediate = immediate

    def binary_format(self) -> str:
        # Gera o binário do campo immediate em complemento de 2
        if self.immediate < 0:
            imm_val = (1 << 16) + self.immediate
        else:
            imm_val = self.immediate
        imm_bin = f"{imm_val:016b}"

        return f"{self.opcode:06b}{self.rt:05b}{self.rs:05b}{imm_bin}"
    def __str__(self):
        return f'NOME: {self.nome} OPCODE: {self.opcode}; RS: {self.rs}; RT: {self.rt}; IMEDIATE: {self.immediate}'




# ---------------------- Tipo J ----------------------


class InstrucaoTipoJ(InstrucaoMIPS):
    def __init__(self, nome, opcode, address):
        super().__init__(nome, 'J')
        self.opcode = opcode
        self.address = address

    def binary_format(self) -> str:
        adress = self.address + 0x00400000
        adress = f'{adress:032b}'
        adress = adress[4:30]
        return f"{self.opcode:06b}{adress}"

    def __str__(self):
        return f'NOME: {self.nome} OPCODE: {self.opcode}; ADDRESS: {self.address}'

if __name__ == "__main__":
    # ADD R-type: add $s1, $s2, $s3
    add_instr = InstrucaoTipoR("add", rs=18, rt=19, rd=17, shamt=0, funct=10)
    print("ADD:", add_instr.binary_format())

    # LW I-type: lw $t0, 4($s3)
    lw_instr = InstrucaoTipoI("lw", opcode="100011", rs=19, rt=8, immediate=4)
    print("LW:", lw_instr.binary_format())

    # J J-type: j 0x004000
    j_instr = InstrucaoTipoJ("j", opcode="000010", address=0x004000)
    print("J:", j_instr.binary_format())