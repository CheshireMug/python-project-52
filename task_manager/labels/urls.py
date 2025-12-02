from django.urls import path
from .views import LabelsListView, LableCreateView, \
    LableUpdateView, LableDeleteView

app_name = 'labels'

urlpatterns = [
    path('', LabelsListView.as_view(), name='labels_list'),
    path('create/', LableCreateView.as_view(), name='labels_create'),
    path(
        '<int:pk>/update/',
        LableUpdateView.as_view(),
        name='labels_update'
        ),
    path(
        '<int:pk>/delete/',
        LableDeleteView.as_view(),
        name='labels_delete'
        ),
]
