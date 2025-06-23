from transformers import T5Tokenizer, T5ForConditionalGeneration

# Загрузка обученной модели
model = T5ForConditionalGeneration.from_pretrained("flan_sql_explainer")
tokenizer = T5Tokenizer.from_pretrained("flan_sql_explainer")


def explain_sql_error(sql_query: str) -> str:
    input_text = "explain error: " + sql_query
    inputs = tokenizer(input_text, return_tensors="pt", truncation=True)

    outputs = model.generate(
        inputs["input_ids"],
        max_length=64,
        num_beams=4,
        early_stopping=True
    )
    explanation = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return explanation


# Пример
query = "SELECT * FROM employees WHERE department = 'Sales';"
print("Запрос:", query)
print("Объяснение:", explain_sql_error(query))
