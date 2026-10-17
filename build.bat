@echo off
REM Double-click this after adding or changing a lesson.
REM It rescans the courses folder and updates the home page list + sitemap.
cd /d "%~dp0"
node tools\build-manifest.js
pause
