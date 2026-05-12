from datasets import load_dataset

dataset = load_dataset("google/code_x_glue_cc_defect_detection")

print(dataset)
print(dataset["train"][0])

train_data = dataset["train"]

for item in train_data:
    if item["target"] == True:
        print("=== 취약 코드 발견 ===")
        print("Project:", item["project"])
        print("Commit ID:", item["commit_id"])
        print(item["func"])
        break