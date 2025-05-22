# Django core imports
from django.urls import reverse
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView

# Authentication and permissions
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

# Third-party packages
from django_tables2 import SingleTableView
from django_tables2.export.views import ExportMixin

# Local app imports
from .models import Bill
from .tables import BillTable
from accounts.models import Profile
from utils.pdf import generate_pdf, generate_pdf_response


class BillListView(LoginRequiredMixin, ExportMixin, SingleTableView):
    """View for listing bills."""
    model = Bill
    table_class = BillTable
    template_name = 'bills/bill_list.html'
    context_object_name = 'bills'
    paginate_by = 10
    SingleTableView.table_pagination = False


class BillCreateView(LoginRequiredMixin, CreateView):
    """View for creating a new bill."""
    model = Bill
    template_name = 'bills/billcreate.html'
    fields = [
        'institution_name',
        'phone_number',
        'email',
        'address',
        'description',
        'payment_details',
        'amount',
        'status'
    ]

    def get_success_url(self):
        """Redirect to the list of bills after a successful update."""
        return reverse('bill_list')


class BillUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """View for updating an existing bill."""
    model = Bill
    template_name = 'bills/billupdate.html'
    fields = [
        'institution_name',
        'phone_number',
        'email',
        'address',
        'description',
        'payment_details',
        'amount',
        'status'
    ]

    def test_func(self):
        """Check if the user has the required permissions."""
        return self.request.user.profile in Profile.objects.all()

    def get_success_url(self):
        """Redirect to the list of bills after a successful update."""
        return reverse('bill_list')


class BillDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """View for deleting a bill."""
    model = Bill
    template_name = 'bills/billdelete.html'

    def test_func(self):
        """Check if the user is a superuser."""
        return self.request.user.is_superuser

    def get_success_url(self):
        """Redirect to the list of bills after successful deletion."""
        return reverse('bill_list')


class BillPDFView(LoginRequiredMixin, DetailView):
    """View for generating PDF version of a bill."""
    model = Bill
    
    def get(self, request, *args, **kwargs):
        bill = self.get_object()
        context = {'bill': bill}
        
        # Generate PDF
        pdf_content = generate_pdf('pdf/bill.html', context)
        
        # Create response
        filename = f'bill_{bill.id}.pdf'
        return generate_pdf_response(pdf_content, filename)
