@echo off
echo.
echo ==============================
echo   Deploying to thedebasish.com
echo ==============================
echo.

set PATH=%PATH%;C:\Program Files\Git\cmd

echo [1/3] Adding all changes...
git add .

echo.
set /p msg="[2/3] What did you change? (type a short description): "

git commit -m "%msg%"

echo.
echo [3/3] Pushing to GitHub...
git push

echo.
echo ==============================
echo   DONE! Your site will update
echo   at thedebasish.com in 1-2 mins
echo ==============================
echo.
pause
