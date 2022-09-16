import pandas as pd
import numpy as np
import sys
path      = "/home/mzamith/Documents/dev/qgis-3/RJ-Parque-Chico-Mendes/CSV/"
csv_file  = "bairros_populacao.csv"
field     = "distrito"
compared  = "Ilha do Governador"
out_file   = "lixo.csv"
geom       = "geom"
# init code
dbData = pd.read_csv(path + csv_file)

print("Extract records")
print("   Path: ", path)
print("   File: ", csv_file)
print("  Field: ", field)
print("outfile: ", out_file)
compared = compared.upper()
str_size = len(compared)


output = open(path + out_file, "w+")

col = len(list(dbData))
line = ""
for col2 in range(0, col):
    line = "%s, %s" % (line, list(dbData)[col2]);

line = line[1:]
output.write(line + "\n")

nrecords = 0
for index, record in dbData.iterrows():
    if (not pd.isnull(record[field])):
        line = record[field]
        if (len(line) >= str_size):
            sub_line = line[:str_size].upper()
            if (sub_line == compared):
                line = ""
                for col2 in range(0, col):
                    nrecords = nrecords + 1
                    if (list(dbData)[col2] == geom):
                        aux = record[col2]
                        line = "%s, \"%s\"" % (line, aux)
                        #print(aux)
                        #sys.exit(-1)
                    else:
                        line = "%s, %s" % (line , record[col2])

                line = line[1:]
                output.write(line + "\n")
                #print(line)
 #               table = np.append(table, [record])

    #bairro = dbData["bairro"][index]
    #print(index, "  ", bairro)
    #if (compared == dbData[field][index]):
    #    print(dbData['bairro'][index])

#print(np.size(table))

#print(table[1])
output.close()
print("Total records: ", nrecords);
print("File: ", path + out_file, "[SAVED]")

'''
size = dbData.size
print(dbPopulationata.keys())
print(len(dbPopulationata.keys()))
print(size)
print(dbPopulationata['distrito'][1])
'''

#print(sys.argv[1])
