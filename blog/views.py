from django.shortcuts import render, redirect
from .models import Post, FollowUser, LikePost, Comment
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from authentication.models import Profile


@login_required(login_url='/auth/signin/')
def search_view(request):
    query = request.GET.get('q')

    if query is '':
        return redirect('/')

    profile = Profile.objects.filter(user=request.user).first()
    posts = Post.objects.filter(is_published=True, author=query).order_by('-created_at')
    users = User.objects.filter()
    foll = [i.following for i in FollowUser.objects.filter(follower=r.user.id)]

    context = {
        'profile': profile,
        'foll': foll,
        'users': users,
        'posts': posts,
    }

    return render(request, 'index.html', context)


@login_required(login_url='/auth/signin/')
def home_view(r):
    if r.method == 'POST':
        Comment.objects.create(message=r.POST['message'],
                               post_id=r.POST['post_id'],
                               author_id=r.user.id).save()

        return redirect(f'/#{r.POST["post_id"]}')

    fo = FollowUser.objects.filter(follower=r.user)
    # for i in fo:
    posts = Post.objects.filter(is_published=True)

    profile = Profile.objects.filter(user=r.user).first()

    comments = Comment.objects.all()
    for post in posts:
        post.comments = comments.filter(post_id=post.id)

    users = User.objects.filter()
    foll = [i.following for i in FollowUser.objects.filter(follower=r.user.id)]

    context = {
        'posts': posts,
        'users': users,
        'profile': profile,
        'foll': foll,
    }

    return render(r, 'index.html', context)


@login_required(login_url='/auth/signin/')
def follow(r):
    follower = User.objects.filter(id=r.user.id).first()
    following = User.objects.filter(id=r.GET.get('following_id')).first()

    FollowUser.objects.create(follower=follower, following=following).save()

    return redirect('/')


@login_required(login_url='/auth/signin/')
def like(r):
    if r.user in [i.author for i in LikePost.objects.filter(post_id=r.GET.get('post_id'))]:
        LikePost.objects.filter(author=r.user,
                                post_id=r.GET.get('post_id')).delete()
    else:
        LikePost.objects.create(author=r.user,
                                post_id=r.GET.get('post_id')).save()

    return redirect(f'/#{r.GET.get("post_id")}')


@login_required(login_url='/auth/signin/?next=/profile/')
def profile_view(r):
    profile = Profile.objects.filter(user=r.user).first()

    context = {
        'profile': profile
    }
    return render(r, 'profile.html', context)


@login_required(login_url='/auth/signin/?next=/settings/')
def settings_view(r):
    return render(r, 'setting.html')


@login_required(login_url='/auth/signin/')
def upload(r):
    if r.method == 'POST':
        Post.objects.create(author_id=r.user.id,
                            image=r.FILES['file']).save()

        return redirect('/')
