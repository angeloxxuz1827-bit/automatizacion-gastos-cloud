@echo off
title AWS Lambda Build

echo.
echo ==========================================
echo        AWS LAMBDA BUILD SCRIPT
echo ==========================================
echo.

REM ==========================================
REM Eliminar carpeta build
REM ==========================================

if exist build (
    echo [1/6] Eliminando carpeta build...
    rmdir /S /Q build
)

REM ==========================================
REM Crear carpeta build
REM ==========================================

echo [2/6] Creando carpeta build...
mkdir build

REM ==========================================
REM Instalar dependencias
REM ==========================================

echo [3/6] Instalando dependencias...
venv\Scripts\python.exe -m pip install -r requirements.txt -t build

if errorlevel 1 (
    echo.
    echo ERROR instalando dependencias.
    pause
    exit /b
)

REM ==========================================
REM Copiar carpetas del proyecto
REM ==========================================

echo [4/6] Copiando codigo...

xcopy config build\config /E /I /Y >nul
xcopy core build\core /E /I /Y >nul
xcopy ingestion build\ingestion /E /I /Y >nul
xcopy llm build\llm /E /I /Y >nul

REM ==========================================
REM Copiar archivos necesarios
REM ==========================================

echo [5/6] Copiando archivos...

copy lambda_function.py build >nul

REM ==========================================
REM Crear ZIP
REM ==========================================

echo [6/6] Creando lambda.zip...

if exist lambda.zip del lambda.zip

powershell -Command "Compress-Archive -Path build\* -DestinationPath lambda.zip -Force"

echo.
echo ==========================================
echo BUILD FINALIZADO CORRECTAMENTE
echo ==========================================
echo.
echo Carpeta generada:
echo    build\
echo.
echo Archivo generado:
echo    lambda.zip
echo.

pause