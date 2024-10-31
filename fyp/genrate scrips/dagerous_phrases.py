import random

# Define lists of actions, targets, and adjectives
actions = [
    "attack", "destroy", "bomb", "kill", "sabotage", "threaten", "assault",
    "shoot", "hijack", "takeover", "release", "initiate", "create", "plant", "unleash",
    "cause", "stage", "plot", "prepare", "disrupt", "incite"
]
targets = [
    "building", "facility", "city", "government", "people", "infrastructure",
    "public area", "transport system", "hospital", "school", "data center",
    "military base", "embassy", "power plant", "water supply", "communication network"
]
adjectives = [
    "massive", "deadly", "devastating", "large-scale", "severe", "high-risk",
    "dangerous", "extreme", "violent", "critical", "major", "catastrophic",
    "threatening", "hostile", "destructive", "disruptive", "fatal", "harmful"
]

# Function to generate a set of phrases with weights
def generate_phrases(num_phrases):
    phrases = set()
    while len(phrases) < num_phrases:
        action = random.choice(actions)
        target = random.choice(targets)
        adjective = random.choice(adjectives)
        phrase = f"{adjective} {action} {target}"
        weight = random.randint(50, 90)  # Example weight range
        phrases.add((phrase, weight))
    return phrases

# Generate 2,000 phrases
phrases = generate_phrases(20000)

# Write the phrases to the file
with open("dangerous_phrases.py", "w") as file:
    file.write("dangerous_phrases = {\n")
    for phrase, weight in phrases:
        file.write(f'    "{phrase}": {weight},\n')
    file.write("}\n")

print("Generated 2,000 dangerous phrases and saved to 'dangerous_phrases.py'.")
