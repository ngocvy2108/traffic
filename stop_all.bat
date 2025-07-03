
@echo off
echo === DỪNG TOÀN BỘ HỆ THỐNG GIAO THÔNG FIWARE ===

REM Dừng toàn bộ tiến trình Python (nếu còn chạy)
echo 1. Dừng các script Python đang chạy...
taskkill /F /IM python.exe

echo ✅ Hệ thống đã được dừng hoàn toàn.
pause
