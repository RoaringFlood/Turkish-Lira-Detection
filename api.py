from flask import  Flask, jsonify, request
from tahmin_et import tahmin
from firebase_baglanti import resim_indir

app = Flask(__name__)



@app.post('/predict')
def predict():
    data = request.json
    print(data)
    try:
        sample = data['UID']
    except KeyError:
        return jsonify({'error': 'No UID Sent'})
    print(sample)
    uniqe_id = sample
    ###################################
    #uniqe_id = "deneme"
    resim_indir(str(uniqe_id))
    predictions = tahmin()
    ###################################
    try:
        result = jsonify(predictions)
    except TypeError as e:
        return  jsonify({'error': str(e)})
    #x = {'yavuz': predictions}
    x = {'UID': predictions}
    return jsonify(x)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
