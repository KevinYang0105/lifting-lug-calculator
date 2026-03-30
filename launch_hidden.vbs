Set shell = CreateObject("WScript.Shell")
projectDir = CreateObject("Scripting.FileSystemObject").GetParentFolderName(WScript.ScriptFullName)
shell.Run Chr(34) & projectDir & "\start_app.bat" & Chr(34), 0, False
