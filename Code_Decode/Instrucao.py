from abc import ABC, abstractmethod


class InstrucaoMIPS(ABC):
    """
    Classe abstrata base para instruções MIPS.
    """
    def __init__(self, nome: str):
        self.nome = nome

    @abstractmethod
    def binary_format(self) -> str:
        """
        Retorna a codificação binária da instrução.
        """
        pass


# ---------------------- Tipo R ----------------------


class InstrucaoTipoR(InstrucaoMIPS):
    def __init__(self, nome, rs, rt, rd, shamt, funct):
        super().__init__(nome)
        self.opcode = "000000"
        self.rs = rs
        self.rt = rt
        self.rd = rd
        self.shamt = shamt
        self.funct = funct

    def encode(self) -> str:
        return f"{self.opcode}{self.rs:05b}{self.rt:05b}{self.rd:05b}{self.shamt:05b}{self.funct}"

# ---------------------- Tipo I ----------------------


class InstrucaoTipoI(InstrucaoMIPS):
    def __init__(self, nome, opcode, rs, rt, immediate):
        super().__init__(nome)
        self.opcode = opcode
        self.rs = rs
        self.rt = rt
        self.immediate = immediate

    def encode(self) -> str:
        return f"{self.opcode}{self.rs:05b}{self.rt:05b}{self.immediate:016b}"

# ---------------------- Tipo J ----------------------


class InstrucaoTipoJ(InstrucaoMIPS):
    def __init__(self, nome, opcode, address):
        super().__init__(nome)
        self.opcode = opcode
        self.address = address

    def encode(self) -> str:
        return f"{self.opcode}{self.address:026b}"

if __name__ == "__main__":
    # ADD R-type: add $s1, $s2, $s3
    add_instr = InstrucaoTipoR("add", rs=18, rt=19, rd=17, shamt=0, funct="100000")
    print("ADD:", add_instr.encode())

    # LW I-type: lw $t0, 4($s3)
    lw_instr = InstrucaoTipoI("lw", opcode="100011", rs=19, rt=8, immediate=4)
    print("LW:", lw_instr.encode())

    # J J-type: j 0x004000
    j_instr = InstrucaoTipoJ("j", opcode="000010", address=0x004000)
    print("J:", j_instr.encode())