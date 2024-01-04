import pygame
from pydub import AudioSegment # Requires FFMPEG
import librosa

from time import sleep
import threading
import sys
import random
import os

mode = ""

WIDTH = 1280
HEIGHT = 720

round_bpm_to_nearest = 1

def main():
    global mode
    global WIDTH
    global HEIGHT

    print(100*"\u200b\n")

    supported_formats = ["mp3", "wav", "ogg"]

    # Song selection
    files = []

    for roots, dirs, files in os.walk(os.getcwd()):
        for file in files:
            files.append(str(file))
            break
        break

    filesstring = ""
    for i in files:
        if str(i).split(".")[-1] in supported_formats:
            filesstring += i.split(".")[0] + ", "
    filesstring = filesstring[:-2]

    if len(filesstring) <= 0:
        finalstring = ""
        for i in supported_formats:
            finalstring += i + ", "
        finalstring = finalstring[:-2]

        print("No valid files detected! Supported formats are: \n\u200b\n" + finalstring + "\n")
        input("Enter any text to exit...\n")
        sys.exit(0)


    file = ""
    file_correct = False
    while not file_correct:
        file = input("Select song: \n\u200b\n" + filesstring + "\n\nYour choice : ")
        tests = 0
        for i in supported_formats:
            if file + "." + i not in files:
                tests += 1
            else:
                worked = i

        if tests == len(supported_formats):
            file_correct = False
            print("\nThat is not a valid song!\n")
        else:
            file_correct = True
            file = file + "." + worked


    if file.split(".")[-1] == "mp3":
        print("\nConverting from MP3 to OGG and WAV...")
        AudioSegment.from_mp3(file).export('temp', format='ogg')
        AudioSegment.from_mp3(file).export('temp2', format='wav')

    elif file.split(".")[-1] == "wav":
        print("\nConverting from WAV to OGG and WAV...")
        AudioSegment.from_wav(file).export('temp', format='ogg')
        AudioSegment.from_wav(file).export('temp2', format='wav')

    elif file.split(".")[-1] == "ogg":
        print("\nConverting from OGG to OGG and WAV...")
        AudioSegment.from_ogg(file).export('temp', format='ogg')
        AudioSegment.from_ogg(file).export('temp2', format='wav')

    elif file.split(".")[-1] == "ogg":
        print("\nConverting from FLV to OGG and WAV...")
        AudioSegment.from_flv(file).export('temp', format='ogg')
        AudioSegment.from_flv(file).export('temp2', format='wav')

    print("Audio successfully converted and saved in temporary file!")

    print("Loading the temporary WAV file...")
    y, sr = librosa.core.load(os.path.join(os.getcwd(), "temp2"))
    print("Finished loading.")
    print("Getting the BPM of the audio...")
    onset_env = librosa.onset.onset_strength(y=y, sr=sr)
    bpm = round(int(librosa.beat.tempo(onset_envelope=onset_env, sr=sr)[0])/round_bpm_to_nearest)*round_bpm_to_nearest
    print("Done! BPM is", bpm)
    print("Deleting the temporary WAV file...")
    os.remove("temp2")
    print("The temporary file has been deleted.")

    print()

    # Mode selection
    modes = ["rand", "swirlup", "swirldown", "swirlleft", "swirlright", "swirlrand", "up", "down", "left", "right", "diagonal_upleft",
             "diagonal_upright", "diagonal_downleft", "diagonal_downright", "fullrand", "blank"]

    modesstring = ""
    for i in modes:
        modesstring += i + ", "
    modesstring = modesstring[:-2]

    mode = ""
    while mode not in modes:
        mode = input("Select mode: \n\u200b\n" + modesstring + "\n\nYour choice : ")
        if mode not in modes:
            print("\nThat is not a valid mode!\n")

    print()

    # Background blink selection
    blinkingchoices = ["yes", "no"]

    blinkingstring = ""
    for i in blinkingchoices:
        blinkingstring += i + ", "
    blinkingstring = blinkingstring[:-2]

    metronome_blink = ""
    while metronome_blink not in blinkingchoices:
        metronome_blink = input("Should the background blink?: \n\u200b\n" + blinkingstring + "\n\nYour choice : ")
        if metronome_blink not in blinkingchoices:
            print("\nThat is not a valid choice!\n")

    if metronome_blink == "yes":
        metronome_blink = True
    else:
        metronome_blink = False

    print()

    # Metronome sound choices
    metrochoices = ["yes", "no"]

    metronome_string = ""
    for i in metrochoices:
        metronome_string += i + ", "
    metronome_string = metronome_string[:-2]

    metronome_sound = ""
    while metronome_sound not in metrochoices:
        metronome_sound = input("Do you want a metronome?: \n\u200b\n" + metronome_string + "\n\nYour choice : ")
        if metronome_sound not in metrochoices:
            print("\nThat is not a valid choice!\n")

    if metronome_sound == "yes":
        metronome_sound = True
    else:
        metronome_sound = False

    print()

    # Start delay choice
    startdelay = 0
    working = False
    while not working:
        startdelay = input("How much start delay should there be? (If not sure, type 0) \n\nYour choice : ")
        try:
            startdelay = float(startdelay)
            working = True
        except:
            working = False

    # FPS choice
    fps = 0
    working = False
    while not working:
        fps = input(
            "How many FPS do you want? (More FPS = More detailed effects. NOTE: Going too high can break some effects!) \n\nYour choice : ")
        try:
            fps = int(fps)
            working = True
        except:
            working = False

    pygame.init()
    info = pygame.display.Info()

    WIDTH = info.current_w
    HEIGHT = info.current_h

    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)

    pygame.display.set_caption("Audio Visualizer | By Fguzy")
    clock = pygame.time.Clock()


    class Player(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.Surface((50, 50))
            self.image.fill((0, 255, 0))
            self.rect = self.image.get_rect()
            self.rect.center = (WIDTH / 2, HEIGHT / 2)

        def update(self, steps):
            global mode

            if mode == "fullrand":
                nowmode = modes[random.randint(0, len(modes) - 1)]
            else:
                nowmode = mode

            if nowmode == "rand":
                x = random.randint(0, 2)
                y = random.randint(0, 2)
            elif nowmode == "swirlup":
                x = random.randint(1, 2)
                y = 1
            elif nowmode == "swirldown":
                x = random.randint(1, 2)
                y = 2
            elif nowmode == "swirlleft":
                x = 2
                y = random.randint(1, 2)
            elif nowmode == "swirlright":
                x = 1
                y = random.randint(1, 2)
            elif nowmode == "swirlrand":
                x = random.randint(1, 2)
                y = random.randint(1, 2)
            elif nowmode == "up":
                x = 0
                y = 1
            elif nowmode == "down":
                x = 0
                y = 2
            elif nowmode == "left":
                x = 2
                y = 0
            elif nowmode == "right":
                x = 1
                y = 0
            elif nowmode == "diagonal_upleft":
                x = 2
                y = 1
            elif nowmode == "diagonal_upright":
                x = 1
                y = 1
            elif nowmode == "diagonal_downleft":
                x = 1
                y = 2
            elif nowmode == "diagonal_downright":
                x = 2
                y = 2
            else:
                x = 0
                self.rect.x = 100000
                y = 0
                self.rect.y = 100000

            if y == 1:
                self.rect.y -= steps

                if self.rect.top <= 0:
                    self.image.fill((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
                    self.rect.y = HEIGHT
            elif y == 2:
                self.rect.y += steps

                if self.rect.bottom >= HEIGHT:
                    self.image.fill((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
                    self.rect.y = 0

            if x == 1:
                self.rect.x += steps

                if self.rect.x >= WIDTH:
                    self.image.fill((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
                    self.rect.x = 0

            elif x == 2:
                self.rect.x -= steps

                if self.rect.x <= 0:
                    self.image.fill((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
                    self.rect.x = WIDTH


    all_sprites = pygame.sprite.Group()
    player = Player()
    all_sprites.add(player)

    screen.fill((0, 0, 0))
    all_sprites.draw(screen)
    pygame.display.flip()

    mixer = pygame.mixer

    mixer.init()

    mixer.music.set_volume(1)

    print("Loading the metronome sound...")
    beat = pygame.mixer.Sound('metronome.sound')
    print("Done!")

    print("Loading the OGG audio...")
    mixer.music.load("temp")
    print("Done!")
    print("Deleting the temporary OGG file...")
    os.remove("temp")
    print("The temporary OGG file has been deleted.")

    name = file.split(".")[0]

    print(100*"\u200b\n")

    print("Song name:", name)
    print("BPM:", bpm)
    print("Start delay:", startdelay)
    print("Vis mode:", mode)
    print("Background blink:", metronome_blink)
    print("Metronome:", metronome_sound)
    print("FPS:", fps)

    running = True

    def metronome():
        if metronome_sound:
            pygame.mixer.Sound.play(beat)
        if metronome_blink:
            screen.fill((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
        sleep(30 / bpm)
        if running:
            screen.fill((0, 0, 0))
        sleep(30 / bpm)
        if running:
            metronome()


    thread = threading.Thread(target=metronome)
    MUSIC_END = pygame.USEREVENT + 1
    pygame.mixer.music.set_endevent(MUSIC_END)

    print("Starting audio playback...")
    mixer.music.play()
    sleep(startdelay)

    print("Starting metronome thread...")
    thread.start()

    print("Starting effect " + "'" + mode + "'...")
    while running:
        clock.tick(fps)

        step = (HEIGHT / fps) / (60 / bpm)
        all_sprites.update(int(step))

        all_sprites.draw(screen)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                mixer.music.stop()
                pygame.quit()
                break
            if event.type == MUSIC_END:
                running = False
                pygame.quit()
                break

    restartchoices = ["yes", "no"]

    restart_string = ""
    for i in restartchoices:
        restart_string += i + ", "
    restart_string = restart_string[:-2]

    restart = ""
    while restart not in restartchoices:
        restart = input("Do you want to restart the app?: \n\u200b\n" + restart_string + "\n\nYour choice : ")
        if restart not in restartchoices:
            print("\nThat is not a valid choice!\n")

    if restart == "yes":
        main()
    else:
        sys.exit(0)

if __name__ == '__main__':
    main()
