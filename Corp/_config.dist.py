"""
Note: Form ID's are different when viewing/editing than when submitting.

To get your post form id, visit your google form's edit page, click the triple-dot menu in the top right, and click
'get pre-filled link'. Fill out all sections using easily recognized placeholder names, then click 'get link' at the
bottom. The page will reload and a popup will display in the bottom left of the window. Click 'copy link' to get your
full URL. The form ID will be between the '/e/' and '/viewform' sections.

After you've got your form id, you want to get each section that needs filling out. In this new URL, there should
be several sections following a format of '&entry.#########=YOUR-PLACEHOLDER-NAME'. Each one of those is a section
that can be filled out. Use these to create the parameter dictionary.
"""

FORM_ID = 'YOUR-FORM-ID'

ENTRIES = {
    'name': 'entry.##########',
    'killmail_url': 'entry.##########',
    'extry_info': 'entry.##########'
}

