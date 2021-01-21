from . import views
from django.conf.urls import url

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^administrator/$', views.administrator, name='administrator'),
    url(r'^employee/$', views.employee, name='employee'),
    url(r'^LogoutProfile/$', views.LogoutProfile, name='logoutProfile'),
    url(r'^LunchBox/(?P<lunch_id>[0-9]+)/$', views.LunchRedaction, name='lunchRedaction'),
    url(r'^LunchBox/Create/$', views.LunchCreate, name='lunchCreate'),
    url(r'^Empl/Create/$', views.EmplCreate, name='emplCreate'),
    url(r'^Empl/(?P<empl_id>[0-9]+)/Type/Create/$', views.TypeCreate, name='typeCreate'),
    url(r'^Order/(?P<order_id>[0-9]+)/$', views.OrderV, name='order'),
    url(r'^employee-orders/', views.employee_orders, name='prepare'),
    url(r'^statistics/', views.statistics, name='statistics'),
    url(r'^ajax/employee/', views.statistics_employee, name='statistics_employee'),
    url(r'^ajax/employee_graf/', views.statistics_employee_graf, name='employee_graf'),
    url(r'^ajax/sales/', views.statistics_sales, name='statistics_sales'),
    url(r'^ajax/sales_content/', views.sales_content, name='sales_content'),
    url(r'^ajax/sales_content_day/', views.sales_content_day, name='sales_content_day'),
    url(r'^ajax/sales_month/graf/', views.sales_graf_month, name='sales_graf_month'),
    url(r'^ajax/sales_day/graf/', views.sales_graf_day, name='sales_graf_day'),
    url(r'^ajax/lunchboxs/', views.statistics_lunchboxs, name='statistics_lunchboxs'),
    url(r'^ajax/lunchboxs_graf/', views.lunchbox_graf, name='lunchbox_graf'),
]