from utils import get_json_data
from utils import get_file_instructions
from Instrucao import *

instrucoes_asm = get_file_instructions('data/asm.txt')
instrucoes_asm = [instruct.replace(',', '').split(' ') for instruct in instrucoes_asm]
instrucoes_hexa = get_file_instructions('data/hexa.txt')

mips_dict = get_json_data('data/mips.json')
registers = mips_dict.get('registers')
instructions_i = mips_dict.get('instructions_i')
instructions_r = mips_dict.get('instructions_r')
instructions_j = mips_dict.get('instructions_j')

print(instrucoes_asm)
print(instrucoes_hexa)
print(instructions_i)
print(instructions_j)
print(instructions_r)
print(registers)

def salvar_decodificacoes(lista):
    with open('data/asm_to_hexa', 'a') as f:
        for l in lista:
            f.write(f'{l}\n')
labels_dict = {
    instrucao[0].rstrip(':'): i
    for i, instrucao in enumerate(instrucoes_asm)
    if instrucao[0].endswith(':')
}


def calcular_deslocamento(start, end, label):
    deslocamneto = 0
    for i in range(start, end):
        linha = instrucoes_asm[i]  # linha do código
        instrucao = linha[0]  # primeiro elemento da linha instrucao

        if instrucao.startswith(label):
            instrucao = linha[1]  # a instrucao recebe o segundo elemento da lista caso o primeiro seja o label
        if instrucao == 'la' or instrucao == 'li':  # verifica se é a instrucao sw ou lw pq ela incrementa 2 no deslocamento
            deslocamneto += 2
            continue  # avança pr
        deslocamneto += 1
    return deslocamneto




print(labels_dict)
print('========================')
hexa_list = []
for c, instrucoes in enumerate(instrucoes_asm):

    for i, instrucao in enumerate(instrucoes):
        if instrucao in instructions_r.keys():
            opcode = "000000"
            shampt = 0
            print('========================')
            if instrucoes[i+1] in registers.keys():
                print(instrucoes[i+1])
                rs = registers[instrucoes[i+1]]
            if instrucoes[i+2] in registers.keys():
                print(instrucoes[i + 2])
                rt = registers[instrucoes[i+2]]
            if instrucoes[i+3] in registers.keys():
                print(instrucoes[i + 3])
                rd = registers[instrucoes[i+3]]
            else:
                if instrucoes[i + 3].isdigit():
                    rt, rd = 0, rt
                    shampt = int(instrucoes[i + 3])

            function = instructions_r[instrucao]
            inst = InstrucaoTipoR(instrucao, rs, rt, rd, shampt, function)
            binario = inst.binary_format()
            hexa = inst.hexa_format()
            print(inst)
            print(f'Binario: {binario} Tamanho -> {len(binario)}')
            print('Hexadecimal: ', hexa)
            hexa_list.append(hexa)

        if instrucao in instructions_i.keys():

            opcode = instructions_i[instrucao]
            print('========================')
            if instrucoes[i+1] in registers.keys():
                rs = registers[instrucoes[i+1]]
            if instrucoes[i+2] in registers.keys():
                rt = registers[instrucoes[i+2]]
                if instrucoes[i + 3].isdigit():
                    imediate = int(instrucoes[i + 3])
                else:
                    if instrucoes[i + 3] in labels_dict.keys():

                        pos_label = labels_dict[instrucoes[i + 3]] # calcular o endereco
                        if c > pos_label:
                            deslocamento = calcular_deslocamento(pos_label, c+1, instrucoes[i + 3])
                            deslocamento *= -1
                        else:
                            deslocamento = calcular_deslocamento(c+2, pos_label+1, instrucoes[i + 3])
                        print('deslocamento final:', deslocamento)
                        imediate = deslocamento
                        rs, rt = rt, rs # inverte a ordem se bor condicional
            else:
                if instrucoes[i+2][0].isdigit():
                    rt = registers[instrucoes[i+2][1:].replace('(', '').replace(')', '')]
                    imediate = int(instrucoes[i+2][0])

            inst = InstrucaoTipoI(nome=instrucao, opcode=opcode, rt=rt, rs=rs,immediate=imediate)

            binario = inst.binary_format()
            hexa = inst.hexa_format()
            print(inst)
            print('Binario: ', binario)
            print('Hexadecimal: ', hexa)
            print(f'Binario: {binario} Tamanho -> {len(binario)}')
            hexa_list.append(hexa)

        if instrucao in instructions_j.keys():
            opcode = instructions_j[instrucao]
            print(instrucao)
            if instrucoes[i+1] in labels_dict.keys():
                print(c)
                label_pos = labels_dict[instrucoes[i+1]]
                adress = calcular_deslocamento(1, label_pos, instrucoes[i+1])*4
                instruct_j = InstrucaoTipoJ(instrucao, opcode, adress)

                print(instruct_j.binary_format())
                hexa= instruct_j.hexa_format()
                hexa_list.append(hexa)




salvar_decodificacoes(hexa_list)

print(labels_dict)





