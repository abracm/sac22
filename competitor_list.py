import json
import collections
import csv

with open("resources\\Results for SAC2022.json", "r", encoding = "utf-8") as f:
    
    conteudo = json.load(f)
    
#print(conteudo)

nomes = []

quant_estrangeiros = 0
nacional_estrangeiros = []
for person in conteudo["persons"]:
    #print(person["name"])
    nomes.append(person["name"])
    if person["countryId"] != "BR":
        quant_estrangeiros += 1
        nacional_estrangeiros.append(person["countryId"])
print(quant_estrangeiros)

print(collections.Counter(nacional_estrangeiros))

nomes = sorted(nomes)
print(len(nomes))
with open("lista_competidores.csv", "w", newline="") as f:
    '''
    writer = csv.writer(f)
    writer.writerow("{}".format("nome"))
    writer.writerows("{}".format(nomes))
    '''
    f.write("nome\n")
    for name in nomes:
        f.write(name + "\n")