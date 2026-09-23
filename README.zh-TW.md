# Nomily

> **錄音裝置 → Nomily → 你的 API Key → 你的 AI**

<p align="center">
  <img src="media/nomily-workflow-banner.png" width="100%" alt="Nomily BYOK 語音錄製流程：從錄音裝置到轉錄、摘要與 AI 服務商">
</p>

<p align="center">
  <a href="https://github.com/Nomily-Ai/nomily-ios"><img src="https://img.shields.io/badge/iOS%20%2B%20Apple%20Watch-SwiftUI-111318?style=for-the-badge&logo=swift&logoColor=white" alt="iOS 與 Apple Watch 用戶端"></a>
  <a href="https://github.com/Nomily-Ai/nomily-android"><img src="https://img.shields.io/badge/Android-Jetpack%20Compose-3DDC84?style=for-the-badge&logo=android&logoColor=white" alt="Android 用戶端"></a>
  <a href="https://geekis.com"><img src="https://img.shields.io/badge/BYOK-Your%20Key%20Your%20AI-E4002B?style=for-the-badge" alt="自帶金鑰"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-Source--available-4B5563?style=for-the-badge" alt="原始碼可用授權"></a>
</p>

<p align="center">
  <a href="README.md">English</a> · <a href="README.zh-CN.md">简体中文</a> · <a href="README.zh-TW.md">繁體中文</a>
</p>

**面向 V05E、Apple Watch 與 iPhone 匯入音訊的 BYOK 錄音夥伴：支援 ASR 轉錄、說話者分離、AI 摘要與本機 ASR 端點。**

Nomily 將錄音帶入原生用戶端，使用你設定的服務商轉錄，並透過你選擇的 AI 服務商產生摘要。

