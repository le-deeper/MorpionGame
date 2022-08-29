import pickle

format_plateau = """   a1 |  b1 |  c1
------------------
   a2 |  b2 |  c2
------------------
   a3 |  b3 |  c3"""

print(
    f"Bienvenu dans le jeu du morpion\nvoici ce qu'il faut saisir pour séléctionner une case:\n{format_plateau}\n\nSi "
    f"vous souhaitez le revoir pendant la partie, saisissez la commande 'format'\n"
    f"Si vous trouver que le choix du robot n'est pas judicieux, tapez 'problem:' et il apprendra tout seul :)\n")

status = {
    0: "Le match est terminée et il s'agit d'une égalité",
    1: "Le match est terminée et vous avez perdu !",
    -1: "Le match est terminée et vous avez gagné !"
}


class Plateau:
    def __init__(self, a1=" ", a2=" ", a3=" ", b1=" ", b2=" ", b3=" ", c1=" ", c2=" ", c3=" ", previous_plateau=None):
        previous_plateau: Plateau
        self.a1 = a1 if not previous_plateau else previous_plateau.a1
        self.a2 = a2 if not previous_plateau else previous_plateau.a2
        self.a3 = a3 if not previous_plateau else previous_plateau.a3
        self.b1 = b1 if not previous_plateau else previous_plateau.b1
        self.b2 = b2 if not previous_plateau else previous_plateau.b2
        self.b3 = b3 if not previous_plateau else previous_plateau.b3
        self.c1 = c1 if not previous_plateau else previous_plateau.c1
        self.c2 = c2 if not previous_plateau else previous_plateau.c2
        self.c3 = c3 if not previous_plateau else previous_plateau.c3
        self.sep_bar = "\n------------------\n"
        self.last_moves = []
        self.o_turn = False if not previous_plateau else previous_plateau.o_turn
        self.x_turn = True if not previous_plateau else previous_plateau.x_turn
        self.tout = []

    def maj(self):
        """
        Met à jour le plateau
        :return: le plateau -> str"""
        self.tout = [self.a1, self.b1, self.c1, self.a2, self.b2, self.c2, self.a3, self.b3, self.c3]
        intfce = []
        i = 0
        for c in range(3):
            intfce.append("   ")
            intfce.append(self.tout[i])
            intfce.append("  |  ")
            i += 1
            intfce.append(self.tout[i])
            intfce.append("  |  ")
            i += 1
            intfce.append(self.tout[i])
            i += 1
            if c != 2:
                intfce.append(self.sep_bar)
        return intfce

    def available_fields(self):
        """Renvoie les coordonnées vides"""
        available = []
        if self.a1 == " ":
            available.append("a1")
        if self.a2 == " ":
            available.append("a2")
        if self.a3 == " ":
            available.append("a3")
        if self.b1 == " ":
            available.append("b1")
        if self.b2 == " ":
            available.append("b2")
        if self.b3 == " ":
            available.append("b3")
        if self.c1 == " ":
            available.append("c1")
        if self.c2 == " ":
            available.append("c2")
        if self.c3 == " ":
            available.append("c3")
        return available

    def not_available_fields(self):
        """Renvoie les coordonnées non vides"""
        non_available = []
        if self.a1 != " ":
            non_available.append("a1")
        if self.a2 != " ":
            non_available.append("a2")
        if self.a3 != " ":
            non_available.append("a3")
        if self.b1 != " ":
            non_available.append("b1")
        if self.b2 != " ":
            non_available.append("b2")
        if self.b3 != " ":
            non_available.append("b3")
        if self.c1 != " ":
            non_available.append("c1")
        if self.c2 != " ":
            non_available.append("c2")
        if self.c3 != " ":
            non_available.append("c3")
        return non_available

    def display(self):
        """Affiche le plateau"""
        intfce = self.maj()
        total = ""
        for c in intfce:
            total += c
        print(total)

    @staticmethod
    def check(a, b, c):
        """
        Vérifie si a, b et c sont égaux et différents de " "
        :return: -1 s'il y a 3 x alignés, 1 s'il y a 3 y alignés et 0 s'il y a pas d'alignements de x ou de y
        """
        # print(a, b, c)
        if a == b == c and a != " ":
            if a == "x":
                return -1
            else:
                return 1
        else:
            return 0

    def update_combinations(self):
        """
        met à jour les emplacements pris dans le plateau
        """
        combinations = [(self.a1, self.a2, self.a3, "|"), (self.a1, self.b1, self.c1, "———"),
                        (self.a1, self.b2, self.c3, "\\"),
                        (self.a2, self.b2, self.c2, "———"), (self.a3, self.b3, self.c3, "———"),
                        (self.c1, self.c2, self.c3, "|"),
                        (self.c1, self.b2, self.a3, "/"), (self.b1, self.b2, self.b3, "|")]
        return combinations

    def finish(self):
        """vérifie si le jeu est terminé"""
        combinations = self.update_combinations()
        for c in combinations:
            final = self.check(c[0], c[1], c[2])
            if final == 1 or final == -1:
                return c, final
        if self.a1 != " " and self.a2 != " " and self.a3 != " " and self.b1 != " " and self.b2 != " " and \
                self.b3 != " " and self.c1 != " " and self.c2 != " " and self.c3 != " ":
            return True, 0
        return False, 0

    def set_point(self, coord, point):
        """
        Place les points sur le plateau et affiche le plateau
        :param coord: coordonées du point
        :param point: type du point (x ou y)
        :return: False si le point n'a pas été mis (car il existe déjà un point à ces coordonnées) ou True si le
                 placement du point est un succès
        """
        if coord == "a1":
            if self.a1 == " ":
                self.a1 = point
            else:
                return False
        elif coord == "a2":
            if self.a2 == " ":
                self.a2 = point
            else:
                return False
        elif coord == "a3":
            if self.a3 == " ":
                self.a3 = point
            else:
                return False
        elif coord == "b1":
            if self.b1 == " ":
                self.b1 = point
            else:
                return False
        elif coord == "b2":
            if self.b2 == " ":
                self.b2 = point
            else:
                return False
        elif coord == "b3":
            if self.b3 == " ":
                self.b3 = point
            else:
                return False
        elif coord == "c1":
            if self.c1 == " ":
                self.c1 = point
            else:
                return False
        elif coord == "c2":
            if self.c2 == " ":
                self.c2 = point
            else:
                return False
        elif coord == "c3":
            if self.c3 == " ":
                self.c3 = point
            else:
                return False
        self.last_moves.append(coord)
        # self.display()
        return True

    def change_turn(self):
        if self.x_turn:
            self.x_turn = False
            self.o_turn = True
        else:
            self.x_turn = True
            self.o_turn = False

    def who_turn(self):
        return "x" if self.x_turn else "o"


