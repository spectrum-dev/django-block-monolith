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
from django.middleware.csrf import get_token

import computational_blocks.views
import signal_blocks.views
import strategy_blocks.views
import data_blocks.views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("DATA_BLOCK/1/equityName", data_blocks.views.get_equity_name),
    path("DATA_BLOCK/1/candlestick", data_blocks.views.get_us_stock_data_candlesticks),
    path("DATA_BLOCK/1/run", data_blocks.views.USStockDataRunView.as_view()),
    path("DATA_BLOCK/2/cryptoName", data_blocks.views.get_symbol),
    path("DATA_BLOCK/2/candlestick", data_blocks.views.get_crypto_candlesticks),
    path("DATA_BLOCK/2/run", data_blocks.views.CryptoRunView.as_view()),
    path("COMPUTATIONAL_BLOCK/1/indicator", computational_blocks.views.get_indicators),
    path(
        "COMPUTATIONAL_BLOCK/1/indicatorField",
        computational_blocks.views.get_indiciator_fields,
    ),
    path(
        "COMPUTATIONAL_BLOCK/1/run",
        computational_blocks.views.TechnicalAnalysisRunView.as_view(),
    ),
    path("SIGNAL_BLOCK/1/eventType", signal_blocks.views.get_event_types),
    path("SIGNAL_BLOCK/1/eventAction", signal_blocks.views.get_event_actions),
    path("SIGNAL_BLOCK/1/run", signal_blocks.views.PostRun.as_view()),
    path("SIGNAL_BLOCK/2/eventAction", signal_blocks.views.get_event_actions),
    path("SIGNAL_BLOCK/2/saddleType", signal_blocks.views.get_saddle_types),
    path("SIGNAL_BLOCK/2/run", signal_blocks.views.PostSaddleRun.as_view()),
    path("SIGNAL_BLOCK/3/run", signal_blocks.views.PostAndRunView.as_view()),
    path("STRATEGY_BLOCK/1/run", strategy_blocks.views.PostRun.as_view()),
]
