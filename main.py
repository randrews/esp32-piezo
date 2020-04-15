# Ross Andrews
# ross.andrews@gmail.com
#
# Released under GNU Public License version 3
# https://www.gnu.org/licenses/gpl-3.0.en.html
#
# Instructions:
# Copy this to an esp32 running Micropython, wire
# a piezo buzzer between pin 32 and gnd, and call
# anacreon() from the REPL.
from machine import Pin, PWM, Timer
from time import sleep_ms

# Any PWM pin would work
pin = PWM(Pin(32), freq=440, duty=0)
tempo = 30
volume = 500

# A note looks like 'd3' or 'c#4', the note name followed by the octave
def freq(note, a4=440):
  scale = ['c', 'c#', 'd', 'd#', 'e', 'f', 'f#', 'g', 'g#', 'a', 'a#', 'b']
  tone = note[0:-1]
  octave = int(note[-1])
  index = octave * 12 + (scale.index(tone))
  distance = index - 57 # A4 is the key note, which is 48 + 9
  return round(a4 * (2 ** (distance / 12)))

def note(note, length):
  pin.duty(volume)
  pin.freq(freq(note))
  sleep_ms(length)
  pin.duty(0)

def play(notes):
  current_note_idx = 0
  tim = Timer(2)
  def note():
    if current_note_idx >= len(notes): return
    (current_note, duration) = notes[current_note_idx]
    pin.duty(volume)
    pin.freq(freq(current_note))
    tim.init(period=duration * tempo, mode=Timer.ONE_SHOT, callback=lambda t: staccato())
  def staccato():
    nonlocal current_note_idx
    current_note_idx += 1
    pin.duty(0)
    tim.init(period=1, mode=Timer.ONE_SHOT, callback=lambda t: note())
  note()

# I'm calling 48 a whole note, so I can easily divide that into
# 16ths and 3rds. So an 8th is length 6, a half with a dot is
# length 36, etc etc. We'll multiply the delay by the tempo to
# slow it down enough to hear
anacreon_notes = [
  ('g4', 6), ('e4', 6),
  ('c4', 12), ('e4', 12), ('g4', 12),
  ('c5', 24), ('e5', 6), ('d5', 6),
  ('c5', 12), ('e4', 12), ('f#4', 12),
  ('g4', 24), ('g4', 6), ('g4', 6),
  ('e5', 18), ('d5', 6), ('c5', 12),
  ('b4', 24), ('a4', 6), ('b4', 6),
  ('c5', 12), ('c5', 12), ('g4', 12),
  ('e4', 12), ('c4', 12), ('g4', 6), ('e4', 6),
  ('c4', 12), ('e4', 12), ('g4', 12),
  ('c5', 24), ('e5', 6), ('d5', 6),
  ('c5', 12), ('e4', 12), ('f#4', 12),
  ('g4', 24), ('g4', 6), ('g4', 6),
  ('e5', 18), ('d5', 6), ('c5', 12),
  ('b4', 24), ('a4', 6), ('b4', 6),
  ('c5', 12), ('c5', 12), ('g4', 12),
  ('e4', 12), ('c4', 12), ('e5', 6), ('e5', 6),
  ('e5', 12), ('f5', 12), ('g5', 12),
  ('g5', 24), ('f5', 6), ('e5', 6),
  ('d5', 12), ('e5', 12), ('f5', 12),
  ('f5', 24), ('f5', 12),
  ('e5', 18), ('d5', 6), ('c5', 12),
  ('b4', 24), ('a4', 6), ('b4', 6),
  ('c5', 12), ('e4', 12), ('f#4', 12),
  ('g4', 24), ('g4', 12),
  ('c5', 12), ('c5', 12), ('c5', 6), ('b4', 6),
  ('a4', 12), ('a4', 12), ('a4', 12),
  ('d5', 12), ('f5', 6), ('e5', 6), ('d5', 6), ('c5', 6),
  ('c5', 12), ('b4', 40), ('g4', 6), ('g4', 6),
  ('c5', 18), ('d5', 6), ('e5', 6), ('f5', 6),
  ('g5', 24), ('c5', 6), ('d5', 6),
  ('e5', 18), ('f5', 6), ('d5', 12),
  ('c5', 36)
  ]
  
def anacreon(): play(anacreon_notes)
