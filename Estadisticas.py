import random
import statistics

numeros = [random.randint(150, 250) for i in range(50)]

print("Números:", numeros)
print("Media:", statistics.mean(numeros))
print("Mediana:", statistics.median(numeros))
print("Moda:", statistics.mode(numeros))
print("Desviación estándar:", statistics.stdev(numeros))
print("Varianza:", statistics.variance(numeros))