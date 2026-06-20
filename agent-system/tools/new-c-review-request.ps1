param(
  [Parameter(Mandatory = $true)]
  [string]$ActionId,

  [Parameter(ValueFromRemainingArguments = $true)]
  [string[]]$RemainingArgs
)

$ErrorActionPreference = "Stop"

Write-Warning "agent-system/tools/new-c-review-request.ps1 is deprecated. Use agent-system/tools/draft-c-review-request.ps1. This alias creates drafts/audit records only and does not contact C."

$script = Join-Path $PSScriptRoot "draft-c-review-request.ps1"
& $script -ActionId $ActionId @RemainingArgs
