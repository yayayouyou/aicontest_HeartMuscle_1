# aicontest_HeartMuscle_1
心肌ai cup 比賽  (心臟肌肉影像分割)

# project structrue

    project_root/
    ├── training_image/             # 原始訓練影像
    │   ├── patient0001.nii.gz
    │   ├── patient0002.nii.gz
    │   └── ... 
    ├── training_label/             # 原始訓練標註
    │   ├── patient0001.nii.gz
    │   ├── patient0002.nii.gz
    │   └── ...
    ├── testing_image/              # 原始測試影像
    │   ├── patient0051.nii.gz
    │   ├── patient0052.nii.gz
    │   └── ...
    ├── run_nnunet.py               # 一鍵版腳本
    ├── nnUNet_raw/                 # nnU-Net v2 原始資料夾
    │   └── Dataset001_CT/
    │       ├── imagesTr/           # 訓練影像 (nnU-Net 規範)
    │       │   ├── patient0001_0000.nii.gz
    │       │   ├── patient0002_0000.nii.gz
    │       │   └── ...
    │       ├── labelsTr/           # 訓練標註 (nnU-Net 規範)
    │       │   ├── patient0001.nii.gz
    │       │   ├── patient0002.nii.gz
    │       │   └── ...
    │       ├── imagesTs/           # 測試影像 (nnU-Net 規範)
    │       │   ├── patient0051_0000.nii.gz
    │       │   ├── patient0052_0000.nii.gz
    │       │   └── ...
    │       └── dataset.json        # 資料描述檔
    ├── predictions/                # 推論結果
    │   ├── patient0051.nii.gz
    │   ├── patient0052.nii.gz
    │   └── ... 
