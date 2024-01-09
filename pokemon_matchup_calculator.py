import json
from weighted_matchup_calculator import run_multiple_tournaments

all_types = [
    "Normal",
    "Fire",
    "Water",
    "Electric",
    "Grass",
    "Ice",
    "Fighting",
    "Poison",
    "Ground",
    "Flying",
    "Psychic",
    "Bug",
    "Rock",
    "Ghost",
    "Dragon",
    "Dark",
    "Steel",
    "Fairy"
]

ODDS_MULTIPLIER = 1.5

# Import the pokemon type info from disk
def get_type_chart():
    with open('type_chart.json') as f:
        return json.load(f)
        
# A helper function for checking pokemon type info
def check(type1, verb, type2):
    if not hasattr(check, "type_chart"):
        check.type_chart = get_type_chart()
    return type2 in check.type_chart[type1][verb]

# A multi-dimensional dictionary for getting the odds that A beats B
def get_matchup_chart():
    matchup_chart = {}
    for me in all_types:
        matchup_chart[me] = {}
        for you in all_types:
            odds = 1

            # Positive Interactions
            if check(you, "weak", me):
                odds *= ODDS_MULTIPLIER
            if check(me, "resist", you):
                odds *= ODDS_MULTIPLIER
            if check(me, "immune", you):
                odds = odds * ODDS_MULTIPLIER * ODDS_MULTIPLIER
                
            # Negative Interactions
            if check(me, "weak", you):
                odds /= ODDS_MULTIPLIER
            if check(you, "resist", me):
                odds /= ODDS_MULTIPLIER
            if check(you, "immune", me):
                odds = odds / ODDS_MULTIPLIER / ODDS_MULTIPLIER
            
            matchup_chart[me][you] = odds
    
    return matchup_chart
    
def sort_dictionary(dictionary):
    return dict(sorted(dictionary.items(), key=lambda item: item[1], reverse=True))

def main():
    matchup_chart = get_matchup_chart()
    (type_distribution, weighted_odds, average_type_distribution, average_weighted_odds) = run_multiple_tournaments(matchup_chart, 30, all_types)
    
    # Sort
    type_distribution = sort_dictionary(average_type_distribution)
    weighted_odds = sort_dictionary(average_weighted_odds)
    
    print("Type Distributions (in a 10,000 person tournament)")
    for key, value in type_distribution.items():
        # print(f"{key}: {oct(int(value * 512))} / 0o1000")
        print(f"{key}: {round(value*10000)}")

    print()
    print("Weighted Odds")
    for key, value in weighted_odds.items():
        # print(f"{key}: {oct(int(value * 512))} : 0o1000")
        print(f"{key}: {value:.3f}:1")

main()