plateau = Plateau()
# plateau = Plateau(b1="x", b3="o", c1="o", c3="x", a1="o")
problems = [  # Problème qui doivent être remarqués par le robot
    # cross_problem
    {
        # length of emptys fields
        "len": 6,
        "cases": [("a1", "c3"),
                  ("c1", "a3"),
                  ],
        "solutions": ("a2", "b3", "b1", "c2"),
        "name": "Problème de la croix"
    }
]

# Ces variables vous donnent un aperçu
grid = []
final_plateaus = []
paths_groups = {}


def charger(nom_fichier):
    """
    Charge une liste de variables liées dans un fichier
    :param nom_fichier: Nom du fichier
    :return: liste de variables liées
    """
    try:
        with open(nom_fichier, "rb") as fichier:
            load = pickle.Unpickler(fichier)
            data = load.load()
    except FileNotFoundError:
        data = []
    return data


def ajouter(data, nom_fichier):
    """
    Sauvegarde une variable dans une liste de variables liées
    :param data: variable
    :param nom_fichier: nom du fichier
    :return: liste des variables liées
    """
    try:
        with open(nom_fichier, "rb") as fichier:
            loader = pickle.Unpickler(fichier)
            content = loader.load()
            content.append(data)
            # print("Fichier Trouvée")
    except FileNotFoundError:
        content = [data]
    with open(nom_fichier, "wb") as fichier:
        save = pickle.Pickler(fichier)
        save.dump(content)
    return content


