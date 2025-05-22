from utils import get_json_data
from utils import get_file_instructions

instrucoes_asm = get_file_instructions('data/asm.txt')
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


