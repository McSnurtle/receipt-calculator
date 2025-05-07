#src/utils/id_generator.py
# imports
import os
import json

def last_id() -> int:
    """Returns the last (greatest) receipt ID of the stored receipts in the `data/receipts/` directory."""

    receipts_dir = 'data/receipts/'
    if not os.path.exists(receipts_dir):
        raise FileNotFoundError(f"Directory {receipts_dir} does not exist!")

    receipt_ids = []
    for filename in os.listdir(receipts_dir):
        if filename.endswith('.json'):
            with open(os.path.join(receipts_dir, filename), 'r', encoding="utf-8") as file:
                receipt = json.load(file)
                receipt_ids.append(receipt['id'])

    return max(receipt_ids, default=0)
