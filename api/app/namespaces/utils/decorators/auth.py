from functools import wraps

from flask import request, g
from werkzeug.exceptions import Unauthorized, Forbidden

from ...auth.service import TokenService

#https://stackoverflow.com/questions/653368/how-to-create-a-python-decorator-that-can-be-used-either-with-or-without-paramet
def doublewrap(f):
    '''
    a decorator decorator, allowing the decorator to be used as:
    @decorator(with, arguments, and=kwargs)
    or
    @decorator
    '''
    @wraps(f)
    def new_dec(*args, **kwargs):
        if len(args) == 1 and len(kwargs) == 0 and callable(args[0]):
            # actual decorated function
            return f(args[0])
        else:
            # decorator arguments
            return lambda realf: f(realf, *args, **kwargs)

    return new_dec


def login_required(f):
    # @wraps(f)
    def wrap(*args, **kwargs):
        if request.headers.get("Authorization"):
            # get user via authorization token
            user = TokenService.current_user(request.headers["Authorization"])
            # make user available down the pipeline via flask.g
            g.user = user
            user.update_last_seen()
            # finally call f. [f() now has access to g.user]
            return f(*args, **kwargs)
        else:
            raise Unauthorized('You are not authorized to access the resource. Please provide a valid auth token.')

    return wrap

# accepted_u_types accepts arguments (more info here: https://blog.miguelgrinberg.com/post/the-ultimate-guide-to-python-decorators-part-iii-decorators-with-arguments)
# also: https://www.artima.com/weblogs/viewpost.jsp?thread=240845#decorator-functions-with-decorator-arguments


def accepted_u_types(*u_types):
    def accepted_u_types_inner_decorator(f):
        # @wraps(f)
        def wrap(*args, **kwargs):
            # user is available from @login_required
            # # admin is always able to enter
            # if g.user.u_type == 'admin':
            #     return f(*args, **kwargs)
            # else:
            for u_type in u_types:
                if g.user.u_type == u_type:
                    return f(*args, **kwargs)
            raise Forbidden('You do not possess the rights to access the requested resource.')

        return wrap
    return accepted_u_types_inner_decorator



def accepted_roles(*roles):
    def accepted_roles_inner_decorator(f):
        @wraps(f)
        def wrap(*args, **kwargs):
            # user is available from @login_required
            for role in roles:
                if g.user.role == role or g.user.u_type == 'admin':
                    return f(*args, **kwargs)
            raise Forbidden(
                'You do not possess the rights to access the requested resource.')

        return wrap
    return accepted_roles_inner_decorator

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
