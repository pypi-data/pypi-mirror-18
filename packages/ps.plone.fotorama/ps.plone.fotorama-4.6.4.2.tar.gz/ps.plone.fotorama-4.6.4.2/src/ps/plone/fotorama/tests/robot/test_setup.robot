*** Settings ***

Resource  keywords.robot

Suite Setup  Setup
Suite Teardown  Teardown


*** Test cases ***

Show how to activate the add-on
    Enable autologin as  Manager
    Go to  ${PLONE_URL}/prefs_install_products_form
    Page should contain element  xpath=//*[@value='ps.plone.fotorama']
    Assign id to element
    ...  xpath=//*[@value='ps.plone.fotorama']/parent::*
    ...  addons-psplonefotorama
    Assign id to element
    ...  xpath=//*[@value='ps.plone.fotorama']/ancestor::form
    ...  addons-enabled

    Highlight  addons-psplonefotorama
    Capture and crop page screenshot
    ...  setup_select_add_on.png
    ...  id=addons-enabled
