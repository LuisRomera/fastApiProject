class Calculadora:
    def sumar(self, a, b):
        print("Sum de {} + {}".format(a, b))
        return a + b

    def restar(self, a, b):
        print("Restar de {} - {}".format(a, b))
        return a - b

    def multiplicar(self, a, b):
        print("Multiplica de {} * {}".format(a, b))
        return a * b

    def dividir(self, a, b):
        print("Dividir de {} / {}".format(a, b))
        if b == 0:
            raise ZeroDivisionError("No se puede dividir por cero")
        return a / b
