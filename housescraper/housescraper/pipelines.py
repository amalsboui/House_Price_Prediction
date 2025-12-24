# Define your adapter pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/adapter-pipeline.html


# useful for handling different adapter types with a single interface

import re
from scrapy.exceptions import DropItem
from itemadapter import ItemAdapter


class HousescraperPipeline:

    @staticmethod
    def remove_emojis_and_quotes(text):
        if not text:
            return text

        # Remove emojis
        emoji_pattern = re.compile(
            "["
            "\U0001F600-\U0001F64F"
            "\U0001F300-\U0001F5FF"
            "\U0001F680-\U0001F6FF"
            "\U0001F1E0-\U0001F1FF"
            "]+",
            flags=re.UNICODE,
        )
        text = emoji_pattern.sub("", text)

        # Remove quotes
        text = text.replace('"', "").replace("'", "")

        return text.strip()

    @staticmethod
    def extract_governorate(ville):
        if not ville:
            return None

        parts = [p.strip() for p in ville.split(",")]
        return parts[-1] if parts else None

    
    immobilier_type_map = {
       "Appart": "Appart",
       "Villa": "House", 
       "Duplex": "House",   
       "Triplex": "House",       
    }  

    tayara_type_map = {
       "Appartements": "Appart",
       "Maisons et villas": "House",     
    }   

    mubawab_type_map = {
       "Apartment": "Appart",
       "House": "House", 
       "Villa": "House",    
    }   

    def process_item(self, item, spider):

        adapter = ItemAdapter(item)

        source = adapter.get("source")    
        
        if source == "tayara":
            # Keep only À Vendre
            if adapter.get("type_transaction") != "À Vendre":
                raise DropItem("Tayara item not for sale")

            raw_type = adapter.get("type_bien")
            if raw_type in self.tayara_type_map:
                adapter["type_bien"] = self.tayara_type_map[raw_type]
            else:
                raise DropItem(f"Tayara type not allowed: {raw_type}")
            
        if source == "mubawab":
            raw_type = adapter.get("type_bien")
            adapter["type_bien"] = self.mubawab_type_map[raw_type]
        
        if source == "immobilier":
            raw_type = adapter.get("type_bien")
            if raw_type in self.immobilier_type_map:
                adapter["type_bien"] = self.immobilier_type_map[raw_type]
            else:
                raise DropItem(f"Immobilier type not allowed: {raw_type}")
            
        # Clean titre
        if adapter.get("titre"):
            adapter["titre"] = self.remove_emojis_and_quotes(adapter["titre"])

        # Clean prix
        if adapter.get("prix"):
            prix = adapter["prix"].replace("DT", "").replace(" ", "").replace("TND", "").strip()
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
            adapter["ville"] = self.extract_governorate(adapter["ville"])

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
        
        return item
