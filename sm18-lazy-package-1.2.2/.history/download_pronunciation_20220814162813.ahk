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
    Sleep, 100
    Click, 420 40
    Click, 440 230 0
    Sleep, 100
    Send, d
    Sleep, 300
    MouseClickDrag, L, 780, 180, 780, 355
    Send, ^q
    Sleep, 200
    if WinActive("Error!"){
        Send, {Enter 2}
    }
    WinWaitActive, Sound files, ,2
    If ErrorLevel{
        Return
    }
    CoordMode, Mouse, Window
    Send, {Tab 4}F:\Desktop\SuperMemo_17_18破解版_17直接解压_18安装后把key粘贴上去后unlock就好\sm18-lazy-package-1.2.2\CET4\pronunciation\%Clipboard%\{Tab 2}{Enter}
    Sleep, 500
    If WinActive("Error!"){
        Send, {Enter 2}
        Sleep, 100
        Send, {Click 320 100 R}r{Right}{BackSpace 3}wav{Enter}
        Run %A_ScriptDir%\CET4\download_pronunciation.pyw
        Sleep, 100
        Click 300 100
    }
    Click 700 520
    Sleep, 200
    Send, ^v{Enter 2}
    CoordMode, Mouse, Screen
    Sleep, 100
    Send {Click 780 360 R}zqo
Return

+!x::
    While, 1{
        If (WinActive(ahk_exe sm18.exe))
        Else{
            Return
        }
        CoordMode, Mouse, Screen
        Click 0 0
        Send {Down}
        Click 500 0
        Begin1:
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
        Sleep, 100
        Click, 420 40
        Click, 440 230 0
        Sleep, 100
        Send, d
        Sleep, 300
        MouseClickDrag, L, 780, 180, 780, 355
        Send, ^q
        Sleep, 200
        if WinActive("Error!"){
            Send, {Enter 2}
        }
        WinWaitActive, Sound files, ,2
        If ErrorLevel{
            Return
        }
        CoordMode, Mouse, Window
        Send, {Tab 4}F:\Desktop\SuperMemo_17_18破解版_17直接解压_18安装后把key粘贴上去后unlock就好\sm18-lazy-package-1.2.2\CET4\pronunciation\%Clipboard%\{Tab 2}{Enter}
        Sleep, 500
        If WinActive("Error!"){
            Send, {Enter 2}
            Sleep, 100
            Send, {Click 320 100 R}r{Right}{BackSpace 3}wav{Enter}
            Run %A_ScriptDir%\CET4\download_pronunciation.pyw
            Sleep, 100
            Click 300 100
        }
        Click 700 520
        Sleep, 200
        Send, ^v{Enter 2}
        CoordMode, Mouse, Screen
        Sleep, 100
        Send {Click 780 360 R}zqo
    }
Return