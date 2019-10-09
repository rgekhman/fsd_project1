# PowerShell Kill Process
#Clear-Host

try
{    
    $A = Get-Process Microsoft.PythonTools.Analyzer 
    Write-Host $A #| Get-Process | Format-Table -View ProcessName
    stop-process -name Microsoft.PythonTools.Analyzer
    $A = Get-Process Microsoft.PythonTools.Analyzer
    Write-Host $A #| Get-Process | Format-Table -View ProcessName
    ##$A | Get-Process | Format-Table -View ProcessNam

    #$A = Get-Process ServiceHub.Host.CLR*
    #$A | Get-Process | Format-Table -View ProcessName
    #stop-process -name ServiceHub.Host.CLR.x86*
    #$A = Get-Process ServiceHub.Host.CLR.x86*
    #$A | Get-Process | Format-Table -View ProcessNam
}
Catch
{
    $ErrorMessage = $_.Exception.Message
    Write-Host $ErrorMessage 
}

