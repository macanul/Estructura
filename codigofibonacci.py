def generar_fibonacci(n):
    """Genera una lista con los primeros n números de Fibonacci."""
    if n <= 0:
        return []
    elif n == 1:
        return [0]
    
    fib_sequence = [0, 1]
    for _ in range(2, n):
        siguiente = fib_sequence[-1] + fib_sequence[-2]
        fib_sequence.append(siguiente)
        
    return fib_sequence

# Definimos la cantidad de números que queremos
n = 501
resultado = generar_fibonacci(n)

# Mostramos los resultados numerados
for i, numero in enumerate(resultado):
    print(f"F({i}) = {numero}")
