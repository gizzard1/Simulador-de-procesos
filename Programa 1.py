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

        #Cambio: botón para interrupción por E/S
        self.botonInterrupcionES = tk.Button(master, text="Interrupción", command=lambda: self.interrupcionError(2), font=font_style)
        self.botonInterrupcionES.grid(row=3, column=6, pady=1,sticky="w")

        #Cambio: botón para interrupción por Error 
        self.botonInterrupcionError = tk.Button(master, text="Error", command=lambda: self.interrupcionError(1), font=font_style)
        self.botonInterrupcionError.grid(row=3, column=5, pady=10)

        self.clear()

    def clear(self):        
        #Cambios: Listado de procesos interrumpidos
        self.procesos_interrumpidos = []

        #Definición de las listas que contendrán los procesos por etapa
        self.procesos_en_espera = []
        self.procesos_en_ejecucion = []
        self.procesos_terminados = []
        self.procesos_archivar = []
        self.tiempo_transcurrido = 0
        self.numero_lotes = 0  # Variable para contar el número de lotes
        self.lote_actual = 0  # Variable para rastrear el lote actual

        #Cambios: bandera que indica si hubo interrupcion 
        self.huboInterrupcion = False

        

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
            #Validación para que el número de lotes sean máximo 5
            if procesos > 26:
                #arroja mensaje de error y detiene el reloj
                self.enEspera.insert(tk.END, f"Número máximo de lotes permitidos 5...\n")
                procesos=0
                self.start = 0
            else:
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
            tme = random.randint(5, 10)
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
<<<<<<< HEAD
            proceso = {"id": i + 1, "programador": programador, "a": a, "operador": operador, "b": b, "tme": tme, "resultado": resultado, "lote": lote_actual, "tiempo_transcurrido":0,"tme_no_modificado": tme,"interrupcion":0}
=======
            proceso = {"id": i + 1, "programador": programador, "a": a, "operador": operador, "b": b, "tme": tme, "resultado": resultado, "lote": lote_actual, "tme_no_modificado": tme}
>>>>>>> 27a4c3b65384c8791373623bb64aa71590778f15
            self.procesos_en_espera.append(proceso)

        datos.close()

        self.ejecutar_procesos()

    def ejecutar_procesos(self):
<<<<<<< HEAD
        self.huboInterrupcion = False
        #Contabilizamos el número de procesos interrumpidos
        procesosInterrumpidos = len(self.procesos_interrumpidos)
=======
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
>>>>>>> 27a4c3b65384c8791373623bb64aa71590778f15

        #Validación para saber el estado del lote. Cambio: validar que haya un proceso interrumpido
        if self.procesos_por_lote > 0 or self.procesos_interrumpidos:
            #mientras se encuentre en el mismo lote se decrementara el contador
            self.procesos_por_lote -= 1
        else:
            #De lo contrario se valida si hay más lotes verificando que la cuenta de procesos en espera sea mayor a 5
            self.procesos_por_lote = len(self.procesos_en_espera)-1 
            if self.procesos_por_lote > 5:
                #Si es válido, se toma un lote completo para iniciar el contador
                self.procesos_por_lote = 4
            
<<<<<<< HEAD
        #Verifica si hay procesos en espera
        if self.procesos_en_espera or self.procesos_interrumpidos:
            
            #Cambio: valida que haya procesos interrumpidos por E/S antes de cambiar de lote
            if self.procesos_interrumpidos and self.procesos_por_lote == procesosInterrumpidos-1:
                #Se inserta en la pila de espera el proceso 
                self.procesos_en_espera.insert(0, self.procesos_interrumpidos.pop(0))
                self.ejecutar_procesos
                
            #Toma el proceso en posición cero y lo guardamos en la variable
            self.proceso_actual = self.procesos_en_espera.pop(0)
            self.procesos_archivar.append(self.proceso_actual)
            #Limpia el área de espera
            self.enEspera.delete(1.0, tk.END)   
=======
            #Agregamos la cantidad de procesos pendientes contando con el método len()
            self.enEspera.insert(tk.END, f"{self.procesos_por_lote} procesos pendientes")
>>>>>>> 27a4c3b65384c8791373623bb64aa71590778f15



            #Verificar si el proceso actual pertenece a un lote diferente al anterior
            if self.proceso_actual['lote'] != self.lote_actual:

                #Si la validación es cierta, entonces inicia con el número de lote
                self.lote_actual = self.proceso_actual['lote']
                self.terminados.insert(tk.END, f"Lote {self.lote_actual}\n")
                self.lotesPendientes.config(text=f"# de Lotes pendientes: {self.numero_lotes}")
                #Se resta uno al número de lotes pendientes 
                if self.numero_lotes != 0:
                    self.numero_lotes -= 1

<<<<<<< HEAD
            if self.procesos_en_espera:
                #Definimos el proceso que se encuentra en la posición final y lo insertamos en el área de espera
                proceso_anterior = self.procesos_en_espera[-1]
                self.enEspera.insert(tk.END, f"{self.proceso_actual['id']+1}. {proceso_anterior['programador']} {proceso_anterior['a']} {proceso_anterior['operador']} {proceso_anterior['b']}\n")
            
            #Agregamos la cantidad de procesos pendientes contando con el método len()
            self.enEspera.insert(tk.END, f"{self.procesos_por_lote} procesos pendientes")

            #Limpiamos el área de ejecución
            self.enEjecucion.delete(1.0, tk.END)
