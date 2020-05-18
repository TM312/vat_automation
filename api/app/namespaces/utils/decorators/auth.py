from functools import wraps

from flask import request, g
from werkzeug.exceptions import Unauthorized, Forbidden

from ...auth.service import TokenService


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if request.headers.get("Authorization"):
            # get user via authorization token
            user = TokenService.current_user(request.headers["Authorization"])
            # make user available down the pipeline via flask.g
            g.user = user
            # finally call f. [f() now has access to g.user]
            return f(*args, **kwargs)
        else:
            raise Unauthorized('You are not authorized to access the resource. Please provide a valid auth token.')

    return wrap

# acccepted_roles accepts arguments (more info here: https://blog.miguelgrinberg.com/post/the-ultimate-guide-to-python-decorators-part-iii-decorators-with-arguments)
def accepted_roles(*roles):
    def accepted_roles_inner_decorator(f):
        @wraps(f)
        def wrap(*args, **kwargs):
            # user is available from @login_required
            for role in roles:
                if g.user.role == role:
                    return f(*args, **kwargs)
            raise Forbidden('You do not possess the rights to access the requested resource.')

        return wrap
    return accepted_roles_inner_decorator




def accepted_u_types(*u_types):
    def accepted_u_types_inner_decorator(f):
        @wraps(f)
        def wrap(*args, **kwargs):
            # user is available from @login_required
            for u_type in u_types:
                if g.user.u_type == u_type:
                    return f(*args, **kwargs)
            raise Forbidden('You do not possess the rights to access the requested resource.')

        return wrap
    return accepted_u_types_inner_decorator

#provides access to the resource only if the user's (mail) confirmation status is True
#to be used only in combination with login_required
def confirmation_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        #check for confirmation status
        if g.user.confirmed:
            return f(*args, **kwargs)
        else:
            raise Forbidden("You don't have the permission to access the requested resource. Please confirm your email for access.")

    return wrap


#provides access to the resource only if the user's (mail) confirmation status is True
#to be used only in combination with login_required
def employer_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        #check for confirmation status
        if g.user.employer:
            return f(*args, **kwargs)
        else:
            raise Forbidden(
                "You don't have the permission to access the requested resource. Please provide information about your company first.")

    return wrap
