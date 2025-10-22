import csv

arquivo = 'dados_alunos.csv'

def carregar_dados():
    try:
        with open(arquivo, 'r', newline='', encoding='utf-8') as f:
            leitor = csv.DictReader(f)
            return list(leitor)
    except FileNotFoundError:
        return []

def salvar_dados(dados):
    with open(arquivo, 'w', newline='', encoding='utf-8') as f:
        campos = ['nome', 'curso', 'media']
        escritor = csv.DictWriter(f, fieldnames=campos)
        escritor.writeheader()
        escritor.writerows(dados)

def cadastrar_aluno(dados):
    nome = input('Nome do aluno: ')
    curso = input('Curso: ')
    media = input('Média final: ')
    dados.append({'nome': nome, 'curso': curso, 'media': media})
    salvar_dados(dados)
    print('Aluno cadastrado com sucesso!')

def listar_alunos(dados):
    if not dados:
        print('Nenhum aluno cadastrado.')
        return
    for i, aluno in enumerate(dados, start=1):
        print(f"{i}. Nome: {aluno['nome']} | Curso: {aluno['curso']} | Média: {aluno['media']}")
    print()

def editar_aluno(dados):
    listar_alunos(dados)
    indice = int(input('Número do aluno a editar: ')) - 1
    if 0 <= indice < len(dados):
        aluno = dados[indice]
        aluno['curso'] = input('Novo curso: ')
        aluno['media'] = input('Nova média: ')
        salvar_dados(dados)
        print('Aluno atualizado com sucesso!')
    else:
        print('Aluno não encontrado.')

def excluir_aluno(dados):
    listar_alunos(dados)
    indice = int(input('Número do aluno a excluir: ')) - 1
    if 0 <= indice < len(dados):
        removido = dados.pop(indice)
        salvar_dados(dados)
        print(f"Aluno {removido['nome']} excluído!")
    else:
        print('Aluno não encontrado.')

def menu():
    dados = carregar_dados()
    while True:
        print('''\n===== SISTEMA DE CADASTRO DE ALUNOS =====
1. Cadastrar aluno
2. Listar alunos
3. Editar aluno
4. Excluir aluno
5. Sair
===========================================''')
        opcao = input('Escolha uma opção: ')
        if opcao == '1':
            cadastrar_aluno(dados)
        elif opcao == '2':
            listar_alunos(dados)
        elif opcao == '3':
            editar_aluno(dados)
        elif opcao == '4':
            excluir_aluno(dados)
        elif opcao == '5':
            print('Encerrando o sistema...')
            break
        else:
            print('Opção inválida!')

if __name__ == '__main__':
    menu()

