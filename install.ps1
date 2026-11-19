# Installer Otomatis Unila Academic & Research Skills (Windows PowerShell)
$ErrorActionPreference = "Stop"

$RepoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$SkillsSource = Join-Path $RepoRoot "skills"
$SkillNames = @("panduan-kti-unila", "riset-dan-sidang-ilmiah")

$TargetRoots = @(
    (Join-Path $HOME ".gemini\config\skills"),
    (Join-Path $HOME ".gemini\antigravity\skills"),
    (Join-Path $HOME ".gemini\skills"),
    (Join-Path $HOME ".agents\skills"),
    (Join-Path $HOME ".claude\skills")
)

foreach ($root in $TargetRoots) {
    New-Item -ItemType Directory -Force -Path $root | Out-Null
    foreach ($name in $SkillNames) {
        $src = Join-Path $SkillsSource $name
        $dst = Join-Path $root $name
        if (Test-Path $dst) { Remove-Item -Path $dst -Recurse -Force }
        Copy-Item -Path $src -Destination $dst -Recurse -Force
        Write-Host "[OK] Terpasang: $dst" -ForegroundColor Green
    }
}

Write-Host "`nSeluruh skill berhasil dipasang! Silakan mulai ulang sesi chat AI Agent Anda." -ForegroundColor Cyan