def check_input(x):
    """Vérifie la saisie de l'utilisateur"""
    filter_input = ["a1", "a2", "a3", "b1", "b2", "b3", "c1", "c2", "c3", "format", "problem"]
    if x not in filter_input and x.split(":")[0] not in filter_input:
        passe = False
        while not passe:
            x = input("vous n'avez pas saisi une donnée correct, veuillez recommencez: ")
            if x in filter_input or x.split(":")[0] in filter_input:
                return x
    else:
        return x


def clear_spaces(sentence):
    """
    Supprime les espaces au début et à la fin d'une phrase s'il y en a
    :param sentence: phrase
    :return: phrase sans les espaces au début et à la fin
    """
    starts_with_space = sentence[0] == " "
    ends_with_space = sentence[-1] == " "
    if starts_with_space:
        sentence = sentence[1:]
    if ends_with_space:
        sentence = sentence[:-1]
    return sentence


def get_probability(path):
    """
    Retourne la probabilité d'un chemin grâce à une fonction
    :param path:
    :return:
    """
    shots = path[0].split(";")[:-1]
    n = len(shots)
    i = path[1]
    # fonction par défaut: path[1] + 1/len(shots) ou i + 1/n
    p_path = i + 1 / n  # POINT SENSIBLE: modifiez cette fonction pour obtenir des prévisions différentes!
    # print(f"La probabilité de {shots} est {p_path}")
    return p_path


def get_best_shot(best_shots_list=False):
    """
    Retourne le ou les meilleurs coup(s)
    :param best_shots_list: S'il faut retourner le meilleur coup ou les meilleurs coups
    :return:
    """
    # paths_groups: {'b1,o': [['b1,o;c2,x;', 0, 0.5], 0.5], 'c2,o': [['c2,o;b1,x;', -1, -0.5], -0.5]}
    for base, paths in paths_groups.items():
        probs = []
        # base: a2,o
        # paths: [['a3,o;b1,x;b3,o;c1,x;', -1], ['a3,o;b1,x;c1,o;', 1], ['a3,o;b3,x;b1,o;c1,x;', -1],
        #         ['a3,o;b3,x;c1,o;', 1], ['a3,o;c1,x;', -1]]
        for path in paths:
            # print(path)
            p_path = get_probability(path)
            path.append(p_path)  # on ajoute la probabilité de ce chemin à la fin
            probs.append(p_path)

        # Moyenne
        moy = sum(probs) / len(probs)
        paths_groups[base].append(moy)  # on ajoute la probabilité de cette base après ses chemins

        # Écart type
        # standart_deviation = 0
        # for x in probs:
        #     standart_deviation += (x - moy)**2
        # standart_deviation = standart_deviation / len(probs)
        # paths_groups[base].append(standart_deviation)

        # Médiane
        # sorted_probs = sorted(probs)
        # if len(sorted_probs) % 2 == 0:
        #     mediane = sorted_probs[int(len(sorted_probs) / 2)]
        # else:
        #     if len(sorted_probs) == 1:
        #         mediane = sorted_probs[0]
        #     else:
        #         mediane1 = sorted_probs[int((len(sorted_probs) + 1) / 2)]
        #         mediane2 = sorted_probs[int((len(sorted_probs) - 1) / 2)]
        #         mediane = (mediane1 + mediane2) / 2
        # paths_groups[base].append(mediane)

    # best_shots: [('c2,o', 0.5), ('b1,o', -0.5)]
    best_shots = sorted([(x, y[-1]) for x, y in paths_groups.items()], key=lambda x: x[1], reverse=True)

    if not best_shots_list:
        # path = best_path_group[0]
        # shots = path[0].split(";")
        # best_shot = shots[0]
        [print(f"la probabilité des chemins avec comme base {base} est {p_base}") for base, p_base in
         best_shots].clear()  # moyen efficace d'utiliser des listes compréhensions !
        # best_shots[0]: ('b2,o', 0.10519855000823883)
        best_shot = best_shots[0][0]
        return best_shot
    else:
        # print(f"Les meilleurs coups sont: {best_shots}")
        return [shot[0] for shot in best_shots]


