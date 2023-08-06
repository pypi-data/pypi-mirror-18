import os
import webbrowser
import requests
import rinocloud
from rino import config, login, utils


def open():
    remote = config.get('remote')

    token = login.get_token()
    project = login.get_project()
    rinocloud.api_key = token
    rinocloud.set_local_path(os.getcwd())
    rinoFolderId = utils.get_rino_folder(rinocloud, remote).json()

    url = 'https://' + project + '.rinocloud.com/app/folder/%s' % rinoFolderId['id']
    webbrowser.open(url, new=2, autoraise=True)
