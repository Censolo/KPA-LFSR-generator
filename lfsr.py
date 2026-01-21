from bits import Bits

class LFSR:
    def __init__(self, poly, state=None):
        self.poly = set(poly)
        if not self.poly:
            raise ValueError("Polynomial must have at least one term.")

        self.length = max(self.poly)
        if self.length <= 0:
            raise ValueError("Polynomial degree must be >= 1 for a valid LFSR.")

        # State assignment
        tmp = Bits(state) if state is not None else Bits([True] * self.length)

        if len(tmp) < self.length:
            pad_needed = self.length - len(tmp)
            padded = [False] * pad_needed + tmp.bits
            self.state = Bits(padded)
        else:
            self.state = tmp

        self.output = self.state[-1]           

    def __iter__(self):
        return self

    def __str__(self):
        poly_str = "{" + ",".join(str(p) for p in sorted(self.poly, reverse=True)) + "}"      
        return f"LFSR(poly={poly_str}, length={self.length}, state={str(self.state)})"

    def __next__(self):
        bits_to_xor = []
        for exp in self.poly:
            if exp != 0:        # if exp is zero then skip
                bits_to_xor.append(self.state[exp-1])
        fb = False
        for b in bits_to_xor:
            fb ^= b

        self.feedback = fb  # feedback update for subsequent iteration

        new_bits = [self.feedback] + self.state[:-1]    # BIG ENDIAN => MSB to the left
        self.state = Bits(new_bits)

        self.output = self.state[self.length-1]
        return self.output

    def run_steps(self, N=1, state=None):
        old_state = self.state
        if state is not None:
            tmp_bits = Bits(state)
            if len(tmp_bits) != self.length:
                raise ValueError("Provided state must match LFSR length.")
            self.state = tmp_bits

        outputs = []
        for _ in range(N):
            bit_out = next(self)
            outputs.append(bit_out)

        if state is not None:
            self.state = old_state

        return Bits(outputs)

    def cycle(self, state=None):  
        old_state = self.state

        if state is not None:
            tmp_bits = Bits(state)
            if len(tmp_bits) != self.length:
                raise ValueError("Provided state must match LFSR length.")
            self.state = tmp_bits

        start_state_str = str(self.state)
        outputs = []

        max_steps = 2 ** self.length 
        steps = 0
        while True:
            bit_out = next(self)
            outputs.append(bit_out)
            steps += 1

            if str(self.state) == start_state_str or steps >= max_steps:
                break

        if state is not None:
            self.state = old_state

        return Bits(outputs)

############## END LFSR CLASS #############

# Berlekamp Algorithm - outside of class scope in order to be called as is
def berlekamp_massey(b):
    N = len(b) - 1
    P = [1]  # P(x) representation as list of coefficients
    m = 0    # degree of P(x)
    Q = [1]  # Q(x) representation
    r = 1    # step counter

    for tau in range(N):
        # Discrepancy calculation
        d = 0
        for j in range(m + 1):
            if tau - j >= 0:
                d ^= P[j] & b[tau - j]

        # Discrepancy detection
        if d == 1:
            if 2 * m <= tau:
                R = P.copy() # R(x) as copy of P(x)

                # P(x) ← P(x) + Q(x) * x^r
                shifted_Q = [0] * r + Q # Q(x) shifted by "r" positions before XOR with P(x)

                if len(shifted_Q) < len(P):
                    shifted_Q += [0] * (len(P) - len(shifted_Q))
                elif len(shifted_Q) > len(P):
                    P += [0] * (len(shifted_Q) - len(P))
                P = [p ^ q for p, q in zip(P, shifted_Q)]

                # Q(x) ← R(x)
                Q = R
                m = tau + 1 - m
                r = 0
            else:
                shifted_Q = [0] * r + Q
                if len(shifted_Q) < len(P):
                    shifted_Q += [0] * (len(P) - len(shifted_Q))
                elif len(shifted_Q) > len(P):
                    P += [0] * (len(shifted_Q) - len(P))
                P = [p ^ q for p, q in zip(P, shifted_Q)]

        r += 1  # r update
    return P, (len(P)-1)