from sf_matchup_calculator import get_sf_matchup_chart, sf_characters, sort_dictionary
from weighted_matchup_calculator import get_weighted_matchups, run_single_tournament

# luke	10
# ken	6.5
# dj	6
# juri	4.5
# chun-li	3.5
# jp	3
# guile	3
# dhalsim	3
# rashid	1.5
# cammy	1.5
# zangief	1
# ryu	0.5
# marisa	0.5
# blanka	0.5

cpt_characters = {
    "Luke": 10,
    "Ken": 6.5,
    "Dee Jay": 6,
    "Juri": 4.5,
    "Chun-Li": 3.5,
    "Dhalsim": 3,
    "Guile": 3,
    "JP": 3,
    "Cammy": 1.5,
    "Rashid": 1.5,
    "Zangief": 1,
    "Blanka": .5,
    "Marisa": .5,
    "Ryu": .5,
    "AKI": 0,
    "Honda": 0,
    "Jamie": 0,
    "Kimberly": 0,
    "Lily": 0,
    "Manon": 0,
}

def get_cpt_probabilities():
    return {
        character: cpt_characters[character] / 45
        for character in sf_characters
    }
    
def main():
    matchup_chart = get_sf_matchup_chart()
    character_distribution = get_cpt_probabilities()
    
    weighted_odds = get_weighted_matchups(matchup_chart, character_distribution, sf_characters)
    theoretical_character_distribution = run_single_tournament(weighted_odds, sf_characters)
    
    # Sort
    char_distribution = sort_dictionary(theoretical_character_distribution)
    weighted_odds = sort_dictionary(weighted_odds)
    
    print("Type Distributions (in a 10,000 person tournament)")
    for key, value in char_distribution.items():
        # print(f"{key}: {oct(int(value * 512))} / 0o1000")
        print(f"{key}: {round(value*10000)}")

    print()
    print("Weighted Odds")
    for key, value in weighted_odds.items():
        # print(f"{key}: {oct(int(value * 512))} : 0o1000")
        print(f"{key}: {value:.3f}:1")

if __name__ == "__main__":
    main()
    
    
    
    