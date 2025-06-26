from transformers import T5Tokenizer, T5ForConditionalGeneration

model = T5ForConditionalGeneration.from_pretrained("ai/flan_sql_explainer")
tokenizer = T5Tokenizer.from_pretrained("ai/flan_sql_explainer")


def explain_sql_error(sql_query: str) -> str:
    input_text = (
            "Проанализируй SQL-запрос и выведи результат в формате:\n"
            "Синтаксические ошибки: Syntax error\n"
            "Логические ошибки: Logic error\n"
            "Рекомендации по оптимизации: optimization_error\n."
            "If incorrect query: Ошибка, запрос не корректен"
            "Запрос: " + sql_query
    )
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
# query = "SELEC * FROM employees;"
# print("Запрос:", query)
# print("Объяснение:", explain_sql_error(query))
