"""
File: messaging/views.py
Author: Yusuf (Student 3)
Purpose: Views for inbox, conversation, compose, drafts, sent, and message actions.
Co-authors: None
"""

from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from .forms import MessageForm
from .models import Message

User = get_user_model()


def _get_conversation_list(user):
    sent_messages = Message.objects.filter(status='sent').filter(
        Q(sender=user) | Q(recipient=user)
    )
    partner_ids = set()
    for msg in sent_messages:
        if msg.sender == user:
            if msg.recipient_id:
                partner_ids.add(msg.recipient_id)
        else:
            partner_ids.add(msg.sender_id)
    conversations = []
    for pid in partner_ids:
        partner = User.objects.get(id=pid)
        latest = sent_messages.filter(
            Q(sender=user, recipient_id=pid) |
            Q(sender_id=pid, recipient=user)
        ).order_by('-created_at').first()
        conversations.append({'partner': partner, 'latest': latest})
    conversations.sort(key=lambda c: c['latest'].created_at, reverse=True)
    return conversations


@login_required
def inbox(request):
    unread_count = Message.objects.filter(
        recipient=request.user,
        status='sent',
        read_at__isnull=True
    ).count()

    return render(request, 'messaging/inbox.html', {
        'conversations': _get_conversation_list(request.user),
        'unread_count': unread_count,
    })


@login_required
def conversation(request, user_id):
    partner = get_object_or_404(User, id=user_id)
    messages = Message.objects.filter(
        Q(sender=request.user, recipient=partner) |
        Q(sender=partner, recipient=request.user)
    ).filter(status='sent').order_by('created_at')

    Message.objects.filter(
        sender=partner,
        recipient=request.user,
        status='sent',
        read_at__isnull=True
    ).update(read_at=timezone.now())

    form = MessageForm(user=request.user)
    return render(request, 'messaging/conversation.html', {
        'partner': partner,
        'messages': messages,
        'form': form,
        'conversations': _get_conversation_list(request.user),
    })


@require_POST
@login_required
def send_in_thread(request, user_id):
    partner = get_object_or_404(User, id=user_id)
    body = request.POST.get('body', '').strip()
    if body:
        Message.objects.create(
            sender=request.user,
            recipient=partner,
            subject='',
            body=body,
            status='sent',
            sent_at=timezone.now(),
        )
    return redirect('messages:conversation', user_id=user_id)


@login_required
def compose(request):
    initial = {}
    if request.method == 'GET':
        recipient_id = request.GET.get('recipient')
        if recipient_id:
            try:
                pre = User.objects.get(id=recipient_id)
                if pre != request.user:
                    initial['recipient'] = pre
            except User.DoesNotExist:
                pass

    if request.method == 'POST':
        form = MessageForm(request.POST, user=request.user)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.sender = request.user
            if 'send' in request.POST:
                msg.status = 'sent'
                msg.sent_at = timezone.now()
                msg.save()
                return redirect('messages:inbox')
            else:
                msg.status = 'draft'
                msg.save()
                return redirect('messages:drafts')
    else:
        form = MessageForm(initial=initial, user=request.user)

    return render(request, 'messaging/compose.html', {'form': form})


@login_required
def drafts(request):
    draft_list = Message.objects.filter(sender=request.user, status='draft')
    return render(request, 'messaging/drafts.html', {'drafts': draft_list})


@login_required
def sent(request):
    sent_list = Message.objects.filter(sender=request.user, status='sent')
    return render(request, 'messaging/sent.html', {'sent_messages': sent_list})


@require_POST
@login_required
def send_draft(request, message_id):
    msg = get_object_or_404(Message, id=message_id, sender=request.user)
    msg.status = 'sent'
    msg.sent_at = timezone.now()
    msg.save()
    return redirect('messages:inbox')


@require_POST
@login_required
def delete_message(request, message_id):
    msg = get_object_or_404(Message, id=message_id, sender=request.user)
    msg.delete()
    return redirect('messages:inbox')
