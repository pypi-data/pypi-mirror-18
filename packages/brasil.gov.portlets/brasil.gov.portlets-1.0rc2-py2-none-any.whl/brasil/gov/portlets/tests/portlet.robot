*** Settings ***

Resource  plone/app/robotframework/keywords.robot
Variables  plone/app/testing/interfaces.py

*** Variables ***

${PORT} =  55001
${ZOPE_URL} =  http://localhost:${PORT}
${PLONE_URL} =  ${ZOPE_URL}/plone
${BROWSER} =  Firefox

*** Keywords ***

Manage Portlets
    Go to   ${PLONE_URL}/@@manage-portlets

Add Left Portlet
    [arguments]  ${portlet}
    Manage Portlets
    Select from list  xpath=//div[@id="portletmanager-plone-leftcolumn"]//select  ${portlet}
    Wait Until Page Contains element  name=form.actions.save

Add Right Portlet
    [arguments]  ${portlet}
    Manage Portlets
    Select from list  xpath=//div[@id="portletmanager-plone-rightcolumn"]//select  ${portlet}
    Wait Until Page Contains element  name=form.actions.save

Edit Left Portlet
    Manage Portlets
    Page Should Contain Element  css=#portletmanager-plone-leftcolumn .portletHeader>a
    Click Link  css=#portletmanager-plone-leftcolumn .portletHeader>a
    Wait Until Page Contains element  name=form.actions.save

Edit Right Portlet
    Manage Portlets
    Page Should Contain Element  css=#portletmanager-plone-rightcolumn .portletHeader>a
    Click Link  css=#portletmanager-plone-rightcolumn .portletHeader>a
    Wait Until Page Contains element  name=form.actions.save

Delete Left Portlet
    Manage Portlets
    Page Should Contain Element  css=#portletmanager-plone-leftcolumn .delete button
    Click Element  css=#portletmanager-plone-leftcolumn .delete button

Delete Right Portlet
    Manage Portlets
    Page Should Contain Element  css=#portletmanager-plone-rightcolumn .delete button
    Click Element  css=#portletmanager-plone-rightcolumn .delete button

Hide Left Portlet
    Manage Portlets
    Page Should Contain Element  css=#portletmanager-plone-leftcolumn .portlet-action:nth-child(1) button
    Click Element  css=#portletmanager-plone-leftcolumn .portlet-action:nth-child(1) button

Hide Right Portlet
    Manage Portlets
    Page Should Contain Element  css=#portletmanager-plone-rightcolumn .portlet-action:nth-child(1) button
    Click Element  css=#portletmanager-plone-rightcolumn .portlet-action:nth-child(1) button

Show Left Portlet
    Manage Portlets
    Page Should Contain Element  css=#portletmanager-plone-leftcolumn .portlet-action:nth-child(1) button
    Click Element  css=#portletmanager-plone-leftcolumn .portlet-action:nth-child(1) button

Show Right Portlet
    Manage Portlets
    Page Should Contain Element  css=#portletmanager-plone-rightcolumn .portlet-action:nth-child(1) button
    Click Element  css=#portletmanager-plone-rightcolumn .portlet-action:nth-child(1) button

Select Collection
    [arguments]  ${collection_field_id}  ${collection_name}
    Page Should Contain Element  id=${collection_field_id}
    Input Text  id=${collection_field_id}  ${collection_name}
    Click Button  name=${collection_field_id}.search
    Wait Until Page Contains element  name=${collection_field_id}.update
    Click Element  xpath=//div[@data-fieldname='${collection_field_id}']//input[@type='radio'][@name='${collection_field_id}']
    
Save Portlet
    Click Button  Save
    Wait Until Page Contains element  css=.portlets-manager
    Go to Homepage

Cancel Portlet
    Click Button  Cancel
    Wait Until Page Contains element  css=.portlets-manager
    Go to Homepage
