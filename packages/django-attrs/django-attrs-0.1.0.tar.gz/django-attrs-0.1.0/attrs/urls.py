from django.conf.urls import url

from attrs.views import AttrUpdateView, AttrCreateView, AttrListView, AttrDetailView, ChoiceUpdateView, ChoiceCreateView, \
    ChoiceDeleteView

urlpatterns = [
    url(r'^$', AttrListView.as_view(), name='attr_list'),
    url(r'^(?P<pk>\d+)/edit/$', AttrUpdateView.as_view(), name='attr_edit'),
    url(r'^(?P<pk>\d+)/$', AttrDetailView.as_view(), name='attr_detail'),
    url(r'^create/$', AttrCreateView.as_view(), name='attr_create'),
    # choices
    url(r'^(?P<attr_pk>\d+)/choices/(?P<pk>\d+)/edit/$', ChoiceUpdateView.as_view(), name='choice_edit'),
    url(r'^(?P<attr_pk>\d+)/choices/(?P<pk>\d+)/delete/$', ChoiceDeleteView.as_view(), name='choice_delete'),
    url(r'^(?P<attr_pk>\d+)/choices/create/$', ChoiceCreateView.as_view(), name='choice_create'),
]
