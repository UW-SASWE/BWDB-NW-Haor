set "root=cd /d D:\SASWMS_Shahzaib\barind"
%root%

CALL C:\ProgramData\Anaconda2\Scripts\activate.bat

CALL C:\ProgramData\Anaconda2\python.exe D:\SASWMS_Shahzaib\barind\Web\Download_Haor_from_server.py

cd D:\SASWMS_Shahzaib\barind\ProcessHaorsAutom_V97\for_redistribution_files_only
ProcessHaorsAutom_V97.exe

cd D:\SASWMS_Shahzaib\barind\Web
D:\SASWMS_Shahzaib\barind\ProcessHaorsAutom_V97\for_redistribution_files_only\Correcting_OutputHaor.py
CALL C:\ProgramData\Anaconda2\python.exe D:\SASWMS_Shahzaib\barind\Web\Upload_Haor_to_server.py
@REM ECHO uploaded!
ECHO Done!
