from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path
from textwrap import shorten
from uuid import uuid4

from app.core.config import settings


def _escape_ass(text: str) -> str:
    return text.replace("\\", "\\\\").replace("{", "\\{").replace("}", "\\}").replace("\n", "\\N")


def _format_time(seconds: float) -> str:
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    centis = int((seconds - int(seconds)) * 100)
    return f"{hours}:{minutes:02d}:{secs:02d}.{centis:02d}"


def _make_ass(words: list[dict], output_path: Path) -> None:
    # 1080x1920 Shorts canvas. Alignment 2 = bottom center.
    header = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 0
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Title,Arial,74,&H00FFFFFF,&H00FFFFFF,&H00000000,&H99000000,1,0,0,0,100,100,0,0,1,4,2,8,60,60,110,1
Style: Word,Arial,118,&H00FFFFFF,&H00FFFFFF,&H00000000,&H99000000,1,0,0,0,100,100,0,0,1,5,2,5,60,60,80,1
Style: Pinyin,Arial,54,&H0000D7FF,&H0000D7FF,&H00000000,&H99000000,0,0,0,0,100,100,0,0,1,3,1,5,60,60,80,1
Style: Meaning,Arial,64,&H00FFFFFF,&H00FFFFFF,&H00000000,&H99000000,1,0,0,0,100,100,0,0,1,4,2,2,80,80,250,1
Style: Sentence,Arial,42,&H00E6E6E6,&H00E6E6E6,&H00000000,&H99000000,0,0,0,0,100,100,0,0,1,3,1,2,90,90,140,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    lines = [header]
    lines.append("Dialogue: 0,0:00:00.00,0:00:02.00,Title,,0,0,0,,오늘의 중국어 단어")
    start = 2.0
    for item in words[:3]:
        end = start + 5.0
        word = _escape_ass(str(item.get("word", "")))
        pinyin = _escape_ass(str(item.get("pinyin", "")))
        meaning = _escape_ass(str(item.get("meaning", "")))
        sentence = _escape_ass(str(item.get("sentence", "")))
        translation = _escape_ass(str(item.get("translation", "")))
        lines.append(f"Dialogue: 0,{_format_time(start)},{_format_time(end)},Word,,0,0,0,,{word}")
        lines.append(f"Dialogue: 0,{_format_time(start+0.4)},{_format_time(end)},Pinyin,,0,0,0,,{pinyin}")
        lines.append(f"Dialogue: 0,{_format_time(start+1.2)},{_format_time(end)},Meaning,,0,0,0,,{meaning}")
        lines.append(f"Dialogue: 0,{_format_time(start+2.2)},{_format_time(end)},Sentence,,0,0,0,,{sentence}\\N{translation}")
        start = end
    output_path.write_text("\n".join(lines), encoding="utf-8")


def normalize_words(ai_result: dict) -> list[dict]:
    if isinstance(ai_result, dict):
        words = ai_result.get("words") or ai_result.get("data") or []
    else:
        words = []
    if not isinstance(words, list):
        words = []
    normalized: list[dict] = []
    for item in words:
        if not isinstance(item, dict):
            continue
        normalized.append(
            {
                "word": str(item.get("word", "")),
                "pinyin": str(item.get("pinyin", "")),
                "meaning": str(item.get("meaning", "")),
                "sentence": str(item.get("sentence", "")),
                "translation": str(item.get("translation", "")),
            }
        )
    return normalized[:3]


def fallback_words(topic: str) -> list[dict]:
    base = {
        "카페": [
            {"word": "咖啡", "pinyin": "kā fēi", "meaning": "커피", "sentence": "我喜欢喝咖啡。", "translation": "나는 커피를 좋아합니다."},
            {"word": "牛奶", "pinyin": "niú nǎi", "meaning": "우유", "sentence": "请给我一杯牛奶。", "translation": "우유 한 잔 주세요."},
            {"word": "蛋糕", "pinyin": "dàn gāo", "meaning": "케이크", "sentence": "这个蛋糕很好吃。", "translation": "이 케이크는 맛있습니다."},
        ]
    }
    return base.get(topic, [
        {"word": "学习", "pinyin": "xué xí", "meaning": "공부하다", "sentence": "我每天学习中文。", "translation": "나는 매일 중국어를 공부합니다."},
        {"word": "朋友", "pinyin": "péng you", "meaning": "친구", "sentence": "他是我的朋友。", "translation": "그는 나의 친구입니다."},
        {"word": "今天", "pinyin": "jīn tiān", "meaning": "오늘", "sentence": "今天我很忙。", "translation": "오늘 나는 매우 바쁩니다."},
    ])


def render_short(topic: str, words: list[dict]) -> dict:
    job_id = str(uuid4())
    output_root = Path(settings.STORAGE_PATH).resolve()
    job_dir = output_root / job_id
    job_dir.mkdir(parents=True, exist_ok=True)

    ass_path = job_dir / "subtitle.ass"
    video_path = job_dir / "shorts.mp4"
    json_path = job_dir / "result.json"

    _make_ass(words, ass_path)
    json_path.write_text(json.dumps({"topic": topic, "words": words}, ensure_ascii=False, indent=2), encoding="utf-8")

    ffmpeg = shutil.which("ffmpeg")
    if ffmpeg is None:
        return {
            "job_id": job_id,
            "status": "NO_FFMPEG",
            "message": "FFmpeg가 설치되어 있지 않아 JSON과 자막만 생성했습니다. brew install ffmpeg 후 다시 실행하세요.",
            "words": words,
            "subtitle_url": f"/outputs/{job_id}/subtitle.ass",
            "json_url": f"/outputs/{job_id}/result.json",
            "video_url": None,
        }

    # Use a generated gradient-like dark background and ASS subtitles.
    # duration = 2s intro + 5s * 3 words = 17s
    duration = 17
    title = shorten(topic, width=28, placeholder="...")
    vf = f"ass='{ass_path.as_posix()}'"
    cmd = [
        ffmpeg,
        "-y",
        "-f",
        "lavfi",
        "-i",
        "color=c=0x08090c:s=1080x1920:d=17",
        "-f",
        "lavfi",
        "-i",
        "anullsrc=channel_layout=stereo:sample_rate=44100",
        "-t",
        str(duration),
        "-vf",
        vf,
        "-c:v",
        "libx264",
        "-pix_fmt",
        "yuv420p",
        "-c:a",
        "aac",
        "-shortest",
        video_path.as_posix(),
    ]
    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True, timeout=120)
        status = "SUCCESS"
        message = "숏츠 MP4 생성 완료"
    except subprocess.CalledProcessError as exc:
        status = "RENDER_FAILED"
        message = exc.stderr[-1200:] if exc.stderr else "FFmpeg 렌더링 실패"
    except subprocess.TimeoutExpired:
        status = "RENDER_TIMEOUT"
        message = "FFmpeg 렌더링 시간이 초과되었습니다."

    return {
        "job_id": job_id,
        "status": status,
        "message": message,
        "topic": topic,
        "title": f"오늘의 중국어: {title}",
        "words": words,
        "video_url": f"/outputs/{job_id}/shorts.mp4" if video_path.exists() else None,
        "subtitle_url": f"/outputs/{job_id}/subtitle.ass",
        "json_url": f"/outputs/{job_id}/result.json",
    }
