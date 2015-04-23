from datetime import date, timedelta

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib import messages
from django.contrib.auth.views import password_reset, password_reset_confirm
from django.core.urlresolvers import reverse

from django.db.models import Sum
from django.template import RequestContext
from django.shortcuts import render_to_response, HttpResponseRedirect, render
from ..models import Shipment, Inventory, Customer, WorkOrder


def index (request):
    context = RequestContext(request)
    context_dict = dict()

    if not request.user.is_authenticated():
        return render_to_response('tracker/login.html', context_dict, context)
    else:
        context_dict['cust_act_count'] = Customer.objects.filter(status = 1).count()
        context_dict['item_count'] = Inventory.objects.exclude(status = 4).count()
        context_dict['ship_count'] = Shipment.objects.exclude(status = 4).count()
        context_dict['total_item_volume'] = Inventory.objects.exclude(status = 4).aggregate(
            Sum('volume'))['volume__sum']
        context_dict['work_order_count'] = WorkOrder.objects.exclude(status = 4).exclude(
            status = 999).count()
        context_dict['unmatched_orders'] = WorkOrder.objects.exclude(status = 4).exclude(
            status = 999).exclude(shipment__isnull = False).count()

        ten_days_ago = date.today() - timedelta(days = 10)

        context_dict['item_storage_count'] = Inventory.objects.exclude(status = 4) \
            .filter(arrival__lte = ten_days_ago).count()
        context_dict['item_no_storage_count'] = Inventory.objects.exclude(status = 4) \
            .filter(arrival__range = (ten_days_ago, date.today())).count()

        return render_to_response('tracker/index.html', context_dict, context)


def reset (request):
    """ Wrap the built-in password reset view and pass it the arguments
    like the template name, email template name, subject template name
    and the url to redirect after the password reset is initiated.

    These views aren't login-restricted because end-users will be able to
    use these views to reset their passwords (at least until I write an
    equivalent API endpoint). """
    # From http://runnable.com/UqMu5Wsrl3YsAAfX/using-django-s-built-in-views-for-password-reset-for-python
    return password_reset(request, template_name = 'reset.html',
                          email_template_name = 'reset_email.html',
                          subject_template_name = 'reset_subject.txt',
                          post_reset_redirect = reverse('password_reset_success'))


def reset_confirm (request, uidb64=None, token=None):
    op_group = Group.objects.get_by_natural_key('Operator')

    if op_group not in request.user.groups:
        messages.add_message(request, messages.ERROR, "Your account does not have the \
        appropriate permissions. Please contact an administrator.")
        # TODO: Log these things
        return HttpResponseRedirect('/')
    else:
        return password_reset_confirm(request, template_name = 'reset_confirm.html',
                                      uidb64 = uidb64, token = token,
                                      post_reset_redirect = reverse('password_reset_success'))


def success (request):
    return render(request, 'success.html')