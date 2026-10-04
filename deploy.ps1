# ============================================================
#  AI 家具銷售平台 — 一鍵部署到 GitHub Pages
# ============================================================
#  用法：
#  1. 在 https://github.com/new 建立一個 public repo（名稱 e.g. zhijia-pitch）
#  2. 在 PowerShell 中執行此腳本：
#     .\deploy.ps1 -GitHubUser "你的帳號" -RepoName "zhijia-pitch"
#  3. 跑完去 GitHub repo Settings → Pages → 啟用 main branch
# ============================================================

param(
    [Parameter(Mandatory=$true)]
    [string]$GitHubUser,

    [Parameter(Mandatory=$false)]
    [string]$RepoName = "zhijia-pitch",

    [Parameter(Mandatory=$false)]
    [string]$CommitMessage = "Deploy: AI furniture pitch deck"
)

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host "=== AI 家具銷售平台 — GitHub Pages 部署 ===" -ForegroundColor Cyan
Write-Host "Source: $ScriptDir"
Write-Host "Target: https://github.com/$GitHubUser/$RepoName"
Write-Host ""

# 1. 檢查 git
Write-Host "[1/5] Check git..." -ForegroundColor Yellow
$git = Get-Command git -ErrorAction SilentlyContinue
if (-not $git) {
    Write-Host "❌ git not found. Install from https://git-scm.com/download/win" -ForegroundColor Red
    exit 1
}
Write-Host "  ✅ git $($git.Version)" -ForegroundColor Green

# 2. 檢查必要檔案
Write-Host "`n[2/5] Check files..." -ForegroundColor Yellow
$requiredFiles = @(
    "01-pitch-complete.html",
    "02-customer-acquisition.md",
    "03-deploy-guide.md",
    "04-tech-architecture.md",
    "README.md"
)
$missing = @()
foreach ($f in $requiredFiles) {
    if (-not (Test-Path "$ScriptDir\$f")) {
        $missing += $f
    }
}
if ($missing.Count -gt 0) {
    Write-Host "  ❌ Missing files: $($missing -join ', ')" -ForegroundColor Red
    exit 1
}
Write-Host "  ✅ All $($requiredFiles.Count) files present" -ForegroundColor Green

# 3. 初始化 git（如果還沒有）
Write-Host "`n[3/5] Init git..." -ForegroundColor Yellow
Push-Location $ScriptDir
if (-not (Test-Path ".git")) {
    git init | Out-Null
    Write-Host "  ✅ git init"
} else {
    Write-Host "  ⏭ Already a git repo"
}

# 4. Commit
Write-Host "`n[4/5] Commit..." -ForegroundColor Yellow
git add .
$status = git status --short
if ($status) {
    git commit -m $CommitMessage
    Write-Host "  ✅ Committed"
} else {
    Write-Host "  ⏭ Nothing to commit (already up to date)"
}

# 5. Push
Write-Host "`n[5/5] Push to GitHub..." -ForegroundColor Yellow
$remoteUrl = "https://github.com/$GitHubUser/$RepoName.git"

# 檢查 remote 是否存在
$existingRemote = git remote get-url origin 2>$null
if ($existingRemote -ne $remoteUrl) {
    if ($existingRemote) {
        git remote set-url origin $remoteUrl
    } else {
        git remote add origin $remoteUrl
    }
}

# 確認 branch 是 main
$currentBranch = git branch --show-current
if ($currentBranch -ne "main") {
    git branch -M main
}

# Push（會問 username/password 或 token）
try {
    git push -u origin main
    Write-Host "  ✅ Pushed to origin/main" -ForegroundColor Green
} catch {
    Write-Host "  ❌ Push failed: $_" -ForegroundColor Red
    Write-Host "`n請確認：" -ForegroundColor Yellow
    Write-Host "  1. 你已經在 https://github.com/new 建立 repo: $RepoName (要 public)"
    Write-Host "  2. 你的 GitHub 帳號是: $GitHubUser"
    Write-Host "  3. 如果用 2FA，要用 Personal Access Token (https://github.com/settings/tokens)"
    Pop-Location
    exit 1
}

Pop-Location

# 6. 完成
Write-Host "`n=== ✅ 部署完成 ===" -ForegroundColor Green
Write-Host ""
Write-Host "下一步：" -ForegroundColor Cyan
Write-Host "  1. 開啟 https://github.com/$GitHubUser/$RepoName"
Write-Host "  2. 點 Settings → Pages"
Write-Host "  3. Source 選 'Deploy from a branch'"
Write-Host "  4. Branch 選 main / (root)"
Write-Host "  5. 點 Save"
Write-Host ""
Write-Host "  等待 1-2 分鐘，你的 deck 就會上線：" -ForegroundColor Cyan
Write-Host "  → https://$GitHubUser.github.io/$RepoName/" -ForegroundColor Yellow
Write-Host ""
Write-Host "  PPT 入口檔：01-pitch-complete.html"
Write-Host "  完整連結：https://$GitHubUser.github.io/$RepoName/01-pitch-complete.html" -ForegroundColor Yellow
