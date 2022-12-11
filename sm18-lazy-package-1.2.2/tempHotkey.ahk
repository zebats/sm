; This is an AutoHotkey script that allows you to add new hotkeys at any time
; and automatically clears them after a set period of time.

; Set the amount of time (in seconds) to wait before clearing the hotkeys
hotkey_timeout = 3600

; Create an empty list to store the hotkeys
hotkeys = []

; This is the main loop that runs continuously
loop
{
    ; Prompt the user to enter a new hotkey
    InputBox, hotkey, Please enter a new hotkey:
    if (ErrorLevel)
        continue

    ; Prompt the user to enter the action for the hotkey
    InputBox, action, Please enter the action for hotkey %hotkey%:
    if (ErrorLevel)
        continue

    ; Add the new hotkey and action to the list
    hotkeys.push([hotkey, action])

    ; Create the hotkey using the hotkey and action
    %hotkey%::
        ; Insert the action here
        ; For example:
        Send, %action%
        return

    ; Sleep for the specified amount of time before clearing the hotkeys
    Sleep, %hotkey_timeout%

    ; Clear the hotkeys
    hotkeys = []
}