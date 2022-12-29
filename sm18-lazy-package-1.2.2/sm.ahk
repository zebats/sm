#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
; #Warn  ; Enable warnings to assist with detecting common errors.
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.
#Include WinClipAPI.ahk
#Include WinClip.ahk

AddNew(){
    FormatTime, DateNow , , yyyy/M/d hh:mm:ss
    Send ^{End}
    ; Send {Text}Q: <SPAN class=field>组胚</SPAN>
    ; Send {Text}Q: <SPAN class=field>高数</SPAN>
    Send {Text}Q: <SPAN class=field>基化</SPAN>
    ; Send {Text}Q: <SPAN class=field>近代史</SPAN>
    ; Send {Text}Q: <SPAN class=field>德法</SPAN>
    ; Send {Text}Q: <SPAN class=field>英语</SPAN>
    Send {Space}
    Send {Text}<BR><DIV class=footer><BR>------------------<BR>&nbsp;&nbsp;&nbsp; Chapter:5<BR>&nbsp;&nbsp;&nbsp; Date:%DateNow%</DIV>
    Send {Space}{Enter}
    ;如果有开自动补全就会多个tab
    Send {BackSpace}
    Send {Text}A:
    Send {Space}{Enter}
    Send {Text}<hr>
    Send {Enter 2}{Up 4}{Right 31}
    ;有展开的话不注释下面这行
    ; Send {Up}{Right 2}
}
; count:=1
; ^q::
;     while (count<131){
;         Send <SPAN style="display:none">%count%</SPAN>
;         count:=count+1
;         Send {Down}{Right}{Down 2}{Right 3}
;     }
; Return



; ^r::
;     Send {Click}lu
; return

^r::
    Reload
Return

CapsLock::
    Send {BackSpace}
Return

; ::/aa::aaaa

:o?:/delta::δ
:o?:/left::→
:o?:/theta::θ
:o?:/la::
    FormatTime, DateNow , , yyyy/M/d hh:mm:ss
    Send {Text}<SPAN class=latex>[$][/$]</SPAN><SPAN style="display:none;">%DateNow%</SPAN>
    Send {Left 65}
Return
:o?:\la::
    FormatTime, DateNow , , yyyy/M/d hh:mm:ss
    Send {Text}<SPAN class=latex>[$$][/$$]</SPAN><SPAN style="display:none;">%DateNow%</SPAN>
    Send {Left 66}
Return
:o?:/fr::\frac{{}{}}{{}{}}{Left 3}
:o?:/sq::\sqrt{{}{}}{Left}
:o?:/int::\int{Space}
:o?:/over::\overset{{}{}}{{}{}}{Left 3}
:o?:/lim::\lim_{{}{}}{Left}x \to{Space}
:o?:/inf::\infty{Space}
;这个好像会被vscode吞了
:o?:/Del::\Delta{Space}
:o?:/fx::f(x)
:o?:/...::{Text}[...]
:o?:/>::&gt;
:o?:/<::&lt;
:o?:/dot::·
:o?:/+-::±
:o?:/infty::∞

;field
::/f::
    WinClip.SetHTML("<SPAN class=field>组胚</SPAN> ")
    ;Send {ctrl down}v{ctrl up}{left}{ShiftDown}{left 5}{ShiftUp}组胚{Right}
Return

; ^w::
;     RunWait, rich_clipboard.pyw "<SUP>sup</SUP> "
; Return
;     Send ^v{left}{ShiftDown}{left 3}{ShiftUp}

;新建卡
#IfWinActive, ahk_exe code.exe
!a::
    AddNew()
Return

!x::
    RunWait, img2base64.pyw
    Send ^v
Return

#IfWinActive, ahk_exe sm18.exe
^+m::
    Send ^+m
    Send {Text}cloz
    Send {Enter}
Return

^d::
    Send  ^d{Enter}{Enter}
Return

MButton::
    Send !z


^q::
    Send ^a^+1
Return

!l::
    Send ^!l    
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
!z::
    c:=Clipboard
    Clipboard:=
    Send ^x
    ClipWait 
    Send {Text}<SPAN class=cloze>[...]</SPAN>
    Send {Down}%Clipboard%{Esc}
    Clipboard:=c
Return
!^s::
    c:=Clipboard
    Clipboard:=
    Send ^c
    ClipWait
    temple=%Clipboard%
    Clipboard:=c
Return
!+s::
    AddNew()
    Send %temple%
Return
^!c::
    Send ^s
    ; c:=Clipboard
    Send ^a
    Sleep, 200
    Clipboard:=
    Send ^c
    ClipWait
    RunWait, duplicate.pyw
    Send {Right}
    Send ^v
    Sleep 200
    ; Clipboard:=c
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
!z::
    ; c:=Clipboard
    Send ^x
    Send {Text}<SPAN class=cloze>[...]</SPAN>
    Send {Down}^v{Esc}
    ; Clipboard:=c
Return
!^s::
    c:=Clipboard
    Clipboard:=
    Send ^c
    ClipWait
    temple=%Clipboard%
    Clipboard:=c
Return
!+s::
    AddNew()
    Send %temple%
Return
^!c::
    Send ^s
    ; c:=Clipboard
    Send ^a
    Sleep, 200
    Clipboard:=
    Send ^c
    ClipWait
    RunWait, duplicate.pyw
    Send {Right}
    Send ^v
    Sleep 200
    ; Clipboard:=c
Return