# AI 家具銷售平台 — 技術實現方法

> 版本：v1.0 · 2026-10-03
> 用途：技術藍圖 / 工程評估 / 開發排期
> 受眾：CTO、後端工程師、AI 工程師、3D 工程師

---

## 目錄

1. [整體技術架構（5 層）](#一整體技術架構-5-層)
2. [每個模塊的實現細節](#二每個模塊的實現細節)
3. [核心算法（AI 部分）](#三核心算法ai-部分)
4. [系統依賴與基礎設施](#四系統依賴與基礎設施)
5. [開發順序與里程碑](#五開發順序與里程碑)
6. [技術風險與緩解](#六技術風險與緩解)
7. [技術選型最終推薦](#七技術選型最終推薦)
8. [立即可做的（推薦）](#八立即可做的推薦)

---

## 一、整體技術架構（5 層）

```
┌────────────────────────────────────────────────────────────┐
│  Layer 1: 用戶端 (C 端)                                    │
│  - 手機 H5 (React)                                         │
│  - iOS / Android (React Native 或原生)                    │
│  - 微信小程式                                              │
└────────────────────────────────────────────────────────────┘
                              ↕ WSS / WebRTC
┌────────────────────────────────────────────────────────────┐
│  Layer 2: 邊緣層 (Edge)                                    │
│  - RTC 服務 (聲網 / 騰訊雲 / LiveKit)                      │
│  - CDN (Cloudflare / 阿里雲)                              │
│  - WAF / DDoS 防護                                         │
└────────────────────────────────────────────────────────────┘
                              ↕ HTTPS
┌────────────────────────────────────────────────────────────┐
│  Layer 3: AI 編排層 (Orchestrator) ⭐ 核心                  │
│  - API Gateway (Kong / Nginx)                              │
│  - ASR Worker Pool                                         │
│  - VLM Worker Pool                                         │
│  - LLM Gateway (轉發到 GPT-4o Realtime / Doubao / Gemini)  │
│  - TTS Worker Pool                                         │
│  - Function Calling Router                                 │
│  - Session Manager (Redis)                                 │
└────────────────────────────────────────────────────────────┘
                              ↕ gRPC / SQL
┌────────────────────────────────────────────────────────────┐
│  Layer 4: 業務服務層 (Business Services)                    │
│  - 商品服務 (Product Service)                               │
│  - 訂單服務 (Order Service)                                 │
│  - 用戶服務 (User Service)                                  │
│  - 商家服務 (Merchant Service)                              │
│  - 推薦服務 (Recommendation)                                │
│  - 支付服務 (Payment Service)                                │
│  - 物流服務 (Logistics Service)                              │
│  - CRM 服務 (EspoCRM 整合)                                  │
└────────────────────────────────────────────────────────────┘
                              ↕ SQL / Vector Search
┌────────────────────────────────────────────────────────────┐
│  Layer 5: 數據層 (Data Layer)                              │
│  - PostgreSQL (主數據庫)                                    │
│  - Redis (快取 + Session)                                   │
│  - Qdrant / Milvus (向量資料庫)                             │
│  - S3 / OSS (商品圖、3D 模型、用戶上傳)                    │
│  - ClickHouse (分析、BI)                                    │
└────────────────────────────────────────────────────────────┘
```

---

## 二、每個模塊的實現細節

### A. 用戶端（手機）

| 模塊 | 技術選型 | 難度 | 備註 |
|---|---|---|---|
| **H5 Web App** | React + Vite + TypeScript | ⭐⭐ | MVP 首選 |
| **狀態管理** | Zustand / Redux Toolkit | ⭐ | 中小型用 Zustand |
| **路由** | React Router v6 | ⭐ | |
| **UI 庫** | Tailwind CSS + shadcn/ui | ⭐⭐ | 快速標準化 |
| **WebRTC 客戶端** | 聲網 SDK / LiveKit Client SDK | ⭐⭐⭐ | 需 RTC 帳號 |
| **WebSocket** | Socket.IO Client | ⭐⭐ | |
| **AR 試擺 (iOS)** | ARKit + RoomPlan (Swift) | ⭐⭐⭐⭐ | LiDAR 限定 |
| **AR 試擺 (Android)** | ARCore + Scene Semantics (Kotlin) | ⭐⭐⭐⭐ | |
| **AR 試擺 (Web)** | WebXR + 8th Wall / model-viewer | ⭐⭐⭐ | 跨平台備選 |
| **3D 渲染** | Three.js / Babylon.js + glTF | ⭐⭐⭐ | |
| **音訊處理** | Web Audio API + AudioWorklet | ⭐⭐⭐ | VAD + 降噪 |
| **拍照 / 上傳** | HTML5 `<input capture>` | ⭐ | |

**推薦 MVP 組合**：React + Vite + Tailwind + 聲網 SDK + Three.js + WebXR

---

### B. 後端服務（業務邏輯）

| 模塊 | 技術選型 | 難度 | 備註 |
|---|---|---|---|
| **後端語言** | Python (FastAPI) + Node.js (BFF) | ⭐⭐ | Python 處理 AI，Node 做 BFF |
| **API Gateway** | Kong / APISIX | ⭐⭐ | |
| **服務通信** | gRPC + Protocol Buffers | ⭐⭐⭐ | 高性能 |
| **任務佇列** | Celery / BullMQ | ⭐⭐ | 異步任務 |
| **WebSocket Hub** | Socket.IO Server / uWebSockets.js | ⭐⭐ | |
| **定時任務** | APScheduler / Airflow | ⭐ | |
| **監控** | Prometheus + Grafana | ⭐⭐ | |
| **日誌** | ELK Stack | ⭐⭐ | |
| **錯誤追蹤** | Sentry | ⭐ | |
| **CI/CD** | GitHub Actions / GitLab CI | ⭐⭐ | |

---

### C. AI 編排層（最核心、最難）

#### C.1 ASR（語音識別）

| 方案 | 延遲 | 中文品質 | 串流 |
|---|---|---|---|
| **阿里雲一句話識別** | < 500ms | ⭐⭐⭐⭐⭐ | ❌ |
| **阿里雲實時語音識別** | < 300ms | ⭐⭐⭐⭐⭐ | ✅ |
| **火山引擎流式 ASR** | < 300ms | ⭐⭐⭐⭐⭐ | ✅ |
| **Azure Speech** | < 600ms | ⭐⭐⭐⭐ | ✅ |
| **Whisper (自建)** | 1-3s | ⭐⭐⭐⭐ | ⚠️ |

**推薦**：阿里雲 / 火山引擎 串流 ASR（中文最佳 + 延遲低）

#### C.2 LLM（大語言模型對話）

| 方案 | 延遲 | 中文 | full-duplex | 視訊 | 成本 |
|---|---|---|---|---|---|
| **GPT-4o Realtime** | 232ms | ⭐⭐⭐⭐ | ✅ | ✅ | $40/$80 per M tokens |
| **GPT-4o-mini Realtime** | <300ms | ⭐⭐⭐⭐ | ✅ | ✅ | $0.6/$2.4 |
| **Gemini 2.5 Flash Live** | sub-sec | ⭐⭐⭐⭐ | ✅ | ✅ | $0.075/$0.30 |
| **Doubao Pro 1.5** | <400ms | ⭐⭐⭐⭐⭐ | 部分 | ✅ | 國內便宜 |
| **Qwen3-Omni** | <600ms | ⭐⭐⭐⭐⭐ | 串流 | ✅ | 國內便宜 |

**推薦組合**：
- MVP → GPT-4o-mini Realtime
- 生產 → GPT-4o Realtime + Doubao（分流）
- 國內備援 → Qwen3-Omni

**Function Calling 設計範例**：

```python
tools = [
    {
        "type": "function",
        "function": {
            "name": "search_products",
            "description": "搜索家具商品",
            "parameters": {
                "type": "object",
                "properties": {
                    "category": {"type": "string"},
                    "style": {"type": "string"},
                    "budget_max": {"type": "number"},
                    "in_stock": {"type": "boolean"}
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "generate_ar_preview",
            "description": "生成 AR 試擺預覽"
        }
    },
    {
        "type": "function",
        "function": {
            "name": "create_order",
            "description": "創建訂單"
        }
    }
]
```

#### C.3 VLM（視覺理解）

| 方案 | 用途 | 部署 |
|---|---|---|
| **Qwen2.5-VL-7B** | 房間照片分析、風格識別 | 自建 GPU / API |
| **GPT-4o vision** | 同上 | API |
| **Gemini 2.0 Flash Vision** | 同上，便宜 | API |

**推薦**：Qwen2.5-VL-7B 自建（中文最優，性價比高）

#### C.4 TTS（語音合成）

| 方案 | 品質 | 串流 | 成本 |
|---|---|---|---|
| **edge-tts** | ⭐⭐⭐⭐ | ✅ | 免費 |
| **阿里雲 CosyVoice 2.0** | ⭐⭐⭐⭐⭐ | ✅ | ¥0.02/萬字 |
| **火山引擎 TTS** | ⭐⭐⭐⭐⭐ | ✅ | ¥0.018/萬字 |
| **ElevenLabs** | ⭐⭐⭐⭐⭐ | ✅ | $5/月起 |
| **GPT-4o Realtime TTS** | ⭐⭐⭐⭐⭐ | ✅ native | 包含在 LLM |

**推薦**：MVP 用 edge-tts；生產用 CosyVoice 2.0

---

### D. 數據層

#### D.1 PostgreSQL（主數據庫）

```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    phone VARCHAR(20) UNIQUE,
    nickname VARCHAR(50),
    avatar_url TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE merchants (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL,
    business_license VARCHAR(50),
    contact_phone VARCHAR(20),
    status VARCHAR(20) DEFAULT 'pending',
    plan VARCHAR(20) DEFAULT 'free',
    monthly_fee DECIMAL(10,2),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE products (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    merchant_id UUID REFERENCES merchants(id),
    name VARCHAR(200) NOT NULL,
    description TEXT,
    category VARCHAR(50),
    style_tags TEXT[],
    price DECIMAL(10,2),
    original_price DECIMAL(10,2),
    stock INT DEFAULT 0,
    images TEXT[],
    model_3d_url TEXT,
    dimensions JSONB,
    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE orders (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    merchant_id UUID REFERENCES merchants(id),
    items JSONB NOT NULL,
    total_amount DECIMAL(10,2),
    status VARCHAR(20),
    shipping_address JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE conversations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    merchant_id UUID REFERENCES merchants(id),
    started_at TIMESTAMPTZ DEFAULT NOW(),
    ended_at TIMESTAMPTZ,
    transcript JSONB,
    metadata JSONB,
    sentiment VARCHAR(20),
    converted_to_order BOOLEAN DEFAULT FALSE,
    order_id UUID REFERENCES orders(id)
);

CREATE INDEX idx_products_merchant ON products(merchant_id);
CREATE INDEX idx_products_category ON products(category);
CREATE INDEX idx_products_tags ON products USING GIN(style_tags);
CREATE INDEX idx_orders_user ON orders(user_id);
CREATE INDEX idx_orders_merchant ON orders(merchant_id);
CREATE INDEX idx_conversations_user ON conversations(user_id);
```

#### D.2 Qdrant（向量資料庫）

```python
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

client = QdrantClient(host="localhost", port=6333)

# 1. 建立 collection
client.create_collection(
    collection_name="products",
    vectors_config=VectorParams(size=1024, distance=Distance.COSINE)
)

# 2. 為每個商品生成 embedding

# 3. 批量入庫
points = [
    PointStruct(
        id=product.id,
        vector=embedding,
        payload={
            "name": product.name,
            "category": product.category,
            "style": product.style_tags,
            "price": product.price,
            "image": product.images[0]
        }
    )
    for product, embedding in zip(products, embeddings)
]
client.upsert(collection_name="products", points=points)

# 4. 搜尋
results = client.search(
    collection_name="products",
    query_vector=user_query_embedding,
    limit=10,
    query_filter={
        "must": [
            {"key": "price", "range": {"lte": 5000}},
            {"key": "category", "match": "沙發"}
        ]
    }
)
```

#### D.3 Redis（快取 + Session）

```python
import redis.asyncio as redis

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

# Session 管理
async def get_session(user_id):
    return await r.get(f"session:{user_id}")

async def save_session(user_id, data, ttl=3600):
    await r.setex(f"session:{user_id}", ttl, json.dumps(data))

# 商品快取
async def cache_product(product_id, data, ttl=300):
    await r.setex(f"product:{product_id}", ttl, json.dumps(data))

# 限流
async def rate_limit(user_id, max_per_min=60):
    key = f"ratelimit:{user_id}:{int(time.time()//60)}"
    count = await r.incr(key)
    if count == 1:
        await r.expire(key, 60)
    return count <= max_per_min
```

---

### E. 3D + AR 模塊

#### E.1 3D 模型生產 pipeline

```
   方式 A: 廠商提供          方式 B: AI 生成           方式 C: 手工建模
   ┌──────────────┐         ┌──────────────┐         ┌──────────────┐
   │ 發送 GLB 模板 │         │ 拍照         │         │ Blender      │
   │ ↓ 廠商建模   │         │ ↓ Tripo3D    │         │ ↓ 4-8 小時   │
   │ 上傳 S3       │         │ ↓ 30 秒      │         │ 50 件 → 200小時 │
   └──────┬───────┘         └──────┬───────┘         └──────┬───────┘
          ↓                        ↓                        ↓
   ┌──────────────────────────────────────────────────────────────────┐
   │ 統一格式: glTF 2.0 (含 KTX2 textures + Draco compression)        │
   │ 自動 CDN 分發 (S3 + CloudFront)                                 │
   │ 自動生成 USDZ (iOS Quick Look)                                   │
   └──────────────────────────────────────────────────────────────────┘
```

**glTF 2.0 標準化**：
- 紋理用 KTX2 + Basis Universal（壓縮比高）
- 網格用 Draco 壓縮
- 動畫用 baked transforms（不用骨骼動畫）

#### E.2 AR 試擺實現

**iOS (ARKit + RoomPlan)**：
```swift
import ARKit
import RealityKit

class ARTryOnView: ARView {
    func loadAndPlace(model: ModelEntity) {
        let entity = try! ModelEntity.loadModel(named: "sofa.usdz")
        entity.generateCollisionShapes(recursive: true)
        
        let anchor = AnchorEntity(plane: .horizontal, classification: .floor)
        anchor.addChild(entity)
        scene.addAnchor(anchor)
    }
}
```

**Android (ARCore)**：
```kotlin
import com.google.ar.core.Anchor
import com.google.ar.sceneform.AnchorNode

fun placeModel(model: ModelRenderable) {
    val anchor = hitResult!!.createAnchor()
    val anchorNode = AnchorNode(anchor)
    anchorNode.renderable = model
    arSceneView.scene.addChild(anchorNode)
}
```

**Web (8th Wall)**：
```javascript
import * as XR8 from '@8thwall/web'

XR8.run({canvas: document.querySelector('#arcanvas')})
XR8.XrController.on('update', () => {
  scene.add(model)
})
```

#### E.3 室內空間掃描（RoomPlan）

```swift
let roomCaptureView = RoomCaptureView(frame: .zero)
roomCaptureView.delegate = self
roomCaptureView.captureSession.run(configuration: ...)
```

掃描後得到：
- 牆壁位置
- 地板平面
- 傢俱 bounding box
- 門窗位置

---

## 三、核心算法（AI 部分）

### 1. VAD（語音活動檢測）

```python
import torch
model, utils = torch.hub.load(
    repo_or_dir='snakers4/silero-vad',
    model='silero_vad',
    force_reload=False
)

def is_speech(audio_chunk):
    confidence = model(audio_chunk, 16000).item()
    return confidence > 0.5
```

### 2. 迴聲消除（AEC）

```python
from webrtc_audio_processing import AudioProcessing

ap = AudioProcessing()
ap.set_stream_format(sample_rate=16000, num_channels=1)

def process_audio(mic_chunk, speaker_chunk):
    out = ap.process_stream(mic_chunk, speaker_chunk)
    return out
```

### 3. 全雙工邏輯（核心算法）

```python
async def full_duplex_loop(
    user_mic_stream: AsyncIterator[bytes],
    user_cam_stream: AsyncIterator[bytes],
    ai_speaker_stream: AsyncIterator[bytes]
):
    state = {
        'ai_speaking': False,
        'user_speaking': False,
        'last_user_speech_end': None,
        'interrupted': False
    }
    
    while True:
        await asyncio.gather(
            handle_mic_input(user_mic_stream, state),
            handle_cam_input(user_cam_stream, state),
            generate_ai_response(ai_speaker_stream, state),
            handle_barge_in(state)
        )
```

### 4. RAG 商品推薦

```python
class ProductRAG:
    def __init__(self):
        self.qdrant = QdrantClient(...)
        self.embedder = TextEmbedder(...)
    
    async def search(self, query: str, filters: dict):
        query_vec = await self.embedder.embed(query)
        candidates = self.qdrant.search(
            collection_name="products",
            query_vector=query_vec,
            limit=20,
            query_filter=filters
        )
        ranked = await self.rerank(query, candidates)
        return ranked[:5]
    
    async def rerank(self, query, candidates):
        prompt = f"""
        用戶查詢：「{query}」
        候選商品：{[c.payload for c in candidates]}
        
        給每個商品評分（0-10），按相關性排序。
        返回 JSON: {{"ranked_ids": [...], "reasons": [...]}}
        """
        return await self.llm.agenerate(prompt)
```

---

## 四、系統依賴與基礎設施

### A. 基礎服務清單

| 服務 | 用途 | 託管 |
|---|---|---|
| **PostgreSQL 15+** | 主數據庫 | 阿里雲 RDS |
| **Redis 7+** | 快取、Session | 阿里雲 Redis |
| **Qdrant** | 向量資料庫 | 自建（Docker）|
| **MinIO** | S3 相容儲存 | 自建 |
| **Nginx** | 反向代理 | 自建 |
| **Certbot** | HTTPS 憑證 | 自動續 |
| **Prometheus + Grafana** | 監控 | 自建 |
| **Sentry** | 錯誤追蹤 | SaaS |
| **ELK** | 日誌 | 阿里雲 ES |

### B. 雲端供應商

| 場景 | 推薦 |
|---|---|
| **中國用戶** | 阿里雲（華北/華東）+ 火山引擎 RTC |
| **海外用戶** | AWS / GCP + 聲網 Global |
| **混合** | 阿里雲（國內）+ Cloudflare（海外） |

### C. 成本估算（月，1 萬月活）

| 項目 | 規格 | 月成本 |
|---|---|---|
| 雲端伺服器（API + DB + Redis）| 4 vCPU / 16GB × 3 台 | ¥3,000-5,000 |
| Qdrant 向量 DB | 1 台 | ¥500 |
| S3/OSS | 1TB | ¥200 |
| CDN | 1TB 流量 | ¥500 |
| 阿里雲 RTC | 5 萬分鐘 | ¥5,000 |
| 阿里雲 ASR | 100 萬次 | ¥600 |
| 阿里雲 TTS | 100 萬字 | ¥2,000 |
| GPT-4o Realtime API | 100 萬 in + 200 萬 out tokens | ¥15,000-30,000 |
| 監控 + 日誌 + Sentry | — | ¥500 |
| **總計** | — | **¥27,000-44,000 / 月** |

---

## 五、開發順序與里程碑

### Sprint 0 — 基礎設施（1 週）

- [ ] GitHub repo + CI/CD pipeline
- [ ] 雲端帳號 + 域名 + DNS
- [ ] PostgreSQL / Redis / Qdrant / MinIO 部署
- [ ] HTTPS 憑證
- [ ] 監控系統
- [ ] 開發環境 Docker Compose

### Sprint 1 — MVP 文字版電商（4 週）

- [ ] 用戶端 React + Vite
- [ ] 商品列表 / 詳情 / 搜尋
- [ ] 訂單流程 + 支付
- [ ] 商家後台 v1
- [ ] 文字版 AI 客服（GPT-4o + Function Calling）

### Sprint 2 — 語音版（4 週）

- [ ] WebRTC 整合（聲網 SDK）
- [ ] ASR + LLM + TTS 串流 pipeline
- [ ] 全雙工對話介面
- [ ] Barge-in 處理
- [ ] 對話歷史記錄

### Sprint 3 — 視覺版（4 週）

- [ ] 房間照片上傳
- [ ] Qwen2.5-VL 整合
- [ ] AI 搭配推薦
- [ ] 風格識別 + 標籤

### Sprint 4 — AR 試擺（6 週）

- [ ] 3D viewer (Three.js)
- [ ] 3D 模型庫（首批 50 件）
- [ ] ARKit / ARCore / WebXR 整合
- [ ] RoomPlan 室內掃描
- [ ] 1:1 真實尺寸試擺

### Sprint 5 — 數字人 + 視訊（8 週）

- [ ] 數字人模型
- [ ] 視訊流整合
- [ ] 表情同步
- [ ] 視訊內容生成

---

## 六、技術風險與緩解

| 風險 | 嚴重度 | 緩解方案 |
|---|---|---|
| **GPT-4o 中文不夠本地化** | 🟡 | Doubao Pro / Qwen3-Omni 雙引擎分流 |
| **全雙工延遲超 500ms** | 🔴 | L40S GPU + 串流式 pipeline |
| **3D 模型品質差** | 🟡 | 強迫供應商提供 GLB + AI 校正 |
| **AR 準確度問題** | 🟡 | RoomPlan + LiDAR 限定高端用戶 |
| **AI 幻覺推薦** | 🔴 | 所有推薦走 RAG + DB 查詢 |
| **個資隱私** | 🔴 | 視訊明確告知 + 端到端加密 + 不存原始 |
| **GPU 成本爆炸** | 🟡 | 優先用 API，按用量付費 |
| **VAD 失誤** | 🟡 | silero-vad + 多重確認 |
| **大量併發** | 🟡 | 自動擴容 + RTC 分散 |

---

## 七、技術選型最終推薦

| 層 | 推薦 |
|---|---|
| **前端** | React + Vite + TypeScript + Tailwind + shadcn/ui |
| **後端** | Python FastAPI（AI）+ Node.js Fastify（BFF）|
| **數據庫** | PostgreSQL + Redis + Qdrant + ClickHouse |
| **RTC** | 聲網 Agora |
| **ASR** | 阿里雲 NLS |
| **LLM** | GPT-4o Realtime（海外）+ Doubao（國內）|
| **VLM** | Qwen2.5-VL-7B |
| **TTS** | edge-tts（開發）→ CosyVoice 2.0（生產）|
| **3D** | Three.js + glTF 2.0 |
| **AR** | ARKit + RoomPlan（iOS）/ ARCore（Android）/ WebXR（Web）|
| **雲端** | 阿里雲（中國）+ AWS（海外）|
| **CI/CD** | GitHub Actions |
| **監控** | Prometheus + Grafana + Sentry |

---

## 八、立即可做的（推薦）

| # | 動作 | 預計時間 |
|---|---|---|
| 1 | 建立 GitHub repo + 專案結構 | 1 天 |
| 2 | 跑通 GPT-4o Realtime API hello world | 1 天 |
| 3 | 跑通阿里雲 ASR + edge-tts 串流 | 2 天 |
| 4 | React + Vite + Tailwind 起手 | 1 天 |
| 5 | 設計 DB schema（前面 D.1）| 1 天 |
| 6 | 寫「GPT-4o Realtime + ASR + TTS 串流對接」技術驗證 POC | 1 週 |

---

## 附錄：核心算法流程圖

```
用戶語音輸入 (20ms chunks)
  ↓
[VAD] silero-vad → 判斷是否語音
  ↓ 是
[AEC] WebRTC AudioProcessing → 消除 speaker 迴聲
  ↓
[ASR] 阿里雲 NLS → 串流回傳部分文字
  ↓
[LLM] GPT-4o Realtime → 思考 + 生成文字回應
  ↓
[Function Calling] 決定是否需要查詢/下單/AR
  ├─ 是 → 並行調用 API → 結果回 LLM
  └─ 否 → 直接進入 TTS
  ↓
[TTS] CosyVoice 2.0 / edge-tts → 串流語音輸出
  ↓
用戶端播放（同時繼續接收用戶輸入 → 全雙工）
```

---

**文件結束**。

對應 PDF / 完整 PPT 版本可由投資人/合作方瀏覽 PPT 1 號 (01-pitch-complete.html) 取得。
