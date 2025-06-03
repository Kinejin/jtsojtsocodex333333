import json
import os
import uuid

from config import FAVORITES_FILE


class FavoritesManager:
    def __init__(self):
        self.favorites = []
        self.load()

    def load(self):
        if os.path.exists(FAVORITES_FILE):
            try:
                with open(FAVORITES_FILE, 'r', encoding='utf-8') as f:
                    self.favorites = json.load(f)
            except Exception:
                self.favorites = []
        else:
            self.favorites = []

    def save(self):
        with open(FAVORITES_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.favorites, f, indent=2, ensure_ascii=False)

    def add_favorite(self, name, url, quality='best', auto_capture=False):
        fav = {
            'id': str(uuid.uuid4()),
            'name': name,
            'url': url,
            'quality': quality,
            'auto_capture': auto_capture,
            'is_live_detected': False
        }
        self.favorites.append(fav)
        self.save()
        return fav

    def remove_favorite(self, fav_id):
        self.favorites = [f for f in self.favorites if f['id'] != fav_id]
        self.save()

    def update_favorite(self, fav_id, **kwargs):
        for fav in self.favorites:
            if fav['id'] == fav_id:
                fav.update(kwargs)
                self.save()
                return fav
        return None

    def get_favorite(self, fav_id):
        for fav in self.favorites:
            if fav['id'] == fav_id:
                return fav
        return None