def problems_recognition(plateau: Plateau):
    """
    Reconnait les différents problèmes signalés par le joueur
    :param plateau: plateau actuel
    :return:
    """
    empty_fields = plateau.available_fields()
    problems.extend(charger("problems"))
    # print(problems)
    for problem in problems:
        # problems = [
        #     {
        #         # length of emptys fields
        #         "len": 6,
        #         "cases": [("a1", "c3"),
        #                   ("c1", "a3"),
        #                   ],
        #         "solutions": ("a2", "b3", "b1", "c2"),
        #         "name": "Problème de la croix"
        #     }
        # ]
        if len(empty_fields) == problem["len"]:
            for points in problem["cases"]:
                # print(f"{x} et {y}: {empty_fields}")
                condition_situation = all([point not in empty_fields for point in points])
                condition_same_point = True
                i = 0
                point_value = ""
                while i < len(points):
                    if i == 0:
                        point_value = plateau.__getattribute__(points[i])
                        i += 1
                        continue
                    condition_same_point = plateau.__getattribute__(points[i]) == point_value
                    i += 1
                if condition_situation and condition_same_point:
                    if isinstance(problem["solutions"], tuple):
                        for solution in problem["solutions"]:
                            if solution in empty_fields:
                                return problem["name"], f"{solution},{plateau.who_turn()}"
                    elif isinstance(problem["solutions"], int):
                        best_shots = get_best_shot(best_shots_list=True)
                        # print(best_shots)
                        # print(problem['solutions'])
                        # print(best_shots[problem['solutions']])
                        return problem["name"], f"{best_shots[problem['solutions']]}"
    return False, ""


def create_problem(plateau, parameters):
    """
    Crée un problème car la solution fournie par la probabilité n'est pas celle préférée par l'utilisateur
    :param plateau:
    :param parameters:
    :return:
    """
    # print(f"Les paramètres sont: {parameters}")
    length = len(plateau.available_fields()) + 1

    name = parameters.get("name", None)
    if not name:
        name = "Problème"
    else:
        name: str
        name = name.capitalize()

    solutions = parameters.get("solutions", None)
    if not solutions:
        # solutions = 1
        # [('c2,o', -0.5), ('b1,o', 0.5)]
        best_shots = sorted([(x, y[-1]) for x, y in paths_groups.items()], key=lambda x: x[1], reverse=True)
        p_best_shots = [round(shot[1], 3) for shot in best_shots]
        p_prev_shot = p_best_shots[0]
        i = 0
        for p_shot in p_best_shots:
            if p_shot != p_prev_shot:
                break
            else:
                i += 1
        solutions = i
        print(f"L'indice de la solution sera {solutions}")
    else:
        if len(solutions.split(",")) == 1:
            solutions = int(solutions)
        else:
            solutions = tuple(solutions.split(","))
    cases = []
    case = []
    point = plateau.who_turn()
    # print(plateau.not_available_fields())
    for field in plateau.not_available_fields():
        if plateau.__getattribute__(field) == point:
            case.append(field)
    cases.append(tuple(case))

    new_problem = {
        "len": length,
        "cases": cases,
        "solutions": solutions,
        "name": name
    }

    ajouter(new_problem, "problems")


