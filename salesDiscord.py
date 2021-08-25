import requests
import json
import sys
import os
import random
import time
from discord_webhook import DiscordWebhook, DiscordEmbed

"""
This bot works for projects with their own contract address, so it will not work on projects that use the opensea contract address
"""

def override_where():
    """ overrides certifi.core.where to return actual location of cacert.pem"""
    # change this to match the location of cacert.pem
    return os.path.abspath("cacert.pem")

# is the program compiled?
if hasattr(sys, "frozen"):
    import certifi.core

    os.environ["REQUESTS_CA_BUNDLE"] = override_where()
    certifi.core.where = override_where

    # delay importing until after where() has been replaced
    import requests.utils
    import requests.adapters
    # replace these variables in case these modules were
    # imported before we replaced certifi.core.where
    requests.utils.DEFAULT_CA_BUNDLE_PATH = override_where()

class openseaSales():

    def requestLastSale(self):
        # Request last sale from opensea API
        url = "https://api.opensea.io/api/v1/events"
        asset_contract_address = '' # Enter the projects contract address
        
        querystring = {"only_opensea":"true","offset":"0","limit": "1", "asset_contract_address": asset_contract_address, "event_type": "successful"}
        response = requests.request("GET", url, headers={"Accept": "application/json"}, params=querystring)
        
        return json.loads(response.text)

    def main(self):
        last_sales_list = []

        # Request old sale and append to last_sales_list
        last_sale_data = self.requestLastSale()
        tx_id = last_sale_data['asset_events'][0]['transaction']['id']
        last_sales_list.append(tx_id)

        while(True):
            # Request new sale
            try:
                sale_data = self.requestLastSale()
                tx_id = sale_data['asset_events'][0]['transaction']['id']
                
                if tx_id not in last_sales_list:
                    last_sales_list.append(tx_id)
                    
                    # If the list gets too big remove the first element
                    if len(last_sales_list) > 5:
                        last_sales_list.pop(0)
                        
                    asset_name = sale_data['asset_events'][0]['asset']['name']
                    asset_image = sale_data['asset_events'][0]['asset']['image_url']
                    asset_url = sale_data['asset_events'][0]['asset']['permalink']
                    
                    payment_token = sale_data['asset_events'][0]['payment_token']['symbol']
                    sale_price = int(sale_data['asset_events'][0]['total_price']) / 1000000000000000000
                    
                    random_color = random.randint(0, 0xffffff)
                    
                    # Send discord webhook
                    webhook = DiscordWebhook(url='') # Enter your discord webhook
                    
                    embed = DiscordEmbed(title=f'{asset_name} was purchased for {sale_price} {payment_token}', url=asset_url, color=random_color)
                    embed.set_image(url=asset_image)
                    
                    webhook.add_embed(embed)
                    webhook.execute()

                time.sleep(5)
            except:
                pass

openseaSales().main()
