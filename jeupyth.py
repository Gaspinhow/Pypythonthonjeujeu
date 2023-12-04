import os
import random
import time

def effacer_ecran():
    os.system('cls' if os.name == 'nt' else 'clear')

def afficher_carte(c, symboles, p, score, vies):
    print('\033c')  # Effacer l'écran
    for i, ligne in enumerate(c):
        for j, num in enumerate(ligne):
            if (j, i) == (p["x"], p["y"]):
                print(f'\033[91m{p["char"]}\033[0m', end="")
            else:
                if num == 0:
                    print(" ", end="")
                elif num == 2:
                    print('\033[92mD\033[0m', end="")
                elif num == 1:
                    print('\033[90m#\033[0m', end="")

        print()
    print("Score:", score, "Vies:", vies)

def generer_carte(lignes, colonnes, probabilite):
    matrice_carte = [[0] * colonnes for _ in range(lignes)]
    for i in range(lignes):
        for j in range(colonnes):
            if random.random() < probabilite:
                matrice_carte[i][j] = 1
            elif random.random() < 0.05:
                matrice_carte[i][j] = 2
    return matrice_carte

def creer_personnage(position_depart, max_vies):
    return {"char": "o", "x": position_depart[0], "y": position_depart[1], "vies": max_vies}

def mettre_a_jour_personnage(lettre, p, c, score):
    nouvelle_x, nouvelle_y = p["x"], p["y"]

    if lettre == "z":
        nouvelle_y -= 1
    elif lettre == "q":
        nouvelle_x -= 1
    elif lettre == "s":
        nouvelle_y += 1
    elif lettre == "d":
        nouvelle_x += 1

    if 0 <= nouvelle_y < len(c) and 0 <= nouvelle_x < len(c[0]):
        if c[nouvelle_y][nouvelle_x] == 1:
            p["vies"] -= 1
            if p["vies"] == 0:
                print("Game Over ! Vous avez épuisé toutes vos vies.")
                time.sleep(2)
                return None, score
            else:
                print(f"Vous avez heurté un obstacle ! Vies restantes : {p['vies']}")
                time.sleep(2)
                return p, score
        elif c[nouvelle_y][nouvelle_x] == 2:
            c[nouvelle_y][nouvelle_x] = 0
            score += 1
        p["x"], p["y"] = nouvelle_x, nouvelle_y

    return p, score

def jouer_etape(lignes, colonnes, probabilite_de_un, max_vies):
    carte = generer_carte(lignes, colonnes, probabilite_de_un)
    personnage = creer_personnage((0, 0), max_vies)
    score = 0
    total_objets = sum(ligne.count(2) for ligne in carte)

    temps_debut = time.time()

    while True:
        afficher_carte(carte, {0: "_", 1: "#", 2: "d"}, personnage, score, personnage["vies"])

        entree_utilisateur = input("Entrez une direction (z, q, s, d) ou 'exit' pour quitter : ")

        if entree_utilisateur.lower() == 'exit':
            return None

        if entree_utilisateur.lower() in ["z", "q", "s", "d"]:
            personnage_mis_a_jour, score_mis_a_jour = mettre_a_jour_personnage(entree_utilisateur.lower(), personnage, carte, score)
            if personnage_mis_a_jour is not None:
                personnage, score = personnage_mis_a_jour, score_mis_a_jour

        if score == total_objets or personnage["vies"] == 0:
            temps_fin = time.time()
            temps_ecoule = temps_fin - temps_debut

            afficher_carte(carte, {0: "_", 1: "#", 2: "d"}, personnage, score, personnage["vies"])
            if personnage["vies"] == 0:
                print("Game Over ! Vous avez épuisé toutes vos vies.")
            else:
                print("Bravo, vous passez au niveau suivant !")
                print(f"Votre temps est de {temps_ecoule:.2f} secondes.")
            time.sleep(2)

            return temps_ecoule, personnage["vies"]  # Retourner le temps écoulé et les vies restantes lorsque le dernier niveau est atteint

def afficher_menu():
    print('\033c')  # Effacer l'écran
    print("\033[1;33m===== Menu du jeu =====\033[0m")
    print("\033[1;36m1. Commencer le jeu\033[0m")
    print("\033[1;36m2. Instructions\033[0m")
    print("\033[1;36m3. Quitter\033[0m")
    print("\033[1;33m=======================\033[0m")

def afficher_instructions():
    print('\033c')  # Effacer l'écran
    print("\033[1;33m===== Instructions =====\033[0m")
    print("\033[1;36mUtilisez 'z', 'q', 's', 'd' pour vous déplacer.\033[0m")
    print("\033[1;36mCollectez les objets 'd' pour marquer des points.\033[0m")
    print("\033[1;36mÉvitez les obstacles représentés par '#'\033[0m")
    print("\033[1;36mQuittez le jeu à tout moment en tapant 'exit'\033[0m")
    print("\033[1;36mFinissez les niveaux le plus vite possible!\033[0m")
    input("\033[1;36mAppuyez sur Entrée pour revenir au menu.\033[0m")
   

def principal():
    temps_total = 0  # Variable pour stocker le temps total

    while True:
        afficher_menu()
        choix = input("\033[1;32mEntrez votre choix (1-3) :\033[0m ")

        if choix == '1':
            nombre_etapes = 3
            lignes = 15
            colonnes = 15
            probabilite_de_un = 0.15
            vies_max = 3

            for etape in range(1, nombre_etapes + 1):
                print(f"Étape {etape}")
                resultat = jouer_etape(lignes, colonnes, probabilite_de_un, vies_max)
                if resultat is None:
                    break

                temps_total += resultat[0]  # Ajouter le temps de l'étape complétée
                if resultat[1] == 0:
                    break  # Si game over, sortir de la boucle

            if resultat is not None:  # Si toutes les étapes sont terminées ou game over
                print(f"Temps total de jeu : {temps_total:.2f} secondes")
                input("\033[1;32mAppuyez sur Entrée pour revenir au menu.\033[0m")

        elif choix == '2':
            afficher_instructions()

        elif choix == '3':
            print('\033c')  # Effacer l'écran
            if temps_total > 0:
                print(f"Temps total de jeu : {temps_total:.2f} secondes")
            print("\033[1;31mAu revoir !\033[0m")
            break

        else:
            input("\033[1;31mChoix invalide. Appuyez sur Entrée pour continuer.\033[0m")

if __name__ == "__main__":
    principal()
