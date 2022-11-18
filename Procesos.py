import pandas as pd

#Usar un archivo Excel como fuente de datos iniciales
faenas = pd.read_excel("faenas_chile.xlsx", header=0, index_col=0)
print("faenas: ", faenas)

#Modificar algunos nombres de columnas de datos
faenas.rename(columns={"RUT EMPRE":"Rut empresa","Este":"este","COMUNA F":"Comuna"}, inplace=True)
print("faenas: ",faenas)

#Crear una columna de datos en el DataFrame
faenas["Fecha de Proceso"] = "14 de noviembre"
print("faenas: ",faenas)

#Crear una columna vacía en el DataFrame con el nombre “Clima” y API
faenas["Clima"]= ""

#El DataFrame resultante, debe ser almacenado en una base de datos local

#Obtener los registros de la base de datos y exportar a un nuevo archivo Excel y otro archivo CSV.
faenas.to_csv("faenas_edit.csv", encoding="utf-8")
faenas.to_excel("faenas_edit.xlsx")