import csv

competidores = []
grupos = []
with open("resources\\SA Champs 2022 Groups - All Groups.csv", "r", encoding="utf-8") as f:
    
    reader = csv.DictReader(f)
    for row in reader:
        #print(row)
        competidores.append(row)

with open("resources\\groups.csv", "r", encoding="utf-8-sig") as f:
    reader = csv.DictReader(f, delimiter=";")
    for row in reader:
        grupos.append(row)

for grupo in grupos:
    nome_evento = {"333" : "3x3x3",
                   "222" : "2x2x2",
                   "444":"4x4x4",
                   "555":"5x5x5",
                   "666":"6x6x6",
                   "777":"7x7x7",
                   "333bf":"3x3x3 Vendado/a Ciegas",
                   "333fm":"3x3x3 Menos Movimentos/Movimientos",
                   "333oh":"3x3x3 com Uma Mão/a Una Mano",
                   "333mbfa":"3x3x3 Multi Vendado/Multi Ciegas",
                   "333mbfb":"3x3x3 Multi Vendado/Multi Ciegas",
                   "clock":"Clock",
                   "sq1": "Square-1",
                   "minx":"Megaminx",
                   "pyram":"Pyraminx",
                   "skewb":"Skewb",
                   "444bf":"4x4x4 Vendado/a Ciegas",
                   "555bf":"5x5x5 Vendado/a Ciegas"}
    grupo["nome_oficial"] = nome_evento[grupo["modalidade"]]
    
    palco_oficial = {"blue":"Auditório (Azul)",
                     "red":"Salão (Vermelho)",
                     "green":"Sala do BLD (Verde)"}
    grupo["palco_oficial"] = palco_oficial[grupo["palco"]]

    print(grupo)
for competidor in competidores:
    
    grupos_competidor = []
    for key in competidor:
        #print(competidor["Name"])
        if key not in ["Name","WCA ID","Staff?","Scrambler?"]:
            if competidor[key] != "0":
                total = competidor[key]
                #print(competidor[key])
                palco = total[0]
                grupo = total[1]
                
                palco_replacement = {"B":"blue",
                                     "R":"red",
                                     "G":"green"}
                
                palco = palco_replacement[palco]
                #print(key)
                #print(competidor[key], key)
                
                #if key != "333fm":
                filtrado_modalidade = [d for d in grupos if d["modalidade"]==key]
                filtrado_grupo = [d for d in filtrado_modalidade if d["grupo"]==grupo]
                filtrado_palco = [d for d in filtrado_grupo if d["palco"]==palco]
                #print(filtrado_grupo)
                grupos_competidor.append(filtrado_palco[0])
                #print(filtrado_palco[0])
    competidor["grupos"] = grupos_competidor
    
#TODO - incluir fewest moves
'''
for competidor in competidores:
    novos_grupos = []
    for grupos in competidor["grupos"]:
        for grupo in grupos:
            novos_grupos.append(grupo)          
'''


for competidor in competidores:
    competidor["grupos"] = sorted(competidor["grupos"], key=lambda i: i['início'])


for competidor in competidores:
    if competidor["grupos"] != []:
        if competidor["grupos"][0]["modalidade"] == "333fm":
            competidor["grupos"].append({'modalidade': '333fm', 'grupo': '1', 'início': '22/07/2022 16:20', 'fim': '22/07/2022 17:25', 'palco': 'green', 'nome_oficial': '3x3x3 Menos Movimentos/Movimientos', 'palco_oficial': 'Sala do BLD (Verde)'})
            competidor["grupos"].append({'modalidade': '333fm', 'grupo': '1', 'início': '22/07/2022 17:25', 'fim': '22/07/2022 18:25', 'palco': 'green', 'nome_oficial': '3x3x3 Menos Movimentos/Movimientos', 'palco_oficial': 'Sala do BLD (Verde)'})

for competidor in competidores:
    competidor["grupos"] = sorted(competidor["grupos"], key=lambda i: i['início'])

for competidor in competidores:
    sexta = []
    sabado = []
    for grupo in competidor["grupos"]:
        if "22/07/2022" in grupo["início"]:
            sexta.append(grupo)
        if "23/07/2022" in grupo["início"]:
            sabado.append(grupo)
    competidor["sexta"] = sexta
    competidor["sabado"] = sabado

for competidor in competidores:
    if competidor["grupos"] != []:
        em_construcao = ""
        em_construcao += "Campeonato Sul-Americano Rubik's WCA 2022 - Cronograma Individual"
        em_construcao += "\n\n" + competidor["Name"]
        
        if competidor["WCA ID"]  != None:
            em_construcao += " - " + competidor["WCA ID"]
        if competidor["sexta"] != []:
            em_construcao += "\n\nSEXTA-FEIRA/VIERNES (22/07/2022):"
            for grupo in competidor["sexta"]:
                em_construcao += "\n- "+grupo["início"][11:] + "-" + grupo["fim"][11:]+\
                    " (Grupo " +grupo["grupo"]+")" + " - " + grupo["nome_oficial"]+ " | Palco: " + grupo["palco_oficial"]
    
        if competidor["sabado"] != []:
            em_construcao += "\n\nSÁBADO (23/07/2022):"
            for grupo in competidor["sabado"]:
                em_construcao += "\n- "+grupo["início"][11:] + "-" + grupo["fim"][11:]+\
                    " (Grupo " +grupo["grupo"]+")" + " - " + grupo["nome_oficial"]+ " | Palco: " + grupo["palco_oficial"]
                    
        with open('Cronogramas Individuais\\'+competidor["Name"]+".txt", 'w') as f:
            f.write(str(em_construcao))