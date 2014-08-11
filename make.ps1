param($p)

If($p -eq "clean"){
    if(Test-Path build){ rm -r build}
    if(Test-Path dist){ rm -r dist}
    if(Test-Path gitime.egg-info){ rm -r gitime.egg-info}
    if(Test-Path docs\_build\doctrees){ rm -r docs\_build\doctrees}
    if(Test-Path docs\_build\html){ rm -r docs\_build\html}
}

ElseIf($p -eq "reinstall"){
    pip uninstall -y gitime
    python setup.py install
}

ElseIf($p -eq "test"){
    python -Wall -3 -m unittest discover tests\ '*test.py' --failfast
}

ElseIf($p -eq "publish"){
    python setup.py sdist upload
}

Else{
    echo "Not understood."
}