@echo off
REM Configuración de variables de entorno para el proyecto

REM Obtener el directorio donde se encuentra este archivo .bat
set "SCRIPT_DIR=%~dp0"

REM Configurar el PATH relativo
set "PATH=%PATH%;%SCRIPT_DIR%RandomForestModel"
set "PATH=%PATH%;%SCRIPT_DIR%back"

REM Configuración de variables específicas del entorno
set "MY_PROJECT_HOME=%SCRIPT_DIR%"
set "MY_PROJECT_CONFIG=%SCRIPT_DIR%data"

REM Imprimir variables de entorno para verificar
echo PATH=%PATH%
echo MY_PROJECT_HOME=%MY_PROJECT_HOME%
echo MY_PROJECT_CONFIG=%MY_PROJECT_CONFIG%

REM Ejecutar el script de tu aplicación o entorno
REM %SCRIPT_DIR%path\to\your\python.exe %SCRIPT_DIR%streamlit_app.py

pause
