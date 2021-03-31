import jwt, time

from util.GoogleCaptcha import GoogleCaptcha as GCap
from api import RedisCache


def level1_authorization(obj, info, token):
    cap = GCap("6LcY9mgaAAAAAA9lRhGDBvVzoR_58T4urtl8i8aj", token)
    if True:#cap.verify_captcha():

        # TODO CHANGE SECRET

        cache = RedisCache.CacheUserSession(address=info.context.remote_addr, authorization_level=0)
        cache.register()

        return {
            "success": True,
            "session_id": cache.id
        }
    else:
        return {
            "success": False
        }
