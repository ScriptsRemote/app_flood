# Criado com base em : https://brasil.mapbiomas.org/wp-content/uploads/sites/4/2023/08/Legenda-Colecao-8-LEGEND-CODE.pdf
dicionario_cores = {
    0: "white",
    1: "#32a65e",
    3: "#1f8d49",
    4: "#7dc975",
    5: "#04381d",
    6: "#026975",
    49: "#02d659",
    10: "#ad975a",
    11: "#519799",
    12: "#d6bc74",
    32: "#fc8114",
    29: "#ffaa5f",
    50: "#ad5100",
    13: "#d89f5c",
    14: "#FFFFB2",
    15: "#edde8e",
    18: "#E974ED",
    19: "#C27BA0",
    39: "#f5b3c8",
    20: "#db7093",
    40: "#c71585",
    62: "#ff69b4",
    41: "#f54ca9",
    36: "#d082de",
    46: "#d68fe2",
    47: "#9932cc",
    48: "#e6ccff",
    9: "#7a5900",
    21: "#ffefc3",
    22: "#d4271e",
    23: "#ffa07a",
    24: "#d4271e",
    30: "#9c0027",
    25: "#db4d4f",
    26: "#0000FF",
    33: "#2532e4",
    31: "#091077",
    27: "#ffffff"
}

dicionario_classes = {
    0:"Fora da área de interesse",
    1: "Floresta",
    3: "Formação Florestal",
    4: "Formação Savânica",
    5: "Mangue",
    6: "Floresta Alagável (beta)",
    49: "Restinga Arborizada",
    10: "Formação Natural não Florestal",
    11: "Campo Alagado e Área Pantanosa",
    12: "Formação Campestre",
    32: "Apicum",
    29: "Afloramento Rochoso",
    50: "Restinga Herbácea",
    13: "Outras Formações não Florestais",
    14: "Agropecuária",
    15: "Pastagem",
    18: "Agricultura",
    19: "Lavoura Temporária",
    39: "Soja",
    20: "Cana",
    40: "Arroz",
    62: "Algodão (beta)",
    41: "Outras Lavouras Temporárias",
    36: "Lavoura Perene",
    46: "Café",
    47: "Citrus",
    48: "Outras Lavouras Perenes",
    9: "Silvicultura",
    21: "Mosaico de Usos",
    22: "Área não Vegetada",
    23: "Praia, Duna e Areal",
    24: "Área Urbanizada",
    30: "Mineração",
    25: "Outras Áreas não Vegetadas",
    26: "Corpo D'água",
    33: "Rio, Lago e Oceano",
    31: "Aquicultura",
    27: "Não observado"
}

## paleta
paleta_nomes = {key:value for key, value in zip(dicionario_classes.values(), dicionario_cores.values())}
# paleta_nomes

# Criando a paleta de cores
paleta_cores = {
    0: "#ffffff",1: "#32a65e", 2: "#32a65e",3: "#1f8d49",
    4: "#7dc975",5: "#04381d", 6: "#026975",7: "#000000",
    8: "#000000",9: "#7a6c00", 10: "#ad975a",11: "#519799",
    12: "#d6bc74",13: "#d89f5c", 14: "#FFFFB2",15: "#edde8e",
    16: "#000000",17: "#000000", 18: "#f5b3c8",19: "#C27BA0",
    20: "#db7093",21: "#ffefc3", 22: "#db4d4f",23: "#ffa07a",
    24: "#d4271e",25: "#db4d4f", 26: "#0000FF",27: "#000000",
    28: "#000000",29: "#ffaa5f", 30: "#9c0027",31: "#091077",
    32: "#fc8114",33: "#2532e4", 34: "#93dfe6",35: "#9065d0",
    36: "#d082de",37: "#000000", 38: "#000000",39: "#f5b3c8",
    40: "#c71585",41: "#f54ca9", 42: "#cca0d4",43: "#dbd26b",
    44: "#807a40",45: "#e04cfa", 46: "#d68fe2",47: "#9932cc",
    48: "#e6ccff",49: "#02d659", 50: "#ad5100",51: "#000000",
    52: "#000000",53: "#000000", 54: "#000000",55: "#000000",
    56: "#000000",57: "#CC66FF", 58: "#FF6666",59: "#006400",
    60: "#8d9e8b",61: "#f5d5d5", 62: "#ff69b4"
}
palette_list = list(paleta_cores.values())
# len(palette_list)

palette_cos =[
              'ffffff','ffffe5','fff7bc','fee391','fec44f','fe9929','ec7014','cc4c02','993404','662506'
            ]

