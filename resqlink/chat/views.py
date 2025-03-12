from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import Conversation, Message
from django.utils import timezone
from django.db.models import Q
from django.http import HttpResponseForbidden

User = get_user_model()

@login_required
def user_search(request):
    """
    Display a search bar to find other users by username.
    If a query is provided, show matching results.
    """
    query = request.GET.get('q', '')  # the search term
    results = []

    if query:
        # exclude the current user from the results
        results = User.objects.filter(username__icontains=query).exclude(pk=request.user.pk)

    return render(request, 'chat/user_search.html', {'query': query, 'results': results})


@login_required
def start_conversation(request, user_id):
    """
    If a conversation between request.user and user_id doesn't exist, create it.
    Then redirect to the conversation detail page.
    """
    target_user = get_object_or_404(User, pk=user_id)
    if target_user == request.user:
        # Optionally handle if someone tries to chat with themselves
        return redirect('user_search')

    # Check if a conversation already exists
    conversation = (Conversation.objects.filter(
        participant1__in=[request.user, target_user],
        participant2__in=[request.user, target_user]
    ).first())

    # If no conversation found, create one
    if not conversation:
        conversation = Conversation.objects.create(
            participant1=request.user,
            participant2=target_user
        )

    return redirect('conversation_detail', conversation_id=conversation.id)


@login_required
def conversation_detail(request, conversation_id):
    conversation = get_object_or_404(Conversation, pk=conversation_id)

    # Check if the user is one of the participants
    if request.user not in [conversation.participant1, conversation.participant2]:
        return HttpResponseForbidden("You don't have access to this conversation.")

    # If the user posted a new message
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Message.objects.create(
                conversation=conversation,
                sender=request.user,
                content=content,
                timestamp=timezone.now()
            )
        return redirect('conversation_detail', conversation_id=conversation_id)

    # For GET requests, show the conversation messages
    messages = conversation.messages.order_by('timestamp')
    other_user = conversation.participant2 if conversation.participant1 == request.user else conversation.participant1

    return render(request, 'chat/conversation_detail.html', {
        'conversation': conversation,
        'messages': messages,
        'other_user': other_user
    })



@login_required
def conversation_list(request):
    """
    Show all conversations where request.user is a participant.
    """
    conversations = Conversation.objects.filter(
        Q(participant1=request.user) | Q(participant2=request.user)
    ).order_by('-created_at')

    return render(request, 'chat/conversation_list.html', {'conversations': conversations})
