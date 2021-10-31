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
from django.conf import settings
from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from django.views.static import serve

import bulk_data_block.views
import computational_block.views
import data_block.views
import signal_block.views

urlpatterns = [
    url(r"^static/(?P<path>.*)$", serve, {"document_root": settings.STATIC_ROOT}),
    path("admin/", admin.site.urls),
    path("DATA_BLOCK/1/equityName", data_block.views.get_equity_name),
    path("DATA_BLOCK/1/candlestick", data_block.views.get_us_stock_data_candlesticks),
    path("DATA_BLOCK/2/cryptoName", data_block.views.get_symbol),
    path("DATA_BLOCK/2/candlestick", data_block.views.get_crypto_candlesticks),
    path("BULK_DATA_BLOCK/1/exchange", bulk_data_block.views.get_screener_exchanges),
    path(
        "BULK_DATA_BLOCK/1/candlestick", bulk_data_block.views.get_screener_candlesticks
    ),
    path("COMPUTATIONAL_BLOCK/1/indicator", computational_block.views.get_indicators),
    path(
        "COMPUTATIONAL_BLOCK/1/indicatorField",
        computational_block.views.get_indiciator_fields,
    ),
    path(
        "COMPUTATIONAL_BLOCK/2/operationType",
        computational_block.views.get_operation_types,
    ),
    path("SIGNAL_BLOCK/1/eventAction", signal_block.views.get_event_actions),
    path("SIGNAL_BLOCK/2/eventAction", signal_block.views.get_event_actions),
    path("SIGNAL_BLOCK/2/saddleType", signal_block.views.get_saddle_types),
    path("SIGNAL_BLOCK/4/eventAction", signal_block.views.get_event_actions),
    path("SIGNAL_BLOCK/4/crossoverType", signal_block.views.get_crossover_types),
    path("SIGNAL_BLOCK/6/eventAction", signal_block.views.get_event_actions),
    path("SIGNAL_BLOCK/6/candleCloseType", signal_block.views.get_candle_close_types),
    path("SIGNAL_BLOCK/7/eventAction", signal_block.views.get_event_actions),
    path("SIGNAL_BLOCK/7/comparisonType", signal_block.views.get_comparison_types),
]
