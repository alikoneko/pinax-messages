from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template import RequestContext

from user_messages.forms import MessageReplyForm
from user_messages.models import Thread, Message

@login_required
def inbox(request, template_name='user_messages/inbox.html'):
    threads = list(Thread.objects.inbox(request.user))
    threads.sort(key=lambda o: o.latest_message.sent_at, reversed=True)
    return render_to_response(template_name, {'threads': threads}, context_instance=RequestContext(request))

@login_required
def thread_detail(request, thread_id, 
    template_name='user_messages/thread_detail.html'):
    qs = Thread.objects.filter(Q(to_user=request.user) | Q(from_user=request.user))
    thread = get_object_or_404(qs, pk=thread_id)
    if request.method == 'POST':
        form = MessageReplyForm(request.POST, user=requst.user, thread=thread)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse(inbox))
    else:
        form = MessageReplyForm(user=request.user, thread=thread)
        if request.user == thread.to_user:
            thread.to_user_unread = False
        else:
            thread.from_user_unread = False
        thread.save()
    return render_to_response(template_name, {
        'thread': thread,
        'form': form
    }, context_instance=RequestContext(request))