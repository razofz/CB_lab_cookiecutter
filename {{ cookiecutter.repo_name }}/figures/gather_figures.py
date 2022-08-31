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


def copy_figure(key, value, level):
    TAB = level*"\t"
    # print(f"{TAB}> cf_entry: {key=}")
    # print(f"\t> copy_figure: {type(value)=}")
    if type(value) == str:
        source = value
        destination = GLOBAL_FIGURES_PATH + key + os.path.splitext(value)[1]
        # print(f"{TAB}\t!> cf: cp {source} {destination}")
        yield (source, destination)
    elif type(value) == dict:
        # print(f"{TAB}\t> a dict: {len(value.keys())=}")
        if len(value.keys()) == 1:
            print(f"{TAB}\t> dictcopy: Copying {value[1]}..")
            pass
        else:
            for subfig in value.items():
                yield from copy_figure(key+subfig[0], subfig[1], level+1)
    elif type(value) == list:
        for i in range(len(value)):
            # print(f"{TAB}\t!> cf: Copying {key+str(i+1)} {value[i]}..")
            # print(f"{TAB}\t!> cf: cp {GLOBAL_FIGURES_PATH}{key+str(i+1)+os.path.splitext(value[i])[1]} {value[i]}")
            # print(TAB+"\t", key+str(i+1), value[i], level+1)
            yield from copy_figure(key+str(i+1), value[i], level+1)
    else:
        # print(f"\t> cf: {value}, {type(value)}")
        raise Exception("Something went wrong with the figure gathering, " +
                        "check that the yaml file is read correctly.")
results = []
for fig in fig_map_dict["mainfigs"].items():
    # print(f"{fig[0]}:: {len(fig[1])}")
    result = [x for x in copy_figure(fig[0], fig[1], 0)]
    if isinstance(result, str):
        results.append(result)
    elif isinstance(result, list):
        for r in result:
            results.append(r)
    print(f"> RETURN: \n\t{len(result)=} \n\t{result=}")
for fig in fig_map_dict["supfigs"].items():
    # print(f"{fig[0]}:: {len(fig[1])}")
    result = [x for x in copy_figure(fig[0], fig[1], 0)]
    if isinstance(result, str):
        results.append(result)
    elif isinstance(result, list):
        for r in result:
            results.append(r)
    print(f"> RETURN: \n\t{len(result)=} \n\t{result=}")
    # copy_figure(fig[0], fig[1], 0)
print("\n")
print(f"{len(results)=}")
for r in results:
    print(f"{r}")
