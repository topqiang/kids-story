# -*- coding: utf-8 -*-
"""生成第一集 HyperFrames 视频所需的分句配音和轻量音效。"""

from __future__ import annotations

import json
import math
import subprocess
import wave
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VIDEO_DIR = ROOT / "videos" / "episode_001_bao_bao_chu_ru_you_er_yuan"
AUDIO_DIR = VIDEO_DIR / "assets" / "audio"


LINES = [
    {"id": "line_01", "role": "小北斗", "start": 0.0, "duration": 8.0, "rate": 205, "text": "小书包背好啦，幼儿园我来啦，见到老师笑一笑，早上好！"},
    {"id": "line_02", "role": "婷婷妈妈", "start": 8.0, "duration": 3.0, "rate": 180, "text": "小北斗，要不妈妈再陪你五分钟？"},
    {"id": "line_03", "role": "小北斗", "start": 11.0, "duration": 4.0, "rate": 205, "text": "妈妈，你也要上幼儿园吗？"},
    {"id": "line_04", "role": "北斗爸爸", "start": 15.0, "duration": 5.0, "rate": 168, "text": "爸爸觉得，可以先开个家庭会议。"},
    {"id": "line_05", "role": "小北斗", "start": 20.0, "duration": 6.0, "rate": 205, "text": "不用开会，我已经是大班预备队了。"},
    {"id": "line_06", "role": "婷婷妈妈", "start": 26.0, "duration": 6.0, "rate": 180, "text": "你要是想妈妈，就跟老师说。"},
    {"id": "line_07", "role": "小北斗", "start": 32.0, "duration": 6.0, "rate": 205, "text": "那妈妈想我，也要跟爸爸说。"},
    {"id": "line_08", "role": "小北斗", "start": 38.0, "duration": 6.0, "rate": 205, "text": "来，一人一个勇气贴纸。"},
    {"id": "line_09", "role": "北斗爸爸", "start": 44.0, "duration": 6.0, "rate": 168, "text": "爸爸也需要吗？"},
    {"id": "line_10", "role": "小北斗", "start": 50.0, "duration": 5.0, "rate": 205, "text": "你刚刚已经看了门口三次。"},
    {"id": "line_11", "role": "林老师", "start": 55.0, "duration": 6.0, "rate": 176, "text": "小北斗，早上好，我们一起去看小汽车积木吧。"},
    {"id": "line_12", "role": "小北斗", "start": 61.0, "duration": 6.0, "rate": 205, "text": "好！妈妈爸爸，挥手三下，不能多。"},
    {"id": "line_13", "role": "北斗爸爸", "start": 67.0, "duration": 6.0, "rate": 168, "text": "那爸爸偷偷再看一眼。"},
    {"id": "line_14", "role": "小北斗", "start": 73.0, "duration": 5.0, "rate": 205, "text": "爸爸，不能趴门缝，会吓到积木。"},
    {"id": "line_15", "role": "婷婷妈妈", "start": 78.0, "duration": 5.0, "rate": 180, "text": "他跑回来了，是不是舍不得？"},
    {"id": "line_16", "role": "小北斗", "start": 83.0, "duration": 5.0, "rate": 205, "text": "不是，妈妈，你的勇气贴纸掉了。"},
    {"id": "line_17", "role": "小北斗", "start": 88.0, "duration": 5.0, "rate": 205, "text": "你们乖乖上班，下午我来接你们。"},
]

SFX = [
    {"id": "sfx_steps", "start": 0.15, "duration": 2.6, "kind": "steps", "volume": 0.22},
    {"id": "sfx_pause", "start": 8.0, "duration": 0.55, "kind": "pause", "volume": 0.18},
    {"id": "sfx_ding", "start": 11.3, "duration": 0.55, "kind": "ding", "volume": 0.25},
    {"id": "sfx_gavel", "start": 15.2, "duration": 0.65, "kind": "gavel", "volume": 0.22},
    {"id": "sfx_sticker", "start": 38.35, "duration": 0.55, "kind": "sticker", "volume": 0.24},
    {"id": "sfx_brake", "start": 67.3, "duration": 0.85, "kind": "brake", "volume": 0.20},
    {"id": "sfx_chime", "start": 83.2, "duration": 0.7, "kind": "chime", "volume": 0.20},
]


def run_checked(args: list[str]) -> None:
    subprocess.run(args, check=True)


