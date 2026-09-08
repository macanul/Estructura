import time
inicio = time.time()
def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n - 1)
    
if __name__ == "__main__":
    a = 10
    print(factorial(a))

    fin = time.time()
    tiempo_total = fin - inicio
    print(f"Tiempo total: {tiempo_total}")