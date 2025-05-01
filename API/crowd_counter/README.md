---
library_name: monai
tags:
- crowd-counting
- cnn
- detection
license: mit
metrics:
- mae
pipeline_tag: object-detection
datasets:
- ShanghaiTechDataset
---
---

### Model Description
A machine learning model for crowd counting

- **Model type:** image-classifier
- **License:** mit

## Crowd Counting Model
The aim is to build a model that can estimate the amount of people in a crowd from an image-

The model was built using **CSRNet** a  crowd counting neural network designed by Yuhong Li, Xiaofan Zhang and Deming Chen ([https://github.com/leeyeehoo/CSRNet-pytorch](https://github.com/leeyeehoo/CSRNet-pytorch))

### Model Sources 

- **Repository:** [https://github.com/leeyeehoo/CSRNet-pytorch](https://github.com/leeyeehoo/CSRNet-pytorch)

## Uses

This model was created in the spirit of creating a model capable of counting the amount of people in a crowd using images.

### Direct Use

```bash
model = CSRNet()
checkpoint = torch.load("weights.pth")
model.load_state_dict(checkpoint)
model.predict()

```

## Bias, Risks, and Limitations

Although the model can be very accurate its not exact, it has a 2%-6% error in the prediction.

## Training Details

### Training Data

The model was trained using the ShanghaiTech Dataset, specifically the Shanghai B Dataset.

### Training Procedure

The info on training procedure can be found in this repository [https://github.com/leeyeehoo/CSRNet-pytorch](https://github.com/leeyeehoo/CSRNet-pytorch)

## Evaluation and Results

The model reached a MAE of 10.6

## Citation

### Model creation and training

@inproceedings{li2018csrnet,
  title={CSRNet: Dilated convolutional neural networks for understanding the highly congested scenes},
  author={Li, Yuhong and Zhang, Xiaofan and Chen, Deming},
  booktitle={Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition},
  pages={1091--1100},
  year={2018}
}

### Dataset

@inproceedings{zhang2016single,
  title={Single-image crowd counting via multi-column convolutional neural network},
  author={Zhang, Yingying and Zhou, Desen and Chen, Siqin and Gao, Shenghua and Ma, Yi},
  booktitle={Proceedings of the IEEE conference on computer vision and pattern recognition},
  pages={589--597},
  year={2016}
}