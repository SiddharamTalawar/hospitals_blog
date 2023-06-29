
from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from .models import post,Profile,Appointment
from django.views.generic import ListView,CreateView,DetailView,UpdateView,DeleteView
from .forms import add_post_form,ProfilePage_Form
from django.urls import  reverse_lazy,reverse
from datetime import timedelta
import datetime
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/calendar']










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
    
    #adding the user automatically.
    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    


class artical_detailview(DetailView):
    """provides detail view of blog post whoes pk is provided."""
    model=post
    template_name='artical_detail.html'


class upadte_post_view(UpdateView):
    """provides Update view of blog post whoes pk is provided."""
    model=post
    template_name = 'update_post.html'
    fields= ("title","summary","content","category","post_image","draft")

class delete_post_view(DeleteView):
    """provides delete view of blog post whoes pk is provided."""

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
	
    #adding the user automatically.
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
     """provides the list of posts created by user."""
     user=request.user
     my_post = post.objects.filter(author=user).order_by('-date_created')
     context = {'my_post':my_post}
     return render(request, 'my_post.html', context)


class doctor_list_View(ListView):
    """this view returns all the doctors profile."""
    template_name = 'doctor_list.html'
    def get_queryset(self):
        queryset = Profile.objects.filter(Doctor=True)
        return queryset
    

def book_Appointment_view(request,pk):
    """fetches the data from request to saves it to database and craetes a google calender event for that data."""
    if request.method == 'POST':
         speciality = request.POST['speciality']
         Date = request.POST['Date']
         start_time = request.POST['start_time']
         #creating a datetime object from the given string in required format.
         time = datetime.datetime.strptime(start_time, "%H:%M")
         #fetching the doctors name for appointment.
         Doctor = Profile.objects.get(id = pk)
         start_event = Date +' '+ start_time +':' '00'
         #creating a datetime object from the given string in required format.
         start_event_time = datetime.datetime.strptime(start_event,"%Y-%m-%d %H:%M:%S")
         #calculating end event time.
         end_event_time  = start_event_time + datetime.timedelta(minutes=45)
         end_time  = end_event_time.time().strftime("%H:%M")
         context ={'speciality':speciality,'Date':Date,'start_time':start_time,'Doctor':Doctor,'end_time':end_time}
         data = Appointment.objects.create(Doctor = Doctor.user, speciality = speciality, Date = Date, start_time = start_time, end_time = end_time )
         data.save()



         creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
         if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
            #creating api service instance.
            service = build('calendar', 'v3', credentials=creds)
            #event deatils
            event = {
            'summary': speciality,
  
            'start': {
                'dateTime': start_event_time.isoformat(),
                'timeZone': 'Asia/Kolkata',
             },
             'end': {
                'dateTime': end_event_time.isoformat(),
                'timeZone': 'Asia/Kolkata',
                },
 
  
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'email', 'minutes': 24 * 60},
                    {'method': 'popup', 'minutes': 10},
                        ],
                    },
            }
         #adding an event to calender.
         event = service.events().insert(calendarId='primary', body=event).execute()
         



         return render(request, 'confirm.html',context)
    return render(request, 'book_Appointment.html')

def tokens_view(request):
    """this view helps users to refresh there token if it is expired/ obtain new auth token"""
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
     # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())    
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    try:
        service = build('calendar', 'v3', credentials=creds)

        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        print('Getting the upcoming 10 events')
        events_result = service.events().list(calendarId='primary', timeMin=now,
                                              maxResults=10, singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])
        conext ={
                'events':events,
                'msg':'token refreshed'
                }
        if not events:
            conext ={'msg1':'No upcoming events found.',
                     'msg2':'token refreshed'}
            return render(request, 'tokenss.html',conext)
        return render(request, 'tokenss.html',conext)

    except HttpError as error:
        conext ={
                'msg':'An error occurred: %s' % error
                }
        return render(request, 'tokenss.html',conext)    

        


     