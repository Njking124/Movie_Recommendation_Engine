import random

# Define movie genres and example templates
genres = [
    "action",
    "adventure",
    "animation",
    "biography",
    "comedy",
    "crime",
    "drama",
    "family",
    "fantasy",
    "history",
    "horror",
    "music",
    "musical",
    "mystery",
    "romance",
    "sci-fi",
    "sport",
    "thriller",
    "war",
    "western"
]

templates = [
    "Something thrilling with fights, chases, and explosions. I like stunts. Violence and gore.",
    "I'm in the mood for a treasure hunt or quest, maybe with pirates and epic heroes and villains.",
    "I watch cartoons and anime. My children love wholesome educational artwork.",
    "Something inspiring. About life. Biopic. True story and real life.",
    "Something hilarious and crude. So so funny and lighthearted. Filled with utter joy. Satirical and witty.",
    "Mysterious, Sherlock Holmes. Murder mystery. Tragedy, dark. A whodunnit, similar to Agatha Christie.",
    "A true story or similar to real life. Sad and heavy. About love, life, and loss.",
    "Something I can watch with my kids, age-appropriate. Funny, animated. Disney perhaps.",
    "I like dragons and ogres and folklore. The supernatural like ghosts and zombies and witches. Imagination, unreal.",
    "Something that has happened, low key, low budget, artistic.",
    "Supernatural, psychological, thrilling, on the edge of my seat, terrifying. Apocalyptic.",
    "Fun. Dance numbers, jazzy. Singing.",
    "Dancing and singing.",
    "Agatha Christie, Sherlock Holmes. Piecing together clues. Plot twist. Murder.",
    "Predictable hallmark, sentimental. Emotional tragedy, personal journey. Care Hope. Queer, gay.",
    "Time travel teleportation, telepathy and aliens. Star wars. Fantastic, dystopian.",
    "Baseball, football, Olympics, competition. Underdog protagonist.",
    "I want to be sweating at the edge of my seat. Anxious and uncertain and surprise.",
    "Violence destruction mortality. Life and death and the moments in between. Uncertainty, legality, and ethics.",
    "America, small towns, saloons. Outlaws and bandits. Horse, cowboy.",
    "Heart-pounding and charged. Like a superhero movie."
]

# Generate examples
examples = []
examples_per_label = 5
total_examples = 250

# Create a dictionary to keep track of used examples for each genre
used_examples = {genre: [] for genre in genres}

while len(examples) < total_examples:
    genre = random.choice(genres)
    if len(used_examples[genre]) < examples_per_label:
        example = random.choice(templates)
        if example not in used_examples[genre]:
            used_examples[genre].append(example)
            examples.append((example, genre))

# Shuffle the examples to make them random
random.shuffle(examples)

# Save the examples to a CSV file
import csv

with open("movie_examples.csv", mode="w", newline="") as file:
    writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for example in examples:
        writer.writerow(example)

print(f"CSV file 'movie_examples.csv' has been created with {total_examples} unique examples.")
