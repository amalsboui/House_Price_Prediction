# Define your adapter pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/adapter-pipeline.html


# useful for handling different adapter types with a single interface

import re
from scrapy.exceptions import DropItem
from itemadapter import ItemAdapter


class HousescraperPipeline:

    allowed_types_immobilier = ["Villa", "Appart", "Duplex", "Triplex"]

    def process_item(self, item, spider):
        source = item["source"]

        adapter = ItemAdapter(item)
        
        # Clean titre
        if adapter.get("titre"):
            adapter["titre"] = adapter["titre"].strip()

        # Clean prix
        if adapter.get("prix"):
            prix = adapter["prix"].replace("DT", "").replace(" ", "").strip()
            try:
                adapter["prix"] = float(prix)
            except ValueError:
                adapter["prix"] = None
        
        # Clean surface
        if adapter.get("surface"):
            surface = adapter["surface"].replace("m", "").strip()
            try:
                adapter["surface"] = float(surface)
            except ValueError:
                adapter["surface"] = None

        # Clean ville
        if adapter.get("ville"):
            adapter["ville"] = adapter["ville"].strip()

        # Clean chambres
        if adapter.get("chambres"):
            try:
                adapter["chambres"] = int(adapter["chambres"].split()[0])
            except ValueError:
                adapter["chambres"] = None

        if adapter.get("chambres") is None:
            raise DropItem(f"No chambre info for {adapter.get('titre')}")
        
        # Clean type_bien
        if adapter.get("type_bien"):
            adapter["type_bien"] = adapter["type_bien"].strip()

        # Drop items with missing fields
        essential_fields = ["chambres", "type_bien", "surface", "prix", "ville", "titre"]
        for f in essential_fields:
            if adapter.get(f) is None:
                raise DropItem(f"Missing {f} for item: {adapter.get('titre')}")
        
        # Drop items with type_bien not allowed in immobilier
        if adapter.get("type_bien") not in self.allowed_types_immobilier:
            raise DropItem(f"Ignored adapter because type_bien not allowed: {adapter.get('type_bien')}")


        return item
