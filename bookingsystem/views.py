from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import guest_booking
from .forms import BookingForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView

# Restaurant home page class, renders the page in the browser


class Home (generic.ListView):
    model = guest_booking
    template_name = 'index.html'


# The get request returns the template as above
def get(self, request):
    return render(request, 'base.html')


# class allowing menu page to be rendered in the browser 


class Menu(generic.DetailView):
    def get(self, request):
        return render(request, 'menu.html')

# class for the thank you page to be rendered in the browser


class Thankyou(generic.DetailView):
    def get(self, request):
        return render(request, 'thankyou.html')



# This class will allow the user to create their booking (bookings are being made)

class MakeBooking(generic.CreateView):
    model = guest_booking
    template_name = 'make_booking.html'
    form_class = BookingForm
    
    def get_success_url(self):
        return reverse('thankyou')

    def booking_add(request):
        if request.method == 'POST':
            if form.is_valid:
                booking = form.save()
                booking.user = request.user
                booking.save()
            return redirect('thankyou')
        else:
            form = BookingForm()
            context = {'form': form}
            return render(request, 'make_booking.html', context)



# View bookings made on the my_booking page

def ViewBooking(request):
    bookings = guest_booking.objects.filter()
    context = {'bookings': bookings}
    return render(request, 'my_booking.html', context)


# This class will allow for the user to edit a booking
# Get booking update rendered to my_booking page

class BookingEdit(generic.UpdateView):
    model = guest_booking
    form_class = BookingForm
    template_name = 'edit_booking.html'
    success_url = 'my_booking.html'

    def booking_edit(request, id):
        book = get_object_or_404(guest_booking, id=id)
        if request.method == 'POST':
            form = BookingForm(request.POST, instance=book)
            if form.is_valid():
                booking = form.save()
                booking.user = request.user
                booking.save()
                return redirect('index.html')
                form = BookingForm(instance=book)
                context = {'form': form}
                return render(request, 'edit_booking.html', context)

    # called with pk
    def get_object(self):
        return self.request.user

# This class will allow for the user to delete their booking 
# FIX BUG TO DELETE need pk 

class BookingDelete(generic.DeleteView):
    model = guest_booking
    template_name = 'delete_booking.html'
    success_url = 'my_booking.html'
    
    def delete(request, id):
        booking = get_object_or_404(guest_booking, id=id)
        if request.method == 'POST':
            form = BookingForm(request.POST, instance=booking)
            if booking.delete():
                return redirect('index.html')
                form = BookingForm(instance=booking)
                context = {'form': form}
                return render(request, 'delete_booking', context)

     # deletes user completey? 
     # Generic detail view BookingDelete must be called with either an object pk or a 
     # slug in the URLconf.
    def get_object(self):
        return self.request.user