import requests
import re
import pprint
import time
import csv

def write_to_csv(filepath, pokemon_list):
    with open(f"{filepath}", mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        # เขียน header
        writer.writerow(["Number", "Name", "Type", "All",  "HP", "Attack", "Defense", "Sp. Atk", "Sp. Def", "Speed", "image"])
        
        for p in pokemon_list:
            writer.writerow([p["Number"], p["Name"], p["image"], p["Type"], p["All"], p["HP"], p["Attack"], p["Defense"], p["Sp. Atk"], p["Sp. Def"], p["Speed"]])

def crawling(query: str = None):
    base_path = "https://pokemondb.net/pokedex/"
    start_path = "all"
    response = requests.get(f'{base_path}{start_path}')

    if response.status_code == 200:
        html = response.text

        tbody_match = re.search(r'<tbody>(.*?)</tbody>', html, re.DOTALL)
        if tbody_match:
            tbody_html = tbody_match.group(1)

            rows = re.findall(r'<tr>(.*?)</tr>', tbody_html, re.DOTALL)

            pokemon_list = []

            for row in rows:
                cols = re.findall(r'<td.*?>(.*?)</td>', row, re.DOTALL)
                if len(cols) >= 10:
                    number = re.sub(r'<.*?>', '', cols[0]).strip()
                    name_match = re.search(r'<a [^>]+>([^<]+)</a>', cols[1])
                    image_match = re.search(r'<picture.*?>.*?<img[^>]+src="([^"]+)"', cols[0], re.DOTALL)
                    image = re.sub(r'/sprites/scarlet-violet/icon/(.*)\.png',r'/artwork/large/\1.jpg',image_match.group(1))
                    name = name_match.group(1) if name_match else ''
                    if query and not re.search(query, name, re.IGNORECASE):
                        continue
                    type_text = re.sub(r'<.*?>', '', cols[2]).strip()
                    stats = [re.sub(r'<.*?>', '', c).strip() for c in cols[3:]]
                    pokemon_list.append({
                        "Number": number,
                        "Name": name,
                        "image": image,
                        "Type": type_text.split(),
                        "All":stats[0], 
                        "HP":stats[1], 
                        "Attack":stats[2], 
                        "Defense":stats[3], 
                        "Sp. Atk":stats[4], 
                        "Sp. Def":stats[5],
                        "Speed":stats[6], 
                    })
            # pprint.pp(pokemon_list)
            return pokemon_list
    else:
        return []

if __name__ == "__main__" :
    pokemon_list = crawling()
    write_to_csv('pokemon_2.csv', pokemon_list)
    print(time.ctime())
