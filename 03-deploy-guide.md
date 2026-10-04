# 智家 AI PPT — GitHub Pages 5 分鐘部署教學

> 目標：把 `furniture-ai-complete-deck.html` 變成 `https://你的帳號.github.io/zhijia-pitch/`，永久可分享
> 時間：5-10 分鐘
> 費用：0 元
> 結果：投資人打開連結就能看完整 26 頁 deck

---

## 為什麼選 GitHub Pages？

| 優點 | 細節 |
|---|---|
| **免費** | GitHub 免費帳號即可用 |
| **永久連結** | `username.github.io/repo-name/`，不過期 |
| **HTTPS** | 內建，投資人放心點 |
| **0 維運** | push 程式碼就更新，不用管 server |
| **可下載 PDF** | 任何瀏覽器開啟後 `Ctrl+P → 存 PDF` |
| **私人控制** | 可隨時改成 Private repo（要 GitHub Pro 才能用 Pages）|

---

## 前置準備（5 分鐘內可完成）

### 你需要的東西

| 項目 | 檢查 |
|---|---|
| ✅ GitHub 帳號 | 沒有 → https://github.com/signup 申請 |
| ✅ Git 安裝 | Windows 通常有；沒裝 → https://git-scm.com/download/win |
| ✅ PPT HTML 檔 | `G:\OpenClaw_Data\.openclaw\workspace\agents\dev-tech\out\furniture-ai-complete-deck.html` |

---

## 方案 A — 用 `git` 命令列（最簡單，5 分鐘）

### Step 1：建立 GitHub repo

1. 登入 GitHub
2. 右上角 `+` → `New repository`
3. 填寫：
   - **Repository name**：`zhijia-pitch`（隨意）
   - **Public**（必選，GitHub Pages 免費版要 public）
   - ✅ Add a README file
4. 點 `Create repository`

你會看到一個空 repo，網址像：
```
https://github.com/你的帳號/zhijia-pitch
```

### Step 2：本地建立資料夾並推上去

打開 PowerShell 或 CMD，執行：

```powershell
# 切到工作目錄
cd "G:\OpenClaw_Data\.openclaw\workspace\agents\dev-tech\out"

# 建立子資料夾
mkdir zhijia-pitch
cd zhijia-pitch

# 複製 PPT 進來並改名 index.html（重要！必須叫 index.html）
copy ..\furniture-ai-complete-deck.html .\index.html

# 初始化 git
git init
git add .
git commit -m "Add investor pitch deck"

# 連接到你的 GitHub repo（替換 YOUR_USERNAME）
git remote add origin https://github.com/YOUR_USERNAME/zhijia-pitch.git
git branch -M main
git push -u origin main
```

### Step 3：開啟 GitHub Pages

1. 回到 GitHub repo 頁面
2. 點 `Settings`（右上）
3. 左邊選 `Pages`
4. Source 選 `Deploy from a branch`
5. Branch 選 `main` / 資料夾 `/ (root)`
6. 點 `Save`

### Step 4：等待 1-2 分鐘，拿到永久連結

GitHub Pages 會自動 build。完成後頁面會顯示：

```
Your site is live at https://YOUR_USERNAME.github.io/zhijia-pitch/
```

把這個連結複製 → 傳給投資人 ✅

---

## 方案 B — 用 GitHub Desktop（圖形介面，更簡單）

適合不熟 git 命令列的用戶。

### Step 1：安裝 GitHub Desktop

下載：https://desktop.github.com/

### Step 2：登入並 Clone 你剛建的 repo

1. 開 GitHub Desktop
2. `File` → `Clone repository`
3. 選 `zhijia-pitch`
4. 選本地路徑（建議 `G:\OpenClaw_Data\.openclaw\workspace\agents\dev-tech\out\zhijia-pitch`）

### Step 3：複製 PPT 進資料夾

把 `furniture-ai-complete-deck.html` 複製到資料夾內，**改名 `index.html`**

### Step 4：Commit + Push

1. GitHub Desktop 會自動偵測新檔案
2. 左下角輸入 commit message：`Add investor pitch deck`
3. 點 `Commit to main`
4. 點右上 `Push origin`

### Step 5：開啟 GitHub Pages

同方案 A Step 3-4。

---

## 方案 C — 直接拖曳上傳（最簡，適合非工程師）

完全不用 git。

### Step 1：在 GitHub repo 頁面

1. 進到你剛建的 repo
2. 點 `Add file` → `Upload files`
3. 把 `furniture-ai-complete-deck.html` 拖進去
4. **檔名改成 `index.html`**（重要）
5. 點 `Commit changes`

### Step 2：開啟 GitHub Pages

同方案 A Step 3-4。

> ⚠️ 這個方式之後更新檔案比較麻煩，但首次上線最快。

---

## 進階：客製化網址（選配）

### 自訂網域（你已有網址）

1. 在你的 DNS 商（如 Cloudflare）加 CNAME 記錄：
   ```
   CNAME  www  YOUR_USERNAME.github.io
   ```
2. 在 repo 根目錄加 `CNAME` 檔，內容：
   ```
   pitch.zhijia-ai.com
   ```
3. Settings → Pages → Custom domain 填上

### 短網址（推薦給投資人）

| 服務 | 短網址範例 |
|---|---|
| **bit.ly** | `bit.ly/zhijia-pitch` |
| **rebrand.ly** | `rebrand.ly/zhijia-pitch` |
| **你的官網** | `zhijia-ai.com/pitch` |

投資人比較願意點短網址（看起來正式）。

---

## 客製化 deck（讓它更像品牌網站）

### 換顏色

打開 `index.html`，搜尋這行（CSS 變數）：

