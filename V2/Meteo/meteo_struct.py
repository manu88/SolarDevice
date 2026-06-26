

"""
models.py — Structures de données météo Infoclimat
"""

import json
import datetime


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────

def _kelvin_to_celsius(k):
    """Convertit des Kelvin en Celsius, retourne None si valeur absente."""
    if k is None or k == -0.1:
        return None
    return round(float(k) - 273.15, 1)

def _celsius_to_kelvin(c):
    """Convertit des Kelvin en Celsius, retourne None si valeur absente."""
    k = round(c + 273.15, 1)
    if k <= 0 :
        k = 0
    return k

def _safe(val):
    """Retourne None si val vaut -0.1 (sentinelle Infoclimat), sinon val."""
    if val == -0.1:
        return None
    return val


# ─────────────────────────────────────────────────────────────────────────────
# Sous-structures
# ─────────────────────────────────────────────────────────────────────────────

class Temperature:
    """Températures (°C) à différentes altitudes."""

    def __init__(self, raw: dict):
        self.deux_metres  = _kelvin_to_celsius(raw.get("2m"))
        self.sol          = _kelvin_to_celsius(raw.get("sol"))
        self.cinq_cents_hpa = _kelvin_to_celsius(raw.get("500hPa"))
        self.huit_cents_hpa = _kelvin_to_celsius(raw.get("850hPa"))
        
    def to_dict(self) -> dict:
        return {
            "2m":     _celsius_to_kelvin(self.deux_metres),
            "sol":     _celsius_to_kelvin(self.sol),
            "500hPa": _celsius_to_kelvin(self.cinq_cents_hpa),
            "850hPa":  _celsius_to_kelvin(self.huit_cents_hpa),
        }


    def __repr__(self):
        return f"Temperature(2m={self.deux_metres}°C)"


class Nebulosite:
    """Nébulosité (%) haute / moyenne / basse / totale."""

    def __init__(self, raw: dict):
        self.haute   = _safe(raw.get("haute"))
        self.moyenne = _safe(raw.get("moyenne"))
        self.basse   = _safe(raw.get("basse"))
        self.totale  = _safe(raw.get("totale"))

    def to_dict(self) -> dict:
        return {
            "haute":   self.haute,
            "moyenne": self.moyenne,
            "basse":   self.basse,
            "totale":  self.totale,
        }
    

    def description(self) -> str:
        if self.totale is None:
            return "inconnue"
        if self.totale <= 10:
            return "Ciel dégagé"
        elif self.totale <= 30:
            return "Peu nuageux"
        elif self.totale <= 60:
            return "Partiellement nuageux"
        elif self.totale <= 85:
            return "Très nuageux"
        return "Couvert"

    def __repr__(self):
        return f"Nebulosite(totale={self.totale}%)"


class Vent:
    """Vent moyen, rafales (km/h) et direction (°) à 10m."""

    DIRECTIONS = [
        "N","NNE","NE","ENE","E","ESE","SE","SSE",
        "S","SSO","SO","OSO","O","ONO","NO","NNO",
    ]

    def __init__(self, moyen_raw: dict, rafales_raw: dict, direction_raw: dict):
        self.moyen    = _safe(moyen_raw.get("10m"))
        self.rafales  = _safe(rafales_raw.get("10m"))
        self.direction_deg = _safe(direction_raw.get("10m"))

    @property
    def direction_label(self) -> str:
        if self.direction_deg is None:
            return "–"
        idx = round(float(self.direction_deg) / 22.5) % 16
        return self.DIRECTIONS[idx]    

    def to_dict(self) -> dict:
        return {
            "moyen":     self.moyen,
            "rafales":   self.rafales,
            "direction_deg": self.direction_deg,
        }

    def __repr__(self):
        return f"Vent(moyen={self.moyen} km/h, rafales={self.rafales} km/h, dir={self.direction_label})"


