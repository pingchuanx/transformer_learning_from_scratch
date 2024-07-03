from transformers import BertForSequenceClassification, BertTokenizer
import torch

# 加载模型和Tokenizer
model = BertForSequenceClassification.from_pretrained("bert-base-uncased")
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")

# 准备文本
text = "I love this phone, its camera is amazing!"
inputs = tokenizer(text, return_tensors="pt")

# 预测情感
with torch.no_grad():
    outputs = model(**inputs)
    prediction = torch.argmax(outputs.logits).item()

    # 输出结果
    print("Positive" if prediction == 1 else "Negative")
