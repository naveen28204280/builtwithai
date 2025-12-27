@echo off
echo ===================================================
echo Installing/Verifying Dependencies...
echo ===================================================
pip install Flask Flask-CORS python-dotenv requests pytz python-dateutil
pip install pandas numpy scikit-learn

echo.
echo ===================================================
echo Starting Student Finance AI Backend...
echo ===================================================
start cmd /k "python backend/run.py"

echo.
echo ===================================================
echo Opening Frontend...
echo ===================================================
timeout /t 3
start frontend/index.html

echo.
echo Done! The backend is running in a new window.
echo If you see errors about "pandas" or "numpy", don't worry!
echo The app has fallback modes to work without them.
pause
