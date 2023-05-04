from pymongo import MongoClient
import csv
from ast import literal_eval

# Connect to MongoDB
mongoClient = MongoClient("mongodb://localhost/pokemon")
pokemonDB = mongoClient['pokemondb']
pokemonColl = pokemonDB['pokemon_data']

# Load Data From CSV making sure data types are converted correctly
csvfile = open('pokemon.csv')
reader = csv.DictReader(csvfile)

flist = ["name", "pokedex_number", "types", "hp", "attack", "defense", "speed", "sp_attack", "sp_defense", "abilities"]
numlist = ["pokedex_number", "hp", "attack", "defense", "speed", "sp_attack", "sp_defense"]
for each in reader:
    row={}
    for field in each:
        if field in flist:
            if field in numlist:
                row[field] = int(each[field])
            elif field == "abilities":
                row[field] = literal_eval(each[field])
            else:
                row[field] = each[field]
    pokemonColl.insert_one(row)

# Queries

print("All pokemon named Pikachu")
pikachu = pokemonColl.find_one({"name": "Pikachu"})
print(pikachu)

print("All pokemon with attack greater than 150")
attack150 = pokemonColl.find({"attack": {"$gt": 150}})
for i in attack150:
    print(i["name"] + ": " + str(i["attack"]))

print("All pokemon with Overgrow ability")
overgrow = pokemonColl.find({"abilities": 'Overgrow'})
for i in overgrow:
    print(i["name"] + ": " + str(i["abilities"]))
