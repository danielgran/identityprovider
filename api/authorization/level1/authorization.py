from util.GoogleCaptcha import GoogleCaptcha as GCap
import jwt, time


def level1_authorization(obj, info, token):
    cap = GCap("6LcY9mgaAAAAAA9lRhGDBvVzoR_58T4urtl8i8aj", token)
    if cap.verify_captcha():

        # TODO CHANGE SECRET
        enc_jwt = jwt.encode(
            {
                "verified": True,
                "iss": str(int(time.time())),
                "exp": str(int(time.time()) + 60*60),
                "ipv4": "0.0.0.0", # ToDo
                "token": token,
            }, "supergeheim", algorithm="HS256")

        return {
            "success": True,
            "jwt": enc_jwt
        }
    else:
        return {
            "success": False
        }