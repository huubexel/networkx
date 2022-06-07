
def get_data_first_participant():
    with open("data/NEWwysiwyg_cie_LLLL0_2721341_s_.txt", "r") as f:
        data = f.read()
    print(data)


def get_data_second_participant():
    with open("data/NEWwysiwyg_cie_LLLL0_2721341_o_s2019779.txt", "r") as f:
        data = f.read()
    print(data)


def get_time_between():
    with open("data/NEWwysiwyg_cie_LLLL0_2721341_t_.txt", "r") as f:
        data = f.read()
    print(data)


def get_which_interface():
    with open("data/NEWwysiwyg_cie_LLLL0_2721341_w_.txt", "r") as f:
        data = f.read()
    print(data)

def main():
    get_data_first_participant()
    print("\n\n\n\n\n")
    get_data_second_participant()
    print("\n\n\n\n\n")
    get_time_between()
    print("\n\n\n\n\n")
    get_which_interface()



    # Q1 tijd tussen antwoorden en totale tijd voor het verkrijgen van bijv een antwoord
    # Huub

    # Q2 hoeveelheid woorden nodig per interface, en dan ook kijken naar verschil per persoon
    # Rutger

    # Q3 Je pakt de woorden van beide en gaat kijken welke de meeste overlap hebben.
    # Rutger

    # Q4 woordenlijst met vrolijke woorden en gaat kijken welke interface deze meer voorkomen.

    # Q5 Woordenlijst met zowel vrolijke als niet vrolijke woorden en dan kijken welke meer gebruikt worden in welke
    # dit ook met een percentage enzo.

    # Q6 Je moet door die bestanden gaan en kijken welke woorden of signalen worden gebruikt om
    # confirmatie aan te geven, en dan tegelijkertijd ook welke een fout antwoord aangeven (indien van toepassing)
    # en als je iets tegenkomt dit in de buurt komt dan reken je dat.

    # Q7


if __name__ == "__main__":
    main()
