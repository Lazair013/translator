from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline

class Model():
    def __init__(self, model_path):
        tokenizer = AutoTokenizer.from_pretrained('bert-base-uncased')
        model = AutoModelForSequenceClassification.from_pretrained(model_path)

        self.label_names = ['sadness', 'joy', 'love', 'anger', 'fear', 'surprise']

        self.pipe = pipeline(
            "text-classification",
            model=model,
            tokenizer=tokenizer,
            return_all_scores=True,
        )

    def predict(self, text, n_labels=1):
        preds = self.pipe(text)[0]
        preds = sorted(preds, key= lambda x: x['score'], reverse=True)

        for pred in preds:
            label_id = int(pred["label"].replace("LABEL_", ""))
            label_name = self.label_names[label_id]
            pred['label_name'] = label_name

        n_preds = preds[:n_labels]

        return [{'label': pred['label_name'], 'score': f'{pred["score"]:.3f}'} for pred in n_preds]