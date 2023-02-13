mustHave = [
	"practica", # practicante, practicas
	"beca", # becario, becas	
	"estudiante", # estudiante, estudiantes
 
	"to ciclo", # 5to, 6to ciclo
	"mo ciclo", #  7mo, ultimo ciclo
	"vo ciclo", #  8vo ciclo
	"no ciclo", #  9no ciclo
	
	"to semestre", # 5to, 6to semestre
	"mo semestre", #  7mo, ultimo semestre
	"vo semestre", #  8vo semestre
	"no semestre", #  9no semestre
	
	"er año", # tercer año
	"to año", # cuarto, quinto año
	"mo año", #  ultimo año
 
	"io superior", # tercio superior
	"to superior", # quinto superior
	"mo superior", #  decimo superior
	
	"pre-pro", # pre-profesional, pre-pro
	"pre pro", # pre profesional, pre pro
	
	"egresad", # egresado, egresada
	"graduad", # graduado, graduada
]

from fuzzywuzzy import fuzz

def checkKeywords(keywords):
	for keyword in keywords:
		for must in mustHave:
			if fuzz.ratio(keyword, must) > 90:
				return True
	return False