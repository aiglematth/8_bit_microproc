# Notre jeu d'instructions

## Opérations logiques
- and  r1, r2, r3
- nand r1, r2, r3
- or   r1, r2, r3
- nor  r1, r2, r3
- xor  r1, r2, r3
- nxor r1, r2, r3
- not  r1, r2

## Opérations mathématiques
- add r1, r2, r3

## Opérations autres
- load r1, const
- load r1, from addr
- mov r1, r2
- store r1, r2
- store addr, r1
- jmp addr
- jmp r1
- jz  r1, r2
- jnz r1, r2

## 17 opérations : 5 bits car 2^5 = 32 (15 opérations de rab)

```
| 0-4   | 5-15    |
| instr | payload |
|       | 5-6     | 7-8     | 9-10    |
|       | R1      | R2      | R3      |

--> Largeur d'un mot d'instruction == 16 bits == 2 octets

00000 => add
00001 => and
00010 => or
00011 => nand
00100 => nor
00101 => xor
00110 => nxor
00111 => not

01000 => load r1, const
01001 => load r1, from addr
01010 => mov r1, r2
01011 => store r1, r2
01100 => store addr, r1

10000 => jmp addr
10001 => jmp r1
10010 => jz  r1, r2
10011 => jnz r1, r2
```