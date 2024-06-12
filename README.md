# RealEstate10K_downloader
These scripts are used to download the RealEstate10K dataset.


## Requirement

Create and activate the conda environment:
```shell
conda env create -f environment.yml
conda activate realestate10k
```

## How to use   
First, you should download [RealEstate10K](https://google.github.io/realestate10k/download.html) and extract it here manually.
<!-- Or you can choose to download the subset to do a quick test from [HF: yangtaointernship/RealEstate10K-subset](https://huggingface.co/datasets/yangtaointernship/RealEstate10K-subset) . -->


1 directory, 6 files
.
├── environment.txt
├── environment.yaml
├── generate_dataset.py
├── LICENSE
├── README.md
├── RealEstate10K
│   ├── test
│   └── train
└── vizualizer.py


```shell
python generate_dataset.py test --height 256 --width 384
```
This downloads YouTube movies and extract frames which are needed.  Because of unkown reasons, `pytube` fails to download and save movies. 
In this case, sequence name is added to `failed_videos_{test, train}.txt`.   
Also, `vizualizer.py` is placed here. This shows us camera poses using Open3d.
```shell
python vizualizer.py [/path/to/pose_data.txt]
e.g. (python3 vizualizer.py ./RealEstate10K/test/0c4c5d5f751aabf5.txt)
```

RealEstate10K(including images) is very large. 
Please be careful.    

