import os
import re

import requests


def contribution_figures(contributions_filename='/Users/paulwhipp/Work/flux/fluxdoc/docs/contributing/index.rst'):
    contribution_folder = os.path.dirname(contributions_filename)
    with open(contributions_filename, 'r') as f:
        contributions_text = f.read()

    def replacer(match):
        url = match.group(1)
        response = requests.get(url)
        image_filename = os.path.basename(url)
        with open(os.path.join(contribution_folder, image_filename), 'wb') as image_file:
            image_file.write(response.content)
        return '.. figure:: {}'.format(image_filename)

    rx = re.compile('\.\.\sfigure::\s(http.*)')
    contributions_text = rx.sub(replacer, contributions_text)

    with open(contributions_filename, 'w') as f:
        f.write(contributions_text)
