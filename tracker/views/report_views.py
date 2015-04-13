from datetime import date, timedelta
from calendar import monthrange
import json
import psycopg2

from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
from django.db.models import Model
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

from .. import models
from ..utils import find_subclasses


@login_required
def reports (request):
    """
    Initial page view for /reports/
    """
    context = RequestContext(request)
    context_dict = dict()

    today = date.today()
    context_dict['first_day'] = date(today.year, today.month, 1)
    context_dict['last_day'] = date(today.year, today.month, monthrange(today.year, today.month)[1])

    context_dict['model_list'] = [i.__name__ for i in find_subclasses(models, Model, 'tracker.models')]

    return render_to_response('tracker/graphs.html', context_dict, context)


@csrf_exempt
def form_ajax (request, model_name):
    """
    Function to handle returning attributes for selected model.
    """
    context_dict = dict()

    model_list = find_subclasses(models, Model, 'tracker.models')
    for model in model_list:
        if model.__name__ == model_name:
            _model = model

    context_dict['attr_list'] = [field.name for field in _model._meta.fields]

    return HttpResponse(json.dumps(context_dict), content_type = 'application/json')


@csrf_exempt
def graph_query (request):
    """
    query should be [MODEL]_[ATTRIBUTE]_[OPERATION]
    """
    if request.method != 'GET':
        messages.add_message(request, messages.ERROR, "That URL doesn't accept POSTs.")
        return HttpResponseRedirect('/reports/')
    else:
        today = date.today()
        last_day_of_month = monthrange(today.year, today.month)[1]
        returned_data = dict()

        # Parse dates
        start_date = request.GET.get('start')
        if not start_date:
            start_date = date(today.year, today.month, 1)
        else:
            try:
                _year, _month, _day = start_date.split('-')
                start_date = date(int(_year), int(_month), int(_day))
            except TypeError:
                start_date = date(today.year, today.month, 1)

        finish_date = request.GET.get('finish')
        if not finish_date:
            finish_date = date(today.year, today.month, last_day_of_month)
        else:
            try:
                _year, _month, _day = finish_date.split('-')
                finish_date = date(int(_year), int(_month), int(_day))
            except TypeError:
                finish_date = date(today.year, today.month, last_day_of_month)

        td = finish_date - start_date
        day_labels = range(1, td.days)[::3]

        # Axis labels for dict to return
        returned_data['labels'] = [str(start_date + timedelta(days = day_labels[index])) for index, d in
                                   enumerate(day_labels)]

        # Parse query
        query = request.GET.get('query')
        # 'shipment_num_count', 'inventory_volume_total'
        query_model, query_attr, query_op = query.split(",")

        query_summation = request.GET.get('summation')

        # get model from list of classes under 'tracker.models'
        model_list = find_subclasses(models, Model, 'tracker.models')
        for model in model_list:
            if model.__name__.lower() == query_model:
                query_model = model

        if query_model.__name__.lower() == 'customer':
            query_index = 'createdate'
        elif query_model.__name__.lower() == 'inventory' or query_model.__name__.lower() == 'shipment':
            query_index = 'arrival'
        elif query_model.__name__.lower() == 'optextras':
            query_index = 'tracker_shipment.arrival'
        else:
            query_index = 'dt'

        _table = 'tracker_{}'.format(query_model.__name__.lower())

        # get attribute from list
        # TODO: Alternative to _meta call?
        for field in query_model._meta.fields:
            if field.name == query_attr:
                query_attr = field

        count_dict = {}
        for index, day in enumerate(day_labels, start = 1):
            query = list()

            if query_op == 'count':
                query.append("SELECT COUNT(*) FROM %s " % _table)
            elif query_op == 'sum':
                query.append("SELECT SUM(%s) from %s " % (query_attr.name, _table))
            else:
                query.append("SELECT COUNT(*) FROM %s " % _table)

            if query_summation == 'cumulative':
                # cumulative throughout the whole period
                prev_date = start_date
            elif query_summation == 'per-interval':
                # cumulative during each sliver
                prev_date = start_date + timedelta(days = day_labels[index - 1])
            else:
                prev_date = start_date

            try:
                _date = start_date + timedelta(days = day_labels[index])
            except IndexError:
                _year, _month = start_date.year, start_date.month
                _date = date(_year, _month, monthrange(_year, _month)[1])

            if query_model.__name__.lower() == 'optextras':
                query.append(u"JOIN tracker_shipment ON tracker_optextras.shipment_id = tracker_shipment.id ")

            query.append(u"WHERE {0} BETWEEN \'{1}\' and \'{2}\';".format(
                query_index, str(prev_date), str(_date)))

            c = connection.cursor()
            try:
                c.execute("".join(query))
                cq = c.fetchall()
            except psycopg2.ProgrammingError as e:
                print(e)
            # return HttpResponse(json.dumps(e), content_type='application/json')
            count_dict[index] = cq

        # Chart.js options
        # TODO: Thinking about flot library now
        data_dict = dict()
        data_dict['label'] = query_model.__name__
        data_dict['fillColor'] = '#6886AD'
        data_dict['strokeColor'] = '#185BAD'
        data_dict['pointColor'] = "#5856AD"
        data_dict['pointStrokeColor'] = "#fff"
        data_dict['pointHighlightFill'] = "#6D61CD"
        data_dict['pointHighlightStroke'] = "#7F71EF"

        data_dict['data'] = count_dict.values()

        returned_data['datasets'] = [data_dict]

        returned_data['query'] = [q['sql'] for q in connection.queries]

        chart_args = dict()
        chart_args['bezierCurve'] = False
        chart_args['pointHitDetectionRadius'] = 10

        # TODO: A better way to serialize data for JSON
        return HttpResponse("[{},{}]".format(json.dumps(returned_data), json.dumps(chart_args)),
                            content_type = 'application/json')