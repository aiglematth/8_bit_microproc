;
; Somme des 4 premiers entiers
;
;
; Organisation de la mémoire :
;   0 => Compteur total de la somme
;   1 => Compteur de l'entier actif
;
; Organisation des registres :
;   r1 => Stock du compteur total de la somme
;   r2 => Stock de l'adresse sur laquelle jmp tant que la somme n'est pas finie
;   r3 => Stock de l'entier actif
;   r4 => Stock de la valeur 1, pour incrémenter l'entier actif ou 251 pour faire la comparaison
;
load  r4, 1
load  r2, loop
xor   r3, r3, r3
or    r3, r3, r4
store @1, r3

loop:
    load  r3, @1
    add   r1, r1, r3
    load  r4, 1
    add   r3, r3, r4
    store @1, r3
    load  r4, 251
    add   r3, r3, r4
    jnz   r2, r3

store @0, r1