def generate_voice(line: dict[str, object]) -> None:
    text_path = AUDIO_DIR / f"{line['id']}.txt"
    aiff_path = AUDIO_DIR / f"{line['id']}.aiff"
    wav_path = AUDIO_DIR / f"{line['id']}.wav"
    text_path.write_text(str(line["text"]), encoding="utf-8")
    run_checked(["say", "-v", "Tingting", "-r", str(line["rate"]), "-o", str(aiff_path), "-f", str(text_path)])
    run_checked(["afconvert", str(aiff_path), str(wav_path), "-f", "WAVE", "-d", "LEI16"])
    aiff_path.unlink(missing_ok=True)


def write_wav(path: Path, samples: list[float], sample_rate: int = 44100) -> None:
    with wave.open(str(path), "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(sample_rate)
        frames = bytearray()
        for sample in samples:
            value = max(-1.0, min(1.0, sample))
            frames.extend(int(value * 32767).to_bytes(2, "little", signed=True))
        wav.writeframes(bytes(frames))


def envelope(i: int, total: int, attack: float = 0.04, release: float = 0.12) -> float:
    p = i / max(total - 1, 1)
    if p < attack:
        return p / attack
    if p > 1 - release:
        return max(0.0, (1 - p) / release)
    return 1.0


def make_sfx(kind: str, duration: float, volume: float, sample_rate: int = 44100) -> list[float]:
    total = int(duration * sample_rate)
    samples = [0.0] * total
    if kind == "ding":
        freqs = [880, 1320]
        for idx in range(total):
            env = envelope(idx, total, 0.02, 0.55)
            samples[idx] = sum(math.sin(2 * math.pi * f * idx / sample_rate) for f in freqs) * volume * env / len(freqs)
    elif kind == "pause":
        for idx in range(total):
            freq = 320 - 80 * idx / max(total, 1)
            samples[idx] = math.sin(2 * math.pi * freq * idx / sample_rate) * volume * envelope(idx, total, 0.02, 0.35)
    elif kind == "gavel":
        for idx in range(total):
            burst = math.sin(2 * math.pi * 120 * idx / sample_rate) * math.exp(-idx / (sample_rate * 0.08))
            samples[idx] = burst * volume
    elif kind == "sticker":
        split = int(total * 0.45)
        for idx in range(total):
            if idx < split:
                samples[idx] = math.sin(2 * math.pi * 760 * idx / sample_rate) * volume * envelope(idx, split, 0.01, 0.28)
            else:
                samples[idx] = math.sin(2 * math.pi * 520 * idx / sample_rate) * volume * 0.45 * envelope(idx - split, total - split, 0.01, 0.35)
    elif kind == "brake":
        for idx in range(total):
            freq = 900 - 650 * idx / max(total, 1)
            samples[idx] = math.sin(2 * math.pi * freq * idx / sample_rate) * volume * envelope(idx, total, 0.02, 0.18)
    elif kind == "chime":
        freqs = [660, 990, 1320]
        for idx in range(total):
            env = envelope(idx, total, 0.02, 0.65)
            samples[idx] = sum(math.sin(2 * math.pi * f * idx / sample_rate) for f in freqs) * volume * env / len(freqs)
    elif kind == "steps":
        for step in range(6):
            start = int((0.18 + step * 0.34) * sample_rate)
            length = int(0.08 * sample_rate)
            for j in range(length):
                pos = start + j
                if pos < total:
                    samples[pos] += math.sin(2 * math.pi * 180 * j / sample_rate) * volume * envelope(j, length, 0.02, 0.55)
    return samples


def generate_music() -> None:
    sample_rate = 44100
    duration = 93.0
    total = int(duration * sample_rate)
    notes = [392, 440, 523.25, 587.33, 523.25, 440]
    samples = [0.0] * total
    for idx in range(total):
        beat = int((idx / sample_rate) / 0.72)
        freq = notes[beat % len(notes)]
        phase = idx / sample_rate
        melody = math.sin(2 * math.pi * freq * phase) * 0.045
        harmony = math.sin(2 * math.pi * (freq / 2) * phase) * 0.025
        pulse = 0.65 + 0.35 * math.sin(2 * math.pi * phase / 1.44)
        samples[idx] = (melody + harmony) * pulse
    write_wav(AUDIO_DIR / "music_bed.wav", samples, sample_rate)


def main() -> None:
    AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    for line in LINES:
        generate_voice(line)
    for item in SFX:
        samples = make_sfx(str(item["kind"]), float(item["duration"]), float(item["volume"]))
        write_wav(AUDIO_DIR / f"{item['id']}.wav", samples)
    generate_music()
    manifest = {
        "duration": 93,
        "voice": "Tingting",
        "lines": LINES,
        "sfx": SFX,
        "music": {"id": "music_bed", "start": 0, "duration": 93, "volume": 0.12},
    }
    (VIDEO_DIR / "timeline_audio.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
