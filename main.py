import music21
import mido
import random
from mido import Message, MidiTrack
from typing import List

input_name = 'barbiegirl_mono.mid'
mid = mido.MidiFile(input_name, clip = True)
tact = mid.ticks_per_beat
print(tact)

class Chord:
    def __init__(self, accords, score):
        self.accords = accords
        self.score = score
    def set_score(self, new_score):
        self.score = new_score

    def print(self):
        print(self.accords,  " ", self.score , "\n")

class Accomponiment:
    def __init__(self, accords: List[Chord]):
        self.accomponiment = accords
        self.score = 0
    def get_score(self):
        return self.score
    def reset_score(self):
        self.score=0
    def print(self):
        for i in range(len(self.accomponiment)):
            self.accomponiment[i].print()
        print("Total: ", self.score, "\n")


score = music21.converter.parse(input_name)

def get_key():
    key = score.analyze('key')
    answer = key.tonic.midi
    return answer

def get_major_minor():
    key = score.analyze('key')
    answer = key.mode
    return answer

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

accord_templates = [[0, 4, 7], [0, 3, 7], [0, 2, 5], [0, 5, 2], [4, 7, 12], [3, 7, 12]]

def generate_accords(key):
    accords = []
    for i in range (6):
        temp = []
        temp.append(key+accord_templates[i][0])
        temp.append(key+accord_templates[i][1])
        temp.append(key+accord_templates[i][2])
        accords.append(temp)
    return accords

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

accords = generate_accords(get_key())
print(accords)

def generate_accomponiments():
    accomponiments = []
    for i in range(15):
        accomponiment = []
        for n in range(get_number_of_accords()):
            random_accord_number = random.randint(0, 5)
            accord = Chord(accords[random_accord_number], 0)
            accomponiment.append(accord)
        temp_accomponiment = Accomponiment(accomponiment)
        accomponiments.append(temp_accomponiment)
    return accomponiments

accomponiments = generate_accomponiments()


def belong_to_tone(chord):
    tones = get_tones(get_key(), get_major_minor())
    for i in range(len(tones)):
        if(chord==tones[i]):
            return True
    return False


def bubbleSort(arr: List[Accomponiment]):
    n = 15

    for i in range(n - 1):
        for j in range(0, n - i - 1):
            if arr[j].score < arr[j + 1].score:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    arr=arr[:15]

def fitness_chord(chord: Chord):
    chord.score = 0
    for i in range(3):
        if(belong_to_tone(chord.accords[i])):
            chord.score=chord.score+100
        else:
            chord.score=chord.score-100

def fitness_acomponiment(accomponiment: Accomponiment):
    accomponiment.reset_score()
    for i in range(len(accomponiment.accomponiment)):
        fitness_chord(accomponiment.accomponiment[i])
        accomponiment.score+=accomponiment.accomponiment[i].score

print(get_tones(get_key(), get_major_minor()))
print("\n")

def evaluate_fitness():
    for i in range(15):
        fitness_acomponiment(accomponiments[i])

def mutation():
    length_middle = len(accomponiments[0].accomponiment)//2
    parent1_one = accomponiments[0].accomponiment[:length_middle]
    parent1_two = accomponiments[0].accomponiment[length_middle:]

    parent2_one = accomponiments[1].accomponiment[:length_middle]
    parent2_two = accomponiments[1].accomponiment[length_middle:]

    parent3_one = accomponiments[2].accomponiment[:length_middle]
    parent3_two = accomponiments[2].accomponiment[length_middle:]

    parent4_one = accomponiments[3].accomponiment[:length_middle]
    parent4_two = accomponiments[3].accomponiment[length_middle:]

    child1 = [*parent1_one, *parent2_two]
    child2 = [*parent3_one, *parent3_two]

    accomponiments.append(child1)
    accomponiments.append(child2)

def genetic_alghoritm():
    print("start")
    evaluate_fitness()
    print("fitness evaluated")
    bubbleSort(accomponiments)
    print("sorted")
    mutation()
    print("mutated")

def test():
    for i in range(15):
        accomponiments[i].print()

# genetic_alghoritm()
# test()
# print("ABOBa", "\n")
# bubbleSort(accomponiments)
# test()
for i in range(10):
    genetic_alghoritm()
    print(i, "\n")

#test()

def output(accomponiment: Accomponiment):
    track = MidiTrack()
    for i in range(len(accomponiment.accomponiment)):
        cur_chord = accomponiment.accomponiment[i].accords
        track.append(Message('note_on', channel=0, note= cur_chord[0], velocity=30, time =0))
        track.append(Message('note_on', channel=0, note= cur_chord[1], velocity=30, time =0))
        track.append(Message('note_on', channel=0, note= cur_chord[2], velocity=30, time =0))

        track.append(Message('note_off', channel=0, note=cur_chord[0], velocity=30, time=tact*2))
        track.append(Message('note_off', channel=0, note=cur_chord[0], velocity=30, time=0))
        track.append(Message('note_off', channel=0, note=cur_chord[0], velocity=30, time=0))
    mid.tracks.append(track)


output()
print("output done")
mid.save('output.mid')

# fitness_acomponiment(accomponiments[0])