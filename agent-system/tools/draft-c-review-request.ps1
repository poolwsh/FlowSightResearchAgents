param(
  [Parameter(Mandatory = $true)]
  [string]$ActionId,

  [string]$CorrelationId = "",
  [string]$MessageType = "c_review_request",
  [string]$ReviewType = "",
  [string]$SourceSessionName = "r",
  [string]$SourceThreadId = "",
  [string]$SourceCwd = "",
  [string]$TargetSessionName = "c",
  [string]$TargetThreadId = "",
  [string]$TargetThreadTitle = "",
  [string]$TargetThreadCwd = "",
  [string]$TargetThreadStatus = "",
  [string]$TargetRoleExpected = "Codex review lane / C",
  [string]$DeliveryStatus = "draft_only_not_sent",
  [string]$SendToolUsed = "",
  [string]$SendResultThreadId = "",
  [string]$SentAt = "",
  [string]$FallbackOutboxPath = "",
  [string]$OwnerAuthorization = "missing",
  [string[]]$ChangedPaths = @(),
  [string]$Summary = "",
  [string]$WhyThisLayer = "",
  [string[]]$Evidence = @(),
  [string]$RisksOrOpenQuestions = "",
  [string]$RequestedCodexReview = "",
  [string]$NextStepRProposes = "",
  [string]$OutputPath = ""
)

$ErrorActionPreference = "Stop"

function Convert-ToBulletList {
  param([string[]]$Items)
  if ($null -eq $Items -or $Items.Count -eq 0) {
    return "- none"
  }
  $normalized = @()
  foreach ($item in $Items) {
    if ($null -eq $item) {
      continue
    }
    foreach ($part in ($item -split ',')) {
      $trimmed = $part.Trim()
      if (-not [string]::IsNullOrWhiteSpace($trimmed)) {
        $normalized += $trimmed
      }
    }
  }
  if ($normalized.Count -eq 0) {
    return "- none"
  }
  return (($normalized | ForEach-Object { "- $($_)" }) -join "`n")
}

$safeId = ($ActionId -replace '[^A-Za-z0-9._-]', '-').Trim('-')
if ([string]::IsNullOrWhiteSpace($safeId)) {
  throw "ActionId must contain at least one safe filename character."
}

if ([string]::IsNullOrWhiteSpace($CorrelationId)) {
  $CorrelationId = $ActionId
}

if ([string]::IsNullOrWhiteSpace($OutputPath)) {
  $OutputPath = Join-Path "agent-system\reviews\outbox" "$safeId.md"
}

if ([string]::IsNullOrWhiteSpace($FallbackOutboxPath)) {
  $FallbackOutboxPath = $OutputPath
}

$parent = Split-Path -Parent $OutputPath
if (-not [string]::IsNullOrWhiteSpace($parent)) {
  New-Item -ItemType Directory -Force -Path $parent | Out-Null
}

$changedPathsText = Convert-ToBulletList -Items $ChangedPaths
$evidenceText = Convert-ToBulletList -Items $Evidence
$createdAt = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")
$fence = '```'

$content = @"
# C Review Request: $ActionId

${fence}text
R_REVIEW_FOR_C
action_id: $ActionId
correlation_id: $CorrelationId
message_type: $MessageType
review_type: $ReviewType
source_session_name: $SourceSessionName
source_thread_id: $SourceThreadId
source_cwd: $SourceCwd
target_session_name: $TargetSessionName
target_thread_id: $TargetThreadId
target_thread_title: $TargetThreadTitle
target_thread_cwd: $TargetThreadCwd
target_thread_status: $TargetThreadStatus
target_role_expected: $TargetRoleExpected
delivery_status: $DeliveryStatus
send_tool_used: $SendToolUsed
send_result_thread_id: $SendResultThreadId
sent_at: $SentAt
fallback_outbox_path: $FallbackOutboxPath
owner_authorization: $OwnerAuthorization
changed_paths:
$changedPathsText
summary: $Summary
why_this_layer: $WhyThisLayer
evidence:
$evidenceText
risks_or_open_questions: $RisksOrOpenQuestions
requested_codex_review: $RequestedCodexReview
next_step_r_proposes: $NextStepRProposes
$fence

created_at_utc: $createdAt

## Boundary

This is a ResearchAgents-side review request draft/audit record for C/Codex. It
is not C approval, not proof of delivery unless `delivery_status: sent` is
backed by Codex thread-tool evidence, not a FlowSight app edit request by
itself, not verifier/release/dispatcher authorization, not a research packet,
and not a money-edge, can-trade, or Product GO claim.
"@

Set-Content -LiteralPath $OutputPath -Value $content -Encoding UTF8

Write-Output "wrote: $OutputPath"
