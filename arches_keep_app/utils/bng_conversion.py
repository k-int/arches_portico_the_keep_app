def convert(grid_ref):

    if not grid_ref: return None

    if type(grid_ref) != str:
        raise TypeError("Grid reference argument must be a string")

    grid_squares = {
        "NA": (0, 900), "NB": (100, 900), "NC": (200, 900), "ND": (300, 900), "NE": (400, 900), "OA": (500, 900),
        "NF": (0, 800), "NG": (100, 800), "NH": (200, 800), "NJ": (300, 800), "NK": (400, 800), "OF": (500, 800),
        "NL": (0, 700), "NM": (100, 700), "NN": (200, 700), "NO": (300, 700), "NP": (400, 700), "OL": (500, 700),
        "NQ": (0, 600), "NR": (100, 600), "NS": (200, 600), "NT": (300, 600), "NU": (400, 600), "OQ": (500, 600),
        "NV": (0, 500), "NW": (100, 500), "NX": (200, 500), "NY": (300, 500), "NZ": (400, 500), "OV": (500, 500),
        "SA": (0, 400), "SB": (100, 400), "SC": (200, 400), "SD": (300, 400), "SE": (400, 400), "TA": (500, 400),
        "SF": (0, 300), "SG": (100, 300), "SH": (200, 300), "SJ": (300, 300), "SK": (400, 300), "TF": (500, 300), "TG": (600, 300),
        "SL": (0, 200), "SM": (100, 200), "SN": (200, 200), "SO": (300, 200), "SP": (400, 200), "TL": (500, 200), "TM": (600, 200),
        "SQ": (0, 100), "SR": (100, 100), "SS": (200, 100), "ST": (300, 100), "SU": (400, 100), "TQ": (500, 100), "TR": (600, 100),
        "SV": (0, 0),   "SW": (100, 0),   "SX": (200, 0),   "SY": (300, 0),   "SZ": (400, 0),   "TV": (500, 0),   "TW": (600, 0)
    }  

    prefix = grid_ref[:2]
    digits = grid_ref[2:]

    if len(digits) % 2 != 0:
        raise ValueError("Uneven number of digits in grid reference")
    halfLength = len(digits) // 2

    try:
        prefixLocation = grid_squares[prefix]
    except:
        raise ValueError("Grid square invalid")

    eastingBase = prefixLocation[0] * 1000
    northingBase = prefixLocation[1] * 1000

    eastingDigits = int(digits[:halfLength].ljust(5, '0'))
    northingDigits =  int(digits[halfLength:].ljust(5, '0'))

    returnGrid = (eastingBase + eastingDigits, northingBase + northingDigits)
    return returnGrid