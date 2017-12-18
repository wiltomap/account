# ex = [

	# # [ Id, Opération, Date, Motif, Vérification, Débit, Crédit, Date saisie ]
	# [1, "CB", "2017-11-10", "Super U", 0, 29.51, 0, "2017-11-28 15:23"],
	# [2, "CB", "2017-11-10", "Fournil d'Elina", 1, 9.20, 0, "2017-11-28 15:27"],
	# [3, "CB", "2017-11-11", "Essence", 1, 55.01, 0, "2017-11-29 12:01"],
	# [4, "RET", "2017-11-11", "Liquide", 0, 60.00, 0, "2017-12-01 11:38"],
	# [5, "VIR", "2017-11-12", "CPAM (remboursement)", 0, 0, 23.51, "2017-12-04 13:56"]

# ]

# Répertoire de travail
# Les données sont stockées dans un dictionnaire, dans un fichier binaire
# os.chdir("C:/Users/t-williamson/Data/perso/openclassrooms/python/comptes")

# Lecture / écriture dans le fichier binaire "comptes"
import pickle

# Permet de détecter l'OS pour vider la console > fonction idar()
import platform

# Support des expressions régulières
import re

# Gestion des dates et heures
import time
import datetime


# Patterns de dates pour fonction newOperation()
jm = "^(0[1-9]|[1-2][0-9]|3[0-1])\/(0[1-9]|1[0-2])$" # format jj/mm
jma = "^(0[1-9]|[1-2][0-9]|3[0-1])\/(0[1-9]|1[0-2])\/20[0-9]{2}$" # format jj/mm/aaaa


# Annee en cours pour fonction newOperation()
annee = str(datetime.date.today().year)


# Fonction initiale
def initComptes(fichier, exercice):
	print("*** GESTION DES COMPTES ***")
	affichMenu(fichier, exercice)


# Affiche le menu
def affichMenu(fichier, exercice):

	ajout = "1 : Nouvelle operation"
	marq  = "2 : Marquer une operation"
	maj   = "3 : Mettre a jour une operation"
	suppr = "4 : Supprimer une operation"
	aff0  = "5 : Afficher les operations en attente"
	aff1  = "6 : Filtrer les operations"
	exit  = "7 : Quitter"
	line  = 31 * "_"

	print(line, ajout, marq, maj, suppr, aff0, aff1, exit, "\n", sep = "\n")

	choix = int(input("Que souhaitez-vous faire ? "))

	while choix <= 0 or choix >= 8:
		print("Ce choix n'est pas possible...\n")
		choix = int(input("Que souhaitez-vous faire ? "))

	if choix == 1:
		newOperation(exercice)
	elif choix == 2:
		marqOperation(fichier, exercice)
	elif choix == 3:
		pass
	elif choix == 4:
		pass
	elif choix == 5:
		filterComptes(exercice, **{"verif": 0})
	elif choix == 6:
		affichFilter()
	else:
		exit()


# Vérifie si une opération est enregistrée
def check(exercice, id):
	verif = False
	for operation in exercice:
		if operation[0] == id:
			verif = True
			new_operation = operation
	if verif:
		print("Opération enregistrée : " + str(new_operation))
		#print(new_operation)
	else:
		print("Opération absente...")


# Conversion d'une date saisie en jj/mm ou jj/mm/aaaa -> aaaa-mm-jj
def conversionDate(date):

	if re.match(jm, date):
	    date = "{}-{}-{}".format(annee, date[3:], date[:2])

	if re.match(jma, date):
	    date = "{}-{}-{}".format(date[6:], date[3:5], date[:2])

	return date


# Ajout d'une nouvelle opération
def newOperation(exercice):

	id = max(exercice)[0] + 1

	print("\nNouvelle operation :", "\n")

	typ = input("Type : ")
	date = input("Date : ")

	# Gestion de la date
	while not re.match(jm, date) and not re.match(jma, date):
		print("La date n'est pas au bon format (jj/mm ou jj/mm/aaaa) !")
		date = input("Date : ")

	date = conversionDate(date)

	motif = input("Motif : ")

	# Gestion de l'entrée pour verif
	verif = input("Vérifiée (1/0) ? ")

	while not verif == "1" and not verif == "0":
		print("Saisie incorrecte (0 ou 1) !")
		verif = input("Vérifiée (1/0) ? ")

	verif = int(verif)

	# Gestion du montant
	montant = input("Montant (débits précédés du signe -) : ")

	while True:
		try:
			montant = float(montant.replace(",", "."))
		except ValueError:
			print("Montant saisi invalide !")
			montant = input("Montant (débits précédés du signe -) : ")
		else:
			break

	# Fléchage débit / crédit
	if montant < 0:
		debit = abs(montant)
		credit = 0
	else:
		debit = 0
		credit = abs(montant)

	# Récupération date - heure de saisie
	date_saisie = time.strftime("%Y-%m-%d %H:%M", time.localtime())

	# Ajout de la nouvelle opération
	new = [id, typ, date, motif, verif, debit, credit, date_saisie]
	exercice.append(new)

	# Sauvegarde de la liste dans le fichier binaire "data"
	saveComptes("data", exercice)

	# Confirme l'enregistrement
	exercice = loadComptes("data")
	check(exercice, id)

	# Affiche le menu
	affichMenu("data", exercice)


# Fonction d'écriture dans le fichier
# Prend en paramètre un objet dictionnaire stockant les opérations
def saveComptes(fichier, exercice):
	with open(fichier, "wb") as file:
		a = pickle.Pickler(file)
		a.dump(exercice)


# Fonction de chargement du contenu du fichier
def loadComptes(fichier):
	with open(fichier, "rb") as file:
		a = pickle.Unpickler(file)
		comptes = a.load()
	return comptes


