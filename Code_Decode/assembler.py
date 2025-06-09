import sys
from typing import List, Dict
from utils import (
    get_file_instructions,
    get_json_data,
    salvar_decodificacoes,
    calcular_deslocamento,
)
from Instrucao import InstrucaoTipoR, InstrucaoTipoI, InstrucaoTipoJ


# ───────────────────────────────────────────────────────────────
# Funções utilitárias para montagem de instruções
# ───────────────────────────────────────────────────────────────

def carregar_instrucoes(caminho: str) -> List[List[str]]:
    """
    Lê o arquivo .asm, remove vírgulas e separa cada linha em tokens.
    """
    linhas = get_file_instructions(caminho)
    return [linha.replace(',', '').split() for linha in linhas]


def mapear_labels(instrucoes: List[List[str]]) -> Dict[str, int]:
    """
    Retorna um dicionário associando cada label ao seu índice de linha.
    """
    return {
        tokens[0].rstrip(':'): i
        for i, tokens in enumerate(instrucoes)
        if tokens and tokens[0].endswith(':')
    }


# ───────────────────────────────────────────────────────────────
# Funções de montagem por tipo de instrução
# ───────────────────────────────────────────────────────────────

def montar_R(tokens: List[str]) -> InstrucaoTipoR:
    """
    Monta instruções do tipo R (register).
    Exemplo de tokens: [instrucao, reg1, reg2, reg3_ou_shamt]
    """
    instrucao, reg1, reg2, reg3 = tokens
    codigo_funct = instrucoes_R[instrucao]
    registrador_rs = registradores[reg1]

    if reg3.isdigit():  # Ex: sll
        shift_amount = int(reg3)
        registrador_rt = 0
        registrador_rd = registradores[reg2]
    else:
        shift_amount = 0
        registrador_rt = registradores[reg2]
        registrador_rd = registradores[reg3]

    return InstrucaoTipoR(
        nome=instrucao,
        rs=registrador_rs,
        rt=registrador_rt,
        rd=registrador_rd,
        shamt=shift_amount,
        funct=codigo_funct
    )


def montar_I(tokens: List[str], linha: int) -> InstrucaoTipoI:
    """
    Monta instruções do tipo I (immediate ou branch).
    """
    instrucao = tokens[0]
    codigo_opcode = instrucoes_I[instrucao]

    # Caso lw/sw: [instrucao, rt, offset(base)]
    if len(tokens) == 3 and '(' in tokens[2]:
        reg_rt = registradores[tokens[1]]
        desloc_str, base = tokens[2].split('(')
        base = base.rstrip(')')
        reg_base = registradores[base]
        return InstrucaoTipoI(instrucao, codigo_opcode, reg_base, reg_rt, int(desloc_str))

    # Caso imediato ou branch
    reg_rs = registradores[tokens[1]]
    reg_rt = registradores[tokens[2]]
    valor = tokens[3]

    if valor.lstrip('-').isdigit():
        imediato = int(valor)
    else:
        idx_label = labels_map[valor]
        if linha > idx_label:
            desloc = calcular_deslocamento(idx_label, linha + 1, valor, instrucoes_brutas)
            imediato = -desloc
        else:
            imediato = calcular_deslocamento(linha + 2, idx_label + 1, valor, instrucoes_brutas)

        # Inverte os registradores para branch
        reg_rs, reg_rt = reg_rt,reg_rs

    return InstrucaoTipoI(instrucao, codigo_opcode, reg_rt, reg_rs, imediato)


def montar_J(tokens: List[str]) -> InstrucaoTipoJ:
    """
    Monta instruções do tipo J (jump).
    """
    instrucao, label = tokens
    codigo_opcode = instrucoes_J[instrucao]
    idx_label = labels_map[label]
    endereco = calcular_deslocamento(0, idx_label, label, instrucoes_brutas)*4

    return InstrucaoTipoJ(instrucao, codigo_opcode, endereco)


# ───────────────────────────────────────────────────────────────
# Função principal
# ───────────────────────────────────────────────────────────────

def montar_arquivo(caminho_asm: str):
    global instrucoes_brutas, labels_map, registradores
    global instrucoes_I, instrucoes_R, instrucoes_J

    instrucoes_brutas = carregar_instrucoes(caminho_asm)
    labels_map = mapear_labels(instrucoes_brutas)

    dados_json = get_json_data('data/mips.json')
    registradores = dados_json['registers']
    instrucoes_I = dados_json['instructions_i']
    instrucoes_R = dados_json['instructions_r']
    instrucoes_J = dados_json['instructions_j']

    resultado_hex = []

    for i, tokens in enumerate(instrucoes_brutas):
        if not tokens or tokens[0].startswith('.'):
            continue
        if tokens[0].endswith(':'):
            tokens = tokens[1:]
        if not tokens:
            continue

        instr = tokens[0]
        if instr in instrucoes_R:
            instr_obj = montar_R(tokens)
        elif instr in instrucoes_I:
            instr_obj = montar_I(tokens, i)
        elif instr in instrucoes_J:
            instr_obj = montar_J(tokens)
        else:
            print(f"Instrução desconhecida '{instr}' na linha {i}")
            continue

        resultado_hex.append(instr_obj.hexa_format())

    salvar_decodificacoes('output/to_hexa.txt', resultado_hex)
    print('===== HEXADECIMAL =====')
    for cod in resultado_hex:
        print(cod)
    print('==================')
    print("\nMontagem concluída com sucesso!")
    print("Saída salva em: output/to_hexa.txt")



if __name__ == '__main__':
    montar_arquivo('data/asm.txt')
