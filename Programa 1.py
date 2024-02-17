import tkinter as tk
import time
import random
import math

#Definimos la clase para la aplicación
class ProcesamientoPorLotes:
    #Self es el objeto que contiene todo lo relacionado al procesamiento
    #Master es el widget padre
    def __init__(self, master):

        #Estilo de letra y título de la ventana
        font_style = ("Helvetica", 12)
        self.master = master
        self.master.title("ProcesamientoPorLotes")

        #Etiqueta para el input de procesos
        self.etiquetaCantProcesos = tk.Label(master, text="# Procesos:", font=font_style)
        self.etiquetaCantProcesos.grid(row=0, pady=20, column=0, sticky="w", padx=20)

        #Input para recibir la cantidad de procesos
        self.entradaProcesos = tk.Entry(master, width=7, font=font_style)
        self.entradaProcesos.grid(row=0, pady=20, column=0, padx=5, columnspan=2)

        #Botón que ejecuta el programa e inicia la función propia iniciarSimulacion
        self.botonGenerar = tk.Button(master, text="Generar", command=self.iniciarSimulacion, font=font_style)
        self.botonGenerar.grid(row=0, pady=20, columnspan=2, column=1)

        #Se define un reloj global en 0 para asegurar que esté detenido
        self.start = 0
        self.relojGlobal = tk.Label(master, text="Reloj Global", font=font_style)
        self.relojGlobal.grid(row=0, pady=20, column=6, padx=10)

        #Etiqueta de la columna de procesos en espera
        self.etiquetaProcesosEnEspera = tk.Label(master, text="EN ESPERA", font=font_style)
        self.etiquetaProcesosEnEspera.grid(row=1, column=1)

        #Columna donde se muestran los procesos en espera
        self.enEspera = tk.Text(master, wrap=tk.WORD, width=15, height=15, font=font_style)
        self.enEspera.grid(row=2, column=1)

        #Etiqueta de la columna de procesos en ejecución
        self.etiquetaProcesosEnEjecucion = tk.Label(master, text="EJECUCIÓN", font=font_style)
        self.etiquetaProcesosEnEjecucion.grid(row=1, column=2)

        #Columna donde se muestran los procesos en ejecución
        self.enEjecucion = tk.Text(master, wrap=tk.WORD, width=15, height=5, font=font_style)
        self.enEjecucion.grid(row=2, column=2)

        #Etiqueta de la columna de procesos terminados
        self.etiquetaProcesosTerminados = tk.Label(master, text="TERMINADOS", font=font_style)
        self.etiquetaProcesosTerminados.grid(row=1, column=4)

        #Columna donde se muestran los procesos terminados
        self.terminados = tk.Text(master, wrap=tk.WORD, width=15, height=15, font=font_style)
        self.terminados.grid(row=2, column=4, columnspan=2)

        #Etiqueta que muestra el número de lotes pendientes
        self.lotesPendientes = tk.Label(master, text="# de Lotes pendientes:", font=font_style)
        self.lotesPendientes.grid(row=3, column=1)

        #Botón para crear el archivo lógico con los procesos terminados
        self.botonObtenerResultados = tk.Button(master, text="OBTENER RESULTADOS", command=self.obtenerResultados, font=font_style)
        self.botonObtenerResultados.grid(row=3, column=4, pady=10)

        self.clear()

    def clear(self):        
        #Definición de las listas que contendrán los procesos por etapa
        self.procesos_en_espera = []
        self.procesos_en_ejecucion = []
        self.procesos_terminados = []
        self.procesos_archivar = []
        self.tiempo_transcurrido = 0
        self.numero_lotes = 0  # Variable para contar el número de lotes
        self.lote_actual = 0  # Variable para rastrear el lote actual

    def iniciarSimulacion(self):
        #Deshabilitamos el botón de resultados para evitar comportamientos inesperados
        self.botonObtenerResultados.config(state='disabled')

        #Se toma de referencia el tiempo en el que se inició la simulación
        self.start = time.time()

        #Método que mantiene activo contando al reloj global
        self.actualizar_tiempo()

        #Lectura completa del archivo lógico
        datos = open('programadores.txt')
        self.programadores = datos.readlines()

        #Se obtiene y se valida la cantidad de procesos a ejecutar
        entrada_procesos = self.entradaProcesos.get()
        if entrada_procesos.isdigit():
            procesos = int(entrada_procesos)
            #Deshabilitamos la entrada para evitar una doble simulación
            self.entradaProcesos.config(state='disabled')
        else:
            #arroja mensaje de error y detiene el reloj
            self.enEspera.insert(tk.END, f"Ingrese una cantidad numérica...\n")
            self.start = 0

        #Se nombra el archivo donde se almacenarán los procesos terminados
        self.archivoDatos = "datos.txt"


        #Inicializa el contador dependiendo el número de procesos que se ejecuten
        if procesos < 5:
            self.procesos_por_lote = procesos
        else:
            self.procesos_por_lote = 5

        #Calcula el total de lotes redondeando hacia arriba
        lotes = math.ceil(procesos / 5)

        #Inicializa la variable de lotes
        self.numero_lotes = lotes -1 

        #Inicializamos el contador de lotes
        lote_actual = 0

        #Bucle for que realiza la simulación de cada proceso
        for i in range(procesos):
            
            #Se sobreescribe en la etiqueta de lotes pendientes el número de lotes
            self.lotesPendientes.config(text=f"# de Lotes pendientes: {self.numero_lotes}")

            #Si el modular de 5 es igual a cero quiere decir que se han iterado 5 procesos
            if i % 5 == 0:
                #Por lo que el lote aumenta uno, ya que contiene 5 procesos
                lote_actual +=1

            #Obtenemos los datos al azar tanto la operación como el operando, así también el programador y el tme
            a = random.randint(0, 9)
            b = random.randint(0, 9)
            tme = random.randint(5, 13)
            operador = random.choice(['+', '-', '*', '/'])
            programador = random.choice(self.programadores)
            operacion = f"{a} {operador} {b}"
            
            #Validación de división con cero
            if operador == '/' and b == 0:
                resultado = 'No definido'
            else:
                #Obtenemos el resultado de la operación correctamente planteada
                resultado = eval(operacion)


            #Diccionario con los datos del proceso a ejecutar
            proceso = {"id": i + 1, "programador": programador, "a": a, "operador": operador, "b": b, "tme": tme, "resultado": resultado, "lote": lote_actual, "tme_no_modificado": tme}
            self.procesos_en_espera.append(proceso)

        datos.close()

        self.ejecutar_procesos()

    def ejecutar_procesos(self):
        #Validación para saber el estado del lote
        if self.procesos_por_lote > 1:
            #mientras se encuentre en el mismo lote se decrementara el contador
            self.procesos_por_lote -= 1
        else:
            #De lo contrario se valida si hay más lotes verificando que la cuenta de procesos en espera sea mayor a 5
            self.procesos_por_lote = len(self.procesos_en_espera)-1 
            if self.procesos_por_lote > 5:
                #Si es válido, se toma un lote completo para iniciar el contador
                self.procesos_por_lote = 5
            
        #Verifica si hay procesos en espera
        if self.procesos_en_espera:
            #Toma el proceso en posición cero y lo guardamos en la variable
            proceso_actual = self.procesos_en_espera.pop(0)
            self.procesos_archivar.append(proceso_actual)
            #Limpia el área de espera
            self.enEspera.delete(1.0, tk.END)

            if self.procesos_en_espera:
                #Definimos el proceso que se encuentra en la posición final y lo intertamos en el área de espera
                proceso_anterior = self.procesos_en_espera[-1]
                self.enEspera.insert(tk.END, f"{proceso_actual['id']+1}. {proceso_anterior['programador']} {proceso_anterior['a']} {proceso_anterior['operador']} {proceso_anterior['b']}\n")
            
            #Agregamos la cantidad de procesos pendientes contando con el método len()
            self.enEspera.insert(tk.END, f"{self.procesos_por_lote} procesos pendientes")

            #Limpiamos el área de ejecución
            self.enEjecucion.delete(1.0, tk.END)


            #Verificar si el proceso actual pertenece a un lote diferente al anterior
            if proceso_actual['lote'] != self.lote_actual:
                #Si la validación es cierta, entonces inicia con el número de lote
                self.lote_actual = proceso_actual['lote']
                self.terminados.insert(tk.END, f"Lote {self.lote_actual}\n")
                self.lotesPendientes.config(text=f"# de Lotes pendientes: {self.numero_lotes}")
                #Se resta uno al número de lotes pendientes 
                if self.numero_lotes != 0:
                    self.numero_lotes -= 1


            #Insertamos en ejecución el proceso que tomamos al inicio y luego se inserta en el área correspondiente
            proceso_text = f"{proceso_actual['id']}. {proceso_actual['programador']} {proceso_actual['a']} {proceso_actual['operador']} {proceso_actual['b']}\nTME: {proceso_actual['tme']}"
            self.enEjecucion.insert(tk.END, proceso_text)
            self.procesos_en_ejecucion.append(proceso_actual)
            #Función lambda que actualiza el tme del proceso en ejecución cada segundo
            self.master.after(1000, lambda: self.actualizar_tme(proceso_actual))
        else:
            #Sólo actualiza los lotes pendientes y detiene el reloj global
            self.lotesPendientes.config(text=f"# de Lotes pendientes: {self.numero_lotes}")
            self.start = 0
            #Habilitamos el botón de resultados
            self.botonObtenerResultados.config(state='normal')


    def actualizar_tme(self, proceso_actual):
        #Decrece el valor del tme
        proceso_actual['tme'] -= 1
        #limpia el área de la etiqueta
        self.enEjecucion.delete(1.0, tk.END)
        #Actualiza el proceso con su tme modificado y lo inserta en el área correspondiente
        proceso_text = f"{proceso_actual['id']}. {proceso_actual['programador']} {proceso_actual['a']} {proceso_actual['operador']} {proceso_actual['b']}\nTME: {proceso_actual['tme']}"
        self.enEjecucion.insert(tk.END, proceso_text)

        #Esto tiene recursividad si el tme no ha sido reducido a 0
        if proceso_actual['tme'] > 0:
            self.master.after(1000, lambda: self.actualizar_tme(proceso_actual))
        else:
            #Cualdo es 0 eel proceso pasa a la lista de procesos terminaddos
            self.enEjecucion.delete(1.0, tk.END)
            self.procesos_terminados.append(proceso_actual)
            #Se inserta el proceso en el área de terminados
            terminado_text = f"\n{proceso_actual['id']}. {proceso_actual['programador']} {proceso_actual['a']} {proceso_actual['operador']} {proceso_actual['b']} = {proceso_actual['resultado']}\n"
            self.terminados.insert(tk.END, terminado_text)
            #Llamamos a la función que toma un nuevo proceso o termina la ejecución
            self.ejecutar_procesos()

    def obtenerDatos(self):
        
        #Abrir el archivo en modo de anexar ('a') para agregar resultados
        with open(self.archivoDatos, 'a') as file:
            #Conjunto para realizar un seguimiento de los lotes ya procesados
            lotes_procesados = set()

            #Iterar sobre los procesos terminados
            for proceso in self.procesos_archivar:
                lote = proceso['lote']

                #Verificar si el lote ya ha sido procesado
                if lote not in lotes_procesados:
                    #Escribir el encabezado del lote en el archivo
                    file.write(f"Lote {lote}\n")
                    #Agregar el lote al conjunto de lotes procesados
                    lotes_procesados.add(lote)

                #Escribir en el archivo información sobre el proceso actual
                file.write(f"{proceso['id']}. {proceso['programador'].strip()}\n")
                file.write(f"{proceso['a']} {proceso['operador']} {proceso['b']}\n")
                file.write(f"TME: {proceso['tme_no_modificado']}\n\n")

    def obtenerResultados(self):
        self.obtenerDatos()
        #Se nombra el archivo donde se almacenarán los procesos terminados
        archivo = "Resultados.txt"

        #Abrir el archivo en modo de anexar ('a') para agregar resultados
        with open(archivo, 'a') as file:
            #Conjunto para realizar un seguimiento de los lotes ya procesados
            lotes_procesados = set()

            #Iterar sobre los procesos terminados
            for proceso in self.procesos_terminados:
                lote = proceso['lote']

                #Verificar si el lote ya ha sido procesado
                if lote not in lotes_procesados:
                    #Escribir el encabezado del lote en el archivo
                    file.write(f"Lote {lote}\n")
                    #Agregar el lote al conjunto de lotes procesados
                    lotes_procesados.add(lote)

                #Escribir en el archivo información sobre el proceso actual
                file.write(f"{proceso['id']}. {proceso['programador'].strip()}\n")
                file.write(f"{proceso['a']} {proceso['operador']} {proceso['b']} = {proceso['resultado']}\n\n")

        # Habilitar la entrada para evitar una doble simulación
        self.entradaProcesos.config(state='normal')

        # Limpiar los listados y variables y el área de procesos terminados
        self.clear()
        self.terminados.delete(1.0, tk.END)


  
    #Función que mantiene ejecutándose al reloj global cada 1000 ms
    def actualizar_tiempo(self):
        if self.start > 0:
            #Se calcula la diferencia de tiempo desde que se inició la ejecución hasta el punto actual
            self.tiempo_transcurrido = int(time.time() - self.start)
            #Actualiza la etiqueta con los segundos transcurridos
            self.relojGlobal.config(text=f"Reloj Global {self.tiempo_transcurrido} segundos")
            #Ejecución recursiva hasta que start sea 0
            self.master.after(1000, self.actualizar_tiempo)

interfaz = tk.Tk()
app = ProcesamientoPorLotes(interfaz)
interfaz.mainloop()
