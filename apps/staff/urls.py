from django.urls import path

from . import views

urlpatterns = [
    # Expenses
    path("Expenses/", views.StaffExpenseAPIView.as_view()),
    path("Expenses/<int:id>/", views.StaffExpenseDetailAPIView.as_view()),
    # Type
    path("Type/", views.StaffExpenseTypeAPIView.as_view()),
    path("Type/<int:id>/", views.StaffExpenseTypeDetailAPIView.as_view()),
    # Members
    path("Members/", views.StaffMemberAPIView.as_view()),
    path("Members/<int:id>/", views.StaffMemberDetailAPIView.as_view()),
]
