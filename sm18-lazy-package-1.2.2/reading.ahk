#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
; #Warn  ; Enable warnings to assist with detecting common errors.
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.

; ^r::
;     Reload
; Return

#IfWinActive, ahk_exe msedge.exe
^c::
    Send, ^c
    Run, formatReadingMetrial.pyw
Return

#IfWinActive, ahk_exe POWERPNT.EXE
^c::
    Send, ^c
    Run, removeFormat.pyw
Return

; #IfWinActive, ahk_exe sm18.exe
; ^v::
;     Send ^v
;     clipboard := ""
; Return