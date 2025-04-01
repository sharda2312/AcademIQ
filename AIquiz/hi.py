hi = [{'question': 'What is the largest state in India by area?', 'options': ['Rajasthan', 'Uttar Pradesh', 'Madhya Pradesh', 'Maharashtra'], 'correct': '1'}, {'question': 'Which of the following is a renewable resource?', 'options': ['Coal', 'Water', 'Petroleum', 'Natural Gas'], 'correct': '2'}, {'question': 'What is the process called when plants make their own food from sunlight?', 'options': ['Respiration', 'Photosynthesis', 'Decomposition', 'Fermentation'], 'correct': '2'}, {'question': 'Which of the following is an example of a simple machine?', 'options': ['Bicycle', 'Wheelbarrow', 'Clock', 'Microscope'], 'correct': '2'}]

for i, f in enumerate(hi):
    print(f["question"])
    print(f["options"][0])
    print(f["options"][1])
    print(f["options"][2])
    print(f["options"][3])
    
    print(f["correct"])