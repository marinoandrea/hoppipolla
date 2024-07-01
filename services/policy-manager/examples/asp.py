from datetime import datetime

from policy_manager.asp import AspManager
from policy_manager.entities import Data, Hop, Path


def main():
    asp = AspManager()

    p1, p2, p3 = "", "", ""
    with open("./policies/min-sustainability-index.lp", "r") as file_p1, \
            open("./policies/min-renewable-location.lp", "r") as file_p2, \
            open("./policies/aggregate-energy-consumption.lp", "r") as file_p3:
        p1 = file_p1.read()
        p2 = file_p2.read()
        p3 = file_p3.read()

    asp.create_policy(p1)
    asp.create_policy(p2)
    asp.create_policy(p3)

    d1h1 = Data(data_collected_date=datetime(2024, 5, 1),
                sustainability_index=20,
                location="italy",
                renewable_energy_percentage=0.1)

    d1h2 = Data(data_collected_date=datetime(2024, 5, 1),
                sustainability_index=10,
                location="italy",
                renewable_energy_percentage=0.9)

    d1h3 = Data(data_collected_date=datetime(2024, 5, 1),
                sustainability_index=50,
                location="germany",
                renewable_energy_percentage=0.9)

    h1 = Hop("17-ff00:0:110", [d1h1])
    h2 = Hop("27-ff00:0:230", [d1h2])
    h3 = Hop("42-ff00:0:312", [d1h3])

    p1 = Path(
        "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        [h1, h2, h3])

    print(asp.validate(p1))


if __name__ == "__main__":
    main()
