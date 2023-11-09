from flask import Flask, request, jsonify, render_template, redirect, url_for
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)

client = MongoClient('mongodb://localhost:27017/')  
db = client['veiculos']  
collection = db['veiculos'] 



@app.route('/')
def pagina_inicial():
    return render_template('pagina_inicial.html')

@app.route('/veiculos', methods=['POST'])
def inserir_veiculo():
    marca = request.form.get('marca')
    modelo = request.form.get('modelo')
    ano = int(request.form.get('ano'))
    categoria = request.form.get('categoria')
    preco = float(request.form.get('preco'))
    descricao = request.form.get('descricao')

    novo_veiculo = {
        'marca': marca,
        'modelo': modelo,
        'ano': ano,
        'categoria': categoria,
        'preco': preco,
        'descricao': descricao
    }

    collection.insert_one(novo_veiculo)
    return redirect(url_for('listar_veiculos'))

@app.route('/veiculos', methods=['GET'])
def lista_veiculos():
    veiculos = list(collection.find())
    return jsonify(veiculos)


@app.route('/excluir_veiculo/<string:veiculo_id>', methods=['POST'])
def excluir_veiculo(veiculo_id):
    collection.delete_one({'_id': ObjectId(veiculo_id)})
    return redirect(url_for('listar_veiculos'))

@app.route('/inserir_veiculo', methods=['GET'])
def exibir_formulario_insercao():
    return render_template('inserir_veiculo.html')

@app.route('/listar_veiculos', methods=['GET'])
def listar_veiculos():
    veiculos = list(collection.find())
    return render_template('listar_veiculos.html', veiculos=veiculos)

@app.route('/editar_veiculo/<string:veiculo_id>', methods=['GET'])
def editar_veiculo(veiculo_id):    
    veiculo = collection.find_one({'_id':ObjectId(veiculo_id)})
    return render_template('editar_veiculo.html', veiculo=veiculo)


@app.route('/atualizar_veiculo/<string:veiculo_id>', methods=['POST'])
def atualizar_veiculo(veiculo_id):
    marca = request.form.get('marca')
    modelo = request.form.get('modelo')
    ano = int(request.form.get('ano'))
    categoria = request.form.get('categoria')
    preco = float(request.form.get('preco'))
    descricao = request.form.get('descricao')

    collection.update_one({'_id': ObjectId(veiculo_id)}, {'$set': {
        'marca': marca,
        'modelo': modelo,
        'ano': ano,
        'categoria': categoria,
        'preco': preco,
        'descricao': descricao
    }})

    return redirect(url_for('listar_veiculos'))


@app.route('/inicializar', methods=['GET'])
def inicializar_veiculos():
    lista_veiculos = [
        {
            'marca': 'Ford',
            'modelo': 'F-150',
            'ano': 2022,
            'categoria': 'Caminhonete',
            'preco': 45000.00,
            'descricao': 'Bla bla',
        },
        {
            'marca': 'Toyota',
            'modelo': 'Camry',
            'ano': 2022,
            'categoria': 'Sedan',
            'preco': 35000.00,
            'descricao': 'rgeger',
        },
        {
            'marca': 'Chevrolet',
            'modelo': 'Cruze',
            'ano': 2023,
            'categoria': 'Sedan',
            'preco': 42000.00,
            'descricao': '46b5u',
        },
        {
            'marca': 'Honda',
            'modelo': 'Civic',
            'ano': 2022,
            'categoria': 'Sedan',
            'preco': 38000.00,
            'descricao': 'TEste',
        },
        {
            'marca': 'Volkswagen',
            'modelo': 'Golf',
            'ano': 2022,
            'categoria': 'Hatch',
            'preco': 35000.00,
            'descricao': 'outro',
        },
        {
            'marca': 'Jeep',
            'modelo': 'Renegade',
            'ano': 2022,
            'categoria': 'SUV',
            'preco': 48000.00,
            'descricao': 'fim',
        },
    ]

    collection.insert_many(lista_veiculos)

    return redirect(url_for('listar_veiculos'))


if __name__ == '__main__':
    app.run(debug=True)