import pandas as pd
from transformers import T5Tokenizer, T5ForConditionalGeneration, Trainer, TrainingArguments
from torch.utils.data import Dataset
import torch

# Загрузка данных
df = pd.read_csv("sql_explanation_dataset.csv")

# Препроцессинг: входной текст = SQL-запрос, целевой = объяснение
class SQLExplainDataset(Dataset):
    def __init__(self, dataframe, tokenizer, max_len=128):
        self.tokenizer = tokenizer
        self.inputs = dataframe['query'].tolist()
        self.targets = dataframe['error_explanation'].tolist()
        self.max_len = max_len

    def __len__(self):
        return len(self.inputs)

    def __getitem__(self, idx):
        input_ = "explain error: " + self.inputs[idx]
        target = self.targets[idx]

        input_enc = self.tokenizer(
            input_, padding='max_length', truncation=True,
            max_length=self.max_len, return_tensors="pt"
        )
        target_enc = self.tokenizer(
            target, padding='max_length', truncation=True,
            max_length=self.max_len, return_tensors="pt"
        )

        return {
            'input_ids': input_enc['input_ids'].squeeze(),
            'attention_mask': input_enc['attention_mask'].squeeze(),
            'labels': target_enc['input_ids'].squeeze()
        }

# Модель и токенизатор
model_name = "google/flan-t5-small"
tokenizer = T5Tokenizer.from_pretrained(model_name)
model = T5ForConditionalGeneration.from_pretrained(model_name)

# Датасет
dataset = SQLExplainDataset(df, tokenizer)

# Параметры обучения
args = TrainingArguments(
    output_dir="flan_sql_explainer",
    per_device_train_batch_size=8,
    num_train_epochs=6,
    save_steps=100,
    save_total_limit=2,
    logging_dir='./logs',
    logging_steps=10
)

trainer = Trainer(
    model=model,
    args=args,
    train_dataset=dataset
)

# Обучение
trainer.train()

# Сохранение
model.save_pretrained("flan_sql_explainer")
tokenizer.save_pretrained("flan_sql_explainer")
