import os
import sys
from assembler import montar_arquivo
from disassembler import desmontar_arquivo
def exibir_menu():
    print("\n===== MIPS Assembly Tool =====")
    print("1. Montar código (ASM → HEX)")
    print("2. Desmontar código (HEX → ASM)")
    print("0. Sair")
    print("===============================")


def main():
    while True:
        exibir_menu()
        escolha = input("> Escolha uma opção: ")

        if escolha == '1':
            caminho = input(">> Digite o caminho do arquivo .asm: ").strip()
            if not os.path.exists(caminho):
                print(f">> Arquivo '{caminho}' não encontrado. <<")
            else:
                print("\n========== Resultado asm -> hexa ==========")
                montar_arquivo(caminho)

        elif escolha == '2':
            caminho = input(">> Digite o caminho do arquivo .txt com HEX: ").strip()
            if not os.path.exists(caminho):
                print(f">> Arquivo '{caminho}' não encontrado. <<")
            else:
                print("\n========== Resultado hexa -> asm ==========")
                desmontar_arquivo(caminho)

        elif escolha == '0':
            print(">> Encerrando.")
            break

        else:
            print(">> Opção inválida. Tente novamente.")

if __name__ == '__main__':
    main()
