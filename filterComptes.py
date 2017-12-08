# Filtre les operations selon plusieurs parametres
# p est un dictionnaire attendant les clés suivantes : id, type, debut, fin, motif, verif, debit, credit, saisie
def filterComptes(exercice, **p):
	
	# Liste stockant les paramètres de filtrage
	conditions = list()
		
	for key, value in p.items():
	
		if key == "id":
			conditions.append(lambda ope: ope[0] == value)
		elif key == "type":
			conditions.append(lambda ope: ope[1] == value)

	return filtre
	

list(filter(lambda ope: ope[0]<3 and ope[1]=='CB', ex))
