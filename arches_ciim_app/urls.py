"""URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, re_path
from arches_ciim_app.views.ciim import ChangesView, ConceptsExportView
from arches_ciim_app.views.keep_export import print_ids

urlpatterns = [
    re_path(r"^resource/changes", ChangesView.as_view(), name="ChangesView"),
    re_path(r"^concept/export", ConceptsExportView.as_view(), name="ConceptsExportView"),    
    re_path(r"^keep/export/$", print_ids, name='print_ids'),
]