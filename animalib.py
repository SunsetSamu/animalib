import os
import random
import re
import tempfile
import shutil
from pydub import AudioSegment

class tts:
    def __init__(self, soundbank='male_1', gap=0.15, rnd_factor=0.3, silence_time=0.3):
        self.soundbank = soundbank
        self.gap = gap * 1000
        self.rnd_factor = rnd_factor
        self.silence_time = silence_time * 1000

        # Definition of characters
        self.animalese = list('abcdefghijklmnopqrstuvwxyz0123456789')
        self.sfx = {
            "ampersand": "&", "arrow_down": "↓", "arrow_left": "←",
            "arrow_right": "→", "arrow_up": "↑", "asterisk": "*",
            "at": "@", "brace_closed": "}", "brace_open": "{",
            "bracket_closed": "]", "bracket_open": "[", "caret": "^",
            "default": "�", "dollar": "$", "exclamation": "!",
            "parenthesis_closed": ")", "parenthesis_open": "(",
            "percent": "%", "pound": "#", "question": "?",
            "slash_forward": "/", "tilde": "~"
        }
        self.silence_chars = set(" ,.;:")
        self.accented_vowels = {
            'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u',
            'à': 'a', 'è': 'e', 'ì': 'i', 'ò': 'o', 'ù': 'u',
            'ä': 'a', 'ë': 'e', 'ï': 'i', 'ö': 'o', 'ü': 'u',
            'â': 'a', 'ê': 'e', 'î': 'i', 'ô': 'o', 'û': 'u'
        }

        # Load sounds into memory
        self.sounds = self._load_sound_map()
        self.audio_segments = self._load_audio_segments()

    def _load_sound_map(self):
        sound_map = {}
        base_dir = os.path.dirname(os.path.abspath(__file__))
        alpha_dir = os.path.join(base_dir, "audio", "animalese", self.soundbank)
        sfx_dir = os.path.join(base_dir, "audio", "sfx")

        for ltr in self.animalese:
            sound_map[ltr] = os.path.join(alpha_dir, f"{ltr}.aac")
        for name, symbol in self.sfx.items():
            sound_map[symbol] = os.path.join(sfx_dir, f"{name}.aac")
        return sound_map

    def _load_audio_segments(self):
        audio_segments = {}
        for char, path in self.sounds.items():
            try:
                audio_segments[char] = AudioSegment.from_file(path, format="aac")
            except Exception:
                # In case of failure, assign brief silence
                audio_segments[char] = AudioSegment.silent(duration=350)
        return audio_segments

    def generate_audio(self, text) -> AudioSegment:
        text = text.lower().strip()
        if not text:
            print("Error: Input text is empty.")
            return AudioSegment.silent(duration=1000)

        # Detect sentences and whether they are questions
        pattern = re.compile(r'[^\.!?]+[\.!?]?')
        sentences = [m for m in pattern.finditer(text)]
        sentence_info = []
        for m in sentences:
            start, end = m.span()
            is_question = m.group().strip().endswith('?')
            sentence_info.append((start, end, is_question))

        combined = AudioSegment.empty()
        silence_count = 0
        total = len(text)

        for i, char in enumerate(text, 1):
            # Show progress every 10%
            if total >= 10 and i % max(1, total // 10) == 0:
                percent = round(i / total * 100, 1)
                print(f"Progress: {percent}% ({i}/{total})")

            # Determine if the character belongs to a question sentence
            is_question = False
            idx = i - 1
            for start, end, q in sentence_info:
                if start <= idx < end:
                    is_question = q
                    break

            # Select audio
            # If the character is an accented vowel, replace it with its unaccented version
            if char in self.accented_vowels:
                char = self.accented_vowels[char]
                silence_count = 0
            if char in self.audio_segments:
                sound = self.audio_segments[char]
                silence_count = 0
            elif char in self.silence_chars:
                if silence_count < 3:
                    sound = AudioSegment.silent(duration=self.silence_time)
                    silence_count += 1
                else:
                    continue
            else:
                sound = self.audio_segments.get('�', AudioSegment.silent(duration=self.silence_time))
                silence_count = 0

            # Pitch variation
            if is_question and i >= total * 0.8:
                base_shift = 0.1 + (i - total * 0.8) * 0.01
            else:
                base_shift = 0.0 if is_question else -0.1
            shift = base_shift + random.random() * self.rnd_factor
            new_rate = int(sound.frame_rate / (2.0 ** shift))
            pitched_sound = sound._spawn(sound.raw_data, overrides={'frame_rate': new_rate})
            sound = pitched_sound.set_frame_rate(44100)

            # Add gap if applicable
            if self.gap > 0 and len(combined) > self.gap:
                combined = combined[:-self.gap]
            combined += sound

        # Export the audio provisionally into the system cache
        cache_dir = tempfile.gettempdir()
        cache_file = os.path.join(cache_dir, "animalib-out.mp3")
        combined.export(cache_file, format="mp3")

        return cache_file

    def export(self, combined, filename="audio.mp3", output_dir=None):
        if not isinstance(combined, AudioSegment):
            print("Error: Invalid audio segment.")
            return

        # Copy the cached file to the desired output directory with the given name
        output_dir = output_dir or os.getcwd()
        output_path = os.path.join(output_dir, filename)
        shutil.copy(self.cache_file, output_path)
        print(f"Audio exported to: {output_path}")


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
