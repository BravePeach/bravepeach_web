import datetime

from django.utils import timezone
from django.utils import formats
from django.views.generic import View, ListView
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from ..models import UserPost, UserComment
from ..forms import UserPostForm
from bravepeach.util import flavour_render
from django.contrib.auth.decorators import login_required


@login_required
def write_user_post(request, **kwargs):
    if request.method == "GET":
        form = UserPostForm()
        return flavour_render(request, "post/write_post.html", {"form": form})
    else:
        form = UserPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.writer = request.user
            post.save()
        return flavour_render(request, "post/user_post_detail.html", {"post": post})


class AddUserComment(View):
    def post(self, request):
        # EXAMPLE: 'HTTP_REFERER' = 'bravepeach.com/user_posts/123'
        post_id = int(request.environ.get('HTTP_REFERER').split('/')[-2])
        writer = request.user.id
        content = request.POST.get('content')
        UserComment.objects.create(writer_id=writer, content=content, post_id=post_id)
        c = UserComment.objects.all().last()
        result = {'content': c.content, 'written_date': formats.date_format(timezone.localtime(c.written_date), "Y.m.d H:i")}
        return JsonResponse(result)


class UserPostList(ListView):
    def is_mobile(self):
        return self.request.user_agent.is_mobile

    if is_mobile:
        template = 'pc/post/post_list.html'
    else:
        template = 'mobile/post/post_list.html'

    queryset = UserPost.objects.prefetch_related('user_post_hit', 'user_comment').select_related(
        'writer', 'writer__profile').all().order_by('-id')
    template_name = template
    model = UserPost
    paginate_by = 20
    context_object_name = 'posts'


def user_post_detail(request, user_post_id):
    post = get_object_or_404(UserPost.objects.prefetch_related('user_comment').filter(id=user_post_id))

    # if not UserPostHit.objects.filter(
    #         post_id=user_post_id,
    #         session=request.session.session_key):
    #     if not request.session.session_key:
    #         request.session.save()
    #
    #     hit = UserPostHit(
    #         post_id=user_post_id,
    #         ip=request.META['REMOTE_ADDR'],
    #         created=timezone.now(),
    #         session=request.session.session_key)
    #     hit.save()
    return flavour_render(request, "post/user_post_detail.html", {"post": post})
