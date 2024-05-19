import random
import os
from datetime import datetime

path = os.path.dirname(os.path.abspath(__file__))

teilnehmer = ['Hanna und Yanis','Alexandra','Schäri','Sandra','Joris','Didi','Elisabeth','Kurt']
constraints = {'Elisabeth':['Kurt'], 'Hanna und Yanis':['Kurt']}

weihnachtsbaum = ' '*6 + '*' +'\n' + ' '*5 + '***' +'\n' + ' '*4 + '*****' +'\n' + ' '*5 + '***' +'\n' + ' '*4 + '*****' +'\n' + ' '*3 + '*******' +'\n'  + ' '*4 + '*****' +'\n' + ' '*3 + '*******' +'\n' + ' '*2 + '*********' +'\n'
teilnehmer_str = '\n'.join([f'\t{n}' for n in teilnehmer])
anleitung = f'Informationen:\n- Das Geschenk darf nicht mehr als CHF 100.- kosten\n- Übergabe der Geschenke am 25.12.2023\n- Bei Fragen an Yanis wenden\n- Teilnehmer des diesjährigen Wichtelns:\n{teilnehmer_str}\n\nFROHE WEIHNACHTEN!\n{weihnachtsbaum}'

def write_files(draw: dict, dt: str):
    if not os.path.exists(os.path.join(os.getcwd(), f'Ziehung_{dt}')):
        os.makedirs(os.path.join(path, f'Ziehung_{dt}'))
        print(f'Ordner Ziehung_{dt} erstellt.')
    for key in draw:
        with open(os.path.join(path, f'Ziehung_{dt}', f'{key}.txt'),'w+') as f:
            f.write(f'Liebe:r {key}\n\nWillkommen zum Wichteln 2023. Du hast folgende Person(en) gezogen:\n\n\t{draw[key].upper()}\n\n{anleitung}')

def get_max_key(domains: dict):
    max_key = None
    max_length = 0
    for key, value in domains.items():
        if len(value) > max_length:
            max_key = key
            max_length = len(value)
    return max_key, max_length

def get_min_key(domains: dict):
    min_key = None
    min_length = float('inf')
    for key, value in domains.items():
        if len(value) < min_length and len(value) > 1:
            min_key = key
            min_length = len(value)
    return min_key, min_length

def csp(teilnehmer: list, constraints: dict={}):
    """
    constraints: dict of constraints, e.g. {'Hanna': ['Yanis', 'Alexandra']} means that Hanna cannot draw Yanis or Alexandra
    """
    random.shuffle(teilnehmer)
    domains = {}
    for name in teilnehmer:
        if name in constraints.keys():
            domains[name] = [n for n in teilnehmer if n is not name and n not in constraints[name]]
        else:
            domains[name] = [n for n in teilnehmer if n is not name]

    while get_max_key(domains)[1] > 1:
        min_key, _ = get_min_key(domains)
        draw = random.choice(domains[min_key])
        domains[min_key] = [draw]
        for key in domains:
            if key != min_key and key != draw and len(domains[key]) > 1: # enforce arc consistency
                domains[key].remove(draw)
        if any(len(domains[key]) == 0 for key in domains):
            return None
    return {key: domains[key][0] for key in domains}
        
def main():
    now = datetime.now()
    dt = now.strftime('%d%m%Y_%H%M%S')
    draw = csp(teilnehmer, constraints=constraints)
    if draw is not None:
        write_files(draw, dt)
        print('Ziehung erfolgreich.')
    else:
        print('Ziehung fehlgeschlagen.')
    
if __name__ == '__main__':
    main()

