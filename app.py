from flask import Flask, render_template, request
import math
from itertools import combinations

app = Flask(__name__)

class Symptomes:
    def __init__(self, nausee, toux, maux_de_tete, diarrhee):
        self.nausee = nausee
        self.toux = toux
        self.maux_de_tete = maux_de_tete
        self.diarrhee = diarrhee

class Medicament:
    def __init__(self, nom, prix, effets):
        self.nom = nom
        self.prix = prix
        self.effets = effets

def trouver_medicament_optimal(malades, medicaments):
    symptomes = Symptomes(malades['nausee'], malades['toux'], malades['maux_de_tete'], malades['diarrhee'])
    medicaments_optimaux = []
    cout_total_minimum = float('inf')

    for k in range(1, len(medicaments) + 1):
        for combinaison in combinations(medicaments, k):
            boites = max(
                math.ceil(symptomes.nausee / sum(m.effets.nausee for m in combinaison)),
                math.ceil(symptomes.toux / sum(m.effets.toux for m in combinaison)),
                math.ceil(symptomes.maux_de_tete / sum(m.effets.maux_de_tete for m in combinaison)),
                math.ceil(symptomes.diarrhee / sum(m.effets.diarrhee for m in combinaison)),
            )

            cout_total = sum(boites * m.prix for m in combinaison)

            if cout_total < cout_total_minimum:
                medicaments_optimaux = list(combinaison)
                cout_total_minimum = cout_total

    return medicaments_optimaux, cout_total_minimum

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        malades = {
            'nausee': int(request.form['nausee']),
            'toux': int(request.form['toux']),
            'maux_de_tete': int(request.form['maux_de_tete']),
            'diarrhee': int(request.form['diarrhee'])
        }

        medicaments_optimaux, cout_total_minimum = trouver_medicament_optimal(malades, medicaments)

        return render_template('resultats.html', medicaments_optimaux=medicaments_optimaux, cout_total_minimum=cout_total_minimum)

    return render_template('index.html')

if __name__ == "__main__":
    medicament_A = Medicament("A", 10000, Symptomes(1, 3, 2, 8))
    medicament_B = Medicament("B", 8000, Symptomes(2, 5, 1, 3))
    medicament_C = Medicament("C", 12000, Symptomes(3, 2, 4, 1))
    medicaments = [medicament_A, medicament_B, medicament_C]

    app.run(debug=True)
