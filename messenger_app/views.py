from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Message
from user_app.models import User


@login_required
def send_message(request):
    if request.method == "POST":
        try:
            recipient_username = request.POST.get('receiver').capitalize()
            content = request.POST.get('message')

            try:
                recipient = User.objects.get(username=recipient_username)
            except User.DoesNotExist:
                return render(request, 'send.html', {
                    'error': 'Recipient not found'
                })

            message = Message(sender=request.user, recipient=recipient)
            message.encrypt_content(content)
            message.save()

            return redirect(f"{reverse('inbox')}?sender={recipient_username}")
        
        except User.DoesNotExist:
            return render(request, 'send.html', {
                'error': 'Recipient not found'
            })
        except Exception as e:
            return render(request, 'send.html', {
                'error': f'An error occurred: {str(e)}'
            })

    return render(request, 'send.html')


@login_required
def inbox(request):
    messages = Message.objects.filter(recipient=request.user) | Message.objects.filter(sender=request.user)
    messages = messages.order_by('-timestamp')

    user_ids = set(
        list(messages.values_list('sender_id', flat=True).distinct()) +
        list(messages.values_list('recipient_id', flat=True).distinct())
    ) - {request.user.id}

    senders = [User.objects.get(id=user_id).username for user_id in user_ids]

    selected_sender = request.GET.get('sender')
    if not selected_sender and senders:
        selected_sender = senders[0]

    decrypted_messages = []
    if selected_sender:
        try:
            selected_user = User.objects.get(username=selected_sender)
            selected_messages = messages.filter(
                sender=selected_user, recipient=request.user
            ) | messages.filter(
                sender=request.user, recipient=selected_user
            )
            selected_messages = selected_messages.order_by('timestamp')

            decrypted_messages = [
                (
                    message.sender.username,
                    message.decrypt_content(),
                    message.timestamp.strftime('%Y-%m-%d %H:%M:%S')
                )
                for message in selected_messages
            ]
        except User.DoesNotExist:
            decrypted_messages = []
            selected_sender = None

    return render(request, 'inbox.html', {
        'senders': senders,
        'selected_sender': selected_sender,
        'messages': decrypted_messages,
        'user': request.user
    })