"""blocks URL Configuration

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
from django.contrib import admin
from django.urls import path

import computational_blocks.views
import signal_blocks.views
import strategy_blocks.views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('COMPUTATIONAL_BLOCK/1/indicators', computational_blocks.views.get_indicators),
    path('COMPUTATIONAL_BLOCK/1/<indicator_name>/fields', computational_blocks.views.get_indiciator_fields),
    path('COMPUTATIONAL_BLOCK/1/run', computational_blocks.views.post_run),

    path('SIGNAL_BLOCK/1/eventTypes', signal_blocks.views.get_event_types),
    path('SIGNAL_BLOCK/1/eventActions', signal_blocks.views.get_event_actions),
    path('SIGNAL_BLOCK/1/run', signal_blocks.views.post_run),

    path('STRATEGY_BLOCK/1/run', signal_blocks.views.post_run),
]
