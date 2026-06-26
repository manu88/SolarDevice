import csv
import datetime
import ast
from SharedPacket import SharedPacket
import os
import random

class SharedPacketHelper : 
    @staticmethod
    def csv_header():
        return [
            "date",
            "charge_batterie_pourcent",
            "power_input_watt",
            "power_output_watt",
            "consommation_charge_watt",
            "nebulosite_actuelle",
            "nebulosite_lendemain",
            "lever_soleil",
            "coucher_soleil",
            "lever_soleil_lendemain",
            "coucher_soleil_lendemain",
            "vitesse_mendocinos_rpm",
        ]

    @staticmethod
    def to_csv_row(packet : SharedPacket):
        return [
            packet.date.isoformat(timespec="seconds"),
            packet.charge_batterie_pourcent,
            packet.power_input_watt,
            packet.power_output_watt,
            packet.consommation_charge_watt,
            packet.nebulosite_actuelle,
            packet.nebulosite_lendemain,
            packet.lever_soleil.isoformat(timespec="minutes"),
            packet.coucher_soleil.isoformat(timespec="minutes"),
            packet.lever_soleil_lendemain.isoformat(timespec="minutes"),
            packet.coucher_soleil_lendemain.isoformat(timespec="minutes"),
            str(packet.vitesse_mendocinos_rpm),
        ]

    @staticmethod
    def from_csv_row(row):
        packet = SharedPacket()

        packet.date = datetime.datetime.fromisoformat(row["date"])
        packet.charge_batterie_pourcent = float(row["charge_batterie_pourcent"])
        packet.power_input_watt = float(row["power_input_watt"])
        packet.power_output_watt = float(row["power_output_watt"])
        packet.consommation_charge_watt = float(row["consommation_charge_watt"])
        packet.nebulosite_actuelle = float(row["nebulosite_actuelle"])
        packet.nebulosite_lendemain = float(row["nebulosite_lendemain"])
        
        packet.lever_soleil = datetime.datetime.fromisoformat(row["lever_soleil"]),
        packet.coucher_soleil = datetime.datetime.fromisoformat(row["coucher_soleil"]),
        packet.lever_soleil_lendemain = datetime.datetime.fromisoformat(row["lever_soleil_lendemain"]),
        packet.coucher_soleil_lendemain = datetime.datetime.fromisoformat(row["coucher_soleil_lendemain"]),

        packet.vitesse_mendocinos_rpm = ast.literal_eval(
            row["vitesse_mendocinos_rpm"]
        )

        return packet
    

    @staticmethod
    def append_packet(filename, packet: SharedPacket):
        need_header = (
            not os.path.exists(filename)
            or os.path.getsize(filename) == 0
        )
        with open(filename, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            if need_header:
                writer.writerow(SharedPacketHelper.csv_header())
            writer.writerow(SharedPacketHelper.to_csv_row(packet))
        return

    def load_packets(filename):
        packets = []

        with open(filename, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                packets.append(SharedPacketHelper.from_csv_row(row))

        return packets


    
    @staticmethod
    def create_random_packet() : 
        packet = SharedPacket()

        # Random date within last 30 days
        packet.date = (
            datetime.datetime.now()
            - datetime.timedelta(
                days=random.randint(0, 30),
                hours=random.randint(0, 23),
                minutes=random.randint(0, 59)
            )
        )

        # Battery level (%)
        packet.charge_batterie_pourcent = random.randint(0, 100)

        # Solar irradiance (W)
        packet.power_input_watt = random.randint(0, 1500)
        packet.power_output_watt = random.randint(0, 1500)
        
        # Load consumption (W)
        packet.consommation_charge_watt = random.randint(0, 500)

        # Cloud cover (%)
        packet.nebulosite_actuelle = random.randint(0, 100)
        packet.nebulosite_lendemain = random.randint(0, 100)

        # Sunrise / sunset
        today = packet.date.date()
        
        packet.lever_soleil = datetime.datetime.combine(
            today,
            datetime.time(
                hour=random.randint(5, 8),
                minute=random.randint(0, 59)
            )
        )

        packet.coucher_soleil = datetime.datetime.combine(
            today,
            datetime.time(
                hour=random.randint(18, 22),
                minute=random.randint(0, 59)
            )
        )

        tomorrow = today + datetime.timedelta(days = 1)
        packet.lever_soleil_lendemain = datetime.datetime.combine(
            tomorrow,
            datetime.time(
                hour=random.randint(5, 8),
                minute=random.randint(0, 59)
            )
        )

        packet.coucher_soleil_lendemain = datetime.datetime.combine(
            tomorrow,
            datetime.time(
                hour=random.randint(18, 22),
                minute=random.randint(0, 59)
            )
        )


        # RPM of X motors (1 to 6 motors)
        packet.vitesse_mendocinos_rpm = [
            [random.randint(0, 10)
            for _ in range(6)],
            [random.randint(0, 10)
            for _ in range(6)]
        ]
        return packet