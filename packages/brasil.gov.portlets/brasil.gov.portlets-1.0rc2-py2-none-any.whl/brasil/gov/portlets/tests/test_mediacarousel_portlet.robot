*** Settings ***

Resource  portlet.robot
Library  Remote  ${PLONE_URL}/RobotRemote

Suite Setup  Open Test Browser
Suite Teardown  Close all browsers

*** Variables ***

${portletname_sample}  Portal Padrao Media Carousel
${headercheck_field_id}  form.show_header
${header_field_id}  form.header
${headertype_field_id}  form.header_type
${headertype_sample}  H4
${titlecheck_field_id}  form.show_title
${descriptioncheck_field_id}  form.show_description
${footercheck_field_id}  form.show_footer
${footer_field_id}  form.footer
${footer_sample}  More...
${footerurl_field_id}  form.footer_url
${footerurl_sample}  http://www.google.com
${rightscheck_field_id}  form.show_rights
${limit_field_id}  form.limit
${limit_sample}  2
${collection_field_id}  form.collection

*** Test cases ***

Test MediaCarousel Portlet
    Enable Autologin as  Site Administrator
    Go to Homepage
    Sleep  1s  Wait for overlay

    Add Right Portlet  ${portletname_sample}
    Select Collection  ${collection_field_id}  Images Collection
    Save Portlet
    Page Should Contain Element  xpath=//div[@class='portal-padrao-mediacarousel-portlet']
    Sleep  1s  Wait for overlay

    Edit Right Portlet
    Select Checkbox  id=${headercheck_field_id}
    Page Should Contain Element  id=${header_field_id}
    Input Text  id=${header_field_id}  ${portletname_sample}
    Select from list  id=${headertype_field_id}  ${headertype_sample}
    Save Portlet
    Page Should Contain Element  xpath=//div[@class='portal-padrao-mediacarousel-portlet']//div[@class='portletHeader']/h4
    Sleep  1s  Wait for overlay

    Edit Right Portlet
    Select Checkbox  id=${titlecheck_field_id}
    Save Portlet
    Page Should Contain Element  xpath=//div[@class='portal-padrao-mediacarousel-portlet']//div[contains(@class, 'cycle-player')]//div[@class='portlet-mediacarousel-title']
    Sleep  1s  Wait for overlay

    Edit Right Portlet
    Select Checkbox  id=${descriptioncheck_field_id}
    Save Portlet
    Page Should Contain Element  xpath=//div[@class='portal-padrao-mediacarousel-portlet']//div[contains(@class, 'cycle-player')]//div[@class='portlet-mediacarousel-description']
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
    Page Should Contain Element  xpath=//div[@class='portal-padrao-mediacarousel-portlet']//div[@class='portletFooter']/a[@href='${footerurl_sample}']
    Sleep  1s  Wait for overlay

    Edit Right Portlet
    Select Checkbox  id=${rightscheck_field_id}
    Save Portlet
    Page Should Contain Element  xpath=//div[@class='portal-padrao-mediacarousel-portlet']//div[contains(@class, 'cycle-player')]//div[@class='portlet-mediacarousel-rights']
    Sleep  1s  Wait for overlay

    Edit Right Portlet
    Page Should Contain Element  id=${limit_field_id}
    Input Text  id=${limit_field_id}  ${limit_sample}
    Save Portlet
    Xpath Should Match X Times  //div[@class='portal-padrao-mediacarousel-portlet']//div[contains(@class, 'cycle-player')]/div[not(contains(@class, 'cycle-sentinel'))]  ${limit_sample}
    Xpath Should Match X Times  //div[@class='portal-padrao-mediacarousel-portlet']//div[contains(@class, 'cycle-carousel-wrap')]/div  ${limit_sample}
    Sleep  1s  Wait for overlay

    Hide Right Portlet
    Go to Homepage
    Page Should Not Contain Element  xpath=//div[@class='portal-padrao-mediacarousel-portlet']
    Sleep  1s  Wait for overlay

    Show Right Portlet
    Go to Homepage
    Page Should Contain Element  xpath=//div[@class='portal-padrao-mediacarousel-portlet']
    Sleep  1s  Wait for overlay

    Delete Right Portlet
    Go to Homepage
    Page Should Not Contain Element  xpath=//div[@class='portal-padrao-mediacarousel-portlet']
    Sleep  1s  Wait for overlay

    # Test add in the left side    
    Add Left Portlet  ${portletname_sample}
    Select Collection  ${collection_field_id}  Images Collection
    Save Portlet
    Page Should Contain Element  xpath=//div[@class='portal-padrao-mediacarousel-portlet']
    Sleep  1s  Wait for overlay

    Delete Left Portlet
    Go to Homepage
    Page Should Not Contain Element  xpath=//div[@class='portal-padrao-mediacarousel-portlet']
    Sleep  1s  Wait for overlay