# Marque une opération comme vérifiée
def marqOperation(fichier, exercice):
	id = int(input("Identifiant de l'operation a marquer : "))
	for operation in exercice:
		if operation[0] == id:
			operation[4] = 1
			print("L'operation {} a ete marquee comme vérifiee.".format(str(id)))
			break

	# Sauvegarde de l'operation modifiee
	saveComptes(fichier, exercice)

	# Recharge et affiche le fichier a jour
	exercice = loadComptes(fichier)
	affichMenu(fichier, exercice)


# Calcul du solde
def solde(base, exercice, solde_banque = False):

	solde = base

	for operation in exercice.values():

		# Solde en ignorant les opérations non-vérifiées (solde banque)
		if solde_banque:
			if operation[3] == 1:
				solde = solde - operation[4] + operation[5]

		# Solde toutes opérations (solde réel)
		else:
			solde = solde - operation[4] + operation[5]

	return solde


# Affichage des opérations
def affichComptes(fichier, exercice):

	# Largeur de colonne
	w_id = 5
	w_type = 5
	w_date = 12
	w_motif = 25
	w_verif = 1
	w_debit = 10
	w_credit = 10
	w_saisie = 18

	print("\n")

	for operation in exercice:

		# Stockage des composantes d'une opération dans des variables
		id = str(operation[0])
		type = operation[1]
		date = str(operation[2])
		motif = operation[3]
		verif = "x" if operation[4] == 1 else ""
		debit = str("{0:.2f}".format(operation[5]))
		credit = str("{0:.2f}".format(operation[6]))
		saisie = str(operation[7])

		# Largeur du contenu
		len_id = len(str(id))
		len_type = len(type)
		len_motif = len(motif)
		len_verif = len(verif)
		len_debit = len(debit)
		len_credit = len(credit)
		len_saisie = len(saisie)

		# Largeur des espaces blancs à ajouter
		ws_id = w_id - len_id
		ws_type = w_type - len_type
		ws_motif = w_motif - len_motif
		ws_verif = w_verif - len_verif
		ws_debit = w_debit - len_debit
		ws_credit = w_credit - len_credit
		ws_saisie = w_saisie - len_saisie

		ligne = id + (ws_id * " ") + type + (ws_type * " ") + date + (2 * " ") +	motif + (ws_motif * " ") + verif + (ws_verif * " ") + (ws_debit * " ") + "-" + debit + (ws_credit * " ") + "+" + credit + (ws_saisie * " ") + saisie

		print(ligne)

	# Affiche le menu
	affichMenu(fichier, exercice)


# Menu de filtrage
def affichFilter():

	id      = "1 : Filtrer par référence"
	type    = "2 : Filtrer par type d'operation"
	date    = "3 : Filtrer par date d'operation"
	motif   = "4 : Filtrer par motif"
	verif   = "5 : Filtrer par verification"
	montant = "6 : Filtrer par montant"
	saisie  = "7 : Filtrer par date de saisie"

	print("\n", id, type, date, motif, verif, montant, saisie, "\n", sep = "\n")

	choix = input("Filtre(s) à appliquer ? ")

	filtre = dict()

	for c in choix:

		if c == '1':
			fid = input("id : ")
			filtre["id"] = int(fid)

		elif c == '2':
			ftype = input("Type (CB / WEB / RET / DC / VIR / Numero de cheque): ")
			filtre["type"] = ftype

		elif c == '3':
			fdate = input("Date operation : ")

			while not re.match(jm, fdate) and not re.match(jma, fdate):
				print("La date n'est pas au bon format (jj/mm ou jj/mm/aaaa) !")
				fdate = input("Date operation : ")

			fdate = conversionDate(fdate)
			filtre["date"] = fdate

		elif c == '4':
			fmotif = input("Motif : ")
			filtre["fmotif"] = fmotif

		elif c == '5':
			fverif = input("Verification (0/1) : ")
			filtre["verif"] = int(fverif)

		elif c == '6':
			fmontant = input("Montant (débit précédé du signe -) : ")

			while True:
				try:
					fmontant = float(fmontant.replace(",", "."))
				except ValueError:
					print("Montant saisi invalide !")
					fmontant = input("Montant (débit précédé du signe -) : ")
				else:
					break

			# Fléchage débit / crédit
			if fmontant < 0:
				filtre["debit"] = abs(fmontant)
				filtre["credit"] = 0
			else:
				filtre["debit"] = 0
				filtre["credit"] = abs(fmontant)

		elif c == '7':
			fsaisie = input("Date saisie : ")

			while not re.match(jm, fsaisie) and not re.match(jma, fsaisie):
				print("La date n'est pas au bon format (jj/mm ou jj/mm/aaaa) !")
				fsaisie = input("Date operation : ")

			fsaisie = conversionDate(fsaisie)
			filtre["saisie"] = fsaisie

	print(filtre)


# Filtre les operations selon plusieurs parametres
# p est un dictionnaire attendant les cles suivantes : id, type, debut, fin, motif, verif, debit, credit, saisie
def filterComptes(exercice, **p):

	champs = { "id": 0, "type": 1, "date": 2, "motif": 3, "verif": 4, "debit": 5, "credit": 6, "saisie": 7 }

	def conditions(**p):

		def filtre(ope):

			for key, value in p.items():
				if ope[champs[key]] != value:
					return False
			return True

		return filtre

	# Filtrage des operations sur la liste "exercice"
	resultat = list(filter(conditions(**p), exercice))

	# Affichage du resultat
	affichComptes("data", resultat)


# Vide la console Python
def clear(p):
    # p est l'OS
    commands = {"Windows": "cls", "Linux": "idar"}
    try:
        os.system(commands[p])
    except: # empty string or Java os name
        print(chr(27) + "[2J")
