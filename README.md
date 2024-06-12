# RealEstate10K_downloader
These scripts are used to download the RealEstate10K dataset.


## Requirement

Create and activate the conda environment:
```shell
conda env create -f environment.yaml
conda activate realestate10k
```

## How to use   
1. Prepare your data:
you should download [RealEstate10K](https://google.github.io/realestate10k/download.html) and extract it here manually.

Your directory structure should look like this:
``` 
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
```

2. Run the downloader:
```shell
python generate_dataset.py [mode] --height [HEIGHT] --width [WIDTH]

# Examples
python generate_dataset.py test --height 256 --width 384
python generate_dataset.py train --height 256 --width 384
```
This downloads YouTube movies and extract frames which are needed.  Because of unkown reasons, `pytube` fails to download and save movies. 
In this case, sequence name is added to `failed_videos_{test, train}.txt`.   

3. Check the output:
You can visualize camera poses using vizualizer.py. This script uses Open3D to show camera poses.

```shell
python vizualizer.py [/path/to/pose_data.txt]

# Example
python vizualizer.py ./RealEstate10K/test/0c4c5d5f751aabf5.txt
```

RealEstate10K(including images) is very large. 
Please be careful.    

## Contributing
Feel free to open issues or submit pull requests for improvements or bug fixes.

## License
This project is licensed under the MIT License.