```css
:root {
  --c-primary: #1e40af;   /* 改成你的品牌色 */
  --c-accent: #f59e0b;    /* 改成輔色 */
}
```

### 換 Logo

在封面 slide 找：

```html
<h1>智家 AI 銷售員</h1>
```

改成：

```html
<h1><img src="logo.png" style="height:80px;"> 智家 AI 銷售員</h1>
```

把 `logo.png` 也放到同資料夾，git add + push。

### 加 Google Analytics（追蹤投資人是否打開）

在 `</head>` 前加：

```html
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'GA_MEASUREMENT_ID');
</script>
```

把 `GA_MEASUREMENT_ID` 換成你的 GA ID。

**好處**：知道哪個投資人看了、看幾頁、停留多久 → 跟進更有依據。

---

## 投資人分享 checklist

分享前確認這 5 件事：

- [ ] 連結打開後直接顯示封面（不要有 404 / build 失敗訊息）
- [ ] 方向鍵能翻頁（試試左右鍵）
- [ ] 按 `F` 能進入全螢幕
- [ ] 手機打開能看（Reveal.js 響應式設計）
- [ ] Google Analytics 有裝（追蹤）

## 分享時的話術

Email 主旨範例：

```
[智家 AI] 完整融資計劃書 — 26 頁含完整商業模式與獲客路線
```

Email 內文：

```
您好，

這是我們智家 AI 銷售員的完整融資計劃書（Seed Round ¥800 萬）：

🔗 https://YOUR_USERNAME.github.io/zhijia-pitch/

重點摘要：
- 萬億家具市場 + AI 全雙工對話 + AR 試擺
- 退貨率預期 < 15%（行業平均 30%）
- 6 月內 M4 飛輪啟動、M6 GMV ¥3,000 萬
- 已驗證技術：GPT-4o Realtime、Qwen2.5-VL、ARKit

期待您的回饋。

智家 AI 創辦人
```

---

## 疑難排解

| 問題 | 解法 |
|---|---|
| 連結 404 | 確認檔案叫 `index.html`、在 repo 根目錄 |
| 連結打開是空白 | 等待 2-3 分鐘（GitHub Pages build 需要時間）|
| 圖片顯示不出 | 確認圖片檔案也 push 上去 |
| Reveal.js 沒載入 | 投資人電腦沒網路 → 改用內嵌的 Reveal.js（見下方）|
| 想改成私有 repo | GitHub 免費版不支援，需升級 GitHub Pro 或用 Netlify |

### 內嵌 Reveal.js（離線可用）

把這些 CDN 連結改成內嵌下載：

```html
<!-- 把這些 CDN 改成下載到本地的相對路徑 -->
<link rel="stylesheet" href="reveal.css">
<script src="reveal.js"></script>
```

從 https://github.com/hakimel/reveal.js/releases 下載，解壓縮，把 `dist/` 資料夾的 `reveal.css` / `reveal.js` / 主題檔案複製到你的 repo。

---

## 方案 D — 用 Netlify Drop（最快，30 秒）

不用 git，純拖曳。

1. 打開 https://app.netlify.com/drop
2. 把整個 `zhijia-pitch` 資料夾拖進去
3. Netlify 自動給你 `xxx.netlify.app` 連結
4. 完成 ✅

**優點**：30 秒有連結，不需 GitHub 帳號
**缺點**：每次更新要重新拖

---

## 方案 E — 用 Vercel（中國訪問快）

1. 註冊：https://vercel.com
2. Import Git Repository → 選你的 GitHub repo
3. 一鍵部署
4. 拿到 `xxx.vercel.app` 連結

**優點**：CDN 全球加速，自動 HTTPS
**缺點**：中國訪問有時不穩（要綁定自訂網域才好）

---

## 三方案比較

| | GitHub Pages | Netlify Drop | Vercel |
|---|---|---|---|
| **速度** | 5 分鐘 | **30 秒** | 3 分鐘 |
| **永久連結** | ✅ | ⚠️ 可重命名 | ✅ |
| **中國訪問** | ⚠️ 慢/不穩 | ⚠️ 慢 | ✅ 快 |
| **HTTPS** | ✅ | ✅ | ✅ |
| **可綁網域** | ✅ | ✅ | ✅ |
| **推薦** | 工程師 | 緊急上線 | 中文市場 |

**建議**：
- 投資人在海外 → **GitHub Pages** 或 **Netlify**
- 投資人在中國 → **Vercel** + 自訂網域

---

## 下一步

部署完成後，給我你的公開連結，我可以幫你：
1. 驗證連結可以打開
2. 檢查所有 26 頁都能顯示
3. 提供 email / 微信分享文案

或要不要我幫你**自動化**（每次改 PPT 自動重新部署）？GitHub Actions 可以做到 push 後自動更新 Pages，不用手動操作。

---

## 5 分鐘快速指令碼（複製貼上）

把以下整段貼到 PowerShell（替換 `YOUR_USERNAME`）：

```powershell
cd "G:\OpenClaw_Data\.openclaw\workspace\agents\dev-tech\out"
mkdir zhijia-pitch
copy furniture-ai-complete-deck.html zhijia-pitch\index.html
cd zhijia-pitch
git init
git add .
git commit -m "Add investor pitch deck"
git remote add origin https://github.com/YOUR_USERNAME/zhijia-pitch.git
git branch -M main
git push -u origin main
Write-Host "✅ Done! Now go to GitHub repo Settings → Pages → Enable"
Write-Host "Then wait 1-2 min and visit: https://YOUR_USERNAME.github.io/zhijia-pitch/"
```

執行完成後照指示去 GitHub 點幾下就部署完成。

---

**文件結束**。總時間：5 分鐘（首次） / 1 分鐘（更新）。
