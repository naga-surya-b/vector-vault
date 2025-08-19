# Build Windows single-file EXE using PyInstaller
python -m venv .venv
.\.venv\Scripts\pip install -r requirements.txt
.\.venv\Scripts\pip install pyinstaller

# Build React UI
pushd frontend
npm install
npm run build
popd

# Bundle (note Windows ';' separator in --add-data)
.\.venv\Scripts\pyinstaller --onefile -n VectorVault ^
  --add-data "app\frontend\dist;app\frontend\dist" ^
  --add-data "app;app" app\start.py
