# Sana Factory MVP

로컬 AI 기반 중국어 숏츠 자동 생성 MVP입니다.

## 실행

### 1. 백엔드

```bash
cd backend
source .venv/bin/activate
python -m uvicorn app.main:app --reload --port 8000
```

### 2. 프론트엔드

```bash
cd frontend
npm install
npm run dev
```

### 3. Ollama

```bash
ollama pull qwen2.5:7b
```

`.env`의 `OLLAMA_MODEL`을 설치한 모델명과 맞추세요.

### 4. FFmpeg

MP4 렌더링을 위해 필요합니다.

```bash
brew install ffmpeg
```

## 사용법

1. http://localhost:3000 접속
2. 주제 입력
3. `주제로 숏츠 자동 생성` 클릭
4. MP4, ASS, JSON 결과 확인

## API

- POST `/api/v1/shorts/generate`

```json
{
  "topic": "카페",
  "level": "HSK 1",
  "duration": "20초",
  "subtitle_position": "하단 중앙"
}
```
