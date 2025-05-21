from utils import get_json_data
from utils import get_file_instructions

instrucoes_asm = get_file_instructions('data/asm.txt')
instrucoes_hexa = get_file_instructions('data/hexa.txt')
opcode_i = get_json_data('data/opcode_i.json')
opcode_j = get_json_data('data/opcode_j.json')
funct_r = get_json_data('data/funct_r.json')
registers = get_json_data('data/registers.json')

print(instrucoes_asm)
print(instrucoes_hexa)

print(opcode_i)
print(opcode_j)
print(funct_r)
print(registers)


