from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .forms import NewTopicForm
from .forms import PostForm
from .models import Board, Topic, Post
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


def home(request):
    boards = Board.objects.all()
    return render(request, 'home.html', {'boards': boards})
    # boards_names = list()

    # for board in boards:
    #     boards_names.append(board.name)
    #
    #     response_html = '<br>'.join(boards_names)
    #
    # return HttpResponse(response_html)


def board_topics(request, pk):
    board = Board.objects.get(pk=pk)
    return render(request, 'topics.html', {'board': board})


@login_required(login_url='/login/?next=/boards/1/new/')
def new_topic(request, pk):
    board = get_object_or_404(Board, pk=pk)

    user = User.objects.first()  # TODO: get the currently logged in user
    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = request.user
            topic.save()
            post = Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=request.user
            )
            return redirect('board_topics', pk=board.pk)  # TODO: redirect to the created topic page
    else:
        form = NewTopicForm()
    return render(request, 'new_topic.html', {'board': board, 'form': form})


def topic_posts(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    return render(request, 'topic_posts.html', {'topic': topic})


@login_required
def reply_topic(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.save()
            return redirect('topic_posts', pk=pk, topic_pk=topic_pk)
    else:
        form = PostForm()
    return render(request, 'reply_topic.html', {'topic': topic, 'form': form})
