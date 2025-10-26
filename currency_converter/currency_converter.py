import aiohttp


async def get_exchange_rates(base: str = "USD"):
    url = f"https://api.exchangerate-api.com/v4/latest/{base}"

    try: 
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return {"success": True, "data": data}
                else:
                    data = await response.json()
                    return {"success": False, "data": data}
    except Exception as e:
        return {"success": False, "data": e}
    

async def convert_currency(amount: float, from_currency: str, to_currency: str):

    if from_currency == to_currency:
        return amount
    
    response = await get_exchange_rates(from_currency)


    if not response["success"]:
        return None
    
    rates = response["data"]["rates"]
    

    if to_currency in rates:
        result = amount*rates[to_currency]
        return round(result,2)
    
    return None