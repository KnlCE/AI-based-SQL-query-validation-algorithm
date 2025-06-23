from transformers import DistilBertTokenizerFast, DistilBertForSequenceClassification
import torch
from generate_explanation import explain_sql_error

model = DistilBertForSequenceClassification.from_pretrained('./sql_model')
tokenizer = DistilBertTokenizerFast.from_pretrained('./sql_model')

def check_sql(query: str):
    inputs = tokenizer(query, return_tensors="pt", truncation=True, padding=True)
    outputs = model(**inputs)
    probs = torch.nn.functional.softmax(outputs.logits, dim=1)
    prediction = torch.argmax(probs, dim=1).item()
    return "VALID" if prediction == 1 else "INVALID", probs

# # Пример
# query = "SELECT date, price FROM sales"
# result, probs = check_sql(query)
# print("Результат:", result)
# print("Вероятности:", probs)
query = "UPDAT employees SET salary = salary * 1.1 WHERE department = 'HR';"

status, _ = check_sql(query)

if status == "VALID":
    print("✅ Запрос корректен")
else:
    explanation = explain_sql_error(query)
    print("❌ Ошибка в запросе:")
    print(explanation)