# Estructura
El codigo del arreglo bidimensional (EJER-ARREGLOS.py) consiste en una tabla conformada por 12 filas que representan los meses del año en donde se registra las ventas hechas por distintos departamentos de una tienda (jugueteria, deportes, ropa) que estan representadas en columnas y en donde puedes insertar, eliminar, buscar y mostrar datos de la tabla.

El metodo insertar funciona con el codigo insertar(mes, departamento, venta) en donde se registra una venta en una posicion especifica de la matriz, recibe el mes (0-11), el departamento (0-2) y el valor de la venta, se asigna el valor en matriz[mes][departamento] = venta para que al final se imprima que valor se agrego, en que mes y en que departamento

El metodo buscar recorre toda la matriz para buscar un valor exacto de venta usando ciclos for para recorrer todos los meses y departamentos hasta encontrar el valor indicado y decirle al usuario en que mes y departamento se encuentra, en caso de que el valor solicitado no se encuentre le dice al usuario que no encontro nada

El metodo eliminar se usa para eliminar el valor de una venta, recibe el mes y el departamento que se desee eliminar, guarda el valor que habia en esa celda en una variable auxiliar y luego reemplaza la posicion por 0

El metodo mostrartabla lo hice para que la tabla aparezca como esta especificado en la actividad, primero imprimo los encabezados de Mes, Ropa, Deportes y Jugueteria, luego recorre las 12 filas (los meses) y al lado de estas sus 3 ventas con 10 caracteres de ancho (todo tiene 10 caracteres de ancho, ya sea los encabezados o los numeros de ventas)