=======
>>>>>>> 27a4c3b65384c8791373623bb64aa71590778f15

            #Insertamos en ejecución el proceso que tomamos al inicio y luego se inserta en el área correspondiente
            proceso_text = f"{self.proceso_actual['id']}. {self.proceso_actual['programador']} {self.proceso_actual['a']} {self.proceso_actual['operador']} {self.proceso_actual['b']}\nTME: {self.proceso_actual['tme']}\nEjecución: {self.proceso_actual['tiempo_transcurrido']}"
            self.enEjecucion.insert(tk.END, proceso_text)
            self.procesos_en_ejecucion.append(self.proceso_actual)
            #Función lambda que actualiza el tme del proceso en ejecución cada segundo
            self.master.after(1000, lambda: self.actualizar_tme())
        else:
            #Sólo actualiza los lotes pendientes y detiene el reloj global
            self.lotesPendientes.config(text=f"# de Lotes pendientes: {self.numero_lotes}")
            self.start = 0
            #Habilitamos el botón de resultados
            self.botonObtenerResultados.config(state='normal')


    def actualizar_tme(self):
        if self.huboInterrupcion:
            return

        #Decrece el valor del tme
        self.proceso_actual['tme'] -= 1
        #limpia el área de la etiqueta
        self.enEjecucion.delete(1.0, tk.END)
        
        #Cambio: incrementa el contador de tiempo en ejecución
        self.proceso_actual['tiempo_transcurrido'] +=1
        #Actualiza el proceso con su tme modificado y lo inserta en el área correspondiente
        proceso_text = f"{self.proceso_actual['id']}. {self.proceso_actual['programador']} {self.proceso_actual['a']} {self.proceso_actual['operador']} {self.proceso_actual['b']}\nTME: {self.proceso_actual['tme']}\nEjecución: {self.proceso_actual['tiempo_transcurrido']}"
        self.enEjecucion.insert(tk.END, proceso_text)

        #Esto tiene recursividad si el tme no ha sido reducido a 0
        if self.proceso_actual['tme'] > 0:
            self.master.after(1000, self.actualizar_tme)
        else:
            #Cuando es 0 el proceso pasa a la lista de procesos terminaddos
            self.enEjecucion.delete(1.0, tk.END)
            self.procesos_terminados.append(self.proceso_actual)
            #Se inserta el proceso en el área de terminados
            terminado_text = f"\n{self.proceso_actual['id']}. {self.proceso_actual['programador']} {self.proceso_actual['a']} {self.proceso_actual['operador']} {self.proceso_actual['b']} = {self.proceso_actual['resultado']}\n"
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
<<<<<<< HEAD
            
            #Iterar sobre los procesos terminados
            for proceso in self.procesos_archivar:
=======

            #Iterar sobre los procesos terminados
            for proceso in self.procesos_terminados:
>>>>>>> 27a4c3b65384c8791373623bb64aa71590778f15
                lote = proceso['lote']

                #Verificar si el lote ya ha sido procesado
                if lote not in lotes_procesados:
                    #Escribir el encabezado del lote en el archivo
                    file.write(f"Lote {lote}\n")
                    #Agregar el lote al conjunto de lotes procesados
                    lotes_procesados.add(lote)

                #Escribir en el archivo información sobre el proceso actual
                file.write(f"{proceso['id']}. {proceso['programador'].strip()}\n")

<<<<<<< HEAD
                if proceso['interrupcion'] == 0:
                    file.write(f"{proceso['a']} {proceso['operador']} {proceso['b']} = {proceso['resultado']}\n\n")
                elif proceso['interrupcion'] == 1:
                    file.write(f"ERROR\n\n")


=======
>>>>>>> 27a4c3b65384c8791373623bb64aa71590778f15
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

    #Cambio: Función que simula la interrupción E/S
    def interrupcionError(self,tipoError):
        self.huboInterrupcion = True
        #Forzamos la interrupcion del proceso y guardamos el tipo de interrupcion (1 es por error)
        self.proceso_actual['interrupcion']=tipoError
        #Elminamos información gráfica
        self.enEjecucion.delete(1.0, tk.END)
        if tipoError == 1:
            #Se transfiere a procesos terminados
            self.procesos_terminados.append(self.proceso_actual)
            terminado_text = f"\n{self.proceso_actual['id']}. {self.proceso_actual['programador']} ERROR\n"
            self.terminados.insert(tk.END, terminado_text)

        elif tipoError == 2:
            self.procesos_interrumpidos.append(self.proceso_actual)
            self.procesos_por_lote+=1
            self.procesos_archivar.pop(-1)
                    
        #Continuamos la ejecución
        self.master.after(1000,lambda: self.ejecutar_procesos())


interfaz = tk.Tk()
app = ProcesamientoPorLotes(interfaz)
interfaz.mainloop()
