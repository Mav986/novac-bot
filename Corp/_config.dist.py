"""
To get a proper SRP_URL, visit your google form's edit page, click the triple-dot menu in the top right,
click 'get pre-filled link'. Once on this page, fill out ALL sections with some easily recognizable
data. I recommend using capital letters to make the next part easier.

Once the required sections are complete, click 'get link' at the bottom of the page. The page will reload, and
a new grey popup will be displayed in the bottom left of the window. Click 'copy link' to get the URL. The
final step is to replace the word 'viewform' with the word 'formResponse'. Remove the placeholder responses you filled
in earlier, and replace them with the correct string formatting. An example is shown below.

ENTIRE URL: https://docs.google.com/forms/d/e/1FAIpQLSf86gD81OOSOUVzMqKvD9PQOUER-mAd6pQgeVPDcYjC5Xl-Gw/formResponse
    ?usp=pp_url&entry.445819805={name}&entry.816115494={killmail_url}&entry.1620172123={extra_info}

Any optional fields of the form can defined as constants and removed from the base URL, later added as optional
in the implementation. The example is clarified below.

BASE URL: https://docs.google.com/forms/d/e/1FAIpQLSf86gD81OOSOUVzMqKvD9PQOUER-mAd6pQgeVPDcYjC5Xl-Gw/formResponse
    ?usp=pp_url&entry.445819805={name}&entry.816115494={killmail_url}

OPTIONAL SECTION: &entry.1620172123={extra_info}

Note: Do not split URL onto multiple lines. For some reason, the \ separator breaks the URL to prevent form submission.
"""

SRP_URL = 'SRP FORMRESPONSE URL HERE'
SRP_URL_WITH_COMMENT = SRP_URL + 'EXTRA SECTION HERE'
