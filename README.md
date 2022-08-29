# MorpionGame
A Morpion Game without using any special packages

Programme de Morpion basé sur les probabilités et sur l'apprentissage

Le jeu s'affiche sous une forme de grille:

   a1 |  b1 |  c1
------------------
   a2 |  b2 |  c2
------------------
   a3 |  b3 |  c3

Pour choisir un emplacement entre les coordonnées de cet emplacement.

Ce programme choisit le meilleur coup en calculant la 'probabilité' de chaque chemins et donc en créant une probabilité pour chaque base (moyenne des 'probabilités' des chemins de cette base). À chaque coup, il affiche la probabilité des différents coups

Pour calculer la 'probabilité', une fonction par défaut est utilisé:
i + 1 / n

i: status du chemin (victoire -> 1, défaite -> -1 et nul -> 0)
n: nombre de coups qui compose ce chemin

Cette fonction crée une probabilité définit sur [-2;2] peut bien sûr être modifié.

Comme le programme est basé sur des probabilités, on retrouve des dilemmes logiques comme par exemple:

      |     |  x
------------------
      |  x  |
------------------
   o  |  x  |  o

Dans cette exemple, pour nous, si on jouait o, le prochain coup est évident (b1). Pourtant si on réfléchit, il s'agit d'un dilemme évident.
On peut choisir la sécurité et placer o dans l'emplacement b1 mais si on le fait, on ne peut plus gagner (le jeu finira sur un nul à coup sûr).
En revanche, on peut prendre le risque et choisir de placer o dans a2. Si l'adversaire est déconcentré ou pas très malin, il place son x dans c2 et la victoire est à nous ou si l'adversaire choisit b1 il gagne et le match finit probablement sur nul s'il choisit de placer x dans a1.

Pour changer ce comportement, taper "problem:". Le robot va enregistrer le jeu (les emplacements de x, le nombre d'emplacements vides...) et va choisir le 2e meilleur coup (en général c'est celui-là que l'on veut) lorsque vous effectuez les mêmes choix dans une autre partie: Il apprend!

Cependant, si vous voulez un choix spécifique, vous pouvez bien sûr le spécifier:
"problem: name = Dilemme X ; solutions = b1,c2"
les solutions peuvent être des emplacements et dans ce cas doivent être listées ou un nombre désignant n meilleur coup (le programme choisira n meilleur coup la prochaine fois)

les paramètres (falcultatifs) de "problem" sont:
name: nom du problème
solutions: solution de ce problème (emplacements ou nombre)

Après chaque prévision, les données sont disponnibles dans les variables grid, final_plateaus, paths_groups
Dans grid est stocké une grille qui montre les différents chemins possibles après le coup de l'adversaire
Dans final_plateaux est stocké tous les plateaux qui correspondent aux chemins dans grid (on peut accéder à l'historique des différents coup avec plateau.last_moves)
Dans paths_groups est stocké toutes les bases des chemins avec leur probabilité et tous les chemins avec leur probabilité

La fonction main peut être surchargée ou modifié afin d'afficher ces variables !


Je crois que j'ai tous dit, Bon Jeu!
