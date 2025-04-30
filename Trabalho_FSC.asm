# Trabalho 1 de Fundamentos de Sistemas Computacionais
# Alunos: Pedro Tomielo e Ighor Telles
# Professor: Fabiano Hessel
# Instituição: PUCRS
# --------------------------------------------------------------------------------------------------------------------------
.data
    msg1: .asciiz "\n Informe o tamanho do vetor: "
    msg2: .asciiz "Informe os elementos do vetor: "
    msg3: .asciiz "Quantidade de padroes contabilizados: "
    msg4: .asciiz "Elementos no vetor: "
    l1: .asciiz ">> Nenhum Padrao Encontrado :( \n"
    l2: .asciiz ">> Um padrão encontrado :)\n"
    l3: .asciiz ">> Buscando padroes...\n"
    pula_linha: .asciiz "\n"
    espaco_em_branco: .asciiz ", "
    linha: .asciiz "#------------------------------------------#\n"
    
    vetDados: 
    .align 2
    .space 200
    	
    vetPadrao: 
    .align 2
    .space 20

.text 
.globl main

main:	
	# Abridando 2 posições na pilha
	addi $sp, $sp, -8
    	
    	# Chamando a função 'carrega_vetor' para o vetor de Dados
    	la $s6, vetDados 	# Guarda o endereço do vetDados em $s6
    	sw $s6, 0($sp) 		# Faz um 'push' do endereço do vetDados na pilha
    	jal carrega_vetor 	# Chama a função
   	lw $s0, 4($sp) 		# Faz um 'pop' do retorno da função (tamanho de vetDados)
    	
    	# Chamando a função 'carrega_vetor' para o vetor Padrão
    	la $s7, vetPadrao  	# Guarda o endereço do vetPadrao em $s7
    	sw $s7, 0($sp) 		# Faz um 'push' do endereço do vetPadrao na pilha
    	jal carrega_vetor 	# Chama a função
    	lw $s1, 4($sp) 		# Faz um 'pop' do retorno da função (tamanho de vetPadrao)
    	
    	# Registrando valores para servirem de variáveis auxiliares
    	move $s2, $zero 	# contabiliza padrao
    	move $s3, $zero 	# posição do vetor dados
    	move $s4, $zero 	# posição do vetor padrão
	
	# Ajuste a referência do endereço da pilha
    	addi $sp, $sp, 8
    	
    	addu $s5, $s3, $s1 # posDados+TamanhoVetPadrao
    	
loop_principal:
	# Abre 7 espaços na pilha para a passagem dos parâmetros
    	addi $sp, $sp, -28
    	
    	# while (posDados+TamanhoVetPadrao) <= TamanhoVetorDados
    	bgt $s5, $s0, finaliza_loop	
    	sw $s6, 0($sp)	# endereço do vetor dados
    	sw $s3, 4($sp)  # posição do vetor dados
    	sw $s7, 8($sp)  # endereço do vetor padrão
    	sw $s4, 12($sp) # posição do vetor padrão
    	sw $s1, 16($sp) # tamanho do vetor padrão
    	
    	# Chama a função encontra_padrao
    	jal encontra_padrao
   	
   	# Calcula a posição do retorno da função na pilha -> 28 x tamanhoVetPadrao - 20
    	li $t0, 28		# Atribui o valor de 28 a $t0
    	mul $t0, $t0, $s1	# Multiplica o valor de $t0 pelo valor do tamanho do vetor padrão ($t0 = 28 x tamanhoVetPadrao)
    	addi $t0, $t0, -20	# Subtrai 20 do valor de $t0 (28 x tamanhoVetPadrao - 20)
    	subu $sp, $sp, $t0	# Ajusta o valor de $sp para o endereço do retorno da função 
    	lw $t0, 0($sp)  	# Faz um 'pop' do retorno da função na pilha
    
    	addu $s2, $s2, $t0	# Salva o valor do retorno da função em $s2
    
    	addi $s3, $s3, 1	# Passa para a próxima posição do vetor de dados
    	addu $s5, $s3, $s1	# Incrementar o contador (posDados+TamanhoVetPadrao)
    	j loop_principal	# Volta para o loop
    	
	finaliza_loop:
		li $v0, 4         
        	la $a0, linha
       		syscall
    		# Printa a mensagem "Quantidade de padroes contabilizados: " na tela 
    		li $v0, 4
    		la $a0, msg3
    		syscall
    		
    		# Printa o valor acumulado em $s2 (quantidade de padrões encontrados)
    		li $v0, 1
    		move $a0, $s2
    		syscall
	
		# Encerra o programa
    		li $v0, 10
    		syscall
    
