#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
; #Warn  ; Enable warnings to assist with detecting common errors.
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.
#Include WinClipAPI.ahk
#Include WinClip.ahk

^r::
    Send {Click}lu
return

;field
::/f::
    WinClip.SetHTML("<SPAN class=field>组胚</SPAN> ")
    ;Send {ctrl down}v{ctrl up}{left}{ShiftDown}{left 5}{ShiftUp}组胚{Right}
Return

; ^w::
;     RunWait, rich_clipboard.pyw "<SUP>sup</SUP> "
;     Send ^v{left}{ShiftDown}{left 3}{ShiftUp}
; Return

;新建卡
#IfWinActive, ahk_exe code.exe
!a::
    Send ^{End}
    Send {Text}Q: <SPAN class=field>翻译</SPAN>
    Send {Space}
    Send {Text}<BR><DIV class=footer><BR>------------------<BR>&nbsp;&nbsp;&nbsp; Character:1<BR>&nbsp;&nbsp;&nbsp; Date:2022/9/14</DIV>
    Send {Space}{Enter}
    ;如果有开自动补全就会多个tab
    ;Send {BackSpace}
    Send {Text}A:
    Send {Space}{Enter}
    Send {Text}<hr>
    Send {Enter 2}{Up 4}{Right 31}
Return

; 从Q区切换到A区
#IfWinActive, ● new.htm - Visual Studio Code
Tab::
    Send {Down}{End}
Return