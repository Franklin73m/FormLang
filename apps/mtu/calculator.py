"""Calculatrice unaire. À COMPLÉTER.  -> Jour 4 (E4.3)."""
from .machines import ADD, SUB


def _ones(s: str) -> int:
    return s.count("1")


class Calculatrice:
    def addition(self, n: int, m: int) -> int:
        """Addition unaire: n + m."""
        word = "1" * n + "+" + "1" * m
        result = ADD.run(word)
        return _ones(result.tape)

    def soustraction(self, n: int, m: int) -> int:
        """Soustraction unaire tronquée: max(0, n - m)."""
        if n < m:
            return 0
        word = "1" * n + "-" + "1" * m
        result = SUB.run(word)
        return _ones(result.tape)

    def multiplication(self, n: int, m: int) -> int:
        """Multiplication par addition répétée: n * m."""
        acc = 0
        for _ in range(m):
            acc = self.addition(acc, n)
        return acc

    def division(self, n: int, m: int):
        """Division entière: (n // m, n % m)."""
        if m == 0:
            raise ZeroDivisionError("Division par zéro")
        quotient = 0
        remainder = n
        while remainder >= m:
            remainder = self.soustraction(remainder, m)
            quotient += 1
        return (quotient, remainder)

    def chainer(self, v0: int, ops: list) -> int:
        """Applique une suite d'opérations: [(op, arg), ...]."""
        v = v0
        for op, arg in ops:
            if op == '+':
                v = self.addition(v, arg)
            elif op == '-':
                v = self.soustraction(v, arg)
            elif op == '*':
                v = self.multiplication(v, arg)
            elif op == '/':
                v, _ = self.division(v, arg)
            else:
                raise ValueError(f"Opération inconnue: {op}")
        return v
