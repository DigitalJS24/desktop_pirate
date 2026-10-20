"""
Sound manager for Desktop Pirate.
Generates retro 8-bit sound effects procedurally into WAV format and plays them natively using winsound.
"""

import os
import sys
import math
import wave
import struct
import subprocess
from utils import get_asset_path

# Platform specific audio
if sys.platform == "win32":
    try:
        import winsound
    except ImportError:
        winsound = None
else:
    winsound = None

class SoundManager:
    def __init__(self, sounds_dir=None, enabled=True):
        if sounds_dir is None:
            sounds_dir = get_asset_path("sounds")
        self.sounds_dir = sounds_dir
        self.enabled = enabled
        self.sound_paths = {}
        os.makedirs(self.sounds_dir, exist_ok=True)
        self._generate_sounds()
        self._load_sounds()

    def set_enabled(self, enabled: bool):
        self.enabled = enabled

    def _generate_wav(self, filename, samples, sample_rate=22050):
        path = os.path.join(self.sounds_dir, filename)
        if os.path.exists(path):
            return path
        with wave.open(path, 'w') as wf:
            wf.setnchannels(1)        # mono
            wf.setsampwidth(2)        # 16-bit
            wf.setframerate(sample_rate)
            raw = bytearray()
            for s in samples:
                val = int(max(-1.0, min(1.0, s)) * 32767)
                raw.extend(struct.pack('<h', val))
            wf.writeframes(raw)
        return path

    def _generate_sounds(self):
        sr = 22050

        # 1. Jump sound: pitch slides upwards
        if not os.path.exists(os.path.join(self.sounds_dir, "jump.wav")):
            samples = []
            dur = 0.22
            total_samples = int(sr * dur)
            for i in range(total_samples):
                t = i / sr
                freq = 240 + 700 * (t / dur) ** 1.5
                vol = (1.0 - t / dur) ** 0.5
                phase = (t * freq) % 1.0
                wave_val = 1.0 if phase < 0.5 else -1.0
                samples.append(wave_val * vol * 0.35)
            self._generate_wav("jump.wav", samples, sr)

        # 2. Land sound: soft low frequency thud
        if not os.path.exists(os.path.join(self.sounds_dir, "land.wav")):
            samples = []
            dur = 0.12
            total_samples = int(sr * dur)
            for i in range(total_samples):
                t = i / sr
                freq = 160 * (1.0 - t / dur) + 50
                vol = (1.0 - t / dur) ** 2
                wave_val = math.sin(2 * math.pi * freq * t)
                samples.append(wave_val * vol * 0.45)
            self._generate_wav("land.wav", samples, sr)

        # 3. Sword / Slash sound
        if not os.path.exists(os.path.join(self.sounds_dir, "sword.wav")):
            import random
            samples = []
            dur = 0.22
            total_samples = int(sr * dur)
            for i in range(total_samples):
                t = i / sr
                vol = (1.0 - t / dur) ** 1.5
                noise = random.uniform(-1.0, 1.0)
                tone = math.sin(2 * math.pi * (1600 - 1000 * (t / dur)) * t)
                wave_val = 0.6 * noise + 0.4 * tone
                samples.append(wave_val * vol * 0.3)
            self._generate_wav("sword.wav", samples, sr)

        # 4. Coin / Gold sound: dual bell chime
        if not os.path.exists(os.path.join(self.sounds_dir, "coin.wav")):
            samples = []
            dur = 0.32
            total_samples = int(sr * dur)
            for i in range(total_samples):
                t = i / sr
                freq = 987.77 if t < 0.08 else 1318.51
                vol = (1.0 - (t / dur)) ** 1.2
                wave_val = math.sin(2 * math.pi * freq * t) + 0.3 * math.sin(4 * math.pi * freq * t)
                samples.append(wave_val * vol * 0.35)
            self._generate_wav("coin.wav", samples, sr)

        # 5. Grab / Pick up sound
        if not os.path.exists(os.path.join(self.sounds_dir, "grab.wav")):
            samples = []
            dur = 0.14
            total_samples = int(sr * dur)
            for i in range(total_samples):
                t = i / sr
                freq = 280 + 350 * (t / dur)
                vol = 0.8 * (1.0 - (t / dur) ** 2)
                phase = (t * freq) % 1.0
                wave_val = 1.0 if phase < 0.4 else -0.7
                samples.append(wave_val * vol * 0.3)
            self._generate_wav("grab.wav", samples, sr)

        # 6. Pirate "Arrr!" synth sound
        if not os.path.exists(os.path.join(self.sounds_dir, "arrr.wav")):
            samples = []
            dur = 0.35
            total_samples = int(sr * dur)
            for i in range(total_samples):
                t = i / sr
                mod = math.sin(2 * math.pi * 32 * t)
                freq = 130 + 30 * mod
                vol = math.sin(math.pi * (t / dur)) * 0.85
                phase = (t * freq) % 1.0
                wave_val = (1.0 if phase < 0.5 else -1.0) + 0.25 * math.sin(2 * math.pi * 220 * t)
                samples.append(wave_val * vol * 0.3)
            self._generate_wav("arrr.wav", samples, sr)

        # 7. Pirate whistle sound (calling parrot)
        if not os.path.exists(os.path.join(self.sounds_dir, "whistle.wav")):
            samples = []
            dur = 0.4
            total_samples = int(sr * dur)
            for i in range(total_samples):
                t = i / sr
                # Two tone whistle: 1400Hz then slide to 2200Hz
                if t < 0.12:
                    freq = 1500 + 400 * (t / 0.12)
                else:
                    freq = 1900 + 600 * ((t - 0.12) / 0.28)
                vol = math.sin(math.pi * (t / dur)) * 0.5
                wave_val = math.sin(2 * math.pi * freq * t)
                samples.append(wave_val * vol)
            self._generate_wav("whistle.wav", samples, sr)

        # 8. Parrot squawk sound
        if not os.path.exists(os.path.join(self.sounds_dir, "squawk.wav")):
            import random
            samples = []
            dur = 0.28
            total_samples = int(sr * dur)
            for i in range(total_samples):
                t = i / sr
                freq = 1200 - 400 * (t / dur)
                noise = random.uniform(-0.5, 0.5)
                vol = math.sin(math.pi * (t / dur)) * 0.4
                tone = math.sin(2 * math.pi * freq * t)
                wave_val = tone + noise
                samples.append(wave_val * vol)
            self._generate_wav("squawk.wav", samples, sr)

        # 9. Kiss / Smooch sound (playful chime + pop)
        if not os.path.exists(os.path.join(self.sounds_dir, "kiss.wav")):
            samples = []
            dur = 0.26
            total_samples = int(sr * dur)
            for i in range(total_samples):
                t = i / sr
                # Pop followed by high sparkling chime
                if t < 0.05:
                    freq = 300 + 700 * (t / 0.05)
                    vol = (1.0 - t / 0.05) * 0.6
                    wave_val = math.sin(2 * math.pi * freq * t)
                else:
                    t_chime = t - 0.05
                    freq1 = 1046.50  # C6
                    freq2 = 1318.51  # E6
                    freq3 = 1567.98  # G6
                    vol = (1.0 - t_chime / 0.21) * 0.45
                    wave_val = (math.sin(2 * math.pi * freq1 * t) +
                                0.7 * math.sin(2 * math.pi * freq2 * t) +
                                0.5 * math.sin(2 * math.pi * freq3 * t))
                samples.append(wave_val * vol)
            self._generate_wav("kiss.wav", samples, sr)

        # 10. Minion spawn & "Banana!" sound (high pitch quirky minion chirp)
        if not os.path.exists(os.path.join(self.sounds_dir, "minion.wav")):
            samples = []
            dur = 0.32
            total_samples = int(sr * dur)
            for i in range(total_samples):
                t = i / sr
                # Fast playful minion vocal glide: 450Hz -> 900Hz -> 650Hz
                if t < 0.12:
                    freq = 450 + 450 * (t / 0.12)
                elif t < 0.22:
                    freq = 900 - 250 * ((t - 0.12) / 0.10)
                else:
                    freq = 650 + 350 * ((t - 0.22) / 0.10)
                mod = math.sin(2 * math.pi * 50 * t)
                wave_val = (math.sin(2 * math.pi * (freq + 40 * mod) * t) +
                            0.4 * math.sin(4 * math.pi * freq * t))
                vol = math.sin(math.pi * (t / dur)) * 0.4
                samples.append(wave_val * vol)
            self._generate_wav("minion.wav", samples, sr)

    def _load_sounds(self):
        for name in ["jump", "land", "sword", "coin", "grab", "arrr", "whistle", "squawk", "kiss", "minion"]:
            path = os.path.abspath(os.path.join(self.sounds_dir, f"{name}.wav"))
            if os.path.exists(path):
                self.sound_paths[name] = path

    def play(self, name: str):
        if not self.enabled:
            return
        path = self.sound_paths.get(name)
        if not path or not os.path.exists(path):
            return

        try:
            if sys.platform == "win32" and winsound:
                winsound.PlaySound(path, winsound.SND_FILENAME | winsound.SND_ASYNC | winsound.SND_NODEFAULT)
            elif sys.platform == "darwin":
                # macOS native audio player
                subprocess.Popen(["afplay", path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            else:
                # Linux (aplay or paplay)
                player = "paplay" if subprocess.call(["which", "paplay"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0 else "aplay"
                subprocess.Popen([player, path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception:
            pass
