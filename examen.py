# INTEGRANTES
# José Issac Ramírez Martínez
# Angel Aldayr Rodriguez Gonzalez 
# Angel Adal Martínez Granados


import cplex
problema = cplex.Cplex()

file = 'scp41.txt'  #cambiar el nombre del archivo para poder hacer las demas instancias 

cont = 0 
cont1 = 0 
cont2 = 0 

FuncionObjetivo = [] 
variablesFuncion = []
limiteSupe = []
limiteInfer = []
rhs = []
restricciones = []
sentido = []
valHolgura= []
types_val= []



with open(file) as f:
    linea1 = f.readline() # primera linea del archivo
    linea1 = linea1.split(sep=' ')
    cantidadRestricciones = int(linea1[0]) # cantidad restricciones
    cantidadVariables = int(linea1[1]) # cantidad de variables
    cantEle = 1 # guarda cuantos elementos hay por fila en matriz costos
    limiteSupe = [1] * cantidadVariables
    limiteInfer = [0] * cantidadVariables
    types_val = [problema.variables.type.binary] * cantidadVariables
    sentido = ["G"] * cantidadRestricciones
    rhs = [1] * cantidadRestricciones


    
    for linea in f:
        while linea.split(sep=' ')[len(linea.split(sep=' ')) - 1] == '\n' and cont < cantidadVariables:
            cantEleLinea = len(linea.split())
            while cont1 < cantEleLinea:
                FuncionObjetivo.append(int(linea.split(sep=' ')[cont1]))
                variablesFuncion.append("X"+str(cantEle))
                cantEle += 1
                cont1 += 1            
            cont1 = 0
            cont2 += 1
            cont = cont + len(linea.split())
            break
  
f.close()

with open(file) as f:
    linea2 = f.readlines()
    valor = 0
    cont = 0
    cont2 += 1 
    while cont < cont2:
        linea2.pop(valor)
        cont += 1
    
    linea3 = ""
    for ele in linea2:
        linea3 += ele

    cont = 0
    cont1 = 0
    cont2 = 0
    cont3 = 0
    arregloRestricciones = []
    while cont < cantidadRestricciones:
        cantEleRestriccion = int(linea3.split()[cont3])
        a = []
        b = []
        while cont2 < cantEleRestriccion:
            a = int(linea3.split()[cont1+1])
            b.append(a)
            cont2 += 1
            cont1 += 1
        cont1 = cont1 + 1
        cont2 = 0
        arregloRestricciones.append(b)
        cont3 += cantEleRestriccion + 1
        
        cont += 1


    restricionTemporal = []
    arregloRestriccionesBinario = []
    
    
    
    cont = 0
    cont1 = 0
    while cont < cantidadRestricciones:
        arreglo = [0] * cantidadVariables
        restricionTemporal = []
        restricionTemporal.append(variablesFuncion)
        while cont1 < len(arregloRestricciones[cont]):
            arreglo[arregloRestricciones[cont][cont1]-1] = 1
            #arreglo2
            cont1 += 1
        restricionTemporal.append(arreglo)
        restricciones.append(restricionTemporal)
        arregloRestriccionesBinario.append(arreglo)
        cont1 = 0
        cont += 1
      
    cont = 0
    cont2 = 1
   
    cont = 0
    while cont < cantidadRestricciones:
        valHolgura.append('S'+ str(cont+1))
        cont+=1
        
f.close()

    

problema.objective.set_sense(problema.objective.sense.minimize)

problema.variables.add(obj=FuncionObjetivo,
                       lb=limiteInfer,
                       ub=limiteSupe,
                       names=variablesFuncion,
                       types=types_val)

problema.linear_constraints.add(lin_expr=restricciones,
                                senses=sentido,
                                rhs=rhs,
                                names=valHolgura)

problema.solve()
print("valor optimo: " + str(problema.solution.get_objective_value()))
print()

solucion = problema.solution.get_values()

archivo = open (file.replace(".txt", "") + ".Solucion.txt", "w")
k=0 

for line in solucion:
    archivo.write((str(int(line)).replace("-",""))+ " ")
    k += 1
    if k == 15:
        archivo.write("\n")
        k=0

archivo.close()