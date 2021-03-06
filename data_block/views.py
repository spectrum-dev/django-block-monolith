from django.http import JsonResponse

# US Stock Data (Data Block with ID 1)
# -----------------------------------
from data_block.one.alpha_vantage import search_ticker


# Dropdowns
def get_equity_name(request):
    """
    Gets a list of supported equity names (search)
    """
    ticker_fuzzy_name = request.GET.get("name")
    if ticker_fuzzy_name:
        response = search_ticker(ticker_fuzzy_name)
    else:
        response = {"response": []}

    return JsonResponse(response)


# Crypto Data (Data Block with ID 2)
# -----------------------------------
from data_block.two.supported_crypto import SUPPORTED_CRYPTO


def get_symbol(request):
    crypto_fuzzy_name = str(request.GET.get("name")).lower()

    response = []
    for value in SUPPORTED_CRYPTO:
        currency_code = value["currency_code"].lower()
        currency_name = value["currency_name"].lower()
        if (
            currency_code.find(crypto_fuzzy_name) != -1
            or currency_name.find(crypto_fuzzy_name) != -1
        ):
            response.append(
                {
                    "value": value["currency_code"],
                    "label": f'{value["currency_name"]} ({value["currency_code"]})',
                }
            )

    return JsonResponse({"response": response})