def predict(plateau: Plateau, grid: list, historique: str = False, parent=True):
    """
    Prédit le prochain meilleur coup
    :param plateau: Plateau de morpion
    :param grid: Grille (arbre des probables prochains coups)
    :param historique: crée un historique pour chaque coup en cours
    :param parent: s'il s'agit de l'élement parent (utile car cette fonction est récursive)
    :return:
    """
    available_fields = plateau.available_fields()
    # grid_parts = []
    # available_fields: ['a2', 'a3', 'b1', 'b2', 'b3', 'c1', 'c2', 'c3']
    for field in available_fields:
        # print(available_fields)
        grid_part = {(plateau.who_turn(), field): []}  # crée pour chaque espace vide un dictionnaire
        grid.append(grid_part)  # ajoute le dictionnaire à grid
        new_plateau = Plateau(previous_plateau=plateau)  # instancie new_plateau de la classe Plateau
        new_plateau.set_point(field, plateau.who_turn())  # place un point dans un espace vide
        if not historique:
            historique = ""
        # new_plateau.display()  # affiche le plateau
        finish, winner = new_plateau.finish()  # définit dans finish l'état du jeu et winner le vainqueur
        if finish:  # si le jeu est terminé
            # new_plateau.display()
            [x for x in grid_part.values()][0].append(winner)  # ajoute à la première clé dans grid_part le gagnant
            final_plateaus.append(new_plateau)  # ajoute le plateau final à final_plateaus
            key = paths_groups.get(historique.split(";")[0], False)
            if not key:
                if not historique:
                    paths_groups[f"{field},{plateau.who_turn()}"] = [
                        [historique + f"{field},{plateau.who_turn()};", winner]]
                else:
                    paths_groups[historique.split(";")[0]] = [[historique + f"{field},{plateau.who_turn()};", winner]]
            else:
                key: list
                key.append([historique + f"{field},{plateau.who_turn()};", winner])
            continue  # réiterer la boucle
        new_plateau.change_turn()  # change la personne à qui c'est le tour de jouer
        predict(new_plateau, [x for x in grid_part.values()][0], historique + f"{field},{plateau.who_turn()};",
                False)  # appelle predict pour la première clé de grid_part
    if parent:
        problem_recognized, best_shot = problems_recognition(plateau)
        if problem_recognized:
            print(f"{problem_recognized} reconnu !")
            return best_shot
        else:
            return get_best_shot()


def main(dont_display=False, reset=False):
    """
    Fonction principale
    :param dont_display: S'il faut afficher le tableau dès le début
    :param reset: S'il faut réinitialiser le tableau
    :return:
    """
    global plateau

    if reset:
        plateau = Plateau()
    if not dont_display:
        plateau.display()

    if plateau.x_turn:
        turn = "x"
    else:
        grid.clear()
        final_plateaus.clear()
        paths_groups.clear()
        best_shot = predict(plateau, grid).split(",")
        # print(f"Les chemins possibles sont :\n{paths}")
        # print(plateau.last_moves)
        print(best_shot)
        plateau.set_point(best_shot[0], best_shot[1])
        finish, winner = plateau.finish()
        if finish:
            plateau.display()
            return print(status[winner])
        plateau.change_turn()
        # plateau.display()
        return main()
    data = input(f"C'est au tour de {turn} choisissez la case que vous voulez: ")
    data = check_input(data)
    if data == "format":
        print(format_plateau)
        main(dont_display=True)
    elif data.split(":")[0] == "problem":
        try:
            parameters = data.split(":")[1]
            # parameters: "name:dilemme de la victoire;solutions:1"
            print(f"La longueur des paramètres est {len(parameters)}")
            if len(parameters) == 0:
                parameters = {}
            else:
                parameters = clear_spaces(parameters)
                parameters = {clear_spaces(key.split("=")[0]): clear_spaces(key.split("=")[1])
                              for key in parameters.split(";")}
            create_problem(plateau, parameters)
            return main(reset=True)
        except IndexError:
            print("Le problème n'est pas défini correctement\nLe format est le suivant: "
                  "problem: name=dilemme de la victoire=solutions=a1,b3 (les espaces entre paramètres sont autorisées)")
            return main(dont_display=True)
    else:
        success = plateau.set_point(data, turn)
        if not success:
            print("Aucune modification n'a été appliquée, la case choisie est déjà remplie")
            return main()
        finish, winner = plateau.finish()
        if finish:
            plateau.display()
            return print(status[winner])
        plateau.change_turn()
        main()


main()

# best_shot = predict(plateau, grid)
# print(best_shot)
