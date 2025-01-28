# Configuration
$executionScriptPath = "C:\Users\jhaybok\OneDrive - National Parks Conservation Association\Documents\Github\hackbot\run_python_scripts.ps1"
$taskName = "DailyROIDownloadAndMover"
$taskTime = "4:15AM"

# Create the scheduled task
try {
    # Create the action to run the script
    $action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-NoProfile -ExecutionPolicy Bypass -File `"$executionScriptPath`""
    
    # Create the daily trigger
    $trigger = New-ScheduledTaskTrigger -Daily -At $taskTime
    
    # Create settings
    $settings = New-ScheduledTaskSettingsSet -WakeToRun -ExecutionTimeLimit (New-TimeSpan -Hours 2)
    
    # Remove existing task if it exists
    $existingTask = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue
    if ($existingTask) {
        Unregister-ScheduledTask -TaskName $taskName -Confirm:$false
    }
    
    # Register the task
    Register-ScheduledTask -TaskName $taskName `
        -Action $action `
        -Trigger $trigger `
        -Settings $settings `
        -RunLevel Highest
    
    Write-Host "Task created successfully!"
    Write-Host "To test the task, run: Start-ScheduledTask -TaskName `"$taskName`""
} catch {
    Write-Host "Failed to create task: $_"
    throw
}