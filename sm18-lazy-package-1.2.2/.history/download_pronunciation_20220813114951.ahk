﻿#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
; #Warn  ; Enable warnings to assist with detecting common errors.
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.

!x::
    Begin:
    CoordMode, Mouse, Screen
    Send, {F9}
    WinWaitActive, ahk_exe Code.exe
    Clipboard := ""
    while 1{
        Send, ^a^c
        ClipWait, 2
        If ErrorLevel{
            Continue
        }
        Else{
            Break
        }
    }
    Run getword.pyw
    Send, ^w
    Sleep, 300
    Send, !{Esc}
    Click, 420 40
    Click, 440 230 0
    Sleep, 100
    Send, d
    Sleep, 300
    Click, 660 250
    Send, ^q
    WinWaitActive, Sound files, 2
    If ErrorLevel{
        Return
    }
    
Return