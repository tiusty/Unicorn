from django.conf.urls import url

from . import views

app_name = 'userAuth'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.loginPage, name='loginPage'),
    # url(r'^register/$', views.SignUpView.as_view(), name='signup'),
    url(r'^register/hunter/', views.ApartmentHunterSignupView.as_view(), name='hunter_signup'),
    url(r'^register/broker/', views.BrokerSignupView.as_view(), name='broker_signup'),
    url(r'^password_change/$', views.change_password, name='change_password'),
    url(r'^logout/$', views.logoutPage, name='logoutPage'),
    url(r'^profile$', views.user_profile, name='user_profile'),
    url(r'^surveysOld', views.user_surveys, name='user_surveys'),
    url(r'^surveys/$', views.VisitList.as_view(), name='surveys'),

    # Email verification
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate_account, name='activateAccount'),
    url(r'^termsofuse', views.TermsOfUse.as_view(), name='terms_of_use'),
]
