# ActionViewer
This repository is the Action Viewer for the ICVL Action Dataset. More information can be find on our [paper](https://arxiv.org/abs/1710.03383). Following image indicates a hierarchical action structure. There are 4 layers, posture, locomotiom, gesture, and event layer. So, one action is represented 4 sub-action labels.  

<p align="center">
<img src="https://user-images.githubusercontent.com/37034031/50048699-74ae5080-0116-11e9-805a-a4ef2f93f84c.png" width=700>
</p>

## Requirements
- opencv 3.3.1
- numpy 1.15.4
- xlsxwriter 0.9.6

## Action Viewer Demo
<p align = 'center'>
<img src = 'https://user-images.githubusercontent.com/37034031/50048604-f650af00-0113-11e9-91b5-ec3b3f7f4edc.gif'>
</p> 

## Documentation
### Directory Hierarchy
``` 
.
│   ActionViewer
│   ├── DB
│   │   ├── AR-002-12-20151017-01-09.mkv
│   │   ├── AR-002-12-20151017-01-09.txt
│   │   ├── AR-003-12-20151024-02-04.avi
│   │   └──  AR-003-12-20151024-02-04.txt
│   ├── Icon
│   │   ├── Bending.bmp
│   │   ├── Bicycling.bmp
│   │   ├── Falling.bmp
│   │   ├── Littering.bmp
│   │   ├── Lying.bmp
│   │   ├── Nothing.bmp
│   │   ├── Others.bmp
│   │   ├── Phoning.bmp
│   │   ├── Running.bmp
│   │   ├── Sitting.bmp
│   │   ├── Smoking.bmp
│   │   ├── Standing.bmp
│   │   ├── Stationary.bmp
│   │   ├── Texting.bmp
│   │   └──  Walking.bmp
│   ├── ICVL_action_structure.py
│   ├── ICVL_data_reader.py
│   ├── main.py
│   └──  write2excel.py
```  

### Run Action-Viewer
Run `main.py` in the ActionViewer.

```
python main.py
```  
- `--resize_ratio`: resize ratio for input frame, default: `1.0`  
- `--interval_time`: interval time between two frames, default: `20`  
**Note:** main.py read all of the videos and the corresponing txt files. 

### ICVL Dataset
Click [here](https://www.dropbox.com/sh/qvetvo6eqz1oi9l/AACXIqWiAaXNGlvpD3qUncAva?dl=0) to download ICVL dataset. Please cite our following paper to use ICVL dataset.

### Citation
```
@article{jin2017real,
  title={Real-time action detection in video surveillance using sub-action descriptor with multi-cnn},
  author={Jin, Cheng-Bin and Li, Shengzhe and Kim, Hakil},
  journal={arXiv preprint arXiv:1710.03383},
  year={2017}
}
```  

## License
Copyright (c) 2018 Cheng-Bin Jin. Contact me for commercial use (or rather any use that is not academic research) (email: sbkim0407@gmail.com). Free for research use, as long as proper attribution is given and this copyright notice is retained.
