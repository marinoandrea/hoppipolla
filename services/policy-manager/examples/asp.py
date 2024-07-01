from datetime import datetime

from policy_manager.asp import AspManager
from policy_manager.entities import Data, Hop, Path


def main():
    asp = AspManager()

    # I do not want my traffic to be routed through any AS that has a
    # sustainability index less than a certain X.
    asp.create_policy('''
#const min_sustainability_index = 10.

:- Idx<min_sustainability_index,
    sustainability_index(Data, Idx),
    latest_data(_, Data).
    ''')

    asp.create_policy('''
#const min_renewable_energy_percentage = "0.5".

invalid_renewable_energy(Hop) :- Perc<min_renewable_energy_percentage,
    renewable_energy_percentage(Data, Perc),
    latest_data(Hop, Data).

:- invalid_renewable_energy(Hop), location(Hop, "italy").
:- invalid_renewable_energy(Hop), location(Hop, "greece").
:- invalid_renewable_energy(Hop), location(Hop, "spain").
''')

    # The aggregated sum across the path for energy_consumption_per_hour
    # cannot be higher than a certain X.
    asp.create_policy('''
#const max_sum_energy_consumption_per_hour = 1500.

sum_energy_consumption_per_hour(Path, Sum) :-
    path(Path),
    Sum = #sum { Value : energy_consumption_per_hour(Data, Value),
                latest_data(Hop, Data),
                contains(Path, Hop) }.

:- Value>max_sum_energy_consumption_per_hour,
    sum_energy_consumption_per_hour(Path, Value),
    path(Path).
    ''')

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