這是專案入口儲存庫；可執行的原生用戶端位於
[`nomily-ios`](https://github.com/Nomily-Ai/nomily-ios) 與
[`nomily-android`](https://github.com/Nomily-Ai/nomily-android)。

## 快速連結

| 🌐 線上展示 | 🎥 示範影片 | 𝕏 動態 | 📚 文件 |
|---|---|---|---|
| [體驗固定範例預覽](https://geekis.com/demo/) | [Nomily YouTube Shorts](https://www.youtube.com/@Nomily-Ai/shorts) | [@nomilyai](https://x.com/nomilyai) | [Geekis.com](https://geekis.com) |

## Nomily 是什麼？

Nomily 不是託管式轉錄帳戶或共用錄音雲端，而是面向錄音與使用者自選 AI 服務的原生配套流程。轉錄與摘要服務商由使用者選擇。

公開儲存庫提供原始碼審閱與本機建置。原始碼提交並不代表應用程式商店可用、裝置/韌體相容，或生產服務已發布。

## 目前可以做什麼

- 連線 V05E BLE 錄音器流程、下載錄音並管理本機錄音庫。
- 在 iPhone 匯入錄音，包括 Apple Watch 夥伴傳回的錄音。
- 透過 Azure Speech 或由使用者營運的 local faster-whisper-compatible ASR 端點轉錄即時或已錄製音訊；Azure 轉錄支援最多 10 位說話者分離。
- 透過已設定的 LLM 服務商產生摘要、標題和翻譯：OpenAI、Anthropic、Gemini、OpenRouter、Ollama 或自訂 OpenAI-compatible endpoint。
- 提供原生 iOS / Apple Watch 與 Android 實作，而非跨平台包裝。

## 隱私與服務商界線

Nomily 不是託管轉錄帳戶或共用錄音雲端。API Key 由使用者提供，絕不可提交至儲存庫。請勿在 Issue 或 Pull Request 中提交錄音、轉錄文字、裝置識別、日誌、產生的設定或存取憑證。

| 服務層 | 已設定流程中傳送的資料 | 由誰提供 |
|---|---|---|
| Nomily 用戶端 | 用戶端上的錄音庫、傳輸狀態與產生檔案 | 由你安裝並執行用戶端。 |
| Azure Speech | 選擇 Azure 時用於轉錄的音訊 | 你的 Azure 帳戶與 Key。 |
| 本機 ASR 端點 | 選擇本機端點時用於轉錄的音訊 | 由你執行該端點。 |
| LLM 服務商 | 用於摘要、標題或翻譯所需的轉錄文字 | 你選擇的服務商、模型、端點與 Key。 |

公開儲存庫不包含共用 Nomily 雲端、內建服務商帳戶或完整自託管同步堆疊。本機 ASR 與 Ollama 是服務商整合，不代表整個產品均可自託管。

## 工作流程

```text
V05E 錄音器 / Apple Watch / iPhone 匯入音訊
                  │
                  ▼
          Nomily 原生用戶端
   本機錄音庫 · 傳輸 · 播放
                  │
        ┌─────────┴──────────┐
        ▼                    ▼
Azure Speech 或         你的 LLM 服務商
本機 ASR 端點            摘要 · 標題 · 翻譯
選擇 Azure 時支援         OpenAI · Anthropic · Gemini
說話者分離                OpenRouter · Ollama · 相容端點
        │                    │
        └─────────┬──────────┘
                  ▼
             轉錄文字與摘要
```

## 錄音輸入支援

| 輸入來源 | 目前原始碼狀態 | 說明 |
|---|---|---|
| V05E 錄音器 | 兩個用戶端均已實作 | 主要 BLE 錄音輸入；相容性仍取決於實際測試裝置和韌體。 |
| iPhone 匯入音訊 | `nomily-ios` 已實作 | iPhone 是匯入、管理、轉錄與摘要用戶端。 |
| Apple Watch 麥克風 | `nomily-ios` 已實作 | 已配對的 Watch 夥伴將錄音傳回 iPhone。 |
| 其他錄音器型號 | 未承諾 | 可以錄音不等於已被支援。 |
| Android Watch 夥伴 | 未發布 | 不應從 Android App 原始碼推斷 Wear OS 用戶端。 |

## Apple Watch 夥伴

在已配對 iPhone 安裝 Nomily AI 後，依以下方式安裝 Watch 夥伴：

1. 開啟 iPhone 的 **Watch** App，並捲動到 **可用 App**。
2. 找到 **Nomily AI**，點擊 **安裝**。
3. 在 iPhone 的 Nomily AI 內開啟 **Settings → Apple Watch**，確認顯示 **Installed**。
4. 未攜帶 V05E 時，在 Apple Watch 開啟 Nomily AI 錄音；錄音會同步回 iPhone 的 Nomily AI，用於轉錄、整理和摘要。

| 從 Watch App 安裝 | 在 Nomily 設定中確認 | 在 Apple Watch 錄音 |
|---|---|---|
| <img src="media/apple-watch-install-nomily-ai.png" alt="iPhone Watch App 中 Nomily AI 的安裝按鈕" width="250"> | <img src="media/apple-watch-settings.png" alt="Nomily AI 設定顯示 Apple Watch 已安裝" width="250"> | <img src="media/apple-watch-recording.png" alt="Nomily AI 在 Apple Watch 上準備錄音" width="250"> |

### 計畫中或未發布

| 項目 | 狀態 |
|---|---|
| 其他錄音器型號與協定 | 僅在相關韌體完成測試後才會確認相容性。 |
| Android Watch 夥伴 | 未發布。 |
| RAG、MCP、共用自託管同步 | 目前公開用戶端原始碼未呈現，尚非已宣布能力。 |
| 無需 Key 的線上展示 | 計畫在公開網站提供；暫時入口為 [Geekis.com](https://geekis.com)。 |

## 儲存庫關係

| 儲存庫 | 角色 | 關係 |
|---|---|---|
| **nomily-app** | 專案入口、跨專案文件、授權與預覽素材 | 從這裡開始；本儲存庫本身不包含可安裝用戶端。 |
| [`nomily-ios`](https://github.com/Nomily-Ai/nomily-ios) | iPhone 與 Apple Watch 的 SwiftUI 用戶端 | 有獨立原生專案、建置說明與 Issue 追蹤。 |
| [`nomily-android`](https://github.com/Nomily-Ai/nomily-android) | Android Kotlin / Jetpack Compose 用戶端 | 有獨立原生專案、建置說明與 Issue 追蹤。 |
| `nomily-site` | 私有靜態網站部署原始碼 | 承載設定和展示材料；不是行動用戶端原始碼儲存庫。 |

## 建置與專案結構

用戶端共享產品概念與協定預期，但屬於獨立的原生實作。選擇建置路徑前，請先閱讀對應儲存庫：

```text
nomily-app/       專案說明、授權、公開預覽素材
nomily-ios/       iOS App、Watch 夥伴、BLE / ASR / 本機錄音庫模組
nomily-android/   Android App，以及協定、加密、音訊、ASR、LLM 核心模組
nomily-site/      私有靜態部署原始碼，用於指南與展示
```

| 目標 | 從這裡開始 |
|---|---|
| 建置 iPhone 或 Apple Watch | [`nomily-ios`](https://github.com/Nomily-Ai/nomily-ios)：macOS、Xcode 15+ 與實體 iPhone；Apple Watch 可選。 |
| 建置 Android | [`nomily-android`](https://github.com/Nomily-Ai/nomily-android)：JDK 21、Android Studio 或 Gradle 與實體 Android 手機。 |
| 回報缺陷 | 在受影響的原生用戶端儲存庫建立 Issue，並提供去識別化的重現步驟。 |
| 查看條款 | 閱讀 [Nomily Small Team License](LICENSE)。 |

## App 預覽

| 錄音庫 | 轉錄服務商 | 用於摘要的 LLM 服務商 |
|---|---|---|
| <img src="media/app-recordings.png" alt="Nomily 錄音庫" width="200"> | <img src="media/app-asr-providers.png" alt="Nomily 轉錄服務商設定" width="200"> | <img src="media/app-llm-providers.png" alt="Nomily LLM 服務商和模型選擇" width="200"> |

截圖使用合成或非敏感預覽資料。重複使用產品圖片或品牌素材前請查看 [`media/README.md`](media/README.md)。

## 授權

原始碼使用 [Nomily Small Team License 1.0.0](LICENSE)。個人使用以及 10 人及以下團隊可使用；更大團隊需要另行取得付費授權。商業授權請聯絡 <nomily@geekis.com>。這是一份原始碼可用授權，並非 OSI 批准的開源授權。

[`media/`](media/) 中的品牌素材不包含在該授權內，詳見 [`media/README.md`](media/README.md)。

## Star 歷史

[![Star History Chart](https://api.star-history.com/svg?repos=Nomily-Ai/nomily-app&type=date&legend=top-left)](https://www.star-history.com/#Nomily-Ai/nomily-app&type=date&legend=top-left)
