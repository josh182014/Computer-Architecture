"""CPU functionality."""
import sys

HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MUL  = 0b10100010

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8
        self.ram = [0] * 256
        self.pc = 0
        self.isRunning = True
        self.reg[7] = 0xf4

    def ram_read(self, MAR):
        return self.ram[MAR]

    def ram_write(self, MDR, MAR):
        self.ram[MAR] = MDR

    def load(self, file):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        with open(file) as program:
            for line in program:
                instruction = line.split("#")[0].strip()
                if instruction == "":
                    continue
                value = int(instruction, 2)
                self.ram[address] = value
                address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        while self.isRunning is True:
            IR = self.ram[self.pc]
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            if IR == HLT:
                self.isRunning = False
            elif IR == LDI:
                self.reg[operand_a] = operand_b
            elif IR == PRN:
                print(self.reg[operand_a])
            elif IR == MUL:
                self.reg[operand_a] *= self.reg[operand_b]
            else:
                raise Exception('error: unknown command')

            self.pc += (IR >> 6) + 1
