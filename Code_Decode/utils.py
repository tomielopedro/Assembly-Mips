import json


def get_file_instructions(file):
    with open(file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines if line.strip() != '' ]
        lines = list(filter(lambda x: not x.startswith('.'), lines))
    return lines


def get_json_data(file):
    with open(file, 'r') as f:
        return json.load(f)


def salvar_decodificacoes(file, lista):
    with open(file, 'w') as f:
        for l in lista:
            f.write(f'{l}\n')


def buscar_chave(valor, dict):
    for k, v in dict.items():
        if v == valor:
            return k


def construir_labels(instrucoes_asm):
    return {
        linha[0].rstrip(':'): i
        for i, linha in enumerate(instrucoes_asm)
        if linha[0].endswith(':')
    }


def calcular_deslocamento(start, end, label, instrucoes_asm):
    deslocamneto = 0
    for i in range(start, end):

        linha = instrucoes_asm[i]  # linha do código
        instrucao = linha[0]# primeiro elemento da linha instrucao



        if instrucao.startswith(label):
            instrucao = linha[1]  # a instrucao recebe o segundo elemento da lista caso o primeiro seja o label
        if instrucao == 'la' or instrucao == 'li':  # verifica se é a instrucao sw ou lw pq ela incrementa 2 no deslocamento
            deslocamneto += 2
            continue  # avança pr
        deslocamneto += 1
    return deslocamneto

