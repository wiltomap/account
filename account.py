#/Library/Frameworks/Python.framework/Versions/3.6/bin/python3

import os
os.chdir("C:/Users/t-williamson/Data/perso/account") # Windows
# os.chdir("/Users/tomelsa/Google Drive/informatique/python/comptes") # iMac

# Ligne a coller dans l'IDLE pour executer le fichier
# exec(open("C:/Users/t-williamson/Data/perso/account/account.py").read(), globals())

# cd C:/Users/t-williamson/Data/perso/account

# Fichier contenant les fonctions necessaires au programme
from functions import *

# Chargement de la liste stockee dans le fichier binaire "data"
ex = loadComptes("data")

initComptes("data", ex)

# os.system("pause")
