import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import csv
from google_trans_new import google_translator
import pyperclip as clip

translator = google_translator()

IMG_PATH = './images/'

LOG = 'Rohdaten.LOG'
description = []
head = []
datas = []

OUT_MID = "temp.csv"
INFO = "info.log"


def read_logdata():
    global description
    global head
    with open(LOG, 'r+', encoding='utf-8') as f:
        description = f.readline().split(', ')
        head = f.readline().split(';')[1:]
        line = f.readline()
        while line != '':
            datas.append(line.split(";")[1:])
            line = f.readline()


def write_info():
    with open(INFO, 'w+', encoding="utf-8") as f:
        f.write('Description:\n')
        for desc in description:
            f.write(desc + '\n')


def write_data_to_csv(data):
    with open(OUT_MID, 'w+', encoding='utf-8') as f:
        for i in range(len(head)):
            h = head[i]
            if len(h) > 0 and h[len(h) - 1] == '\n':
                h = h[:len(h) - 1]
            h = translator.translate(h, lang_src='en', lang_tgt='de')
            f.write('\"' + h + '\";')
            head[i] = h
        f.write('\n')
        for dat in data:
            for d in dat:
                if len(d) > 0 and d[len(d) - 1] == '\n':
                    d = d[:len(d)-1]
                f.write('\"' + d + '\";')
            f.write('\n')


read_logdata()
write_info()
write_data_to_csv(datas)

df = pd.read_csv(OUT_MID, sep=';')

"""
print("Welche Spalte: (std: '0 5 6 8 10 12 13 14' -> strg+V)")
clip.copy('0\n5\n6\n8\n10\n12\n13\n14\n')

#Spalten CSV
TIME = int(input("Time: "))
POS_BREITE = int(input("Breitenlage: "))
POS_LANGE = int(input("Längenlage: "))
SPEED = int(input("Geschwindigkeit: "))
HEIGHT = int(input("Höhe: "))
EXTERN_TEMP = int(input("Externe Temperatur: "))
EXTERN_HUM = int(input("Externe Feuchtigkeit"))
EXTERN_PRESS = int(input("Externer Druck: \n"))
"""
TIME = 0
POS_BREITE = 5
POS_LANGE = 6
SPEED = 8
HEIGHT = 10
EXTERN_TEMP = 12
EXTERN_HUM = 13
EXTERN_PRESS = 14


#Bild Namen
ZEIT_HOHE = IMG_PATH + 'zeit_hohe.png'
TEMP_HOHE = IMG_PATH + 'temp_hohe.png'
HOHE_PRESS = IMG_PATH + 'hohe_druck.png'
HOHE_FEUCHT = IMG_PATH + 'hohe_feucht.png'
ZEIT_TEMP = IMG_PATH + 'zeit_temp.png'
ZEIT_PRESS = IMG_PATH + 'zeit_druck.png'
ZEIT_FEUCHT = IMG_PATH + 'zeit_feucht.png'
ZEIT_GESCHW = IMG_PATH + 'zeit_geschw.png'

df.plot(x=head[TIME], y=head[HEIGHT])
plt.savefig(ZEIT_HOHE)

df.plot(x=head[EXTERN_TEMP], y=head[HEIGHT])
plt.savefig(TEMP_HOHE)

df.plot(x=head[HEIGHT], y=head[EXTERN_PRESS])
plt.savefig(HOHE_PRESS)

df.plot(x=head[HEIGHT], y=head[EXTERN_HUM])
plt.savefig(HOHE_FEUCHT)

df.plot(x=head[TIME], y=head[EXTERN_TEMP])
plt.savefig(ZEIT_TEMP)

df.plot(x=head[TIME], y=head[EXTERN_PRESS])
plt.savefig(ZEIT_PRESS)

df.plot(x=head[TIME], y=head[EXTERN_HUM])
plt.savefig(ZEIT_FEUCHT)

df.plot(x=head[TIME], y=head[SPEED])
plt.savefig(ZEIT_GESCHW)
"""
def get_lists():
    maxt = 0
    for i in range(len(df.get(head[HEIGHT]))):
        if df.get(head[HEIGHT])[maxt] < df.get(head[HEIGHT])[i]:
            maxt = i
    time = [i for i in df.get(head[TIME])[:maxt]]
    height = [i for i in df.get(head[HEIGHT])[:maxt]]
    time2 = [i for i in df.get(head[TIME])[maxt:]]
    height2 = [i for i in df.get(head[HEIGHT])[maxt:]]
    return time, height, time2, height2


tmp_time_list, tmp_height_list, tmp_time2_list, tmp_height2_list = get_lists()
plt.close();

plt.plot(tmp_height_list)
plt.show()

plt.plot(tmp_height2_list)
plt.show()
"""
height = df.get(head[HEIGHT])


MIN_SAMPLE = 200


def get_av(st):
    act_samp = 0
    av = 0.
    for i in range(st, st+MIN_SAMPLE):
        val = 0
        try:
            val = int(height[i])
        except Exception as e:
            continue
        act_samp += 1
        av += val
    return av / act_samp


av = get_av(0) / 2. + get_av(len(height)-MIN_SAMPLE-1) / 2.


def get_info_about_time():
    going_down = False
    start, end = '', ''
    it = 0
    for num in height:
        val = 0
        it += 1
        try:
            val = int(num)
        except Exception as e:
            continue
        if not going_down and val > 4 * av:
            start = df.get(head[TIME])[it]
            going_down = True
        if going_down and val < 4 * av:
            end = df.get(head[TIME])[it]
            break
    return start, end


def time_diff(end, start):
    h, m, s = tuple(start.split(":"))
    h = int(h)
    m = int(m)
    s = int(s)
    h2, m2, s2 = tuple(end.split(":"))
    h2 = int(h2)
    m2 = int(m2)
    s2 = int(s2)
    h3, m3, s3 = h2 - h, m2 - m, s2 - s
    if s3 < 0:
        m3 -= 1
        s3 += 60
    if m3 < 0:
        h3 -= 1
        m3 += 60
    return str(h3) + ':' + str(m3) + ':' + str(s3)


start_time, end_time = get_info_about_time()
time_in_air = time_diff(end_time, start_time)

print(len(height))

print("Startzeit: " + str(start_time))
print("Landezeit: " + str(end_time))
print("Zeit im Flug: " + str(time_in_air))
