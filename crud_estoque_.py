import json
import pandas as pd
import os

# Arquivo onde os dados serão salvos
FILENAME = 'produtos.json'

# Categorias predefinidas
CATEGORIES = [
    'Maturado - artesanal',
    'Fresco - artesanal',
]

# Função para carregar os dados do arquivo de produtos
def load_data():
    if not os.path.exists(FILENAME):
        with open(FILENAME, 'w', encoding='utf-8') as file:
            json.dump([], file)
        return []
    try:
        with open(FILENAME, 'r', encoding='utf-8') as file:
            return json.load(file)
    except json.JSONDecodeError:
        print("Arquivo de dados está corrompido. Reinicializando o arquivo.")
        with open(FILENAME, 'w', encoding='utf-8') as file:
            json.dump([], file)
        return []

# Função para salvar os dados no arquivo
def save_data(data):
    with open(FILENAME, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

# Função para obter o próximo IDa
def get_next_id(data):
    if not data:
        return 1
    return max(produto['id'] for produto in data) + 1

# Função para criar um novo produto
def create_product(nome, preco, quantidade):
    if preco <= 0 or quantidade < 0:
        print("Preço e quantidade devem ser números positivos.")
        return
    
    data = load_data()
    new_id = get_next_id(data)
    produto = {
        'id': new_id,
        'nome': nome,
        'preco': preco,
        'quantidade': quantidade,
        'vendido': 0,
        'estoque': quantidade,
        'categoria': choose_category()
    }
    data.append(produto)
    save_data(data)
    print(f"Produto adicionado com sucesso! ID: {new_id}")

# Função para escolher uma categoria
def choose_category():
    print("Categorias disponíveis:")
    for i, categoria in enumerate(CATEGORIES, 1):
        print(f"{i}. {categoria}")
    while True:
        try:
            categoria_idx = int(input("Escolha uma categoria (número): ")) - 1
            if 0 <= categoria_idx < len(CATEGORIES):
                return CATEGORIES[categoria_idx]
            else:
                print("Categoria inválida. Tente novamente.")
        except ValueError:
            print("Entrada inválida. Tente novamente.")

# Função para atualizar um produto
def update_product(produto_id, updated_nome, updated_preco, updated_quantidade):
    if updated_preco <= 0 or updated_quantidade < 0:
        print("Preço e quantidade devem ser números positivos.")
        return
    
    data = load_data()
    for produto in data:
        if produto['id'] == produto_id:
            vendido = produto['vendido']
            estoque = updated_quantidade - vendido
            produto.update({
                'nome': updated_nome,
                'preco': updated_preco,
                'quantidade': updated_quantidade,
                'estoque': estoque,
                'categoria': choose_category()  # Atualizar categoria
            })
            save_data(data)
            print(f"Produto com ID {produto_id} atualizado com sucesso!")
            return
    print(f"Produto com ID {produto_id} não encontrado.")

# Função para deletar um produto
def delete_product(produto_id):
    data = load_data()
    new_data = [produto for produto in data if produto['id'] != produto_id]
    
    if len(new_data) == len(data):
        print(f"Produto com ID {produto_id} não encontrado.")
        return
    
    save_data(new_data)
    print(f"Produto com ID {produto_id} deletado com sucesso!")

# Função para registrar uma venda
def register_sale(produto_id, quantidade_vendida):
    data = load_data()
    for produto in data:
        if produto['id'] == produto_id:
            if quantidade_vendida <= 0 or quantidade_vendida > produto['estoque']:
                print("Quantidade vendida inválida.")
                return
            produto['vendido'] += quantidade_vendida
            produto['estoque'] -= quantidade_vendida
            save_data(data)
            print(f"Venda registrada com sucesso! Produto ID: {produto_id}, Quantidade vendida: {quantidade_vendida}")
            return
    print(f"Produto com ID {produto_id} não encontrado.")

# Função para gerar um relatório
def generate_report():
    data = load_data()
    if not data:
        print("Nenhum dado disponível para gerar o relatório.")
        return
    
    df = pd.DataFrame(data)
    df.to_csv('relatorio_produtos.csv', index=False)
    print("Relatório gerado com sucesso: relatorio_produtos.csv")

# Função para visualizar os dados salvos no terminal
def view_data():
    data = load_data()
    if not data:
        print("Nenhum produto cadastrado.")
    else:
        for produto in data:
            print(produto)

# Função principal para interagir com o CRUD
def main():
    while True:
        print("\nEscolha uma opção:")
        print("1. Adicionar produto")
        print("2. Listar produtos")
        print("3. Atualizar produto")
        print("4. Deletar produto")
        print("5. Registrar venda")
        print("6. Gerar relatório")
        print("7. Sair")
        
        opcao = input("Opção: ")
        
        if opcao == '1':
            nome = input("Nome: ")
            try:
                preco = float(input("Preço: "))
                quantidade = int(input("Quantidade: "))
            except ValueError:
                print("Preço e quantidade devem ser números válidos.")
                continue
            
            create_product(nome, preco, quantidade)
        elif opcao == '2':
            view_data()
        elif opcao == '3':
            try:
                produto_id = int(input("ID do produto a ser atualizado: "))
                nome = input("Nome: ")
                preco = float(input("Preço: "))
                quantidade = int(input("Quantidade: "))
            except ValueError:
                print("ID, preço e quantidade devem ser números válidos.")
                continue
            
            update_product(produto_id, nome, preco, quantidade)
        elif opcao == '4':
            try:
                produto_id = int(input("ID do produto a ser deletado: "))
            except ValueError:
                print("ID deve ser um número válido.")
                continue
            
            delete_product(produto_id)
        elif opcao == '5':
            try:
                produto_id = int(input("ID do produto vendido: "))
                quantidade_vendida = int(input("Quantidade vendida: "))
            except ValueError:
                print("ID e quantidade devem ser números válidos.")
                continue
            
            register_sale(produto_id, quantidade_vendida)
        elif opcao == '6':
            generate_report()
        elif opcao == '7':
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()

