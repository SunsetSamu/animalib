import animalib
from pygame import mixer

if __name__ == "__main__":
    tts_instance = animalib.tts(soundbank="female_4", gap=0.15, rnd_factor=0.45, silence_time=0.25)
    
    while True:
        user_input = input("\nEnter text to generate audio: ")
        if user_input.lower() == "":
            user_input = "Input cannot be None"
        
        audio = tts_instance.generate_audio(user_input)
        print(f"\n{user_input}")
        mixer.init()
        sound = mixer.Sound(audio)
        sound.play()



