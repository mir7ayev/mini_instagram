from django.shortcuts import render, redirect
from .models import Post, FollowUser, LikePost, Comment
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from authentication.models import Profile


@login_required(login_url='/auth/signin/')
def home_view(r):
    if r.method == 'POST':
        Comment.objects.create(message=r.POST['message'],
                               post_id=r.POST['post_id'],
                               author_id=r.user.id).save()

        return redirect(f'/#{r.POST["post_id"]}')

    posts = Post.objects.filter(is_published=True)
    users = User.objects.all()[:5]
    profile = Profile.objects.filter(user=r.user).first()
    comments = Comment.objects.all()

    for post in posts:
        post.comments = comments.filter(post_id=post.id)

    # obj = FollowUser.objects.filter(follower=r.user)

    # p = {}
    # for i in obj:
    #     p = (Post.objects.filter(author=i.following))
    # print('=' * 50)
    # print(p)
    # print('=' * 50)

    context = {
        'posts': posts,
        'users': users,
        'profile': profile,
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
    post_id = r.GET.get('post_id')

    LikePost.objects.create(author_id=r.user.id,
                            post_id=post_id).save()

    return redirect(f'/#{post_id}')


@login_required(login_url='/auth/signin/?next=/profile/')
def profile_view(r):
    return render(r, 'profile.html')


@login_required(login_url='/auth/signin/?next=/settings/')
def settings_view(r):
    return render(r, 'setting.html')
