#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
; #Warn  ; Enable warnings to assist with detecting common errors.
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.

    While, 1{
        PixelGetColor, color1, 1900, 888 , RGB
        PixelGetColor, color2, 1900, 1500 , RGB
        If (color1=="0x263238" and color2=="0x263238"){
            Click, 300 1600
            Sleep 1000
        }
        Sleep, 1000
    }