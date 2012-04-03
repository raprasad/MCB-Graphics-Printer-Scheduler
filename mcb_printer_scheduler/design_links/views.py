
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

from design_links.models import Organization

from cal_util.view_util import get_common_lookup
from cal_util.msg_util import *

from django.core.urlresolvers import reverse

def view_logo_listing(request):

    lu = get_common_lookup(request)

    if not request.user.is_authenticated():
        lu.update({ 'ERR_found' : True, 'ERR_not_authenticated' : True })
        return render_to_response('design_links/logo_listing.html', lu, context_instance=RequestContext(request))

    base_qs = Organization.objects.filter(is_visible=True)
    
    lu.update({ 'primary_organizations' : base_qs.filter(is_primary=True)\
                , 'other_organizations' : base_qs.filter(is_primary=False)\
            })

    return render_to_response('design_links/logo_listing.html', lu, context_instance=RequestContext(request))


        
