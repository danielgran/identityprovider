import api.base as base

import sqlalchemy


def register_user(obj, info, email):

    print(str(info.context.remote_addr) + "HURE")
    try:
        result = base.db.session.execute(sqlalchemy.text("call sp_addNewUser(:email)"), [{"email": data.request.email}])
        base.db.session.commit()
    except:
        print("An exception occured")

    #print(result.all())
    return {
        "success": True
    }
    #api.base.db.engine.execute("CALL dbidentityprovider.sp_addNewUser('whee.whee@whewhe.we');")




