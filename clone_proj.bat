@echo off
setlocal
echo @author: spanishkukli
echo .
git clone https://github.com/spanishkukli/mkproj.git
echo [DONE] Github project has been cloned succesfully

:PROMPT
SET /P yesno=Do you want to install requirements.txt (default: no) (Y/n)?
IF /I "%yesno%" NEQ "Y" GOTO END
    cd mkproj
    pip install -r requirements.txt
    echo [DONE] All requirements are successfully installed
:END

pause
endlocal