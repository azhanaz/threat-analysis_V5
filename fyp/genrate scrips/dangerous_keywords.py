import random

# Define a comprehensive list of keywords
keywords = [
    "threat", "attack", "bomb", "kill", "explosion", "danger", "assault",
    "murder", "hijack", "hostage", "gun", "shoot", "terrorist", "violence",
    "destroy", "explosive", "nuclear", "chemical", "biological", "cyberattack",
    "sabotage", "threaten", "strike", "raid", "crash", "dangerous", "explode",
    "destruction", "hostile", "aggression", "militant", "extremist", "threatening",
    "seize", "capture", "malware", "ransomware", "kidnap", "assassinate",
    "covert operation", "sabotage", "snipe", "combat", "conflict", "insurgency",
    "extortion", "blackmail", "intimidate", "violent", "subversive", "subversion",
    "vandalism", "riot", "uprising", "coup", "overthrow", "rebellion", "sedition",
    "anarchist", "militia", "guerrilla", "sabotage", "bioterrorism", "chemical warfare",
    "radiation", "dirty bomb", "IED", "improvised explosive device", "car bomb",
    "suicide bomber", "nuclear threat", "biological agent", "chemical agent",
    "hazardous material", "dangerous substance", "lethal", "destructive device",
    "aggressive act", "hostile act", "violent act", "terror act", "armed attack",
    "cyber threat", "digital attack", "network intrusion", "data breach", "system hack"
]

# Function to generate keywords with weights
def generate_keywords(num_keywords):
    if num_keywords > len(keywords):
        raise ValueError("Number of keywords requested exceeds available keywords.")
    
    keywords_with_weights = {}
    chosen_keywords = random.sample(keywords, num_keywords)
    
    for keyword in chosen_keywords:
        weight = random.randint(10, 50)  # Example weight range
        keywords_with_weights[keyword] = weight

    return keywords_with_weights

# Generate a set of keywords
keywords_with_weights = generate_keywords(100)  # Example for 100 keywords

# Write the keywords and weights to the file
with open("dangerous_keywords.py", "w") as file:
    file.write("dangerous_keywords = {\n")
    for keyword, weight in keywords_with_weights.items():
        file.write(f'    "{keyword}": {weight},\n')
    file.write("}\n")

print("Generated dangerous keywords and saved to 'dangerous_keywords.py'.")