class Humidite:
    """Humidité relative (%) à 2m."""

    def __init__(self, raw: dict):
        self.deux_metres = _safe(raw.get("2m"))

    def to_dict(self) -> dict:
        return {"2m": self.deux_metres}
    
    @classmethod
    def from_dict(cls, data: dict):
        return cls(data)

    def __repr__(self):
        return f"Humidite(2m={self.deux_metres}%)"


# ─────────────────────────────────────────────────────────────────────────────
# Entrée horaire principale
# ─────────────────────────────────────────────────────────────────────────────

class EntreeMeteo:
    """
    Représente un relevé/prévision météo pour un créneau horaire donné.
    Toutes les valeurs sont typées et en unités lisibles (°C, km/h, mm…).
    """

    SEPARATOR = "---"  # séparateur entre entrées dans le fichier texte

    def __init__(self, horodatage_utc: datetime.datetime, raw: dict):
        self.horodatage_utc = horodatage_utc          # datetime UTC aware
        self.temperature    = Temperature(raw.get("temperature", {}))
        self.nebulosite     = Nebulosite(raw.get("nebulosite", {}))
        self.vent           = Vent(
            raw.get("vent_moyen", {}),
            raw.get("vent_rafales", {}),
            raw.get("vent_direction", {}),
        )
        self.humidite       = Humidite(raw.get("humidite", {}))
        self.pluie          = _safe(raw.get("pluie"))           # mm
        self.pluie_convective = _safe(raw.get("pluie_convective"))  # mm
        self.iso_zero       = _safe(raw.get("iso_zero"))        # m
        self.risque_neige   = raw.get("risque_neige")           # "oui"/"non"
        self.cape           = _safe(raw.get("cape"))            # J/kg
        self.pression_mer   = _safe(
            raw.get("pression", {}).get("niveau_de_la_mer")
        )                                                       # Pa

    # ── Sérialisation ────────────────────────────────────────────────────────
    
    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            horodatage_utc=datetime.datetime.strptime(
                data["horodatage_utc"],
                "%Y-%m-%d %H:%M:%S"),
            raw=data)

    def to_dict(self) -> dict:
        return {
            "horodatage_utc":   self.horodatage_utc.strftime("%Y-%m-%d %H:%M:%S"),
            "temperature":      self.temperature.to_dict(),
            "nebulosite":       self.nebulosite.to_dict(),
            "vent_moyen":       {"10m": self.vent.moyen},
            "vent_rafales":     {"10m": self.vent.rafales},
            "vent_direction":   {"10m":  self.vent.direction_deg},
            "humidite":         self.humidite.to_dict(),
            "pluie":            self.pluie,
            "pluie_convective": self.pluie_convective,
            "iso_zero":         self.iso_zero,
            "risque_neige":     self.risque_neige,
            "cape":             self.cape,
            "pression":         {"niveau_de_la_mer" :self.pression_mer},
        }

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=indent)

    @classmethod
    def from_json(cls, text: str) -> "EntreeMeteo":
        """Recrée une EntreeMeteo depuis sa représentation JSON (pour relecture fichier)."""
        d = json.loads(text)
        dt = datetime.datetime.strptime(
            d["horodatage_utc"], "%Y-%m-%d %H:%M:%S"
        ).replace(tzinfo=datetime.timezone.utc)

        # Reconstruction du dict brut attendu par __init__
        raw = {
            "temperature": {
                "2m":     d["temperature"]["2m"] + 273.15 if d["temperature"]["2m"] is not None else None,
                "sol":    d["temperature"]["sol"] + 273.15 if d["temperature"]["sol"] is not None else None,
            },
            "nebulosite":     d["nebulosite"],
            "vent_moyen":     {"10m": d["vent"]["moyen_kmh"]},
            "vent_rafales":   {"10m": d["vent"]["rafales_kmh"]},
            "vent_direction": {"10m": d["vent"]["direction_deg"]},
            "humidite":       {"2m": d["humidite"]["2m"]},
            "pluie":          d["pluie_mm"],
            "pluie_convective": d["pluie_convective_mm"],
            "iso_zero":       d["iso_zero_m"],
            "risque_neige":   d["risque_neige"],
            "cape":           d["cape_j_kg"],
            "pression":       {"niveau_de_la_mer": d["pression_mer_pa"]},
        }
        return cls(dt, raw)
    
    @staticmethod
    def retrieve_array_from_file_path(file_path : str):
        with open(file_path, "r") as f:
            raw_list = json.load(f)
        return [EntreeMeteo.from_dict(item) for item in raw_list]

    @staticmethod
    def write_array_in_file_path(file_path : str, all_entries):
        with open(file_path, "w") as f:
            json.dump([obj.to_dict() for obj in all_entries], f, indent=4)
    # ── Clé d'unicité ────────────────────────────────────────────────────────

    @property
    def cle_heure(self) -> str:
        """Clé unique par créneau horaire : 'YYYY-MM-DD HH:00'."""
        return self.horodatage_utc.strftime("%Y-%m-%d %H:00")

    # ── Affichage ────────────────────────────────────────────────────────────

    def __repr__(self):
        return (
            f"EntreeMeteo({self.horodatage_utc.strftime('%Y-%m-%d %H:%M')} UTC | "
            f"T={self.temperature.deux_metres}°C | "
            f"{self.nebulosite.description()} | "
            f"Pluie={self.pluie}mm)"
        )


