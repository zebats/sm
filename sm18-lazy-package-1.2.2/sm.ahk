#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
; #Warn  ; Enable warnings to assist with detecting common errors.
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.
#Include WinClipAPI.ahk
#Include WinClip.ahk

; ^r::
;     Send {Click}lu
; return

^r::
    Reload
Return

; ::/aa::aaaa

:o?:/delta::δ
:o?:/left::→
:o?:/theta::θ
:o?:/la::
    Send {Text}<SPAN class=latex>[$][/$]</SPAN>
    Send {Left 11}
Return
:o?:/fr::\frac{{}{}}{{}{}}{Left 3}
:o?:/over::\overset{{}{}}{{}{}}{Left 3}
:o?:/lim::\lim_{{}{}}{Left}x \to{Space}
:o?:/inf::\infty
;这个好像会被vscode吞了
:o?:/Delta::\Delta
:o?:/fx::f(x)
:o?:/...::[...]
:o?:/>::&gt;
:o?:/<::&lt;
:o?:/dot::·
:o?:/+-::±

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
    FormatTime, DateNow , , yyyy/M/d hh:mm:ss
    Send ^{End}
    ; Send {Text}Q: <SPAN class=field>组胚</SPAN>
    Send {Text}Q: <SPAN class=field>高数</SPAN>
    ; Send {Text}Q: <SPAN class=field>基化</SPAN>
    ; Send {Text}Q: <SPAN class=field>近代史</SPAN>
    ; Send {Text}Q: <SPAN class=field>德法</SPAN>
    Send {Space}
    Send {Text}<BR><DIV class=footer><BR>------------------<BR>&nbsp;&nbsp;&nbsp; Chapter:2<BR>&nbsp;&nbsp;&nbsp; Date:%DateNow%</DIV>
    Send {Space}{Enter}
    ;如果有开自动补全就会多个tab
    ; Send {BackSpace}
    Send {Text}A:
    Send {Space}{Enter}
    Send {Text}<hr>
    Send {Enter 2}{Up 4}{Right 31}
    ;有展开的话不注释下面这行
    ; Send {Up}{Right 2}
Return
!x::
    RunWait, img2base64.py
    Send ^v
Return

#IfWinActive, ● new.htm - Visual Studio 
; 从Q区切换到A区
Tab::Send {Down}{End}
:o?:br::{Text}<BR>
!s::
    Send {Text}<SUB></SUB>
    Send {Left 6}
Return
!w::
    Send {Text}<SUP></SUP>
    Send {Left 6}
Return


#IfWinActive, new.htm - Visual Studio 
; 从Q区切换到A区
Tab::Send {Down}{End}
:o?:br::{Text}<BR>
!s::
    Send {Text}<SUB></SUB>
    Send {Left 6}
Return
!w::
    Send {Text}<SUP></SUP>
    Send {Left 6}
Return
