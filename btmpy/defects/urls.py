from django.urls import path
from defects import views

urlpatterns = [
    path('',views.alldefects,name='alldefects'),
    path("completed",views.completed,name='completed'),
    path("pending",views.pending,name='pending'),
    path("<int:id>",views.description,name='description'),
    path("edit/<int:id>",views.edit_defects,name='edit'),
    path('add',views.add,name='add'),
    path('delete/<int:id>',views.delete,name='delete'),
    path('filterdefect',views.filter_defect,name='filterdefect')

]