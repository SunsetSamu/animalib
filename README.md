# Animalib

Animalib is a Python library for generating audio by mapping text characters to pre-recorded sound segments. The library converts text into a sequence of audio clips, simulating a text-to-speech effect with customizable pitch variation and silence gaps.

## Features

- Converts alphanumeric characters and symbols to corresponding audio segments.
- Supports accented vowels by replacing them with their unaccented counterparts.
- Customizable settings such as soundbank selection, gap duration, random pitch variation, and silence duration.
- Generates audio output as an MP3 file.
- Provides basic error handling and progress updates during audio generation.

## Installation

1. Install [Python 3.x](https://www.python.org/downloads/).
2. Install the required dependencies:

   ```shell
   pip install -r requirements.txt
   ```

3. Ensure you have the necessary audio files placed under the following directories relative to `animalib.py`:
   - `audio/animalese/<soundbank>`: Audio files for alphabetic characters (e.g., `a.aac`, `b.aac`, etc.).
   - `audio/sfx`: Audio files for special effects and symbols.

## Usage

Import the `tts` class from the module and create an instance:

```python
from animalib import tts

# Initialize with a soundbank identifier and optional parameters
tts_instance = tts(soundbank="male_1", gap=0.15, rnd_factor=0.45, silence_time=0.25)

# Generate audio from a given text string
audio_file = tts_instance.generate_audio("Your text message here")

# Export the generated audio to an MP3 file
tts_instance.export(audio_file, filename="output_audio.mp3")
```

By running the module directly, a sample text will be processed and an audio file (`test_output.mp3`) will be generated in the current working directory.

## Contributing

Feel free to submit issues or pull requests for improvements or bug fixes. Contributions are welcome!

## License

```plaintext
MIT License

Copyright (c) 2025 SunsetSamu

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
```
