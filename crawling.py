import requests
import re
import csv
import html

class Stack:
    def __init__(self):
        self._items = []

    def push(self, item):
        self._items.append(item)

    def pop(self):
        if not self._items:
            raise IndexError("pop from empty stack")
        return self._items.pop()

    def is_empty(self):
        return len(self._items) == 0

base_path = "https://pokemondb.net/pokedex/"

def write_to_csv(filepath, pokemon_list):
    with open(f"{filepath}", mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Number", "Name", "Description"])
        
        for p in pokemon_list:
            writer.writerow([p["Number"], p["Name"], p["Description"]])

def crawling(query: str = None):
    start_path = "all"
    response = requests.get(f'{base_path}{start_path}')

    if response.status_code == 200:
        source = response.text

        tbody_match = re.search(r'<tbody>(.*?)</tbody>', source, re.DOTALL)
        if tbody_match:
            tbody_html = tbody_match.group(1)

            rows = re.findall(r'<tr>(.*?)</tr>', tbody_html, re.DOTALL)

            pokemon_list = []

            for row in rows:
                cols = re.findall(r'<td.*?>(.*?)</td>', row, re.DOTALL)
                if len(cols) >= 10:
                    number = re.sub(r'<.*?>', '', cols[0]).strip()
                    name_match = re.search(r'<a [^>]+>([^<]+)</a>', cols[1])
                    name = name_match.group(1) if name_match else ''
                    if query and not re.search(query, name, re.IGNORECASE):
                        continue
                    description_match = re.search(r'<small.*?>(.*?)</small>', cols[1], re.DOTALL)
                    description = description_match.group(1) if description_match else " " 
                    image_match = re.search(r'<picture.*?>.*?<img[^>]+src="([^"]+)"', cols[0], re.DOTALL)
                    image = re.sub(r'/sprites/scarlet-violet/icon/(.*)\.png',r'/artwork/large/\1.jpg',image_match.group(1))
                    type_text = re.sub(r'<.*?>', '', cols[2]).strip()
                    stats = [re.sub(r'<.*?>', '', c).strip() for c in cols[3:]]

                    detail = call_detail_pokemon(name,description)

                    pokemon_list.append({
                        "Number": number,
                        "Name": name,
                        "Description": description,
                        "image": detail["Image"],
                        "Type": type_text.split(),
                        "Species": detail["Species"],
                        "Height": detail["Height"],
                        "Weight": detail["Weight"],
                        "All":stats[0], 
                        "HP":stats[1], 
                        "Attack":stats[2], 
                        "Defense":stats[3], 
                        "Sp. Atk":stats[4], 
                        "Sp. Def":stats[5],
                        "Speed":stats[6],
                    })

            return pokemon_list
    else:
        return []
    
def call_detail_pokemon(name: str,description: str):
    tmp_str = ""
    for i in name:
        if i == ' ' :
            tmp_str += '-'
        elif i == "'" or i == '.' or i == ':':
            continue
        elif i == 'é':
            tmp_str += 'e'
        elif i == '♂':
            tmp_str += '-m'
        elif i == '♀':
            tmp_str += '-f'
        else:
            tmp_str += i

    response = requests.get(f'{base_path}{tmp_str.lower()}')
    if response.status_code == 200:
        source = response.text

        new_path = re.search(r'<div class="sv-tabs-tab-list".*?>(.*?)</div>',source,re.DOTALL)
        new_new_path = re.findall(r'<a.*?href="#([^"]+)">(.*?)</a>',new_path.group(1),re.DOTALL)
        path_match = {}

        for path,n in new_new_path:
            path_match[n] = path
        print(new_new_path)
        block = extract_div_block(source,path_match[name if description == " " else description])
        image_match = re.search(r'<p>.*?"(https://[^"]+)+".*?>',block,re.DOTALL)
        image = image_match.group(1)


        data = re.search(r'<div.*?Pokédex data.*?(<tbody>.*?</tbody>).*?</div>',block,re.DOTALL)
        cols = re.findall(r'<td>.*?</td>',data.group(1),re.DOTALL)
        cols_clean = [re.sub(r'<.*?>', '', c).strip() for c in cols]
        species  = cols_clean[2]
        height   = html.unescape(cols_clean[3]).replace('\xa0', ' ')
        weight   = html.unescape(cols_clean[4]).replace('\xa0', ' ')

        pokemon = {
            "Image": image,
            "Species": species,
            "Height": height,
            "Weight": weight,
        }

        return pokemon

    else:
        print("sd")
        return {
            "Image":None,
            "Species": None,
            "Height": None,
            "Weight": None,
        }

def extract_div_block(soruce: str, start_id: str):
    open_tag_pattern = re.compile(rf'<div[^>]*id="{re.escape(start_id)}"[^>]*>', re.IGNORECASE)
    m = open_tag_pattern.search(soruce)
    if not m:
        return None
    
    start_pos = m.start()
    pos = m.end()

    tag_pattern = re.compile(r'</?div\b[^>]*>', re.IGNORECASE)

    stack = Stack()
    stack.push('div')

    for t in tag_pattern.finditer(soruce, pos):
        tag = t.group(0).lower()
        if tag.startswith('</'):
            stack.pop()
            if stack.is_empty():
                return soruce[start_pos:t.end()]
        else:
            stack.push('div')

    return None
   
if __name__ == "__main__" :
    print()
    # pokemon_list = crawling()
    # write_to_csv('pokemon_2.csv', pokemon_list)

    pokemon_list = crawling("Ogerpon")
    print(pokemon_list,sep='\n\n')
    # write_to_csv('pokemon_2.csv', pokemon_list)

    # pokemon = each_pokemon("Bulbasaur"," ")
    # print(pokemon)

    # pokemon = each_pokemon("Venusaur","Mega Venusaur")
    # print(pokemon)

    # pokemon = each_pokemon("Venusaur"," ")
    # print(pokemon)