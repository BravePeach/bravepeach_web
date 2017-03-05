from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login, logout
from .forms import UserRegistrationForm, UserEditForm, ProfileEditForm
from .models import Guide, Review
from django.core import serializers
from django.contrib.auth.decorators import login_required
from dateutil import parser


# def user_login(request):
#     if request.method =="POST":
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#             user = authenticate(email = cd['email'],
#                                 password = cd['password'])
#             if user is not None:
#                 if user.is_active:
#                     login(request, user)
#                     return HttpResponse('Authenticated successfully')
#                 else:
#                     return HttpResponse('Disabled account')
#         else:
#             return HttpResponse('invalid login')
#     else:
#         form = LoginForm()
#     return render(request, 'views/login.html',{'form':form})


def index(request):
    return render(request, "views/index.html", {})


def user_logout(request):
    logout(request)
    return HttpResponseRedirect(request.GET.get('next', '/'))


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        profile_form = ProfileEditForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            profile_form.save()
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            this_user = authenticate(username=user_form.cleaned_data['username'],
                                     password=user_form.cleaned_data['password'],
                                     )
            login(request, this_user)
            return render(request, 'views/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
        profile_form = ProfileEditForm()
    return render(request, 'views/register.html', {'user_form': user_form,
                                                   'profile_form': profile_form})


def guide_search(request):
    return render(request, 'views/guide_search.html', {})


# class GuideSearch(ListView):
#
#     def get(self, request):
#         location = request.GET.get('location')
#         start_date = request.GET.get('start_date')
#         end_date = request.GET.get('end_date')
#         traveler_cnt = request.GET.get('traveler_cnt')
#
#     queryset = Guide.objects.all().filter(max_traveler_cnt__gte=)
#     paginate_by = 9
#     template_name = 'webapp/templates/views/guide_search.html'

def filtering(request):
    result = []
    if request.method == 'GET':
        location = request.GET.get('location')
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        traveler_cnt = request.GET.get('traveler_cnt')

        guide_queryset = Guide.objects.all()
        if traveler_cnt:
            guide_queryset = guide_queryset.filter(max_traveler_cnt__gte=traveler_cnt)

        if bool(start_date) & bool(end_date):
            travel_date = []
            for i in range(int(start_date.replace('.', '')), int(end_date.replace('.', '')) + 1):
                travel_date.append(str(i))
            guide_queryset = guide_queryset.exclude(off_day__has_any_keys=travel_date)

        for guide in guide_queryset:
            temp = {'rating': guide.rating, 'pay_cnt': guide.pay_cnt, 'guide_location': guide.guide_location,
                    'first_name': guide.user.first_name, 'last_name': guide.user.last_name,
                    'review_num': Review.objects.filter(receiver=guide.user.username).count()}
            result.append(temp)

    return JsonResponse(result, safe=False)


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
                                       data=request.POST,
                                       files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            request.user.profile.birthday = profile_form.cleaned_data['birthday']
            user_form.save()
            profile_form.save()
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'views/edit_profile.html',
                  {'user_form': user_form, 'profile_form': profile_form}
                  )
