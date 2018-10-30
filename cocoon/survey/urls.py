from django.conf.urls import url

from . import views

app_name = 'survey'
urlpatterns = [
    url(r'^rent/$', views.RentingSurvey.as_view(), name="rentingSurvey"),
    url(r'^visits/$', views.visit_list, name="visitList"),
    url(r'^result/rent/$', views.survey_result_rent, name="rentSurveyResult"),
    url(r'^result/rent/(?P<survey_url>.*)/$', views.survey_result_rent, name="rentSurveyResult"),
    # Ajax requests
    url(r'^setFavorite/$', views.set_favorite, name="setFavorite"),
    url(r'^deleteSurvey/$', views.delete_survey, name="surveyDelete"),
    url(r'^setVisitHome/$', views.set_visit_house, name="setVisitHouse"),
    url(r'^deleteVisitHome/$', views.delete_visit_house, name="deleteVisitHouse"),
    url(r'^check_pre_tour_documents/$', views.check_pre_tour_documents, name="checkPretourDocuments"),
    url(r'^resend_pre_tour_documents/$', views.resend_pre_tour_documents, name="resendPretourDocuments"),
]
