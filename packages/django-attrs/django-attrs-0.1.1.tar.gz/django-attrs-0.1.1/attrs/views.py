from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.core.checks import messages
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import DetailView
from django.views.generic import UpdateView

from attrs.forms import AttrForm, ChoiceForm
from attrs.models import Attribute, Choice
from attrs.tables import AttrTable
from tables3.views import FilteredTableListView


class AttrViewMixin(object):
    """
    Mixin for all Attr view classes
    """
    model = Attribute




class AttrDetailView(AttrViewMixin, DetailView):
    """
    View the details of an Attr
    """
    template_name = 'attr_detail.html'
    context_object_name = 'attr'


    def get_context_data(self, **kwargs):
        context = super(AttrDetailView, self).get_context_data(**kwargs)
        context['choices'] = Choice.objects.filter(attribute=self.object)

        return context


class AttrListView(AttrViewMixin, FilteredTableListView):
    """
    View a list of Attrs
    """
    table_class = AttrTable
    template_name = 'attr_list.html'
    # filter_form_class = AttrFilterForm



class AttrUpdateView(UserPassesTestMixin, LoginRequiredMixin, AttrViewMixin, UpdateView):
    """
    Update a Attr
    """
    form_class = AttrForm
    template_name = 'attr_form.html'

    def test_func(self):
        """
        Which users are allowed here?
        """
        return self.request.user.is_superuser


class AttrCreateView(UserPassesTestMixin, LoginRequiredMixin, AttrViewMixin, CreateView):
    """
    Update a Attr
    """
    form_class = AttrForm
    template_name = 'attr_form.html'

    def test_func(self):
        """
        Which users are allowed here?
        """
        return self.request.user.is_superuser

    def form_valid(self, form):
        # to prevent error from duplicate slug ''
        attr = form.instance
        attr.slug = attr.name
        attr.save()
        return super(AttrCreateView, self).form_valid(form)



class AttrView(UserPassesTestMixin, LoginRequiredMixin, AttrViewMixin, UpdateView):
    """
    Update a Attr
    """
    form_class = AttrForm
    template_name = 'attr_form.html'

    def test_func(self):
        """
        Which users are allowed here?
        """
        return self.request.user.is_superuser



class ChoiceCreateView(UserPassesTestMixin, LoginRequiredMixin, CreateView):
    """
    create a Choice for an Attribute
    """
    model= Choice
    form_class = ChoiceForm
    template_name = 'attr_form.html'
    attr=None
    def test_func(self):
        """
        Which users are allowed here?
        """
        return self.request.user.is_superuser

    def get_attr(self):
        if not self.attr:
            self.attr = get_object_or_404(Attribute, pk=self.kwargs['attr_pk'])
        return self.attr

    def form_valid(self, form):
        # to prevent error from duplicate slug ''
        choice = form.instance
        choice.attribute = self.get_attr()
        print choice, self.get_attr()
        choice.save()
        return super(ChoiceCreateView, self).form_valid(form)

    def get_success_url(self):
        return self.get_attr().get_absolute_url()




class ChoiceUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    """
    Update a Attr
    """
    model = Choice
    form_class = ChoiceForm
    template_name = 'choice_form.html'
    attr=None

    def test_func(self):
        """
        Which users are allowed here?
        """
        return self.request.user.is_superuser

    def get_attr(self):
        if not self.attr:
            self.attr = get_object_or_404(Attribute, pk=self.kwargs['attr_pk'])
        return self.attr

    def get_success_url(self):
        return self.get_attr().get_absolute_url()




class ChoiceDeleteView(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
    """
    Delete a choice
    """
    model = Choice
    attr=None
    template_name = "choice_delete.html"

    def test_func(self):
        """
        Which users are allowed here?
        """
        return self.request.user.is_superuser

    def get_attr(self):
        if not self.attr:
            self.attr = get_object_or_404(Attribute, pk=self.kwargs['attr_pk'])
        return self.attr

    def get_success_url(self):
            return self.get_attr().get_absolute_url()


