from django.http import HttpResponse
from django.shortcuts import redirect

# our first decorator
def unauthenticated_user (view_func):
    def wrapper_func (request, *args, **kwargs):        # https://www.geeksforgeeks.org/args-kwargs-python/
        # actual code
        if request.user.is_authenticated:
            return redirect ('home')
        else:
            return view_func (request, *args, **kwargs)

    return wrapper_func


# the structure for this decorator is different as it takes more parameters than just view_function

def allowed_users (allowed_roles=[]):                   # like we have passed the parameter here in views.py -> @login_required (login_url = 'login')
    def decorator (view_func):
        def wrapper_func (request, *args, **kwargs):

            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name       # first group in the list of the user's groups. Current assumption - one user is only in one group

            print (group)

            if group in allowed_roles:
                return view_func (request, *args, **kwargs)

            else:
                return HttpResponse ("You are not authorized to view this page")            
    
        return wrapper_func
    
    return decorator


def admin_only(view_func):
    def wrapper_func (request, *args, **kwargs):
        group = None
        if request.user.groups.exists ():
            group = request.user.groups.all()[0].name
        
        if group == 'customer':
            return redirect ('user-page')

        if group == 'admin':
            return view_func (request, *args, **kwargs)

    return wrapper_func