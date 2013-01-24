from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response

from faqs.models import FrequentlyAskedQuestion

from cal_util.view_util import get_common_lookup
from cal_util.msg_util import *

from django.core.urlresolvers import reverse

def view_faqs(request):

    lu = get_common_lookup(request)

    if not request.user.is_authenticated():
        lu.update({ 'ERR_found' : True\
                , 'ERR_not_authenticated' : True\
                , 'next_link_if_not_logged_in' : reverse('view_faqs', kwargs={})
                 })
        return render_to_response('faqs/faq_listing.html', lu, context_instance=RequestContext(request))
    
    lu.update({ 'faqs' : FrequentlyAskedQuestion.objects.filter(is_visible=True)
            
            })

    return render_to_response('faqs/faq_listing.html', lu, context_instance=RequestContext(request))

