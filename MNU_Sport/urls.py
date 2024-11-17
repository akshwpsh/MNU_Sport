from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),  # accounts 앱의 URL 포함
    path('records/', include('records.urls')),  # records 앱의 URL 포함
   path('', RedirectView.as_view(url='records/'), name = 'main_page'),  # 기본 페이지를 records로 리다이렉트
]
