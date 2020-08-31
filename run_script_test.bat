@ECHO OFF

set args = %1

for %%i in (pdf_concept_category\*.txt) do (
"C:\Users\dorer\AppData\Local\Programs\Python\Python38\python.exe" "C:\Users\dorer\Documents\github\Word_Statistics\lib\main.py" %%i
)
pause