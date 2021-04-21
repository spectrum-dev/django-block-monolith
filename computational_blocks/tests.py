from django.test import TestCase, Client

from computational_blocks.technical_analysis.main import run
from computational_blocks.data.technical_analysis import DATA_BLOCK 

class TechnicalAnalysisBlock(TestCase):
    input = {
        "short_name": "MA",
        "indicator_name": "MA",
        "lookback_period": "2",
        "lookback_unit": "DATA_POINT"
    }

    response = run(input, DATA_BLOCK)

    print (response)

    assert False