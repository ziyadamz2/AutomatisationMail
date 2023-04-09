import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE
from email import encoders

# Paramètres SMTP pour Gmail
smtp_server = "smtp.gmail.com"
smtp_port = 587

# Adresse email et mot de passe de l'expéditeur
expediteur = "devfbweb23@gmail.com"
mot_de_passe = "trlpfychbmbfaibm"

# Adresse email du destinataire
destinataire = "amzilziyad10@gmail.com"

# Création du message
msg = MIMEMultipart()
msg['From'] = expediteur
msg['To'] = destinataire
msg['Subject'] = "Extraction du jour"

# Ajout du corps du message
message = "Bonjour,\n\nVoici une pièce jointe pour vous."
msg.attach(MIMEText(message))

# Ajout de la pièce jointe
nom_fichier = "/home/ziyad/projet_informatique/AutomatisationMail/resultat/2023-04-09.csv"
piece_jointe = open(nom_fichier, "rb")
part = MIMEBase('application', 'octet-stream')
part.set_payload((piece_jointe).read())
encoders.encode_base64(part)
part.add_header('Content-Disposition', "attachment; filename= %s" % nom_fichier)
msg.attach(part)

# Connexion au serveur SMTP et envoi du message
serveur_smtp = smtplib.SMTP(smtp_server, smtp_port)
serveur_smtp.starttls()
serveur_smtp.login(expediteur, mot_de_passe)
serveur_smtp.sendmail(expediteur, destinataire, msg.as_string())
serveur_smtp.quit()