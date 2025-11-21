@echo off
echo ================================================================================
echo Installing Dermatology Classification System Dependencies
echo ================================================================================
echo.

echo [1] Upgrading pip...
python -m pip install --upgrade pip

echo.
echo [2] Installing Python packages...
pip install -r requirements.txt

echo.
echo [3] Installing Graphviz (required for architecture diagrams)...
echo Please install Graphviz manually from: https://graphviz.org/download/
echo After installation, add Graphviz to your PATH
echo.

echo ================================================================================
echo Installation complete!
echo ================================================================================
echo.
echo Next steps:
echo 1. Start LM Studio and load medgemma-27b-multimodal model
echo 2. Enable local server on http://localhost:1234
echo 3. Run: python main.py
echo.
pause
