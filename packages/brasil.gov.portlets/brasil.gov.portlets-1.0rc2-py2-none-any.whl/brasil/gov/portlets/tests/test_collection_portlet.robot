*** Settings ***

Resource  portlet.robot
Library  Remote  ${PLONE_URL}/RobotRemote

Suite Setup  Open Test Browser
Suite Teardown  Close all browsers

*** Variables ***

${portletname_sample}  Portal Padrao Collection
${title_field_id}  form.header
${titleurl_field_id}  form.header_url
${titleurl_sample}  http://www.plone.org
${imgcheck_field_id}  form.show_image
${imgsize_field_id}  form.image_size
${imgsize_sample}  mini 200:200
${titletype_field_id}  form.title_type
${titletype_sample}  H4
${footercheck_field_id}  form.show_footer
${footer_field_id}  form.footer
${footer_sample}  More...
${footerurl_field_id}  form.footer_url
${footerurl_sample}  http://www.google.com
${limit_field_id}  form.limit
${limit_sample}  2
${datecheck_field_id}  form.show_date
${timecheck_field_id}  form.show_time
${titletype_field_id}  form.title_type
${collection_field_id}  form.collection

*** Test cases ***

Test Collection Portlet
    Enable Autologin as  Site Administrator
    Go to Homepage
    Sleep  1s  Wait for overlay

    # news collection should get order 2 3 1
    Add Right Portlet  ${portletname_sample}
    Page Should Contain Element  id=${title_field_id}
    Input Text  id=${title_field_id}  ${portletname_sample}
    Select Collection  ${collection_field_id}  News Collection
    Save Portlet
    Page Should Contain Element  xpath=//div[@class='portal-padrao-collection-portlet']
    Sleep  1s  Wait for overlay

    Edit Right Portlet
    Page Should Contain Element  id=${titleurl_field_id}
    Input Text  id=${titleurl_field_id}  ${titleurl_sample}
    Save Portlet
    Page Should Contain Element  xpath=//div[@class='portal-padrao-collection-portlet']//a[@href='${titleurl_sample}']
    Sleep  1s  Wait for overlay

    Edit Right Portlet
    Select Checkbox  id=${imgcheck_field_id}
    Select from list  id=${imgsize_field_id}  ${imgsize_sample}
    Save Portlet
    Page Should Contain Element  xpath=//div[@class='portal-padrao-collection-portlet']//img
    Sleep  1s  Wait for overlay

    Edit Right Portlet
    Select from list  id=${titletype_field_id}  ${titletype_sample}
    Save Portlet
    Page Should Contain Element  xpath=//div[@class='portal-padrao-collection-portlet']//h4
    Sleep  1s  Wait for overlay

    Edit Right Portlet
    Select Checkbox  id=${footercheck_field_id}
    Page Should Contain Element  id=${footer_field_id}
    Input Text  id=${footer_field_id}  ${footer_sample}
    Page Should Contain Element  id=${footer_field_id}
    Input Text  id=${footer_field_id}  ${footer_sample}
    Page Should Contain Element  id=${footerurl_field_id}
    Input Text  id=${footerurl_field_id}  ${footerurl_sample}
    Save Portlet
    Page Should Contain Element  xpath=//div[@class='portal-padrao-collection-portlet']//div[@class='portletFooter']/a[@href='${footerurl_sample}']
    Sleep  1s  Wait for overlay

    Edit Right Portlet
    Page Should Contain Element  id=${limit_field_id}
    Input Text  id=${limit_field_id}  ${limit_sample}
    Save Portlet
    Xpath Should Match X Times  //div[@class='portal-padrao-collection-portlet']//div[@class='portlet-collection-item']  ${limit_sample}
    Sleep  1s  Wait for overlay

    Edit Right Portlet
    Select Checkbox  id=${datecheck_field_id}
    Save Portlet
    Page Should Contain Element  xpath=//div[@class='portal-padrao-collection-portlet']//div[@class='portletItem']//p[@class='portlet-collection-date']
    Sleep  1s  Wait for overlay

    Edit Right Portlet
    Select Checkbox  id=${timecheck_field_id}
    Save Portlet
    Page Should Contain Element  xpath=//div[@class='portal-padrao-collection-portlet']//div[@class='portletItem']//p[@class='portlet-collection-date']
    Sleep  1s  Wait for overlay

    Hide Right Portlet
    Go to Homepage
    Page Should Not Contain Element  xpath=//div[@class='portal-padrao-collection-portlet']
    Sleep  1s  Wait for overlay

    Show Right Portlet
    Go to Homepage
    Page Should Contain Element  xpath=//div[@class='portal-padrao-collection-portlet']
    Sleep  1s  Wait for overlay

    Delete Right Portlet
    Go to Homepage
    Page Should Not Contain Element  xpath=//div[@class='portal-padrao-collection-portlet']
    Sleep  1s  Wait for overlay

    # events collection should get order 3 2 1
    Add Left Portlet  ${portletname_sample}
    Page Should Contain Element  id=${title_field_id}
    Input Text  id=${title_field_id}  ${portletname_sample}
    Select Collection  ${collection_field_id}  Events Collection
    Save Portlet
    Page Should Contain Element  xpath=//div[@class='portal-padrao-collection-portlet']
    Sleep  1s  Wait for overlay

    Delete Left Portlet
    Go to Homepage
    Page Should Not Contain Element  xpath=//div[@class='portal-padrao-collection-portlet']
    Sleep  1s  Wait for overlay
