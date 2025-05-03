import os
import random
import numpy as np
from pydub import AudioSegment


class tts:
    def __init__(self, soundbank='male_1', gap=0.15):

        self.soundbank = soundbank
        self.gap = gap * 1000

        
        self.animalese = [
            'a','b','c','d','e','f','g','h','i','j','k','l','m',
            'n','o','p','q','r','s','t','u','v','w','x','y','z', 
            '0','1','2','3','4','5','6','7','8','9'
        ]

        self.sfx = {
            "ampersand": "&",
            "arrow_down": "↓",
            "arrow_left": "←",
            "arrow_right": "→",
            "arrow_up": "↑",
            "asterisk": "*",
            "at": "@",
            "brace_closed": "}",
            "brace_open": "{",
            "bracket_closed": "]",
            "bracket_open": "[",
            "caret": "^",
            "default": "�",
            "dollar": "$",
            "exclamation": "!",
            "parenthesis_closed": ")",
            "parenthesis_open": "(",
            "percent": "%",
            "pound": "#",
            "question": "?",
            "slash_forward": "/",
            "tilde": "~"
        }
        self.sfx_chars = [
            "&","↓","←","→","↑",
            "*","@","}","{","]","[",
            "^","�","$","!",")","(",
            "%","#","?","/","~"
        ]
        self.silence_chars = [
            " ", ",", ".", ";", ":"
        ]


        self.sounds = self._load_sound_map()
        

    def _load_sound_map(self):
        sound_map = {}
        base_dir = os.path.dirname(os.path.abspath(__file__))

        alpha_dir = os.path.join(base_dir, "audio", "animalese", self.soundbank)
        sfx_dir = os.path.join(base_dir, "audio", "sfx")


        for i, ltr in enumerate(self.animalese):
            filename = f"{ltr}.aac"

            # print(f"animalese> {ltr}, {filename}")

            animalese_path = os.path.join(alpha_dir, filename)
            sound_map[ltr] = animalese_path

        for i, (name, symbol) in enumerate(zip(self.sfx.keys(), self.sfx_chars)):
            filename = f"{name}.aac"
            
            # print(f"sfx> {symbol}, {filename}")

            sfx_path = os.path.join(sfx_dir, filename)
            sound_map[symbol] = sfx_path
        
        # print(sound_map)
        return sound_map

    def generate_audio(self, text) -> AudioSegment:
        text = text.lower().strip()
        infiles = []
        i = 0
        silence_count = 0
        last_percent = 0
        percent = 0

        combined = None
        if not text.strip():
            print("Error: El texto de entrada está vacío.")
            return
        valid_chars = set("abcdefghijklmnopqrstuvwxyz0123456789&↓←→↑*{}[]^$!()#?\\/~ .,;:")
        if not any(char.lower() in valid_chars for char in text):
            print("Error: El texto no contiene caracteres válidos. Se generará un audio vacío.")
            empty_audio = AudioSegment.silent(duration=1000)
            return empty_audio
        
        while i < len(text):
            char = text[i]

            last_percent = percent
            percent = round((i + 1) / len(text) * 100, 2)
            
            if percent == last_percent:
                print(f"--- Skipping {i + 1}th char ---")
                i += 1
                continue

            print(f"{i +1} chars of {len(text)}. Percent: {percent}%")    


            try:
                if char in self.sounds:
                    ltr = self.sounds[char]
                    sound = AudioSegment.from_file(os.path.join(os.getcwd(), ltr), format="aac")

                    silence_count = 0
                    # return sound

                elif char in self.silence_chars:
                    if silence_count < 3:
                        silence_count += 1
                        sound = AudioSegment.silent(duration=350)
                    else:
                        i += 1
                        continue
                    
                    # return sound
                else:
                    ltr = self.sounds['�']
                    sound = AudioSegment.from_file(os.path.join(os.getcwd(), ltr), format="aac")

                    silence_count = 0
                    # return sound
            
            except Exception as e:
                print(f"Error loading {ltr}: {e}")
                ltr = self.sounds['�']
                sound = AudioSegment.from_file(os.path.join(os.getcwd(), ltr), format="aac")

                silence_count = 0
                # return sound
            
            
            gap = self.gap

            if combined is None:
                combined = sound
            elif gap > 0 and len(combined) > gap:
                combined = combined[:-gap]
                combined += sound
            else:
                combined += sound
            
            i += 1
        return combined
    
    def export(self, combined, filename="audio.mp3", output_dir=os.getcwd()):
        self.filename = filename
        self.output_dir = output_dir
        
        if not combined:
            print("Error: No audio to export.")
            return
        if not isinstance(combined, AudioSegment):
            print("Error: Invalid audio segment.")
            return

        if not self.output_dir:
            self.output_dir = os.getcwd()
            return
        output_path = os.path.join(self.output_dir, self.filename)
        combined.export(output_path, format=self.filename.split('.')[-1])


if __name__ == "__main__":
    tts_instance = tts(soundbank="male_1", gap=0.15)
    audio = tts_instance.generate_audio(r"""
                                        Attention! The @agent42 reported ↑ activity at sector 9. Coordinates: [x:25, y:74] ← moving → fast.
                                        Confirm status ↓ ASAP — they're carrying $5000, 3% plutonium, and a mysterious briefcase {code#X9Z}.
                                        Do we proceed? (Y/N) → yes. Initiate sequence: a1b2c3d4e5f6g7h8i9j0klmnopqrstuvwx^yz ← over.

                                        Initiate secondary protocol *Delta_Tilde_~* with payload ~encrypted&ready. Brace for impact! 
                                        Estimated delay: 15s (±3.5%) at 99.9% certainty.

                                        Log file: system/core/security[backup]/vault] → mismatch detected! Recalibrating...
                                        Override password? [admin@server]: root#123!

                                        Execute backup script: /usr/bin/restore.sh & cleanup sequence /tmp/session/* immediately.
                                        Memory dump: {0xDEAD}{0xBEEF}... default handler triggered: replacement → �

                                        End of transmission.
                                        """)
    tts_instance.export(audio, filename="test_output.mp3")
