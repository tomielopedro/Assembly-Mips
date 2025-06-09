.text
.globl main
main: or $t0, $t1, $t2
and $t0, $t1, $t2
sub $t0, $t1, $t2
beq $t2, $t1, 0x7
sltiu $t0, $t1, 2
lw $t0, 0($t0)
sw $t1, 0($t1)
0x7: j main
