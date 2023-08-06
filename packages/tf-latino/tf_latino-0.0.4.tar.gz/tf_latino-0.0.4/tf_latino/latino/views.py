# helperji, context stvari
from django.shortcuts import get_object_or_404
from django.http import HttpResponse

# modeli
from tf_latino.lib.serialization_utils import ToNetObj

from workflows.models import *
# auth fore
from django.contrib.auth.decorators import login_required

@login_required
def get_adc_index(request, widget_id, narrow_doc = 'n', document_id_from=0, document_id_to=-1):
    w = get_object_or_404(Widget, pk=widget_id)
    if w.workflow.user == request.user:
        firstInput = w.inputs.all()[0]
        dc = ToNetObj(firstInput.value)
        data = dc.MakeIndexPage(document_id_from, document_id_to, 100, narrow_doc)
        return HttpResponse(data, mimetype='text/html')
    else:
        return HttpResponse(status=400)

@login_required
def get_adc_page(request, widget_id, document_id, narrow_doc = 'n'):
    w = get_object_or_404(Widget, pk=widget_id)
    if w.workflow.user == request.user:
        firstInput = w.inputs.all()[0]
        dc = ToNetObj(firstInput.value)
        data = dc.MakeDocumentPage(document_id, narrow_doc)
        return HttpResponse(data, mimetype='text/html')
    else:
        return HttpResponse(status=400)
