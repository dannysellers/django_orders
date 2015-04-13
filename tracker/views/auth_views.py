from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib import messages
from django.http import HttpResponseRedirect
from forms import UserForm


def register (request):
    """
    Handles registering new Operators---backend users not
    associated with any Customer accounts.
    """
    context = RequestContext(request)
    context_dict = {}

    if request.method == 'POST':
        user_form = UserForm(data = request.POST)

        if user_form.is_valid():
            user = user_form.save()

            user.set_password(user.password)

            operator_group = Group.objects.get_by_natural_key('Operator')
            user.groups.add(operator_group)

            user.save()

            messages.add_message(request, messages.SUCCESS, "User {} registered successfully".format(user.username))
            return HttpResponseRedirect('/', context)
        else:
            print user_form.errors
    else:
        user_form = UserForm()

    context_dict['form'] = user_form
    context_dict['form_type'] = 'register'

    return render_to_response('tracker/form.html', context_dict, context)


def user_login (request):
    context = RequestContext(request)

    if request.method == 'POST':
        # Login info is provided by the form
        username = request.POST['username']
        password = request.POST['password']

        # Use Django's built-in authentication function
        user = authenticate(username = username, password = password)

        # If no user is returned, login was unsuccessful
        if user:
            # Users in the Customer Group cannot log in
            # Users with no groups are improperly configured, and cannot log in
            customer_group = Group.objects.get_by_natural_key('Customer')
            if customer_group not in user.groups.all() and user.groups.count() > 0:
                # TODO: Possible security issue verifying User Group status *after* verifying credentials?
                if user.is_active:
                    if not request.POST.get('remember_me', None):
                        request.session.set_expiry(0)
                    login(request, user)
                    messages.add_message(request, messages.SUCCESS,
                                         "Login successful. Welcome, {}.".format(user.first_name))
                    # Return user to the same page they were on
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
                else:
                    messages.add_message(request, messages.ERROR, "This account is inactive and cannot be used.")
                    return HttpResponseRedirect('/')
            else:
                messages.add_message(request, messages.ERROR, "This account cannot be used to log in.")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        else:
            messages.add_message(request, messages.ERROR, "Invalid login info")
            return HttpResponseRedirect('/')
    else:
        return render_to_response('tracker/login.html', context)


@login_required
def user_logout (request):
    logout(request)

    messages.add_message(request, messages.SUCCESS, "Logged out successfully.")
    return HttpResponseRedirect('/')