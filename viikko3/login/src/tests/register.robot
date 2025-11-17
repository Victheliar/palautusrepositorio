*** Settings ***
Resource  resource.robot
Suite Setup     Open And Configure Browser
Suite Teardown  Close Browser
Test Setup      Reset Application Create User And Go To Register Page

*** Test Cases ***
Register With Valid Username And Password
    Set Username  vici
    Set Password  vici1234
    Set Password Confirmation  vici1234
    Click Button  Register
    Registration Should Succeed

Register With Too Short Username And Valid Password
    Set Username  v
    Set Password  vici1234
    Set Password Confirmation  vici1234
    Click Button  Register
    Registration Should Fail With Message  Username should contain at least three characters


Register With Valid Username And Too Short Password
    Set Username  vici
    Set Password  vici123
    Set Password Confirmation  vici123
    Click Button  Register
    Registration Should Fail With Message  Password should contain at least 8 characters

Register With Valid Username And Invalid Password
# salasana ei sisällä halutunlaisia merkkejä
    Set Username  vici
    Set Password  viciiiii
    Set Password Confirmation  viciiiii
    Click Button  Register
    Registration Should Fail With Message  Password should contain at least one number or special character

Register With Nonmatching Password And Password Confirmation
    Set Username  vici
    Set Password  vici1234
    Set Password Confirmation  vici1345
    Click Button  Register
    Registration Should Fail With Message  Passwords do not match

Register With Username That Is Already In Use
    Set Username  kalle
    Set Password  vici1234
    Set Password Confirmation  vici1234
    Click Button  Register
    Registration Should Fail With Message  User with username kalle already exists

*** Keywords ***
Registration Should Succeed
    Application Page Should Be Open

Registration Should Fail With Message
    [Arguments]  ${message}
    Register Page Should Be Open
    Page Should Contain  ${message}

Set Username
    [Arguments]  ${username}
    Input Text  username  ${username}

Set Password
    [Arguments]  ${password}
    Input Password  password  ${password}

Set Password Confirmation
    [Arguments]  ${password}
    Input Password  password_confirmation  ${password}

*** Keywords ***
Reset Application Create User And Go To Register Page
    Reset Application
    Create User  kalle  kalle123
    Go To Register Page