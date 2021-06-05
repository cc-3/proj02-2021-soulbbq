beq s0 s0 start

badloop:
  addi sp, sp, -1
  beq x0, x0, badloop

start:
  addi s1, s1, 10
  blt s0, s1, label1
  beq x0, x0, badloop

label2:
  addi s1, s1, -20
  bltu s0, s1, end
  beq x0, x0, badloop

label1:
  addi s0, s0, 20
  blt s1, s0, label2
  beq x0, x0, badloop

end:
  add a0, x0, x0
