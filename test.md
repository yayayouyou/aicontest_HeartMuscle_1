明白了，你希望 **image name 固定為 `ai-cup-2025`**，不需要每次透過參數傳入。那我們可以直接把 Makefile 裡的 `IMAGE_NAME` 改成固定值。

以下是修改後的版本（包含自動 container 名稱 + 背景跑 + volume 映射）：

---

### Makefile（image 固定 + container 自動命名）

```makefile
# =========================
# 變數設定
# =========================
IMAGE_NAME = ai-cup-2025        # 固定 image 名稱
GPU_OPTION = --gpus all
WORKSPACE = /workspace
PROJECT_DIR := $(notdir $(PWD))   # 取得本機資料夾名稱

.PHONY: train train-logs clean

# =========================
# train target
# 用法: make train RUN=run1
train:
ifndef RUN
	$(error RUN variable is not set. Example: make train RUN=run1)
endif

# 建立對應 RUN 子資料夾存輸出
	mkdir -p $(PWD)/$(RUN)

# container 名稱自動為 <專案資料夾>_<RUN>
	CONTAINER_NAME=$(PROJECT_DIR)_$(RUN); \
	docker run -d $(GPU_OPTION) \
		-v $(PWD):$(WORKSPACE) \
		-w $(WORKSPACE) \
		--name $$CONTAINER_NAME \
		$(IMAGE_NAME) \
		bash -c "python train.py --output_dir $(WORKSPACE)/$(RUN)"

# =========================
# train log 追蹤
train-logs:
ifndef RUN
	$(error RUN variable is not set. Example: make train-logs RUN=run1)
endif
	CONTAINER_NAME=$(PROJECT_DIR)_$(RUN); \
	docker logs -f $$CONTAINER_NAME

# =========================
# clean target
clean:
ifndef RUN
	$(error RUN variable is not set. Example: make clean RUN=run1)
endif
	CONTAINER_NAME=$(PROJECT_DIR)_$(RUN); \
	docker rm -f $$CONTAINER_NAME || true
```

---

### 🔹 使用方式

1. 執行訓練：

```bash
make train RUN=run1
```

- container 名稱：`ai_cup_run1`
- image 固定使用：`ai-cup-2025`
- 輸出結果存到：`ai_cup/run1/`
- 背景執行，不會因關掉 terminal 而中斷

2. 追蹤 log：

```bash
make train-logs RUN=run1
```

3. 停止 container：

```bash
make clean RUN=run1
```

---

這樣就符合你之前的需求：

- image 固定
- 不複製 dataset，直接映射
- container 名稱自動對應 RUN
- 背景執行、可追蹤 log

---

如果你希望，我可以再幫你加 **RUN 沒填就自動生成唯一名稱（時間戳）** 的功能，完全不用手動指定 RUN。

你希望我加嗎？
