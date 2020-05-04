from .model import Item

from !!! import Account
from werkzeug.exceptions import NotFound


class ItemService:

    @staticmethod
    def get_by_sku_account_date(item_sku: str, account: Account, date: date) -> Item:
        if account.channel.platform_name == 'amazon':
            item = Item.query.filter(Item.sku==item_sku, Item.seller_firm_id=account.seller_firm_id, Item.valid_from<=date, Item.valid_to>=date).first()
            if item:
                return item
            else:
                raise NotFound('The item specific SKU "{}" is not listed in the item information of the seller. Please update the item information before proceeding'.format(item_sku))