# ------------------------------------------------------------------------------------------------------------------------------------------
carrega_vetor:
    	# Faz um 'pop' na pilha para pegar o vetor passado como parâmetro
    	lw $t0, 0($sp)
	
	# Printa a mensagem "Informe o tamanho do vetor: " na tela
    	li $v0, 4
    	la $a0, msg1
    	syscall
    	
    	# Lê o tamanho do vetor solicitado ao usuário
    	li $v0, 5
    	syscall
    	# Salva o tamanho do vetor em #t1
   	move $t1, $v0 
   	
   	# Printa uma linha na tela apenas por questão de estética
   	li $v0, 4         
        la $a0, linha
       	syscall
    	
    	# Incializa o índice do loop para adicionar elementos ao vetor
    	move $t2, $zero
	loop:	
		# while i <= tamanho do Vetor
    		beq $t2, $t1, fim_loop
		
		# Printa a mensagem "Quantidade de padroes contabilizados: " na tela
    		li $v0, 4
    		la $a0, msg2
    		syscall
		
		# Lê o elemento informado pelo usuário e salva em $t3
    		li $v0, 5
    		syscall
    		move $t3, $v0
		
		# Salva o elemento na posição 'i' do vetor (vetor[i])
    		sll $t5, $t2, 2
    		addu $t4, $t0, $t5
    		sw $t3, 0($t4)
		
		# Incrementa o valor de 'i'
    		addi $t2, $t2, 1
    		j loop

	fim_loop:
		# Printa um espaço na tela
		li $v0, 4         
        	la $a0, pula_linha
       		syscall
       		
		# loop para printar os valores registrados do vetor para debugar o programa
		move $t2, $zero
        	li $v0, 4         
        	la $a0, msg4
        	syscall
        
    		loop_imprime:
        		beq $t2, $t1, fim_loop_imprime
        		
        		sll $t5, $t2, 2
        		addu $t4, $t0, $t5
        		
        		# Carrega o elemento vet[i] e printa na tela
        		lw $t6, 0($t4)   
        		li $v0, 1
        		move $a0, $t6
        		syscall
			
			# Printa um espaço em branco na tela
        		li $v0, 4         
        		la $a0, espaco_em_branco
        		syscall
        		
        		addi $t2, $t2, 1	# incrementa o iterador
        		j loop_imprime
			
		fim_loop_imprime:
			# Printa um espaço na tela
			li $v0, 4         
        		la $a0, pula_linha
       			syscall
       			
       			# Printa uma linha na tela
			li $v0, 4         
        		la $a0, linha
       			syscall
        		
			# Faz um 'push' do tamanho do vetor na pilha
			sw $t1, 4($sp)
    			
    			# Retorna ao endereço registrado em $ra
    			jr $ra

# ------------------------------------------------------------------------------------------------------------------------------------------
encontra_padrao:
	# Abre 7 espaços na pilha
    	addi $sp, $sp, -28
    	
    	# Salva o endereço de $ra no topo da pilha       
    	sw $ra, 24($sp)          
    
    	# Faz um 'pop' dos argumentos da pilha (passados dentro do loop principal)
    	lw $t1, 28($sp)          # vetDados 
    	lw $t2, 32($sp)          # posDados
    	lw $t3, 36($sp)          # vetPadrao
    	lw $t4, 40($sp)          # posPadrao
    	lw $t5, 44($sp)          # tamVetPadrao

   	# Calcula endereços e carrega valores
    	sll $t6, $t2, 2
    	addu $t6, $t6, $t1
    	lw $t7, 0($t6)		# Elemento 'i' do vetor dados
    
    	sll $t6, $t4, 2
    	addu $t6, $t6, $t3
    	lw $t8, 0($t6)           # Elemento 'i' do vetor padrão
	
	# if vetPadrao[i] == vetDados[i]
    	bne $t8, $t7, nenhum_padrao
    	
    	addi $t9, $t5, -1	# Subtrai 1 do tamVetPadrao
    	
    	# if posPadrao != tamVetPadrao
    	beq $t4, $t9, padrao_encontrado
    
    	# Caso recursivo
    	# Printa '>> Buscando padroes...' na tela para ajudar no acompanhamento do código 
    	li $v0, 4
    	la $a0, l3
    	syscall
    
    	# Prepara argumentos para chamada recursiva
    	sw $t1, 0($sp)           # Faz um push do vetDados
    	
    	addi $t0, $t2, 1	 # posDados += 1
    	sw $t0, 4($sp)           # Faz um push do posDados
    	
    	sw $t3, 8($sp)           # Faz um push do vetPadrao
    	
    	addi $t0, $t4, 1	 # posPadrao += 1
    	sw $t0, 12($sp)          # Faz um push do posPadrao
    	
    	sw $t5, 16($sp)          # Faz um push do tamVetPadrao
    
    	jal encontra_padrao      # Chama a função de forma recursiva
    
    	lw $ra, 24($sp)          # Restaura o endereço de $ra da pilha
    	addi $sp, $sp, 28        # Restaura a pilha
    	jr $ra			
    
	nenhum_padrao: # Caso em que não encontrou um padrão
    		# Printa '>> Nenhum Padrao Encontrado :(' na tela para ajudar no acompanhamento do código
    		li $v0, 4
    		la $a0, l1
    		syscall
		
		# Retorna o valor de 0
    		sw $zero, 20($sp)        # Faz um 'push' do retorno da função na pilha
    		lw $ra, 24($sp)          # Faz um 'pop' do endereço de $$ra da pilha
    		jr $ra

	padrao_encontrado: # Caso em que encontrou um padrão
   		# Printa '>> Um padrão encontrado :)' na tela para ajudar no acompanhamento do código
    		li $v0, 4
    		la $a0, l2
    		syscall
    		
    		# Retorna o valor de 1
    		li $t9, 1		# Atribui o valor de 1 a $t9
    		sw $t9, 20($sp)         # Faz um 'push' do retorno da função na pilha
    		lw $ra, 24($sp)   	# Faz um 'pop' do endereço de $$ra da pilha
    		addi $sp, $sp, 28       # Restaura a pilha 
    		jr $ra
