import csv
import pyperclip

CONFS = []
# Define confs here
MAGICIEN = {
    "fichier": "magicien.csv",
    "icone": "fairy-wand",
    "couleur": "maroon",
    "tag": "magicien"
}
CONFS.append(MAGICIEN)

PALADIN = {
    "fichier": "paladin.csv",
    "icone": "templar-shield",
    "couleur": "navy",
    "tag": "paladin"
}
CONFS.append(PALADIN)

DRUIDE = {
    "fichier": "druide.csv",
    "icone": "oak-leaf",
    "couleur": "darkgreen",
    "tag": "druide"
}
CONFS.append(DRUIDE)

DRUIDE = {
    "fichier": "ranger.csv",
    "icone": "hooded-figure",
    "couleur": "saddlebrown",
    "tag": "ranger"
}
CONFS.append(DRUIDE)


def clean_up(row):
    for key, value in row.items():
        row[key] = value.replace("\ufeff", "").replace("\xa0", " ")
    text = row['Description']
    if text[0] == '(':
        paren_index = text.find(')')
        if paren_index != -1:
            mat_comp = text[:paren_index+1]
            row['Description'] = text[paren_index+1:]
            row['Composantes'] = row['Composantes'] + mat_comp
    return row


def get_tags(row, conf):
    tags = []
    tags.append("sort")

    # Tag de la classe
    classe = row['Classe']
    tags.append(conf["tag"])

    # Tag du niveau
    niveau = row['Niveau']
    tags.append(f"niveau{niveau}")
    return tags


def generate_cards(conf):
    cards = []
    with open(conf["fichier"], newline='', encoding="utf-8-sig") as csvfile:
        headers = ["Niveau", "Nom", "École", "Durée d'incantation", "Portée", "Composantes", "Durée", "Description", "Classe"]
        reader = csv.DictReader(csvfile, fieldnames=headers, delimiter=";")
        for row in reader:
            row = clean_up(row)
            duree = row["Durée d'incantation"]
            card_data = {}
            card_data["count"] = 1
            card_data["color"] = conf["couleur"]
            card_data["title"] = row['Nom']
            card_data["icon"] = f"white-book-{row['Niveau']}"
            card_data["icon_back"] = conf["icone"]
            card_data["contents"] = [f"subtitle | {row['École']}",
                                     "rule",
                                     f"property | Durée d'incantation | {duree}",
                                     f"property | Portée | {row['Portée']}",
                                     f"property | Composantes | {row['Composantes']}",
                                     f"property | Durée | {row['Durée']}",
                                     "rule",
                                     "fill | 2",
                                     f"text | {row['Description']}",
                                     "fill | 3",
                                    ]
            card_data["tags"] = get_tags(row, conf)
            cards.append(str(card_data))
    return cards


if __name__ == "__main__":
    cards = []
    for conf in CONFS:
        cards.extend(generate_cards(conf))
    cards_str = ',\n\t'.join(cards)
    return_string = f"var card_data_example = [\n\t{cards_str}\n]"
    pyperclip.copy(return_string)
