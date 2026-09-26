import random

meses = [
    "Enero", "Febrero", "Marzo", "Abril","Mayo", "Junio", "Julio", "Agosto","Septiembre", "Octubre", "Noviembre", "Diciembre"
]

departamentos = [
    "Ropa", "Deportes", "Juguetería"
]

matriz = []
for i in range(12):
    fila = []
    for j in range(3):
        venta = random.randint(1000, 10000)
        fila.append(venta)
    matriz.append(fila)

#método para insertar elementos en el arreglo
def insertar(mes, departamento, venta):
    matriz[mes][departamento] = venta
    print("se ha insertado", venta, "en el mes", meses[mes], "en el departamento", departamentos[departamento])

# método que permita, buscar algún elemento en particular
def buscar(venta):
    for i in range(12):
        for j in range(3):
            if matriz[i][j] == venta:
                print("Venta encontrada")
                print("Mes:", meses[i])
                print("Departamento:", departamentos[j])
                print("Venta:", matriz[i][j])
                return
    print("Venta no encontrada")

#método que permita, eliminar una venta en particular de algún departamento
def eliminar(mes, departamento):
    valor = matriz[mes][departamento]
    matriz[mes][departamento] = 0
    print("Se ha eliminado la venta", valor, "de", meses[mes], "en el departamento", departamentos[departamento])

#método para que la tabla se vea como pide el ejercicio
def mostrartabla():
    print()
    print(f"{'Mes':10} {'Ropa':10} {'Deportes':10} {'Juguetería':10}") #{'valor':ancho}

    for i in range(12):
        print(
            f"{meses[i]:10} " 
            f"{matriz[i][0]:10} "
            f"{matriz[i][1]:10} "
            f"{matriz[i][2]:10}"
        )

print("Tabla de ventas:")
mostrartabla()

insertar(9, 1, 6713)

mostrartabla()

print("\nBuscando la venta de", meses[4], "en el departamento", departamentos[1])
buscar(matriz[4][1])

print("\nEliminando la venta de", meses[5], "en el departamento", departamentos[2])
eliminar(5, 2)

mostrartabla()