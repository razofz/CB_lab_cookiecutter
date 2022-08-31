import os
import re
import shutil
import pandas as pd
import yaml


def set_project_path():
    try:
        path = os.environ["PROJECT_PATH"]
    except KeyError:
        path = ""
    if len(path) == 0:
        path = "../"
    os.chdir(path)


set_project_path()


GLOBAL_FIGURES_PATH = "figures/"

# with open("figure_mapping.yaml", "r") as f:
with open(GLOBAL_FIGURES_PATH + "figmap.yaml", "r") as f:
    fig_map_dict = yaml.safe_load(f)

print(f"> {len(fig_map_dict['mainfigs'].keys())} main figures,")
print(f"> {len(fig_map_dict['supfigs'].keys())} supplementary figures.")

def extract_figure_src_dest(key, value, level):
    TAB = str(level*"\t")
    if isinstance(value, str):
        source = value
        destination = GLOBAL_FIGURES_PATH + key + os.path.splitext(value)[1]
        yield (source, destination)
    elif isinstance(value, dict):
        for subfig in value.items():
            yield from extract_figure_src_dest(key+subfig[0], subfig[1], level+1)
    elif isinstance(value, list):
        for i in range(len(value)):
            yield from extract_figure_src_dest(key+str(i+1), value[i], level+1)
    else:
        raise Exception("Something went wrong with the figure gathering, " +
                        "check that the yaml file is read correctly.")


def get_copylist(map_dict):
    results = []
    for key in map_dict.keys():
        for fig in fig_map_dict[key].items():
            result = [x for x in extract_figure_src_dest(fig[0], fig[1], 0)]
            if isinstance(result, str):
                results.append(result)
            elif isinstance(result, list):
                for r in result:
                    results.append(r)
    return results


results = get_copylist(fig_map_dict)
print("\n")
print(f"{len(results)=}")
for r in results:
    print(f"cp {r[0]} {r[1]}")
