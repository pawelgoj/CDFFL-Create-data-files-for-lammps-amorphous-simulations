import json
import re 



with open('AtomsData.json', 'r') as file:
    jsonFile = json.load(file)


atomicMassdict = {}
for item in jsonFile:
    atomicMass = item['atomicMass']
    if type(atomicMass) == type([0]):
        atomicMass = round(float(atomicMass[0]), 4)
    elif type(atomicMass) == type('strig'):
        atomicMass = round(float(re.sub(r'\(\d*\)', '', atomicMass)), 4)
    else:
        raise Exception('wrong data')
    
    atomicMassdict.update({item['symbol']: atomicMass})

jsonNewFile = json.dumps(atomicMassdict)

print(jsonNewFile)

with open("AtomMass.json", 'a') as file:
    file.write(jsonNewFile)
    