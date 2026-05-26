from classes.game import Game
from classes.races.all import *
from classes.races.neural import NeuralBrain
import math
import random
import os

razas = [
    Prey(), Predator(), 
    Human(), Randomint(), 
    Ant, Bee(), Mimic(), 
    Dog(), Viltrumite(), 
    Comunist()
]

def entrenar(generaciones:int, poblacion:int, dias:int, path = 'archivo.txt', path_log = 'log.txt'):
    #poblacion inicial random
    if os.path.exists(path):
        cerebro = NeuralBrain.cargar(path)
        print("Usando cerebro entrenado")
        cerebros = [cerebro]
        for _ in range(poblacion-1):
            cerebros.append(cerebro.mutar())

    else:
        cerebros = [NeuralBrain().__class__() for _ in range(poblacion)]

    with open(path_log, "w", encoding="utf-8") as f:
        f.write("Nuevo entrenamiento\n")
        f.write(f"Generaciones: {generaciones} - Poblacion: {poblacion}\n")


    gen_amount = 0
    stats_gen = {}
    mejor_cerebro = None
    mejor_fitness = 0

    sigma = 0.5          # empieza explorando amplio
    sin_mejora = 0       # contador de generaciones sin mejorar

    for gen in range(generaciones):
        #evaluar cada cerebro
        resultados = []
        for cerebro in cerebros:
            score = evaluar(cerebro, dias)
            resultados.append((cerebro,score))
        
        #ordenar de mejor a peor
        resultados.sort(key=lambda x: x[1], reverse=True)

        #guardar el mejor
        if resultados[0][1] > mejor_fitness:
            mejor_fitness = resultados[0][1]
            mejor_cerebro = resultados[0][0]
            mejor_cerebro.guardar(path)  # ← esto
            sin_mejora = 0       # reset del contador
            sigma = max(0.05, sigma * 0.7)  # afina un poco al mejorar
            #print(f"  *** Nuevo record, cerebro guardado ***")
        else:
            sin_mejora += 1
            if sin_mejora >= 20:  # 20 generaciones sin mejorar
                sigma = min(1.5, sigma * 1.2)  # explora más amplio
                sin_mejora = 0
                text = f'  [sigma ajustado a {sigma:.3f}]'
                with open(path_log, "a", encoding="utf-8") as f:
                    f.write(f"{text}\n")
                print(text)
                

                # si sigma se fue muy alto, reiniciar desde el mejor cerebro
                if sigma > 0.4:
                    sigma = 0.05
                    text = f'  [reset sigma → {sigma}]'
                    with open(path_log, "a", encoding="utf-8") as f:
                        f.write(f"{text}\n")
                    print(text)
                    cerebro_base = NeuralBrain.cargar(path)
                    cerebros = [cerebro_base]
                    while len(cerebros) < poblacion:
                        cerebros.append(cerebro_base.mutar(sigma=sigma))

                

        if (gen % 100  == 0):
            gen_amount += 1
            stats_gen[f'{gen_amount*100}'] = 0
        stats_gen[f'{gen_amount*100}'] += resultados[0][1]
        
        text = f'Gen {gen+1}/{generaciones} | Mejor: {resultados[0][1]:.1f} | Record: {mejor_fitness:.1f}'

        with open(path_log, "a", encoding="utf-8") as f:
            f.write(f"{text}\n")
        
        print(text)

        #quedarse con los mejores (25%)
        n_elite = max(2,poblacion//4)
        elite = [cerebro for cerebro, _ in resultados[:n_elite]]

        #rellenar el resto con mutaciones del elite
        cerebros = list(elite)
        while len(cerebros) < poblacion:
            padre = elite[len(cerebros) % len(elite)]
            cerebros.append(padre.mutar(sigma=sigma))

    print(f'=======================================')
    print(f'Entrenamiento terminado. Record: {mejor_fitness:.1f}')
    for stat in stats_gen:
        text = f'{stat}: {round(stats_gen[stat]/100,2)}'
        with open(path_log, "a", encoding="utf-8") as f:
            f.write(f"{text}\n")
        print(text)
    
    return mejor_cerebro

        


def evaluar(brain: NeuralBrain, dias:int = 100, other_amount: int = 4) -> float:
    game = Game(trees=30, fruits=4)

    for _ in range(3):
        game.individues.append(Neural(brain=brain))

    #rivales varios
    for i in range(len(razas)): #_ in range(5):
        #i = random.randint(0,len(razas)-1)

        if i == 4:
            ant_type = AntType.QUEEN
            game.individues.append(Ant(ant_type=ant_type))
            for j in range(other_amount-1):
                x = random.random()
                if x < 0.10:
                    ant_type = AntType.WARRIOR
                elif x < 0.20:
                    ant_type = AntType.DEFENSIVE
                elif x < 0.99:
                    ant_type = AntType.WORKER
                else:
                    ant_type = AntType.QUEEN
                game.individues.append(Ant(ant_type=ant_type))
        else:
            game.individues += [razas[i].__class__() for x in range(other_amount)]    

    max_neurales = 0
    dias_sobrevivio = 0

    for dia in range(dias):
        game.simulate_one_day()

        cantidad = sum(1 for ind in game.individues if isinstance(ind, Neural))
        max_neurales = max(max_neurales, cantidad)

        if cantidad > 0:
            dias_sobrevivio = dia + 1
        else:
            break #todos murieron

    #hijos_totales = sum(ind.hijos_totales for ind in game.individues if isinstance(ind, Neural))
    
    fitness = dias_sobrevivio * math.sqrt(max(1,max_neurales))
    return fitness

"""brain = NeuralBrain()
score = evaluar(brain, dias=50)
print(f'fitness de un cerebro random: {score:.2f}')"""


from datetime import datetime
date = datetime.now().strftime("%Y:%m:%d-%H:%M")


#probar el entrenamiento
for i in range(10):
    mejor = entrenar(generaciones=500, poblacion=50+i*10, dias=50,path = 'brains/mejor_cerebro.json', path_log=f'logs/log_cerebro_run{i+1}_{date}.txt')

    print(f"Cerebro entrenado: {mejor}")