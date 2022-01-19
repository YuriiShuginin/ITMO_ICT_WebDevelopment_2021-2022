from django.shortcuts import render
from board_app.models import User, Homework, TaskCompletion
from django.views.generic import TemplateView, ListView, DetailView, UpdateView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from board_app.forms import SolutionForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required


class StudentUpdate(UpdateView):
    model = User
    template_name = 'board_app/user_update.html'
    fields = ["surname", "name", "patronymic", "birthday", "group"]
    success_url = '/profile/'


class AllTasks(LoginRequiredMixin, ListView):
    login_url = '/accounts/login/'
    
    def get(self, request, *args, **kwargs):
        user = self.request.user
        context = {}

        context['user'] = user
        context['task_list'] = Homework.objects.filter(group=user.group)
        
        answers = TaskCompletion.objects.filter(student_id=user.id)
        context['answers'] = answers
        
        context['hw_ids'] = []
        for answer in answers:
            context['hw_ids'].append(answer.homework_id)
        
        return render(request, 'board_app/all_tasks.html', context)


class NotificationView(LoginRequiredMixin, TemplateView):
    login_url = '/accounts/login/'

    def get(self, request, *args, **kwargs):
        context = {}
        context["edit_link"] = f"/accounts/{self.request.user.id}/update/"
        return render(request, 'board_app/account_created.html', context)


class StartPageView(TemplateView):
    def get(self, request, *args, **kwargs):
        return render(request, 'board_app/start_page.html')


class ProfilePageView(LoginRequiredMixin, TemplateView):
    login_url = '/accounts/login/'

    def get(self, request, *args, **kwargs):
        context = {}
        context["edit_link"] = f"/accounts/{self.request.user.id}/update/"
        context["user"] = self.request.user
        return render(request, 'board_app/profile_page.html', context)


@login_required
def solution_create(request):
    task_id = request.GET.get('task_id')
    context = {}

    if request.method == 'POST':
        form = SolutionForm(Homework.objects.get(pk=task_id), request.user, request.POST)

        if form.is_valid():
            form.save()
            return redirect('/profile/all_tasks/')
    
    else:
        form = SolutionForm(Homework.objects.get(pk=task_id), request.user)
        context["form"] = form
        context['task'] = Homework.objects.get(pk=task_id)

    return render(request, 'board_app/solution.html' , context)