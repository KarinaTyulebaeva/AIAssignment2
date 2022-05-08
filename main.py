import music21
import mido
import random
from mido import Message, MidiTrack
from typing import List

# Read the .mid file to the variable
input_name = 'barbiegirl_mono.mid'
mid = mido.MidiFile(input_name, clip = True)
tact = mid.ticks_per_beat
print(tact)

# Class Chord represent the chord in the program
# Contains list of int as chord and score
class Chord:
    def __init__(self, accords, score):
        self.accords = accords
        self.score = score
    def set_score(self, new_score):
        self.score = new_score

    def print(self):
        print(self.accords,  " ", self.score , "\n")

# Class Accompaniment represent the Accompaniment
# Contains list of chords and score
class Accompaniment:
    def __init__(self, accords: List[Chord]):
        self.accompaniment = accords
        self.score = 0
    def get_score(self):
        return self.score
    def reset_score(self):
        self.score=0
    def print(self):
        for i in range(len(self.accompaniment)):
            self.accompaniment[i].print()
        print("Total: ", self.score, "\n")


score = music21.converter.parse(input_name)

# Function to get the main chord of the music
def get_key():
    key = score.analyze('key')
    answer = key.tonic.midi
    return answer

# Function to know whether key is major or minor
def get_major_minor():
    key = score.analyze('key')
    answer = key.mode
    return answer

# Function to get tonality by key and major/minor dependency
def get_tones(key, major_minor):
    major = [2, 2, 1, 2, 2, 2, 1]
    minor = [2, 1, 2, 2, 1, 2, 2]
    tones = []
    if(major_minor=='minor'):
        for i in range (7):
            key=key+minor[i]
            tones.append(key)
    else:
        for i in range (7):
            key=key+major[i]
            tones.append(key)
    return tones

# Template for chords
accord_templates = [[0, 4, 7], [0, 3, 7], [0, 2, 5], [0, 5, 2], [4, 7, 12], [3, 7, 12]]

# Function to generate all possible chords by key and chords template
def generate_accords(key):
    accords = []
    for i in range (6):
        temp = []
        temp.append(key+accord_templates[i][0])
        temp.append(key+accord_templates[i][1])
        temp.append(key+accord_templates[i][2])
        accords.append(temp)
    return accords

# Function to lnow how much chord in one accomponiment
def get_number_of_accords():
    song_duration = 0
    if(input_name=='barbiegirl_mono.mid'):
        song_duration = 6144  # CHANGE IT THEN!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    if(input_name=='input2.mid'):
        song_duration = 12288
    if(input_name=='input3.mid'):
        song_duration = 16896
    accord_numbers = song_duration/(tact*2)
    return round(accord_numbers)

# Set of chords by function above
accords = generate_accords(get_key())
print(accords)

# Function to generate random aco
def generate_accompaniment():
    accomponiments = []
    for i in range(15):
        accompaniment = []
        for n in range(get_number_of_accords()):
            random_accord_number = random.randint(0, 5)
            accord = Chord(accords[random_accord_number], 0)
            accompaniment.append(accord)
        temp_accompaniment = Accompaniment(accompaniment)
        accomponiments.append(temp_accompaniment)
    return accomponiments

# First generation
accomponiments = generate_accompaniment()

# Tonalities
tones = get_tones(get_key(), get_major_minor())

# Function to check whether notes belongs to tonalities
def belong_to_tone(note):
    for i in range(len(tones)):
        if(note==tones[i]):
            return True
    return False

# Sort function for generation
def bubbleSort(arr: List[Accompaniment]):
    n = 15

    for i in range(n - 1):
        for j in range(0, n - i - 1):
            if arr[j].score < arr[j + 1].score:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    arr=arr[:15]

# Fitness function for chord, will be used in fitness function for accompaniment
def fitness_chord(chord: Chord):
    chord.score = 0
    for i in range(3):
        if(belong_to_tone(chord.accords[i])):
            chord.score=chord.score+500
        else:
            chord.score=chord.score-100

# Fitness function for accompaniment
def fitness_acomponiment(accompaniment: Accompaniment):
    accompaniment.reset_score()
    for i in range(len(accompaniment.accompaniment)):
        fitness_chord(accompaniment.accompaniment[i])
        accompaniment.score+=accompaniment.accompaniment[i].score

# Function to call fitness function for generation
def evaluate_fitness():
    for i in range(15):
        fitness_acomponiment(accomponiments[i])

# Function for crossover and mutation
def mutation():
    length_middle = len(accomponiments[0].accompaniment)//2
    parent1_one = accomponiments[0].accompaniment[:length_middle]
    parent1_two = accomponiments[0].accompaniment[length_middle:]

    parent2_one = accomponiments[1].accompaniment[:length_middle]
    parent2_two = accomponiments[1].accompaniment[length_middle:]

    parent3_one = accomponiments[2].accompaniment[:length_middle]
    parent3_two = accomponiments[2].accompaniment[length_middle:]

    parent4_one = accomponiments[3].accompaniment[:length_middle]
    parent4_two = accomponiments[3].accompaniment[length_middle:]

    child1 = [*parent1_one, *parent2_two]
    child2 = [*parent3_one, *parent3_two]
    rand1 =random.randint(0, 5)
    rand2 =random.randint(0, 5)
    child1.accompaniment[rand1] = accords[rand2]
    child2.accompaniment[rand2] = accords[rand1]
    accomponiments.append(child1)
    accomponiments.append(child2)

# Genetic algorithm which call step by step all the necessary functions
def genetic_alghoritm():
    print("start")
    evaluate_fitness()
    print("fitness evaluated")
    bubbleSort(accomponiments)
    print("sorted")
    mutation()
    print("mutated")

# Calling Genetic algorithm 1000 times
for i in range(1000):
    genetic_alghoritm()
    print(i, "\n")

# Function to write the accompaniment to the answer
def output(accompaniment: Accompaniment):
    track = MidiTrack()
    for i in range(len(accompaniment.accompaniment)):
        cur_chord = accompaniment.accompaniment[i].accords
        track.append(Message('note_on', channel=0, note= cur_chord[0], velocity=30, time =0))
        track.append(Message('note_on', channel=0, note= cur_chord[1], velocity=30, time =0))
        track.append(Message('note_on', channel=0, note= cur_chord[2], velocity=30, time =0))

        track.append(Message('note_off', channel=0, note=cur_chord[0], velocity=30, time=tact*2))
        track.append(Message('note_off', channel=0, note=cur_chord[1], velocity=30, time=0))
        track.append(Message('note_off', channel=0, note=cur_chord[2], velocity=30, time=0))
    mid.tracks.append(track)

# Calling output function for the best accompaniment
output(accomponiments[0])

# Saving answer to the file
mid.save('test.mid')

