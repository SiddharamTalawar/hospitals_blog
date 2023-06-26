from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from .models import post,Profile
from django.views.generic import ListView,CreateView,DetailView,UpdateView,DeleteView
from .forms import add_post_form,ProfilePage_Form
from django.urls import  reverse_lazy,reverse


class HomeView(ListView):
    """this view returns all the bolg posts which are not saved as drafts to home page."""
    template_name = 'home.html'
    def get_queryset(self):
        queryset = post.objects.filter(draft=False).order_by('-date_created')
        return queryset
    




class add_postview(CreateView):
    """this view allows users to create post."""
    model=post
    form_class= add_post_form
    template_name ='add_post.html'
    
    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    


class artical_detailview(DetailView):
    model=post
    template_name='artical_detail.html'


class upadte_post_view(UpdateView):
    model=post
    template_name = 'update_post.html'
    fields= ("title","summary","content","category","post_image","draft")

class delete_post_view(DeleteView):
    model=post
    template_name='delete_post.html'
    success_url = reverse_lazy('home')


def categoryview(request, cat):
    """sorts post according to given category"""
    Post=post.objects.filter(category=cat).filter(draft=False).order_by('-date_created')
    context={'Post':Post,'category':cat}
    return render(request,'Category_post_List.html',context)    

class Create_ProfilePage_View(CreateView):
	model = Profile
	form_class = ProfilePage_Form
	template_name = "registration/create_user_profile_page.html"
	

	def form_valid(self, form):
		form.instance.user = self.request.user
		return super().form_valid(form)



class Show_ProfilePage_View(DetailView):
	model = Profile
	template_name = 'registration/user_profile.html'

	def get_context_data(self, *args, **kwargs):
		context = super(Show_ProfilePage_View, self).get_context_data(*args, **kwargs)
		page_user = get_object_or_404(Profile, id=self.kwargs['pk'])

		context["page_user"] = page_user
		return context

class upadte_profile_view(UpdateView):
    model=Profile
    template_name = 'registration/update_profile.html'
    form_class=ProfilePage_Form


def my_post_view(request):
     user=request.user
     my_post = post.objects.filter(author=user).order_by('-date_created')
     context = {'my_post':my_post}
     return render(request, 'my_post.html', context)