#!/usr/bin/env python3
"""
Audio synthesis and music generation.
Based on piano_player.py and interstellar.py.
"""
import math
import struct
import wave
from pathlib import Path
from typing import List, Tuple, Optional, Dict, Any

class AudioSynthesizer:
    """Generate audio tones and music."""
    
    def __init__(self, sample_rate: int = 44100, bits: int = 16):
        self.sample_rate = sample_rate
        self.bits = bits
        self.max_amplitude = 2 ** (bits - 1) - 1
        
        # Piano frequencies
        self.frequencies = {
            'C4': 261.63, 'C#4': 277.18, 'D4': 293.66, 'D#4': 311.13,
            'E4': 329.63, 'F4': 349.23, 'F#4': 369.99, 'G4': 392.00,
            'G#4': 415.30, 'A4': 440.00, 'A#4': 466.16, 'B4': 493.88,
            'C5': 523.25, 'C#5': 554.37, 'D5': 587.33, 'D#5': 622.25,
            'E5': 659.25, 'F5': 698.46, 'F#5': 739.99, 'G5': 783.99,
            'G#5': 830.61, 'A5': 880.00, 'A#5': 932.33, 'B5': 987.77,
        }
    
    def generate_tone(self, freq: float, duration: float, volume: float = 0.7) -> List[int]:
        """Generate a sine wave tone."""
        num_samples = int(duration * self.sample_rate)
        samples = []
        
        for i in range(num_samples):
            t = i / self.sample_rate
            value = math.sin(2 * math.pi * freq * t)
            
            # Simple envelope
            envelope = 1.0
            if t < 0.05:  # Attack
                envelope = t / 0.05
            elif t > duration - 0.1:  # Release
                envelope = (duration - t) / 0.1
            
            samples.append(int(value * envelope * volume * self.max_amplitude))
        
        return samples
    
    def generate_note(self, note: str, duration: float, volume: float = 0.7) -> List[int]:
        """Generate a musical note."""
        if note in self.frequencies:
            return self.generate_tone(self.frequencies[note], duration, volume)
        return []
    
    def generate_chord(self, notes: List[str], duration: float, volume: float = 0.7) -> List[int]:
        """Generate a chord (multiple notes)."""
        samples = [self.generate_note(n, duration, volume) for n in notes]
        if not samples:
            return []
        
        # Mix samples
        max_len = max(len(s) for s in samples)
        mixed = []
        for i in range(max_len):
            value = sum(s[i] if i < len(s) else 0 for s in samples)
            value = max(-self.max_amplitude, min(self.max_amplitude, value))
            mixed.append(value)
        
        return mixed
    
    def save_wav(self, samples: List[int], filename: str) -> None:
        """Save samples as WAV file."""
        with wave.open(filename, 'w') as wav:
            wav.setnchannels(1)
            wav.setsampwidth(self.bits // 8)
            wav.setframerate(self.sample_rate)
            
            if self.bits == 16:
                packed = struct.pack(f'<{len(samples)}h', *samples)
                wav.writeframes(packed)
    
    def create_interstellar_theme(self, output_file: str = "interstellar.wav") -> None:
        """Create Interstellar theme music."""
        notes = ['G4', 'D4', 'G4'] * 8  # Simple pattern
        samples = []
        
        for note in notes:
            samples.extend(self.generate_note(note, 0.5, 0.6))
            # Add subtle rest
            samples.extend(self.generate_tone(0, 0.1, 0))
        
        self.save_wav(samples, output_file)
        print(f"Generated: {output_file}")

def main():
    synth = AudioSynthesizer()
    
    # Generate simple melody
    melody = ['C4', 'D4', 'E4', 'F4', 'G4', 'A4', 'B4', 'C5']
    samples = []
    for note in melody:
        samples.extend(synth.generate_note(note, 0.3, 0.7))
    
    synth.save_wav(samples, "melody.wav")
    print("Generated: melody.wav")
    
    # Generate chord
    samples = synth.generate_chord(['C4', 'E4', 'G4'], 2.0, 0.5)
    synth.save_wav(samples, "chord.wav")
    print("Generated: chord.wav")

if __name__ == "__main__":
    main()
