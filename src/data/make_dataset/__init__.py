import file_manager as fm
import json

def make():
    """
        makes data set

        :returns
        list[dict] fighters
            list of dictionaries containing fighter information
    """

    filePath = fm.get_absolute_path('data/raw/fighters.json')

    fighters = [json.loads(line) for line in open(filePath)]

    return fighters
