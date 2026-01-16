# IDTNet: Brain Tumor Classification Using Hybrid CNN Architecture

A novel deep learning approach for classifying brain tumors in MRI scans using IDTNet, a hybrid convolutional neural network that combines Inception modules, DenseNet connectivity, and transition layers with skip connections.

## 🎯 Overview

This project introduces IDTNet (Inception-Dense-Transition Network), a custom CNN architecture designed specifically for brain tumor classification from MRI images. The model achieves 98.17% accuracy in classifying four types of brain conditions: Glioma, Meningioma, Pituitary tumors, and No Tumor cases.

### Key Features

- **Hybrid Architecture**: Combines strengths of Inception modules, DenseNet connectivity, and transition layers
- **High Performance**: Achieves 98.17% accuracy with 100% recall on meningioma class
- **Comprehensive Dataset**: Trained on 7,023 MRI images from multiple sources (Figshare, SARTAJ, Br35H)
- **Robust Preprocessing**: Includes aggressive data augmentation and normalization techniques
- **Comparative Analysis**: Benchmarked against VGG16, DenseNet121, and InceptionV1 architectures


## 📊 Dataset Information

| Class | Training Set | Testing Set | Total Images |
| :-- | :-- | :-- | :-- |
| Glioma | 1,326 | 300 | 1,626 |
| Meningioma | 1,339 | 306 | 1,645 |
| Pituitary | 1,457 | 300 | 1,757 |
| No Tumor | 1,590 | 405 | 1,995 |
| **Total** | **5,712** | **1,311** | **7,023** |

## 🏗️ Architecture

IDTNet features a novel hybrid architecture that includes:

- **Initial Convolutional Block**: 64 filters with 7×7 kernel size
- **Dense Blocks**: Progressive feature expansion with growth rate of 32
- **Transition Layers**: Feature compression using 1×1 convolution and 2×2 average pooling
- **Skip Connections**: Multi-level connections to preserve intermediate features
- **Parameters**: ~54 million trainable parameters


### Data Preprocessing Pipeline

1. **Image Resizing**: 512×512×3 → 128×128×3 pixels
2. **Data Shuffling**: Prevents concentration on dataset subsets
3. **Train/Validation Split**: 80%/20% distribution
4. **Data Augmentation**:
    - Random rotation (±10 degrees)
    - Width/height shifts (10% range)
    - Shear transformation (10% range)
    - Zoom (10% range)
    - Horizontal flipping
    - Nearest-neighbor filling

## 📈 Results

### Model Performance

| Model | Accuracy | Precision | Recall | F1-Score | MCC |
| :-- | :-- | :-- | :-- | :-- | :-- |
| VGG16 | 95.0% | 0.96 | 0.95 | 0.95 | 0.94 |
| DenseNet121 | 97.0% | 0.97 | 0.97 | 0.97 | 0.95 |
| InceptionV1 | 97.0% | 0.97 | 0.97 | 0.97 | 0.96 |
| **IDTNet** | **98.17%** | **0.98** | **0.98** | **0.98** | **0.97** |

### Class-wise Performance

| Class | Precision | Recall | F1-Score | Accuracy |
| :-- | :-- | :-- | :-- | :-- |
| Pituitary | 0.99 | 0.97 | 0.98 | 98.17% |
| No Tumor | 0.96 | 0.96 | 0.96 | 97.06% |
| Meningioma | 0.99 | 1.00 | 0.99 | 99.85% |
| Glioma | 0.98 | 0.99 | 0.98 | 98.32% |

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- TensorFlow/Keras 2.x
- NumPy
- OpenCV
- Matplotlib
- Scikit-learn

## 🔬 Model Configuration

| Component | Configuration |
| :-- | :-- |
| Optimizer | Adam |
| Learning Rate | 0.0001 |
| Loss Function | Categorical Cross-Entropy |
| Batch Size | 32 |
| Epochs | 15 |
| Callbacks | EarlyStopping, ReduceLROnPlateau |

## 📊 Training Progress

The model was trained for 10 epochs with the following final metrics:

- Training Accuracy: 98.22%
- Validation Accuracy: 92.36%
- Training Loss: 0.0546
- Validation Loss: 0.3329


## 🤝 Contributing

We welcome contributions to improve IDTNet! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Contribution Guidelines

- Follow PEP 8 style guidelines
- Add unit tests for new features
- Update documentation as needed
- Ensure all tests pass before submitting


## 📝 Citation

If you use this work in your research, please cite:

```bibtex
@article{kauchali2024idtnet,
  title={Classifying Brain Tumor in MRI Using IDTNet: Using pre-trained CNN models Architecture},
  author={Kauchali, Rayyan and Sayyed, Faizan},
  journal={Department of Computer Science MIT-WPU},
  year={2024},
  address={Pune, India}
}
```


## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Dataset sources: Figshare, SARTAJ dataset, and Br35H
- MIT-WPU Department of Computer Science for research support
- Contributors and researchers in the medical imaging community


## 📞 Contact

- **Rayyan Kauchali** - rayyan.kauchali@mitwpu.edu.in
- **Faizan Sayyed** - faizan.sayyed@mitwpu.edu.in


## 🔗 Related Work

This work builds upon and compares with several state-of-the-art approaches in brain tumor classification. For detailed comparisons and related research, please refer to the research paper included in this repository.

**Note**: This project is part of ongoing research in medical image analysis and deep learning applications in healthcare. The model should be used for research purposes and not as a substitute for professional medical diagnosis.
