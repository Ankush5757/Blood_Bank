from django.shortcuts import render, redirect


def auth_middleware(get_response):
    # One-time configuration and initialization.

    def middleware(request):
        if (request.path == '/dashboard/') and (request.session.get('id') is None) :
                return redirect('login/')
        
        if (request.path == '/login/' or request.path == 'register/') and (request.session.get('id') is not None) :
                return redirect('/dashboard/')
        

        response = get_response(request)

        return response

    return middleware



