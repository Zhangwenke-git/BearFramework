cd /d %~dp0

del /f/s/q ..\image\screenshots\*.png
del /f/s/q ..\image\identifycode\*.png
del /f/s/q ..\logs\*.*
del /f/s/q ..\Output\*.*
del /f/s/q ..\TestSuit\CLIENT\failures
del /f/s/q ..\TestSuit\API\failures
del /f/s/q ..\TestSuit\WEB\failures
del /f/s/q ..\TestSuit\CLIENT\geckodriver.log
del /f/s/q ..\TestSuit\API\geckodriver.log
del /f/s/q ..\TestSuit\WEB\geckodriver.log
del /f/s/q ..\.pytest_cache\*.*



del /f/s/q ..\report\allure\WEB\*.*
rd /s/q ..\report\allure\WEB
md ..\report\allure\WEB