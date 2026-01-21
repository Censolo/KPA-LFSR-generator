from lfsr import LFSR

class AlternatingStep:
    def __init__(self, seed=None, polyC={5,2,0}, poly0={3,1,0}, poly1={4,1,0}):

        self.lfsrC = LFSR(polyC)
        self.lfsr0 = LFSR(poly0)
        self.lfsr1 = LFSR(poly1)
        self.output = None

        # init state with seed
        if seed:
            total_length = self.lfsrC.length + self.lfsr0.length + self.lfsr1.length
            if len(seed) < total_length:
                raise ValueError("Seed lenght is too short!")
            # Assegna le parti del seed
            self.lfsrC.state = seed[:self.lfsrC.length]
            self.lfsr0.state = seed[self.lfsrC.length:self.lfsrC.length+self.lfsr0.length]
            self.lfsr1.state = seed[self.lfsrC.length+self.lfsr0.length:self.lfsrC.length+self.lfsr0.length+self.lfsr1.length]

    def __iter__(self):
        return self

    def __next__(self):
        control_bit = next(self.lfsrC)
        if control_bit == 0:
            bit0 = next(self.lfsr0)
            bit1 = self.lfsr1.output  # block lfsr1 clocking
        else:
            bit1 = next(self.lfsr1)
            bit0 = self.lfsr0.output  # block lfsr0 clocking

        self.output = bit0 ^ bit1  # output XOR
        return self.output


# CODE SNIPPET
# from bitgenerator import AlternatingStep
# from bits import Bits
#
# from slide example
# gen = AlternatingStep()
#
# # Genera 10 bit
# output_sequence = []
# for _ in range(10):
#     output_sequence.append(next(gen))
#
# print(output_sequence)
