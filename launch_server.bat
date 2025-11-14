call .\venv\Scripts\activate.bat
python .\src\api\local_api.py


if NOT ["%errorlevel%"]==["0"] (
    pause
    exit /b %errorlevel%
)