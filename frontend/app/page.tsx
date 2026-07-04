"use client";

import { useState } from "react";

type WordCard = {
  word: string;
  pinyin: string;
  meaning: string;
  sentence: string;
  translation: string;
};

const API_BASE_URL = "http://localhost:8000";

const sampleWords: WordCard[] = [
  {
    word: "咖啡",
    pinyin: "kā fēi",
    meaning: "커피",
    sentence: "我喜欢喝咖啡。",
    translation: "나는 커피를 좋아합니다.",
  },
  {
    word: "牛奶",
    pinyin: "niú nǎi",
    meaning: "우유",
    sentence: "请给我一杯牛奶。",
    translation: "우유 한 잔 주세요.",
  },
  {
    word: "蛋糕",
    pinyin: "dàn gāo",
    meaning: "케이크",
    sentence: "这个蛋糕很好吃。",
    translation: "이 케이크는 맛있습니다.",
  },
];

export default function Home() {
  const [topic, setTopic] = useState("카페");
  const [level, setLevel] = useState("HSK 1");
  const [duration, setDuration] = useState("20초");
  const [subtitlePosition, setSubtitlePosition] = useState("하단 중앙");

  const [words, setWords] = useState<WordCard[]>(sampleWords);
  const [videoUrl, setVideoUrl] = useState("");
  const [imageUrl, setImageUrl] = useState("");
  const [metadataUrl, setMetadataUrl] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleGenerate() {
    setLoading(true);
    setVideoUrl("");
    setImageUrl("");
    setMetadataUrl("");

    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/shorts/generate`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          topic,
          level,
          duration,
          subtitle_position: subtitlePosition,
        }),
      });

      const result = await response.json();

      if (!result.success) {
        alert(result.error?.message || "생성 실패");
        return;
      }

      const content = result.data.content;

      if (Array.isArray(content.words)) {
        setWords(content.words);
      } else {
        setWords([content]);
      }

      setVideoUrl(`${API_BASE_URL}${result.data.rendered.video_url}`);
      setImageUrl(`${API_BASE_URL}${result.data.rendered.image_url}`);
      setMetadataUrl(`${API_BASE_URL}${result.data.rendered.metadata_url}`);
    } catch (error) {
      console.error(error);
      alert("백엔드 연결 실패");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="page">
      <section className="studio">
        <div className="sectionHeader">
          <div>
            <span>STUDIO</span>
            <h2>숏츠 생성 설정</h2>
          </div>
          <p>
            주제, 난이도, 영상 길이, 자막 위치를 설정하면 AI 파이프라인이
            순서대로 실행됩니다.
          </p>
        </div>

        <div className="studioGrid">
          <div className="panel inputPanel">
            <div className="panelLabel">INPUT</div>
            <h3>주제 입력</h3>

            <label>학습 주제</label>
            <input
              value={topic}
              onChange={(event) => setTopic(event.target.value)}
              placeholder="예: 카페, 병원, 여행, 학교"
            />

            <div className="formGrid">
              <div>
                <label>난이도</label>
                <select
                  value={level}
                  onChange={(event) => setLevel(event.target.value)}
                >
                  <option>HSK 1</option>
                  <option>HSK 2</option>
                  <option>HSK 3</option>
                  <option>기초 회화</option>
                </select>
              </div>

              <div>
                <label>영상 길이</label>
                <select
                  value={duration}
                  onChange={(event) => setDuration(event.target.value)}
                >
                  <option>15초</option>
                  <option>20초</option>
                  <option>30초</option>
                  <option>60초</option>
                </select>
              </div>
            </div>

            <label>자막 위치</label>
            <select
              value={subtitlePosition}
              onChange={(event) => setSubtitlePosition(event.target.value)}
            >
              <option>하단 중앙</option>
              <option>중앙</option>
              <option>상단 중앙</option>
              <option>왼쪽 하단</option>
              <option>오른쪽 하단</option>
            </select>

            <button
              className="wideButton"
              onClick={handleGenerate}
              disabled={loading}
            >
              {loading ? "생성 중..." : "AI로 숏츠 생성하기"}
            </button>
          </div>

          <div className="panel resultPanel">
            <div className="panelLabel">AI RESULT</div>
            <h3>생성된 중국어 단어</h3>

            <div className="wordList">
              {words.map((item, index) => (
                <article className="wordCard" key={`${item.word}-${index}`}>
                  <div>
                    <strong>{item.word}</strong>
                    <span>{item.pinyin}</span>
                  </div>
                  <p>{item.meaning}</p>
                </article>
              ))}
            </div>
          </div>
        </div>
      </section>

      <section className="previewSection">
        <div className="phonePreview">
          <div className="phoneTop">9:16 PREVIEW</div>

          {imageUrl ? (
            <img
              src={imageUrl}
              alt="생성된 숏츠 이미지"
              style={{
                width: "100%",
                borderRadius: "26px",
                marginTop: "16px",
              }}
            />
          ) : (
            <div className="imageMock">
              <div className="circleGlow" />
              <span>{words[0]?.meaning || "미리보기"}</span>
            </div>
          )}

          <div className="subtitleBox">
            <strong>{words[0]?.word}</strong>
            <span>{words[0]?.pinyin}</span>
            <p>{words[0]?.sentence}</p>
            <small>{words[0]?.translation}</small>
          </div>
        </div>

        <div className="panel builderPanel">
          <div className="panelLabel">VIDEO BUILDER</div>
          <h3>영상 패키지</h3>

          <div className="summary">
            <div>
              <span>Topic</span>
              <strong>{topic}</strong>
            </div>
            <div>
              <span>Level</span>
              <strong>{level}</strong>
            </div>
            <div>
              <span>Duration</span>
              <strong>{duration}</strong>
            </div>
            <div>
              <span>Subtitle</span>
              <strong>{subtitlePosition}</strong>
            </div>
          </div>

          {videoUrl && (
            <a className="wideButton" href={videoUrl} target="_blank">
              생성된 숏츠 영상 열기
            </a>
          )}

          {imageUrl && (
            <a className="wideButton" href={imageUrl} target="_blank">
              커버 이미지 열기
            </a>
          )}

          {metadataUrl && (
            <a className="wideButton" href={metadataUrl} target="_blank">
              JSON 결과 열기
            </a>
          )}
        </div>
      </section>
    </main>
  );
}