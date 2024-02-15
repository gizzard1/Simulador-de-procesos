Al ejecutar el archivo “programa.py” inicializa la interfaz gráfica siguiente.
 ![image](https://github.com/gizzard1/Simulador-de-procesos/assets/131214631/93c92e07-443b-45a9-b75a-74c68c63d73e)

Un diseño ligeramente sencillo realizado con la librería tkinter. Se aprecia una entrada para ingresar la cantidad de procesos, dos botones, uno para iniciar la simulacion (“Generar”) y otro para crear el archivo “Resultados.txt” (“OBTENER RESULTADOS”) donde se almacenarán los procesos terminados tal cual se fueron ejecutando con las operaciones resueltas y la separación por lotes. 
Hay un área donde se muestra la etapa de procesos en espera, una de ejecución y otra de terminados. La etiqueta debajo de la primer etapa muestra los lotes pendientes y en la parte superior derecha se encuentra otra donde se muestra el contador del reloj global.
Inicializar con una cantidad numérica válida ejecuta la simulación junto a un reloj global, lotes y procesos pendientes.
 ![image](https://github.com/gizzard1/Simulador-de-procesos/assets/131214631/b85338c9-d6b5-4ead-95b1-a3bd724eeb96)

Los datos del programador son extraídos aleatoriamente de un archivo “datos.txt” el cual contiene n cantidad de nombres, (en mi caso son cinco). La operación y el TME se asignan al azar igualmente, pero la operación se resuelve lógicamente y el TME decrementa con respecto al reloj global.
 ![image](https://github.com/gizzard1/Simulador-de-procesos/assets/131214631/93002583-0bfb-4763-af74-77a717c5d966)

Al finalizar, se habilita el botón de obtener resultados y hacer clic nos genera el archivo mencionado anteriormente, así también, se habilita la entrada de procesos por si se desea ejecutar la simulación nuevamente.
 ![image](https://github.com/gizzard1/Simulador-de-procesos/assets/131214631/6b4cdc64-39ff-49cf-a770-93bd6d1c7088)

