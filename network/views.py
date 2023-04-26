from .models import User, Post
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from faker import Faker


def index(request):
    if request.method == "POST":
        user = request.user
        if "create_post" in request.POST.values():
            # Create new post
            content = request.POST["content"]
            post = Post(user=user, content=content)
            post.save()

        elif "edit_post" in request.POST.values():
            # Edit post content
            post_id = request.POST["post_id"]
            content = request.POST["content"]
            post = Post.objects.get(id=post_id)
            post.content = content
            post.save()

        else:
            # Like post
            post_id = request.POST["post_id"]
            post = Post.objects.get(id=post_id)
            if user in post.likes.all():
                post.likes.remove(user)
                liked = False
            else:
                post.likes.add(user)
                liked = True

            # Return updated data
            data = {"liked": liked, "likes": len(post.likes.all())}
            return JsonResponse(data, status=200)

    # Get all posts
    posts = Post.objects.order_by("-timestamp").all()

    # Apply pagination
    paginator = Paginator(posts, 10)
    current_page = request.GET.get("page")
    page_obj = paginator.get_page(current_page)
    pages = [page for page in paginator.page_range]

    return render(request, "network/index.html", {"page_obj": page_obj, "pages": pages})


@login_required
def following(request):
    user = request.user
    if request.method == "POST":
        if "create_post" in request.POST.values():
            # Create new post
            user = request.user
            content = request.POST["content"]
            post = Post(user=user, content=content)
            post.save()

        elif "edit_post" in request.POST.values():
            # Edit post content
            post_id = request.POST["post_id"]
            content = request.POST["content"]
            post = Post.objects.get(id=post_id)
            post.content = content
            post.save()

        else:
            # Like post
            post_id = request.POST["post_id"]
            post = Post.objects.get(id=post_id)
            if user in post.likes.all():
                post.likes.remove(user)
                liked = False
            else:
                post.likes.add(user)
                liked = True

            # Return updated data
            data = {"liked": liked, "likes": len(post.likes.all())}
            return JsonResponse(data, status=200)

    # Get all posts made by users that the user follows
    following_users = []
    for profile in user.profile.following.all():
        following_users.append(profile.user)
    posts = Post.objects.order_by("-timestamp").filter(user__in=following_users)

    # Apply pagination
    paginator = Paginator(posts, 10)
    current_page = request.GET.get("page")
    page_obj = paginator.get_page(current_page)
    pages = [page for page in paginator.page_range]

    return render(request, "network/following.html", {"page_obj": page_obj, "pages": pages})


def profile(request, username):
    profile = User.objects.get(username=username).profile
    if request.method == "POST":
        if "edit_post" in request.POST.values():
            # Edit post content
            post_id = request.POST["post_id"]
            content = request.POST["content"]
            post = Post.objects.get(id=post_id)
            post.content = content
            post.save()

        elif "like" in request.POST.values():
            # Like post
            user = request.user
            post_id = request.POST["post_id"]
            post = Post.objects.get(id=post_id)
            if user in post.likes.all():
                post.likes.remove(user)
                liked = False
            else:
                post.likes.add(user)
                liked = True

            # Return updated data
            data = {"liked": liked, "likes": len(post.likes.all())}
            return JsonResponse(data, status=200)

        else:
            # Follow/Unfollow profile
            following = request.user.profile.following
            if profile in following.all():
                following.remove(profile)
                follows = False
            else:
                following.add(profile)
                follows = True

            # Return updated data
            data = {"follows": follows, "followers": len(profile.followers.all())}
            return JsonResponse(data, status=200)

    # Get all posts made by the profile's user
    posts = profile.user.posts.order_by("-timestamp").all()

    # Apply pagination
    paginator = Paginator(posts, 10)
    current_page = request.GET.get("page")
    page_obj = paginator.get_page(current_page)
    pages = [page for page in paginator.page_range]

    return render(request, "network/profile.html", {"profile": profile, "page_obj": page_obj, "pages": pages})


@csrf_exempt
def login_view(request):
    if request.method == "POST":
        # Check if user logged in with demo user
        if "demo_user" in request.POST:
            fake = Faker()

            # Generate random user info
            username = fake.user_name()
            email = fake.email()
            password = fake.password()

            # Register demo user
            demo_user = User.objects.create_user(username, email, password)
            demo_user.save()

            # Log user in
            login(request, demo_user)

            # Redirect user to home page
            return HttpResponseRedirect(reverse("index"))
        else:
            # Attempt to sign user in
            username = request.POST["username"]
            password = request.POST["password"]
            user = authenticate(request, username=username, password=password)

            # Check if authentication successful
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse("index"))
            else:
                return render(request, "network/login.html", {"message": "Invalid username and/or password."})
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {"message": "Passwords must match."})

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {"message": "Username already taken."})
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
