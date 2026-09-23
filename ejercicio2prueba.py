import random
import time

inicio = time.time()
alumnos = 500
materias = 6

#matriz de calificaciones
matriz = []

for i in range(alumnos):

    fila = []
    for o in range(materias):
        calificacion = random.randint(0, 10)
        fila.append(calificacion)
    matriz.append(fila)

#tabla de calificaciones
print("Alumno\tMateria 1\tMateria 2\tMateria 3\tMateria 4\tMateria 5\tMateria 6")

for i in range(alumnos):

    print("Alumno", i + 1, end="\t")

    for o in range(materias):
        print(matriz[i][o], end="\t\t")

    print()
fin = time.time()
tiempo_total = fin - inicio

# Buscar alumno y materia
inicio = time.time()

alumno= 299
materia= 2
resultado = matriz[alumno][materia]

fin = time.time()

print("calificacion alumno:", alumno + 1, "materia",materia +1, ":", resultado)
print("Tiempo de búsqueda del alumno:", fin - inicio, "segundos")
print("Tiempo de generación de la matriz:", tiempo_total, "segundos")
