import httpx
from app.core.config import settings
from app.api.models.currency import Currency

class ExternalAPI:
    def __init__(self):
        self.payload = {}
        self.base_link = "https://api.apilayer.com/exchangerates_data"
        self.headers = {'apikey': settings.API_KEY}

    async def get_currency_codes(self):
        async with httpx.AsyncClient(timeout=60) as client:
            ans = await client.get(f'{self.base_link}/symbols', headers=self.headers)
            if ans.status_code != 200:
                raise HTTPException(status_code=ans.status_code, detail='Something went wrong on external API!')
            else:
                return ans.json()

    async def convert(self, currency_data: Currency) -> float:
        async with httpx.AsyncClient(timeout=60) as client:
            ans = await client.get(
                f'{self.base_link}/convert',
                params={'to': currency_data.currency_code2, 'from': currency_data.currency_code1, 'amount': currency_data.amount},
                headers=self.headers)
            if ans.status_code != 200:
                raise HTTPException(status_code=ans.status_code, detail='Something went wrong on external API!')
            return ans.json().get('result')


currency_api = ExternalAPI()