# ─────────────────────────────────────────────────────────────────────────────
# Réponse complète de l'API (ensemble d'entrées)
# ─────────────────────────────────────────────────────────────────────────────

class ReponseAPI:
    """
    Contient toutes les EntreeMeteo parsées depuis une réponse JSON Infoclimat,
    plus les métadonnées de la requête.
    """

    def __init__(self, raw_json: dict):
        self.request_state = raw_json.get("request_state")
        self.request_key   = raw_json.get("request_key")
        self.message       = raw_json.get("message")
        self.model_run     = raw_json.get("model_run")
        self.source        = raw_json.get("source")
        self.entrees: list[EntreeMeteo] = []

        tz_utc = datetime.timezone.utc
        for cle, valeurs in raw_json.items():
            try:
                dt = datetime.datetime.strptime(cle, "%Y-%m-%d %H:%M:%S").replace(tzinfo=tz_utc)
                self.entrees.append(EntreeMeteo(dt, valeurs))
            except (ValueError, TypeError):
                continue

        self.entrees.sort(key=lambda e: e.horodatage_utc)

    @property
    def ok(self) -> bool:
        return self.request_state == 200

    def entrees_du_jour(self, date: datetime.date = None) -> list:
        """Retourne les entrées pour un jour UTC donné (par défaut aujourd'hui)."""
        if date is None:
            date = datetime.datetime.now(datetime.timezone.utc).date()
        return [e for e in self.entrees if e.horodatage_utc.date() == date]

    
    def prochaines_entrees(self, n_heures: int = 4) -> list:
        """Retourne les entrées entre maintenant et maintenant + n_heures."""
        now   = datetime.datetime.now(datetime.timezone.utc)
        limit = now + datetime.timedelta(hours=n_heures)
        return [
            e for e in self.entrees
            if now - datetime.timedelta(hours=1) <= e.horodatage_utc <= limit
        ]

    def entrees_entre_2_dates(self, date_1 : datetime.datetime , date_2 : datetime.datetime) -> list:
        """Retourne les 2 dates."""
        if (date_1 is None or date_2 is None) :
            return []
        return [
            e for e in self.entrees
            if date_1 <= e.horodatage_utc <= date_2
        ]

    def entree_actuelle(self) -> list:
        """Retourne l'entree la plus proche de maintenant"""
        if self.entrees is None or len(self.entrees) <= 0 : 
            return None
        
        now   = datetime.datetime.now(datetime.timezone.utc)
        last_difference = None
        closest_entree = None
        for e in self.entrees : 
            dif = abs(now - e.horodatage_utc)
            if last_difference is None or dif < last_difference : 
                closest_entree = e
                last_difference = dif
        return closest_entree

    def __repr__(self):
        return (
            f"ReponseAPI(state={self.request_state}, "
            f"source={self.source}, "
            f"entrees={len(self.entrees)})"
        )