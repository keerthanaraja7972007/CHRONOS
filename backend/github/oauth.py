from urllib.parse import urlencode
from backend.core.config import get_settings
def authorization_url(state:str)->str:
    settings=get_settings(); return "https://github.com/login/oauth/authorize?"+urlencode({"client_id":settings.github_client_id,"redirect_uri":settings.github_callback_url,"scope":"read:user repo","state":state})
