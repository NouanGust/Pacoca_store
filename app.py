import json
import os
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


def carregar_dados():
    caminho_arquivo = os.path.join(os.path.dirname(__file__), 'produtos.json')
    try:
        with open(caminho_arquivo, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/produtos', methods=['GET'])
def listar_produtos():
    produtos = carregar_dados()
    categoria_query = request.args.get('categoria')
    
    if categoria_query:
        produtos_filtrados = [p for p in produtos if p['categoria'].lower() == categoria_query.lower()]
        return jsonify(produtos_filtrados), 200
        
    return jsonify(produtos), 200

@app.route('/api/produtos/<int:produto_id>', methods=['GET'])
def buscar_produto(produto_id):
    produtos = carregar_dados()
    produto = next((p for p in produtos if p["id"] == produto_id), None)
    
    if produto:
        return jsonify(produto), 200
        
    return jsonify({"erro": "Produto não encontrado"}), 404

if __name__ == '__main__':
    app.run(debug=True)