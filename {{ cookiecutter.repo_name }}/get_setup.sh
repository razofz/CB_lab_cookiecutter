if command -v mamba &> /dev/null
then
    echo ">> Installing conda environment with mamba.."
    mamba env create -f envs/meta/snakemake-bioinf.yaml
    exit
elif command -v conda &> /dev/null
then
    echo ">> Installing conda environment with conda.."
    conda env create -f envs/meta/snakemake-bioinf.yaml
    exit
else
    echo "Neither mamba nor conda is installed, please install. Ask for help if needed."
fi
