import random

NUM_ENTRANTS = 1000000
ODDS_MULTIPLIER = 3

# Converts odds in the form of n:1 to a probability from 0 to 1
def odds_to_prob(odds):
    return odds / (odds + 1)

# Converts probability from 0 to 1 to odds in the form n:1
def prob_to_odds(prob):
    return prob / (1 - prob)

def generate_affinities(all_characters):
    return {
        character: ODDS_MULTIPLIER ** random.uniform(-1, 1) 
        for character in all_characters
    }

# Chooses the best character given the weighted matchup odds and random affinities
def choose_character(weighted_matchup_odds, all_characters): 
    affinities = generate_affinities(all_characters)
    modified_odds = {
        character: weighted_matchup_odds[character] * affinities[character] 
        for character in all_characters
    }
    return max(modified_odds, key=modified_odds.get)
    
# Returns a map of character to probability of being picked
def run_single_tournament(weighted_matchup_odds, all_characters):
    entrants = {character: 0 for character in all_characters}
    
    for _ in range(NUM_ENTRANTS): 
        chosen_character = choose_character(weighted_matchup_odds, all_characters)
        entrants[chosen_character] += 1
    
    print(entrants)

    return {
        character: entrants[character] / NUM_ENTRANTS 
        for character in all_characters
    }
    
# Returns map of character to weighted odds
def get_weighted_matchups(matchup_chart, character_distribution, all_characters):
    weighted_odds = {}
    for me in all_characters:
        prob_win = 0
        for you in all_characters:
            prob_beat_you = character_distribution[you] * odds_to_prob(matchup_chart[me][you])
            prob_win += prob_beat_you
        weighted_odds[me] = prob_to_odds(prob_win)

    return weighted_odds

# Returns a tuple of 
# 1. The character_distribution
# 2. The weighted matchup odds
def run_multiple_tournaments(matchup_chart, num_iterations, all_characters):
    character_distribution = {
        character: 1 / len(all_characters)
        for character in all_characters
    }
    
    weighted_odds = get_weighted_matchups(matchup_chart, character_distribution, all_characters)
    
    average_character_distribution = {}
    average_weighted_odds = {}
    
    for iteration in range(num_iterations - 1):
        character_distribution = run_single_tournament(weighted_odds, all_characters)
        weighted_odds = get_weighted_matchups(matchup_chart, character_distribution, all_characters)
        
        if iteration == 10:
            average_character_distribution.update(character_distribution)
        if iteration > 10:
            average_character_distribution = {
                character: average_character_distribution[character] * .9 + character_distribution[character] * .1
                for character in average_character_distribution
            }

    if (num_iterations >= 12):
        average_weighted_odds = get_weighted_matchups(matchup_chart, average_character_distribution, all_characters)
    
    return (character_distribution, weighted_odds, average_character_distribution, average_weighted_odds)
    
    
