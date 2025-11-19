@echo off
set INPUT_PDF=data/NCRB_STATS.pdf
set OUTPUT_DIR=temp

echo Running logicTwo.py with PyMuPDF

echo.
echo --- Example 1: Remove 1-indexed pages 1, 2, and 546 ---
python logicTwo.py %INPUT_PDF% %OUTPUT_DIR%/filtered_NCRB_STATS_logicTwo_1indexed.pdf -p 1 2 546
echo.

echo.
echo --- Example 2: Remove 0-indexed pages 0, 1, and 545 (equivalent to 1, 2, 546 1-indexed) ---
python logicTwo.py %INPUT_PDF% %OUTPUT_DIR%/filtered_NCRB_STATS_logicTwo_0indexed.pdf -p 0 1 545 --zero-indexed
echo.

echo All logicTwo.py examples finished.
pause