import base64
import json

import keras
import numpy as np
from flask import Flask, request, jsonify

ACCESS_KEY = "tua_chiave_secreta"

app = Flask(__name__)

# Percorso JSON delle classi
classes_path = r'model/classes.json'


def load_model_and_classes(model_path_l, classes_path_l):
    # Carica il modello precedentemente addestrato
    model_l = keras.models.load_model(model_path_l)

    # Carica le classi dal file JSON
    with open(classes_path_l, 'r') as f:
        class_dict = json.load(f)

    # Crea un elenco di classi
    classes_l = [class_name for class_name, class_id in class_dict.items()]

    return model_l, classes_l, class_dict


def recognize_coin(image_path_r, model_r, classes_r):
    # Carica l'immagine
    # img = image.load_img(image_path_r, target_size=(224, 224))
    # img = image.img_to_array(img)
    img = np.expand_dims(image_path_r, axis=0)

    # Effettua la previsione sull'immagine
    predictions = model_r.predict(img)

    # Trova l'etichetta prevista
    predicted_class_index = np.argmax(predictions)
    predicted_class = classes_r[predicted_class_index]

    return predicted_class


def get_value_for_number(class_dict, number):
    # Verifica se il numero è presente nel dizionario
    if str(number) in class_dict:
        return class_dict[str(number)]
    else:
        return "Numero non trovato"


@app.route('/recognize_coin', methods=['POST'])
def recognize_coin_api():
    # Verifica l'accesso autorizzato
    api_key = request.headers.get('api_key')
    if api_key != ACCESS_KEY:
        return jsonify({'error': 'Unauthorized'}), 401

        # Estrai la stringa e l'immagine dal payload JSON
    json_data = request.get_json()
    operation = json_data.get('operation')

    image_data = json_data.get('image', '')

    if image_data:
        image_data = image_data.split(",")[1]
        image_bytes = base64.b64decode(image_data)
        nparr = np.frombuffer(image_bytes, dtype=np.uint8)

        if operation == 'observe':
            model_path = r'model/observe_coins_82.59%.h5'
        else:
            model_path = r'model/reverse_coins_100.00%.h5'

        # Carica il modello e le classi
        model, classes, c_dict = load_model_and_classes(model_path, classes_path)

        # Effettua il riconoscimento
        recognized_class = recognize_coin(nparr, model, classes)

        coin_hash = get_value_for_number(c_dict, recognized_class)

        # Leggi il file JSON
        with open(r'model/coin_reference.json', 'r', encoding="utf-8") as file:
            data = json.load(file)

        if coin_hash in data:
            valore_associato = data[coin_hash]
            result = {'coin_hash': coin_hash, 'value_associated': valore_associato, 'operation': operation}
        else:
            result = {'coin_hash': coin_hash, 'value_associated': 'Value not found', 'operation': operation}

        return jsonify(result)
    else:
        return jsonify({'error': 'Image not provided'}), 400


if __name__ == '__main__':
    app.run(debug=True)
