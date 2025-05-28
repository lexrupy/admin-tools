@echo off
setlocal

REM Obter o caminho completo do arquivo PDF e envolver entre aspas
set "PDF_PATH=%~1"
set "PDF_PATH="%PDF_PATH%""

REM Executar o script Python com o arquivo PDF e o caminho do diretório como argumentos
python "c:\pdfmanage\divide.py" %PDF_PATH%

pause
endlocal
