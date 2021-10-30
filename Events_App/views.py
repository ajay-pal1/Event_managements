from rest_framework.viewsets import ModelViewSet
from .models import Event,EventJoined
from .serializers import EventSerializer,JoinedSerializer
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone  
from rest_framework.response import Response
from django.db.models import F
# Create your views here.

class EventViewSet(ModelViewSet):
    queryset = Event.objects.all() #Return the all Created Events
    # print("================>",queryset)
    serializer_class = EventSerializer
    permission_classes=[IsAuthenticated]
    
    def create(self, request,*args, **kwargs):
        data=request.data
        # print('=========================>',data)
        event_start_date=data["start_date"]
        # print('=========================>',event_start_date)
        event_end_date=data["end_date"]
        event_start_joining_date=data["joining_start_date"]
        event_end_joining_date=data["joining_end_date"]

        if 'Superuser' in request.user.groups.values_list('name',flat=True) or request.user.is_superuser:#Validating the user if current user belong to Superuser or admin will able to create the Events
            if event_start_joining_date > event_end_joining_date > event_start_date > event_end_date: 
                return super().create(request,*args, **kwargs) 
            else:
                return Response({"Details":"Event start date timing is grater then Event start date timing or Event start joing date and event end date is same or grater"})
        else:
            return Response({"Details":"Current user doesn not have permission to create event "})

    def update(self, request, *args, **kwarg,):
        instance=self.get_object() #Return the current event
        # print("================>",instance)
        if request.user.id == instance.creator.id:
            return super().update(request,*args,**kwarg,)
        else:
            return Response({"Details":"Current user Not created this event so he don't have permission to update this event "})


    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user.id == instance.creator.id: #comparing the current user and Event creator user is same or not  
            return super().destroy(request, *args, **kwargs)
        else:
            return Response({"Details":"Current user Not created this event so he don't have permission to delete this event "})



class JoinedEventViewSet(ModelViewSet):
    queryset = EventJoined.objects.all()
    serializer_class = JoinedSerializer
    permission_classes=[IsAuthenticated]

    def get_queryset(self):
        """Only show user related items."""
        return EventJoined.objects.filter(user_profile_id=self.request.user.id)
    
    def create(self, request, *args, **kwargs):
        # current_user=self.request.user
        data= request.data                  #Return the post data
        # print("================>",data)
        id = data['event_name']             #graping the Event_name id
        obj=Event.objects.filter(id = id).first() # Checking that event id is presnt in db or not and retun the id data..
        # obj=Event.objects.get(id = id)
        # print("================>",obj)
        filtered=EventJoined.objects.filter(user_profile=request.user,event_name=obj).exists() # checking that in dp that user is present or not if present then validiting that event data present or not
        joining_start = getattr(obj,"joining_start_date")
        # print("================>",joining_start)
        joining_end = getattr(obj,"joining_end_date")
        # print("================>",joining_end)

        joining_now=timezone.now()
        if joining_start <= joining_now <= joining_end:
            if not filtered:
                obj.seats_available = F("seats_available") - 1
                obj.save()
                return super().create(request, *args, **kwargs)
            else:
                return Response({"Details":"Event Already Present"})
        else:
            return Response({"Details":"can't Joined the Event!! Event_joining_date passed or Event_joining_date not Started "})


    def destroy(self, request, *args, **kwargs):
        joint_event_object=self.get_object()
        obj=Event.objects.get(id=joint_event_object.event_name.id)
        obj.seats_available = F("seats_available") + 1
        obj.save()
        return super().destroy(request, *args, **kwargs)