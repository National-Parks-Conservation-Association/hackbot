# Configuration
$script1Path = "C:\Users\jhaybok\OneDrive - National Parks Conservation Association\Documents\Github\hackbot\mfa_cronjob_open_window.py"
$script2Path = "C:\Users\jhaybok\OneDrive - National Parks Conservation Association\Documents\Github\dop_upload_files\dop_upload_file_mover.py"
$venv1Path = "C:\Users\jhaybok\OneDrive - National Parks Conservation Association\Documents\Github\hackbot\hackbot"  # Path to first virtual environment
$venv2Path = "C:\Users\jhaybok\OneDrive - National Parks Conservation Association\Documents\Github\dop_upload_files\dop-mover"  # Path to second virtual environment
$logPath = "C:\Users\jhaybok\National Parks Conservation Association\Data Vault - General\hackbot_data_vault\ScriptLogs\python_task_log.txt"

# Create log directory
$logDir = Split-Path -Path $logPath -Parent
if (-not (Test-Path -Path $logDir)) {
    New-Item -ItemType Directory -Path $logDir -Force
}

# Write to log
function Write-Log {
    param($Message)
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    "$timestamp - $Message" | Out-File -FilePath $logPath -Append
    Write-Host $Message
}

try {
    Write-Log "=== Task Started ==="
    
    # Run first script
    Set-Location -Path (Split-Path -Parent $script1Path)
    Write-Log "Activating first virtual environment"
    . "$venv1Path\Scripts\activate.ps1"
    Write-Log "Running first script..."
    $output = & python $script1Path 2>&1
    Write-Log $output
    deactivate
    
    if ($LASTEXITCODE -eq 0) {
        # Run second script
        Set-Location -Path (Split-Path -Parent $script2Path)
        Write-Log "Activating second virtual environment"
        . "$venv2Path\Scripts\activate.ps1"
        Write-Log "Running second script..."
        $output = & python $script2Path 2>&1
        Write-Log $output
        deactivate
        
        if ($LASTEXITCODE -eq 0) {
            Write-Log "All scripts completed successfully"
        } else {
            Write-Log "Second script failed"
            exit 1
        }
    } else {
        Write-Log "First script failed"
        exit 1
    }
} catch {
    Write-Log "Error occurred: $_"
    Write-Log $_.ScriptStackTrace
    exit 1
} finally {
    Write-Log "=== Task Completed ==="
}