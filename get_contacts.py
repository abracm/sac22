import csv
import os 
contatos = []

with open("resources\\lista_competidores.csv", "r") as f:
    for row in csv.DictReader(f):
        contatos.append(row)
        
with open("resources\\SAC2022-registration.csv", "r", encoding = "utf-8") as f:
    for row in csv.DictReader(f):
        for contato in contatos:
            if row["Name"] == contato["nome"]:
                contato["email"] = row["Email"]
                contato["competidor"] = "s"
                if row["Country"] in ["Argentina", "Colombia", "Bolivia", "Chille"]:
                    contato["lingua"] = "es"
                else:
                    contato["lingua"] = "pt"
                
with open("resources\\staff.csv", "r", encoding = "utf-8") as f:
    for row in csv.DictReader(f):
        encontrei = "não"
        for contato in contatos:
            if row["nome"] == contato["nome"]:
                contato["staff"] = "s"
                encontrei = "sim"
        if encontrei == "não":
            contatos.append({"nome":row["nome"],
                             "email":row["email"],
                             "staff":"s",
                            "lingua":"pt"})
            
with open("resources\\pódios.csv", "r", encoding = "utf-8-sig") as f:
    for row in csv.DictReader(f, delimiter = ";"):
        encontrei = "não"
        for contato in contatos:
            if row["nomes"] == contato["nome"]:
                contato["medalhista"] = "s"
                encontrei = "sim"
        if encontrei == "não":
            print ("não encontrei o {}".format(row["nomes"]))
            
for contato in contatos:
    try: contato["medalhista"]
    except: contato["medalhista"] = "n"
    
    try: contato["competidor"]
    except: contato["competidor"] = "n"
    
    try: contato["staff"]
    except: contato["staff"] = "n"

competidor = 0
staff = 0
medalhista = 0

for contato in contatos:
    if contato["medalhista"] == "s": medalhista += 1
    if contato["staff"] == "s": staff += 1
    if contato["competidor"] == "s": competidor += 1
    contato["primeiro_nome"] = contato["nome"][:contato["nome"].find(" ")]
    
print("Sanity report:\n{} competiddores, {} staff e {} medalhistas".format(competidor,
                                                                           staff,
                                                                           medalhista))

for file in os.listdir(): #folder with all of the medal certificates
    encontrei = "não"
    for contato in contatos:
        if contato["nome"] in file:
            encontrei = "sim"
    if encontrei == "não":
        print("não encontrei o {}".format(file))
        

with open("contatos.csv", "w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames = ["nome", "email", "lingua", "primeiro_nome",
                                             "competidor", "staff", "medalhista"])
    writer.writeheader()
    writer.writerows(contatos)
    
