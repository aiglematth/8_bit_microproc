"""
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
"""
# Imports
from copy import deepcopy
from re   import compile

# Fonctions
def sanify(code): return [line.strip().lower() for line in code.split("\n") if line.strip() != "" and not line.startswith(";")]
def complete(a):  return a + (16-len(a))*"0"

# Classes
class Compile():
    """
    Compilateur pour mon super microproc !!! Bientôt le Ryzen 99999999999999
    """
    def __init__(self, code):
        self._op_traduc = {
            "and"   : self._and,
            "nand"  : self._nand,
            "or"    : self._or,
            "nor"   : self._nor,
            "xor"   : self._xor,
            "nxor"  : self._nxor,
            "not"   : self._not,
            "add"   : self._add,
            "load"  : self._load,
            "mov"   : self._mov,
            "store" : self._store,
            "jmp"   : self._jmp,
            "jz"    : self._jz,
            "jnz"   : self._jnz
        }
        self._reg = {
            "r1" : "00",
            "r2" : "01",
            "r3" : "10",
            "r4" : "11"
        }
        self._code                 = sanify(code)
        (self._code, self._labels) = self.find_labels()

    def _is_label(self, i):
        c = lambda z: "0"*(8-len(z)) + z
        if self._labels.get(i): return c(bin(self._labels.get(i))[2:])
        return c(bin(int(i))[2:]) if i[0:2] != "0x" else c(bin(int(i[2:], 16))[2:])

    def _and(self, payload): 
        return int(complete("00001" + self._reg[payload[0]] + self._reg[payload[1]] + self._reg[payload[2]]), 2).to_bytes(2, "big")

    def _nand(self, payload): 
        return int(complete("00011" + self._reg[payload[0]] + self._reg[payload[1]] + self._reg[payload[2]]), 2).to_bytes(2, "big")

    def _or(self, payload): 
        return int(complete("00010" + self._reg[payload[0]] + self._reg[payload[1]] + self._reg[payload[2]]), 2).to_bytes(2, "big")

    def _nor(self, payload): 
        return int(complete("00100" + self._reg[payload[0]] + self._reg[payload[1]] + self._reg[payload[2]]), 2).to_bytes(2, "big")

    def _xor(self, payload): 
        return int(complete("00101" + self._reg[payload[0]] + self._reg[payload[1]] + self._reg[payload[2]]), 2).to_bytes(2, "big")

    def _nxor(self, payload): 
        return int(complete("00110" + self._reg[payload[0]] + self._reg[payload[1]] + self._reg[payload[2]]), 2).to_bytes(2, "big")

    def _not(self, payload): 
        return int(complete("00111" + self._reg[payload[0]] + self._reg[payload[1]]), 2).to_bytes(2, "big")

    def _add(self, payload): 
        return int(complete("00000" + self._reg[payload[0]] + self._reg[payload[1]] + self._reg[payload[2]]), 2).to_bytes(2, "big")

    def _load(self, payload):
        if payload[1][0] == "@": return int(complete("01001" + self._reg[payload[0]] + self._is_label(payload[1][1:])), 2).to_bytes(2, "big")
        else:                    return int(complete("01000" + self._reg[payload[0]] + self._is_label(payload[1])), 2).to_bytes(2, "big")

    def _mov(self, payload):
        return int(complete("01010" + self._reg[payload[0]] + self._reg[payload[1]]), 2).to_bytes(2, "big")

    def _store(self, payload):
        c = lambda z: "0"*(8-len(z)) + z
        if payload[0][0] == "@": return int(complete("01100" + self._reg[payload[1]] + (c(bin(int(payload[0][1:]))[2:]) if payload[0][1:3] != "0x" else c(bin(int(payload[0][3:], 16))[2:]))), 2).to_bytes(2, "big")
        else:                    return int(complete("01011" + self._reg[payload[0]] + self._reg[payload[1]]), 2).to_bytes(2, "big")

    def _jmp(self, payload):
        if payload[0][0] == "@": return int(complete("10000" + self._is_label(payload[1][1:])), 2).to_bytes(2, "big")
        else:                    return int(complete("10001" + self._reg[payload[0]]), 2).to_bytes(2, "big")

    def _jz(self, payload): 
        return int(complete("10010" + self._reg[payload[0]] + self._reg[payload[1]]), 2).to_bytes(2, "big")

    def _jnz(self, payload): 
        return int(complete("10011" + self._reg[payload[0]] + self._reg[payload[1]]), 2).to_bytes(2, "big")

    def find_labels(self):
        code        = deepcopy(self._code)
        labels      = {}
        match_label = compile("^.*:$")

        nbr_labels  = 0
        for (addr, label) in enumerate(self._code):
            if match_label.match(label): 
                labels[label.split(":")[0].strip()] = addr-nbr_labels
                nbr_labels += 1
                code.pop(addr)

        return (code, labels)
    
    def compile(self):
        ret = b""
        for instr in self._code:
            (op, reste) = instr.split(maxsplit=1)
            payload     = [x.strip() for x in reste.split(",")]
            ret += self._op_traduc[op](payload)
        return ret

if __name__ == "__main__":
    import argparse

    def to_logisim(code):
        c   = lambda z: "0"*(2-len(z)) + z
        ret = "v2.0 raw\n"
        for i in range(0, len(code), 2):
            ret += c(hex(code[i])[2:]) + c(hex(code[i+1])[2:]) + " "
        return ret

    parser = argparse.ArgumentParser("Assembleur du ryzen 999999999999999999999999")
    parser.add_argument("-i", "--input", help="Fichier en langage d'assemblage", required=True)
    args = parser.parse_args()

    c = Compile(open(args.input, "r").read())
    print(to_logisim(c.compile()))
