## Lector de resultados de COPASI
## Mario Bogantes, Maestria en Bioinformatica, UCR, 2017

## Genera un archivo separado por espacios en formato txt con los
##Objective values de cada especie.

## Requiere 2 argumentos, nombre del archivo que se quiere abrir y nombre del archivo destino
import sys
import re
from  more_itertools import unique_everseen

if len(sys.argv) < 2:
    print("Lector de resultados COPASI, \n Este programa requiere de 2 argumentos \n Argumento 1: Archivo de resultados de COPASI \n Argumento 2: Nombre del archivo que se desea crear con los resultados ")
    print("\n Nota: El programa solo lee el primer ajuste de cada archivo, no soporta ajustes continuos anexados en el mismos archivo.")
    print("Los resultados se presentan en formato de .csv separado por comas y son la suma de todos los Objective Value de todos los experimentos para cada especie")
    exit()

input_file_arg=str(sys.argv[1])
output_file_arg=str(sys.argv[2])+".csv"

input_file=open(input_file_arg,"r" )
data=input_file.readlines()

output_file=open(output_file_arg,"w")

species=[]
temp_result=[]
species_index=[]
species_index_temp=[]


for i in range(len(data)):

    if "Experiment:" in data[i]:# and not species: not species chequea si species es vacio
        temp_species =re.findall('\[(\w+\.*\w*)\]', data[i + 4])

        for j in temp_species:
            if j not in species:
                #print(j)
                species.append(j)
        a_temporal_list=list(unique_everseen(temp_species))
        for k in a_temporal_list:
            if k in species:
                species_index_temp.append(a_temporal_list.index(k))
            else:
                species_index_temp.append(-1)

        species_index.append(species_index_temp)

        temp_result.append(re.findall('(\d+\.\d+e?[+-]?\d*)', data[i+7]))

    elif "Fisher" in data[i]:
        break

    else:
        pass #print("nothing on %s" % i)

big_result=[0]*len(species)

for i in range(len(temp_result)):
    for j in range(len(temp_result[i])):
        #print(temp_result[j])
        #print([0]*len(species))
        #print(i)
        #print(species_index[i][j])

        if species_index[i][j] != -1:
            big_result[species_index[i][j]] += float(temp_result[i][species_index[i][j]])


for i in range(len(species)):
    output_file.write(str(species[i]))
    output_file.write(",")

output_file.write("\n")

for i in range(len(big_result)):
    output_file.write(str(big_result[i]))
    output_file.write(",")

input_file.close()
output_file.close()








