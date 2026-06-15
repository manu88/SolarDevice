import sys
from config.Config import Config


def print_conf(conf: Config):
    print("General:")
    print(f"\tGPS: {conf.get_gps_coords()}")
    print(f"\tHeures: {conf.get_heures()}")
    print(f"\tVernissage: {conf.is_vernissage()}")
    print("Seuils:")
    print(f"\tS-A-1: {conf.get_SA1()}")
    print(f"\tS-A-2: {conf.get_SA2()}")
    print(f"\tS-B: {conf.get_SB()}")
    print(f"\tS-C: {conf.get_SC()}")


def main(config_path: str) -> int:
    conf = Config.from_json_file(config_path)

    valid = "valid" if conf.is_valid else "invalid"
    print(f"file config '{config_path}' is {valid}")
    if conf.is_valid:
        print_conf(conf)
    return 0 if conf.is_valid else 1


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage python3 check-config.py filepath")
        sys.exit(1)
    config_path = sys.argv[1]
    sys.exit(main(config_path))
