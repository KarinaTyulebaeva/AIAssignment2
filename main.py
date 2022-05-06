import music21
import mido
import random
from mido import Message

input_name = 'barbiegirl_mono.mid'
mid = mido.MidiFile(input_name, clip = True)
tact = mid.ticks_per_beat
print(tact)

class Accord:
    def __init__(self, accords, score):
        self.accords = accords
        self.score = score
    def set_score(self, new_score):
        self.score = new_score

    def print(self):
        print(self.score)

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
            accord = Accord(accords[random_accord_number], 0)
            accomponiment.append(accord)
        accomponiments.append(accomponiment)
    return accomponiments

accomponiments = generate_accomponiments()


