import time
inicio = time.time()
def mostrarVector(datos):
    for i in range(len(datos)):
        print(datos[i])


def media(datos):
    suma = 0
    n = len(datos)

    for i in range(n):
        suma = suma + datos[i]

    return suma / n


pares = [2, 4, 6, 8, 10]
impares = [1, 3, 5, 7, 9]

mostrarVector(pares)
print("Media =", media(pares))

mostrarVector(impares)
print("Media =", media(impares))

fin = time.time()
tiempo_total = fin - inicio
print(f"Tiempo total: {tiempo_total}")