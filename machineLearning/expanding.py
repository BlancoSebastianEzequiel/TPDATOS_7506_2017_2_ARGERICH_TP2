from .utils import *
from .dataFrameUtils import *
from .descriptionExpansion import ParsearDescripcion, InicializarDiccionario

def ExpandirFechaCreacion(dataFrame):
	dataFrame['created_on_year'] = MapearColumna(dataFrame['created_on'], lambda x: int(x.split('-')[0]))
	dataFrame['created_on_month'] = MapearColumna(dataFrame['created_on'], lambda x: int(x.split('-')[1]))

def ExpandirFechaVolcado(dataFrame, archivo):
	archiveParts = archivo.split('-')
	dataFrame['dump_date_year'] = pd.Series(int(archiveParts[2]), index = dataFrame.index)
	dataFrame['dump_date_month'] = pd.Series(int(archiveParts[3]), index = dataFrame.index)

def ExpandirPais(dataFrame):
	if not 'country_name' in dataFrame:
		dataFrame['country_name'] = MapearColumna(dataFrame['place_with_parent_names'], lambda x: x.split('|')[1])

def ExpandirProvincia(dataFrame):
	if not 'state_name' in dataFrame:
		dataFrame['state_name'] = MapearColumna(dataFrame['place_with_parent_names'], lambda x: x.split('|')[2])

def GetBarrio(full_place_name):
	partes = full_place_name.split('|')
	barrio = partes[3]
	if (barrio != ''):
		return barrio
	return partes[2]

def ExpandirBarrio(dataFrame):
	dataFrame['barrio'] = MapearColumna(dataFrame['place_with_parent_names'], GetBarrio)

def ExpandirDescripcion(dataFrame, claves):
	if 'description' in dataFrame:
		columnaDescription = Map(dataFrame['description'].values, ParsearDescripcion)
	else:
		diccionario = InicializarDiccionario(claves)
		columnaDescription = [diccionario for i in range(0, len(dataFrame.index))]

	for k in claves:
		dataFrame[k] = pd.Series([diccionario[k] for diccionario in columnaDescription], index = dataFrame.index)
