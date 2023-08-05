*** Settings ***

Resource  portlet.robot
Library  Remote  ${PLONE_URL}/RobotRemote

Suite Setup  Open Test Browser
Suite Teardown  Close all browsers

*** Variables ***

${portletname_sample}  Portal Padrao Audio
${header_field_id}  form.header
${audio_field_id}  form.audio

*** Test cases ***

Test Audio Portlet
    Enable Autologin as  Site Administrator
    Go to Homepage
    Sleep  1s  Wait for overlay

    Add Right Portlet  ${portletname_sample}
    Select Collection  ${audio_field_id}  Audio 1
    Save Portlet
    Page Should Contain Element  xpath=//div[@class='portal-padrao-audio-portlet']
    Sleep  1s  Wait for overlay

    Edit Right Portlet
    Page Should Contain Element  id=${header_field_id}
    Input Text  id=${header_field_id}  ${portletname_sample}
    Save Portlet
    Page Should Contain Element  xpath=//div[@class='portal-padrao-audio-portlet']//div[@class='portletHeader']/h3[@class='portlet-audio-title']
    Sleep  1s  Wait for overlay

    Hide Right Portlet
    Go to Homepage
    Page Should Not Contain Element  xpath=//div[@class='portal-padrao-audio-portlet']
    Sleep  1s  Wait for overlay

    Show Right Portlet
    Go to Homepage
    Page Should Contain Element  xpath=//div[@class='portal-padrao-audio-portlet']
    Sleep  1s  Wait for overlay

    Delete Right Portlet
    Go to Homepage
    Page Should Not Contain Element  xpath=//div[@class='portal-padrao-audio-portlet']
    Sleep  1s  Wait for overlay

    # Test add in the left side
    Add Left Portlet  ${portletname_sample}
    Select Collection  ${audio_field_id}  Audio 1
    Save Portlet
    Page Should Contain Element  xpath=//div[@class='portal-padrao-audio-portlet']
    Sleep  1s  Wait for overlay

    Delete Left Portlet
    Go to Homepage
    Page Should Not Contain Element  xpath=//div[@class='portal-padrao-audio-portlet']
    Sleep  1s  Wait for overlay
