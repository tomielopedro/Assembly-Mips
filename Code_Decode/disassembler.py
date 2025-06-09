from typing import List, Dict
from utils import (
    get_json_data,
    get_file_instructions,
    salvar_decodificacoes,
    buscar_chave
)
from Instrucao import InstrucaoTipoR, InstrucaoTipoI, InstrucaoTipoJ


# ───────────────────────────────────────────────────────────────
# Funções auxiliares para desmontagem
# ───────────────────────────────────────────────────────────────

def binarizar_instrucoes(hex_list: List[str]) -> List[str]:
    """
    Converte lista de strings hexadecimais em strings binárias de 32 bits.
    """
    hex_decimal = list(map(lambda x: int(x, 16), hex_list))
    return list(map(lambda x: f'{x:032b}', hex_decimal))


def desmontar_R(binary: str, registers: Dict[str, int], instructions_r: Dict[str, int]) -> InstrucaoTipoR:
    """
    Desmonta instrução tipo R a partir de binário.
    """
    opcode = int(binary[:6])
    rs = buscar_chave(int(binary[6:11], 2), registers)
    rt = buscar_chave(int(binary[11:16], 2), registers)
    rd = buscar_chave(int(binary[16:21], 2), registers)
    shamt = int(binary[21:26], 2)
    funct = buscar_chave(int(binary[26:32], 2), instructions_r)

    if shamt != 0:
        rt = shamt  # para instruções como sll

    return InstrucaoTipoR(str(opcode), rs, rt, rd, shamt, funct)


def desmontar_I(binary: str, i: int, registers: Dict[str, int], instructions_i: Dict[str, int],
                labels_dict: Dict[str, int]) -> InstrucaoTipoI:
    """
    Desmonta instrução tipo I a partir de binário.
    """
    opcode = buscar_chave(int(binary[:6], 2), instructions_i)
    rs = buscar_chave(int(binary[6:11], 2), registers)
    rt = buscar_chave(int(binary[11:16], 2), registers)
    immediate = int(binary[16:], 2)

    # Trata branches como beq, bne, etc.
    branches = ["beq", "bne", "blez", "bgtz"]
    if opcode in branches:
        posicao = immediate + i + 1
        immediate_hex = hex(posicao)
        labels_dict[f'{immediate_hex}: '] = posicao
        immediate = immediate_hex

    return InstrucaoTipoI(opcode, opcode, rt, rs, immediate)


def desmontar_J(binary: str, instructions_j: Dict[str, int], labels_dict: Dict[str, int]) -> InstrucaoTipoJ:
    """
    Desmonta instrução tipo J a partir de binário.
    """
    opcode = buscar_chave(int(binary[:6], 2), instructions_j)
    address = int(binary[6:], 2) << 2
    address_hex = hex(address)
    idx_instrucao = (address - 0x00400000) // 4
    if address_hex=='0x400000': address_hex= 'main'
    labels_dict[f'{address_hex}: '] = idx_instrucao

    return InstrucaoTipoJ(opcode, opcode, address_hex)


# ───────────────────────────────────────────────────────────────
# Função principal da desmontagem
# ───────────────────────────────────────────────────────────────

def desmontar_arquivo(caminho_hex: str):
    """
    Orquestra a desmontagem do arquivo .txt contendo códigos hexadecimais MIPS.
    Salva as instruções ASM em 'data/to_asm.txt'.
    """
    # Carrega dados de instruções e registradores
    mips_dict = get_json_data('data/mips.json')
    registers = mips_dict['registers']
    instructions_i = mips_dict['instructions_i']
    instructions_r = mips_dict['instructions_r']
    instructions_j = mips_dict['instructions_j']

    # Lê e converte as instruções HEX para binário
    instrucoes_hexa = get_file_instructions(caminho_hex)
    hex_binary = binarizar_instrucoes(instrucoes_hexa)

    asm_list = []
    labels_dict: Dict[str, int] = {}

    # Loop para desmontar cada instrução
    for i, binary in enumerate(hex_binary):
        opcode_bin = binary[:6]

        if opcode_bin == '000000':  # Tipo R
            instr_obj = desmontar_R(binary, registers, instructions_r)
        elif opcode_bin in ['000010', '000011']:  # Tipo J
            instr_obj = desmontar_J(binary, instructions_j, labels_dict)
        else:  # Tipo I
            instr_obj = desmontar_I(binary, i, registers, instructions_i, labels_dict)

        asm_list.append(instr_obj.asm_format())

    # Adiciona labels no código ASM
    for label, index in labels_dict.items():
        asm_list[index] = label + asm_list[index]
    if 'main: ' not in labels_dict.keys():  asm_list[0] = f'main: {asm_list[0]}'
    asm_list.insert(0, '.text')
    asm_list.insert(1, '.globl main')

    # Salva resultado
    salvar_decodificacoes('output/asm.asm', asm_list)
    print('===== ASM =====')
    for cod in asm_list:
        print(cod)
    print('===============')
    print("\nDesmontagem concluída com sucesso!")
    print("Saída salva em: output/to_asm.asm")

if __name__ == '__main__':
    desmontar_arquivo('data/hexa.txt')