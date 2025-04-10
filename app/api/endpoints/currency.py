from fastapi import Cookie, APIRouter, HTTPException, Query

from app.utils.external_api import currency_api
from app.api.models.currency import Currency


currency = APIRouter(prefix='/currency')

@currency.get('/get_currency_codes')
async def get_open_resource(session_token=Cookie()):
    if session_token:
        ans = await currency_api.get_currency_codes()
        return {'currencies': ans}
    else:
        raise HTTPException(403, detail="Invalid session token")

@currency.post('/convert')
async def convert_currency(currency_data: Currency, session_token=Cookie()):
    ans = await currency_api.convert(currency_data)
    return {'message': f"{currency_data.amount} of {currency_data.currency_code1} is {ans} of {currency_data.currency_code2}"}
