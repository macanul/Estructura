calificaciones=[0]*5
for i in range(5):
    calificacion=int(input(f"Captura la calificacion {i+1}: "))
    calificaciones[i]=calificacion
print("Calificaciones:", calificaciones)