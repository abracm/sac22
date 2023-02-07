import smtplib
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE
import datetime
import csv
import os

#Fonte: https://stackoverflow.com/questions/3362600/how-to-send-email-attachments    

#TODO: error handler no envio do email
#TODO: importar dados csv, possibilidade de envios graduais (não enviar para quem já enviou)

server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()
server.login("contato@abracm.org.br", password)

contatos = []

with open("resources\contatos.csv", "r", encoding="utf-8") as f:
    for contato in csv.DictReader(f):
        contatos.append(contato)

def constroi_corpo(contato):
    cabecalho_pt = "Olá, {fulano}!\n\n\
Nós da Associação Brasiliense de Cubo Mágico agradecemos muito a sua participação no Campeonato Sul-Americano Rubik's WCA 2022! Foram dias inesquecíveis de competição, confraternização e alegria, e você foi uma parte muito importante disso!"
    rodape_pt = "Obrigado por tudo e até logo!\n\n\
Atenciosamente,\n\n\
ABRACM"
    competidor_pt = "Receba com carinho, em anexo, o seu certificado de participação no Campeonato! Foi muito especial ter você junto de nós nesse evento. Obrigado pela participação e parabéns pelos seus resultados!"
    staff_pt = "Dedicamos um agradecimento especial a você por ter participado do Campeonato como staff. Seu empenho foi essencial para que o evento acontecesse com tanto esplendor. Em anexo, está o seu certificado de staff, com 40 horas de atividades complementares."
    medalhista_pt = "Por fim, enviamos também o(s) certificado(s) da(s) medalha(s) que recebeu no Campeonato Sul-Americano Rubik's WCA 2022. Seus resultados entraram para sempre na história!"
    
    cabecalho_es = "¡Hola, {fulano}!\n\n\
¡Desde la Associação Brasiliense de Cubo Mágico le agradecemos mucho su participación en el Campeonato Sudamericano Rubik's WCA 2022! Fueron días inolvidables de competencia, confraternización y alegría, ¡y tú fuiste parte muy importante de ello!"
    rodape_es = "¡Gracias por todo y hasta pronto!\n\n\
Tuya sinceramente,\n\n\
ABRACM"
    competidor_es = "¡Reciba adjunto su certificado de participación en el Campeonato! Fue muy especial tenerte con nosotros en este evento. ¡Gracias por participar y enhorabuena por tus resultados!"
    staff_es = "Les agradecemos especialmente su participación en el Campeonato como staff. Su dedicación fue fundamental para que el evento se desarrollara con tanto esplendor. Se adjunta su certificado de personal, con 40 horas de actividades complementarias."
    medalhista_es = "Finalmente, también te enviamos el(los) certificado(s) de la(s) medalla(s) que recibiste en el Campeonato Sudamericano Rubik's WCA 2022. ¡Tus resultados pasarán a la historia para siempre!"
    
    es = {"cabecalho":cabecalho_es,
          "rodape":rodape_es,
          "competidor":competidor_es,
          "staff":staff_es,
          "medalhista":medalhista_es}
    pt = {"cabecalho":cabecalho_pt,
          "rodape":rodape_pt,
          "competidor":competidor_pt,
          "staff":staff_pt,
          "medalhista":medalhista_pt}
    
    linguas = {"es":es,
            "pt":pt}
    
    corpo = ""
    
    corpo += (linguas[contato["lingua"]]["cabecalho"].format(fulano = contato["primeiro_nome"]))
    if contato["competidor"] == "s": corpo += "\n\n"+(linguas[contato["lingua"]]["competidor"])
    if contato["staff"] == "s": corpo += "\n\n"+ (linguas[contato["lingua"]]["staff"])        
    if contato["medalhista"] == "s": corpo += "\n\n"+ (linguas[contato["lingua"]]["medalhista"])
    corpo += "\n\n"+(linguas[contato["lingua"]]["rodape"])
    
    return corpo

def reune_arquivos(contato):
    arquivos = []
    if contato["competidor"] == "s": arquivos.append("\competidor\\Certificado Competidores - "+contato["nome"]+".pdf")
    if contato["staff"] == "s": arquivos.append("\staff\\Certificado Staff - "+contato["nome"]+".pdf")
    if contato["medalhista"] == "s":
        for file in os.listdir("\medalhas"):
            if contato["nome"] in file:
                arquivos.append("\medalhas\\" + file)
    return arquivos

limite = 0
for contato in contatos:
    if limite < 200:
        if contato["enviado"] in ["não"]:
            try:
                subject = "Campeonato Sul-Americano Rubik's WCA 2022 - Certificado"
                
                body = constroi_corpo(contato)
                msg = MIMEMultipart()
                msg['Subject'] = subject
                
                for f in reune_arquivos(contato):
                    with open(f, "rb") as fil:
                        part = MIMEApplication(
                            fil.read(),
                            Name=basename(f)
                        )
                    # After the file is closed
                    part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
                    msg.attach(part)
              
                msg["To"] = contato["email"]
                msg.attach(MIMEText(body))
                server.sendmail("contato@abracm.org.br", contato["email"], msg.as_string())
                print(("enviado para {} às {}").format(contato["nome"], datetime.datetime.now()))
                contato["enviado"] = "sim"
            except:
                print("Deu ruim o {} às {}".format(contato["nome"], datetime.datetime.now()))
                contato["enviado"] = "não"
            with open("listas\contatos.csv", "w", encoding="utf-8", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=["nome", "email", "lingua","primeiro_nome","competidor","staff","medalhista","enviado"])
                writer.writeheader()
                writer.writerows(contatos)
        if contato["enviado"] == "não":
            print(contato["nome"])

        
server.quit()