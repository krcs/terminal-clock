#!/usr/bin/pwsh

param(
    [Parameter(mandatory=$true)]
    [string]$font,
    [Parameter()]
    [int]$margin = 0
)

if (-not (Test-Path $font)) {
    write-host -Foreground RED "Font not found."
    exit
}

if ($margin -lt 0) {
    $margin = 0
}

function get_size($content) {
    $font_width = 0
    $font_height = 0

    $height = 0
    $margin = 0

    foreach ($line in $content) {
        if ($line.Length -eq 0) {
            if ($height -gt 0) {
                $font_height = $height
            }
            $height = 0
            continue
        }

        if ($line.Length -gt $font_width) {
            $font_width = $line.Length
        }

        $height += 1

        $line | ? { $_ -match "^\s*" } | % {
            $slen = $matches[0].Length
            if ($margin -eq 0) {
                $margin = $slen
            } elseif ($slen -lt $margin) {
                $margin = $slen
            }
        }
    }
    return @{
        width = ($font_width - $margin)
        height = $font_height
    }
}

function get_chars($content, $font_size) {
    $result = @()
    $char = @()

    foreach ($line in $content) {
        if ($line.Length -eq 0) {
            if ($char.Length -gt 0) {
                $result += ,$char
            }
            $char = @()
            continue
        }
        $char += $line.Substring($line.Length - $font_size.width)
    }
    if ($char.Length -gt 0) {
        $result += ,$char
    }
    return $result
}

$content = get-content $font
$font_size = get_size $content
$chars = get_chars $content $font_size

$win_width = (7 * ($font_size.width + $margin)) + $font_size.width
$win_height = $font_size.height

$wx = [int](([console]::LargestWindowWidth-$win_width) / 2)
$wy = [int](([console]::LargestWindowHeight-$win_height) / 2)

$posx = $wx
$xoffset = $font_size.width + $margin

[console]::CursorVisible = $false
while ($true) {
    if ([console]::KeyAvailable) {
        [console]::ReadKey("NoEcho,IncludeKeyDown") | Out-Null
        break
    }
    if ([console]::LargestWindowWidth -lt $wx + $win_width) {
        Clear-Host
        break
    }
    $posx = $wx
    (Get-Date -UFormat "%H:%M:%S")[0..9] | % {
        $idx = $chars.Length - 1
        if ($_ -ne ":") {
            $idx = [int]"$_"
        }
        0..($font_size.height - 1) | % {
            [console]::SetCursorPosition($posx - 1, $wy + $_ - 1)
            $chars[$idx][$_]
        }
        $posx += $xoffset
    }
    Start-Sleep -Seconds 1
}
[console]::CursorVisible = $true

Clear-Host
