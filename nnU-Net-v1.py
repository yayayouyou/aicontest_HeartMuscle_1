import os
import shutil
import json
import subprocess

# =============================
# 使用者參數
# =============================
dataset_id = 1   # nnU-Net 的 dataset number
dataset_name = f"Dataset{dataset_id:03d}_CT"
nnunet_raw = "nnUNet_raw"   # nnU-Net raw 資料夾
gpu_id = "0"                # 訓練要用的 GPU 編號
output_dir = "./predictions" # 推論輸出資料夾

# 原始資料夾
train_img_dir = "training_image"
train_lbl_dir = "training_label"
test_img_dir = "testing_image"

# =============================
# 建立資料夾
# =============================
dataset_dir = os.path.join(nnunet_raw, dataset_name)
imagesTr = os.path.join(dataset_dir, "imagesTr")
labelsTr = os.path.join(dataset_dir, "labelsTr")
imagesTs = os.path.join(dataset_dir, "imagesTs")

os.makedirs(imagesTr, exist_ok=True)
os.makedirs(labelsTr, exist_ok=True)
os.makedirs(imagesTs, exist_ok=True)

# =============================
# 複製訓練影像 & 標註
# =============================
train_cases = sorted([f for f in os.listdir(train_img_dir) if f.endswith(".nii.gz")])
for case in train_cases:
    case_id = case.replace(".nii.gz", "")
    shutil.copy(os.path.join(train_img_dir, case), os.path.join(imagesTr, f"{case_id}_0000.nii.gz"))
    shutil.copy(os.path.join(train_lbl_dir, case), os.path.join(labelsTr, f"{case_id}.nii.gz"))

# =============================
# 複製測試影像
# =============================
test_cases = sorted([f for f in os.listdir(test_img_dir) if f.endswith(".nii.gz")])
for case in test_cases:
    case_id = case.replace(".nii.gz", "")
    shutil.copy(os.path.join(test_img_dir, case), os.path.join(imagesTs, f"{case_id}_0000.nii.gz"))

# =============================
# 建立 dataset.json
# =============================
dataset_json = {
    "name": "CT_Segmentation",
    "description": "CT organ segmentation",
    "tensorImageSize": "3D",
    "modality": {"0": "CT"},
    "labels": {
        "0": "background",
        "1": "organ"
    },
    "numTraining": len(train_cases),
    "numTest": len(test_cases),
    "training": [
        {
            "image": f"./imagesTr/{case.replace('.nii.gz', '')}_0000.nii.gz",
            "label": f"./labelsTr/{case.replace('.nii.gz','')}.nii.gz"
        } for case in train_cases
    ],
    "test": [
        f"./imagesTs/{case.replace('.nii.gz','')}_0000.nii.gz" for case in test_cases
    ]
}

with open(os.path.join(dataset_dir, "dataset.json"), "w") as f:
    json.dump(dataset_json, f, indent=4)

print("✅ 已完成 nnU-Net v2 資料準備！")
print(f"資料集存放於: {dataset_dir}")

# =============================
# 執行 nnU-Net pipeline
# =============================

print("\n🚀 開始資料前處理...")
subprocess.run(["nnUNetv2_plan_and_preprocess", "-d", str(dataset_id), "--verify_dataset_integrity"])

print("\n🚀 開始訓練 (3d_fullres, fold=0)...")
subprocess.run(["nnUNetv2_train", str(dataset_id), "3d_fullres", "0", "-g", gpu_id])

print("\n🚀 開始推論...")
os.makedirs(output_dir, exist_ok=True)
subprocess.run([
    "nnUNetv2_predict",
    "-d", str(dataset_id),
    "-i", imagesTs,
    "-o", output_dir,
    "-f", "all",
    "-g", gpu_id
])

print("\n🎉 全流程完成！推論結果已存放於:", output_dir)
