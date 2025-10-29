<<<<<<< HEAD
# CÓDIGO INÍCIO: main.py

# Importa bibliotecas necessárias para manipular arquivos e datas
import os
import datetime
import json
import time 

# ----------------------------------------------------------------------
# VARIÁVEIS DE CONFIGURAÇÃO DO SISTEMA
# ----------------------------------------------------------------------
# Arquivo onde os cadastros serão salvos
ARQUIVO_DADOS = 'dados/cadastros.txt'
# Arquivo onde o registro das ações será salvo
ARQUIVO_LOG = 'log.txt'

# ----------------------------------------------------------------------
# DADOS INICIAIS (Informações obrigatórias do trabalho)
# ----------------------------------------------------------------------
# Esta lista será usada SOMENTE se o arquivo 'dados/cadastros.txt' não for encontrado.
DADOS_INICIAIS = [
    {"RA": 1, "Nome": "Carla Silveira", "Curso": "Ciência da Computação", "Media_Final": 7.0}, 
    {"RA": 2, "Nome": "Jorge luis Mello", "Curso": "Ciência da Computação", "Media_Final": 9.0}, 
    {"RA": 3, "Nome": "Alex Coimbra", "Curso": "Ciência da Computação", "Media_Final": 8.0}, 
    {"RA": 4, "Nome": "Sara Santos", "Curso": "Ciência da Computação", "Media_Final": 7.0}, 
]

# ----------------------------------------------------------------------
# FUNÇÕES DE APOIO (Log e Arquivo)
# ----------------------------------------------------------------------

# FUNÇÃO: registrar_log
def registrar_log(acao):
    """O sistema deve registrar logs de execução (data/hora e ação) em log.txt."""
    # Formato de data e hora: DD/MM/YYYY HH:MM:SS
    data_hora = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    mensagem = f"[{data_hora}] - Ação realizada: {acao}\n"
    
    try:
        # Usa tratamento de erros com try e except para Erros ao abrir/escrever arquivos.
        with open(ARQUIVO_LOG, 'a', encoding='utf-8') as f:
            f.write(mensagem)
    except IOError:
        print("\033[91m[ERRO FATAL]\033[0m Não foi possível escrever no arquivo de log.")

# FUNÇÃO: salvar_dados
def salvar_dados(alunos):
    """Ao cadastrar, editar ou excluir, o sistema deve atualizar o arquivo automaticamente."""
    try:
        with open(ARQUIVO_DADOS, 'w', encoding='utf-8') as f:
            for aluno in alunos:
                # Cada registro deve conter informações organizadas (dicionários).
                f.write(json.dumps(aluno) + '\n')
        
        registrar_log(f"Dados salvos com sucesso. Total: {len(alunos)}")
        return True
    except Exception as e:
        print(f"\n\033[91m[ERRO]\033[0m Não foi possível salvar os dados no arquivo: {e}")
        registrar_log(f"ERRO ao salvar dados: {e}")
        return False

# FUNÇÃO: carregar_dados
def carregar_dados():
    """Ao iniciar o programa, o sistema deve ler os dados do arquivo e carregá-los em memória."""
    dados_alunos = []
    
    try:
        if not os.path.exists('dados'):
            os.makedirs('dados')
            
        with open(ARQUIVO_DADOS, 'r', encoding='utf-8') as f:
            for linha in f:
                dados_alunos.append(json.loads(linha.strip())) 
        
        registrar_log(f"Dados carregados com sucesso. Total: {len(dados_alunos)}")
        
    except FileNotFoundError:
        # Tratamento de erros: Arquivo inexistente (deve ser criado automaticamente).
        print("\n\033[93m[INFO]\033[0m Arquivo de dados não encontrado. Usando dados iniciais...")
        
        dados_alunos = DADOS_INICIAIS 
        salvar_dados(dados_alunos) 
        
        registrar_log("Arquivo de dados inexistente. Criado com dados iniciais.")
        pass 
        
    except Exception as e:
        # Trata Erros ao abrir, ler ou escrever arquivos.
        print(f"\n\033[91m[ERRO]\033[0m Falha ao ler o arquivo de dados: {e}")
        registrar_log(f"ERRO ao ler dados: {e}")
        
    return dados_alunos

# Carrega a lista de alunos ao iniciar o programa
LISTA_ALUNOS = carregar_dados()

# ----------------------------------------------------------------------
# FUNÇÕES DE CRUD (EXIGIDAS NO TRABALHO)
# ----------------------------------------------------------------------

# FUNÇÃO: cadastrar_aluno (Corresponde a "cadastrar nome do aluno_item")
def cadastrar_aluno():
    """Permite ao usuário inserir um novo aluno (Nome, Curso e Média Final)."""
    registrar_log("Início do cadastro de aluno")
    
    while True:
        try:
            nome = input("   Nome completo: ").strip()
            if not nome:
                raise ValueError("O nome não pode ser vazio.")
            
            curso = input("   Curso: ").strip()
            if not curso:
                raise ValueError("O curso não pode ser vazio.")

            # Utiliza tratamento de erros com try e except para Entrada inválida do usuário.
            media_final = float(input("   Média Final (0.0 a 10.0): "))
            if not (0 <= media_final <= 10):
                raise ValueError("A média deve ser um número entre 0 e 10.")
            
            break 
        except ValueError as e:
            print(f"\n\033[91m[ERRO de Validação]\033[0m: {e}. Tente novamente.")
            registrar_log(f"Erro de validação no cadastro: {e}")
        except Exception as e:
            print(f"\n\033[91m[ERRO INESPERADO]\033[0m: {e}")
            registrar_log(f"Erro inesperado no cadastro: {e}")
            return 

    # Gera um RA sequencialmente
    proximo_ra = max([aluno['RA'] for aluno in LISTA_ALUNOS]) + 1 if LISTA_ALUNOS else 1
    
    novo_aluno = {
        "RA": proximo_ra, 
        "Nome": nome,
        "Curso": curso,
        "Media_Final": media_final
    }

    LISTA_ALUNOS.append(novo_aluno)
    salvar_dados(LISTA_ALUNOS)
    
    # O sistema deve apresentar mensagens claras para o usuário.
    print(f"\n\033[92m[SUCESSO]\033[0m Cadastro do aluno '{nome}' realizado com sucesso! RA: {novo_aluno['RA']}\n")
    registrar_log(f"Cadastro de aluno realizado: {nome} (RA: {novo_aluno['RA']})")

# FUNÇÃO: listar_alunos (Corresponde a "listar curso_itens")
def listar_alunos():
    """Exibe todos os alunos cadastrados com seus cursos e média."""
    registrar_log("Visualização da lista de alunos")
    
    if not LISTA_ALUNOS:
        print("\n\033[93m[INFO]\033[0m Nenhum aluno cadastrado.\n")
        return

    # O sistema deve personalizar a saída e listar o total de registros.
    print("\n\033[94m" + "="*70) 
    print(f"LISTA DE ALUNOS CADASTRADOS (Total de registros: {len(LISTA_ALUNOS)})") 
    print("="*70 + "\033[0m")
    
    # Utiliza laços de repetição (for) para percorrer dados.
    for aluno in LISTA_ALUNOS:
        print(f"RA: {aluno['RA']} | Nome: {aluno['Nome']:<25} | Curso: {aluno['Curso']:<20} | Média Final: {aluno['Media_Final']:.2f}")

    print("="*70 + "\n")

# FUNÇÃO: editar_aluno (Corresponde a "editar nota_item")
def editar_aluno():
    """Permite alterar a Média Final de um aluno, buscando pelo RA."""
    registrar_log("Início da edição de aluno")
    
    if not LISTA_ALUNOS:
        print("\n\033[93m[INFO]\033[0m A lista de alunos está vazia. Nada para editar.\n")
        return

    while True:
        try:
            ra_editar = int(input("Digite o RA do aluno que deseja editar a Média Final: "))
            break
        except ValueError:
            print("\033[91m[ERRO]\033[0m Por favor, digite um número inteiro para o RA.")
            registrar_log("Erro de entrada de RA na edição")

    aluno_encontrado = None
    indice = -1
    
    for i, aluno in enumerate(LISTA_ALUNOS):
        if aluno['RA'] == ra_editar:
            aluno_encontrado = aluno
            indice = i
            break
            
    if aluno_encontrado:
        print(f"\nAluno encontrado: {aluno_encontrado['Nome']} | Média atual: {aluno_encontrado['Media_Final']:.2f}")
        
        while True:
            try:
                # Utiliza tratamento de erros com try e except
                nova_media = float(input("Digite a NOVA Média Final (0 a 10): "))
                if not (0 <= nova_media <= 10):
                    raise ValueError("A média deve ser um número entre 0 e 10.")
                
                LISTA_ALUNOS[indice]['Media_Final'] = nova_media
                salvar_dados(LISTA_ALUNOS)
                
                print("\n\033[92m[SUCESSO]\033[0m Média final atualizada com sucesso!\n")
                registrar_log(f"Média do aluno RA {ra_editar} editada para {nova_media}")
                break
            except ValueError as e:
                print(f"\033[91m[ERRO]\033[0m {e}. Tente novamente.")
            except Exception:
                break 
                
    else:
        print(f"\n\033[93m[INFO]\033[0m Aluno com RA {ra_editar} não encontrado.\n")
        registrar_log(f"Tentativa de edição de RA não encontrado: {ra_editar}")

# FUNÇÃO: excluir_aluno (Corresponde a "excluir nota_item")
def excluir_aluno():
    """Remove um aluno do cadastro, buscando pelo RA."""
    registrar_log("Início da exclusão de aluno")
    
    if not LISTA_ALUNOS:
        print("\n\033[93m[INFO]\033[0m A lista de alunos está vazia. Nada para excluir.\n")
        return

    while True:
        try:
            ra_excluir = int(input("Digite o RA do aluno que deseja EXCLUIR: "))
            break
        except ValueError:
            print("\033[91m[ERRO]\033[0m Por favor, digite um número inteiro para o RA.")
            registrar_log("Erro de entrada de RA na exclusão")

    aluno_removido = None
    
    for i, aluno in enumerate(LISTA_ALUNOS):
        if aluno['RA'] == ra_excluir:
            aluno_removido = LISTA_ALUNOS.pop(i)
            break
            
    if aluno_removido:
        salvar_dados(LISTA_ALUNOS)
        print(f"\n\033[92m[SUCESSO]\033[0m Aluno '{aluno_removido['Nome']}' (RA {ra_excluir}) excluído com sucesso.\n")
        registrar_log(f"Aluno excluído: {aluno_removido['Nome']} (RA {ra_excluir})")
    else:
        print(f"\n\033[93m[INFO]\033[0m Aluno com RA {ra_excluir} não encontrado.\n")
        registrar_log(f"Tentativa de exclusão de RA não encontrado: {ra_excluir}")

# ----------------------------------------------------------------------
# FUNÇÃO PRINCIPAL (MENU)
# ----------------------------------------------------------------------

def menu_principal():
    """Exibe o menu e controla a execução do sistema."""
    
    registrar_log("Sistema iniciado")
    
    # Utiliza laços de repetição (while) para manter o menu ativo.
    while True:
        # O sistema deve apresentar um menu principal.
        print("\n" + "="*40)
        print("\033[96mSISTEMA DE CADASTRO DE ALUNOS\033[0m")
        print("="*40)
        
        # Funcionalidades do Sistema (Menu)
        print(" [1] Cadastrar Novo Aluno") 
        print(" [2] Listar Todos os Alunos") 
        print(" [3] Editar Média Final") 
        print(" [4] Excluir Aluno") 
        print(" [5] Sair do Sistema") 
        print("="*40)
        
        opcao = input("Escolha uma opção (1-5): ")
        
        # Utiliza estruturas de condição (if, elif, else) para tratar as opções do menu.
        if opcao == '1':
            cadastrar_aluno()
        elif opcao == '2':
            listar_alunos()
        elif opcao == '3':
            editar_aluno()
        elif opcao == '4':
            excluir_aluno()
        elif opcao == '5':
            registrar_log("Sistema encerrado pelo usuário")
            # O programa deve permanecer em execução até que o usuário escolha Explicitamente Sair.
            print("\n\033[95mObrigado por usar o sistema! Encerrando...\033[0m") 
            time.sleep(1) 
            break 
        else:
            print("\n\033[91m[ERRO]\033[0m Opção inválida. Digite um número de 1 a 5.\n")
            registrar_log("Opção de menu inválida")


# Condição que inicia a execução do programa
if __name__ == "__main__":
    menu_principal()
# CÓDIGO FIM: main.py
=======
429: Too Many Requests
For more on scraping GitHub and how it may affect your rights, please review our Terms of Service (https://docs.github.com/en/site-policy/github-terms/github-terms-of-service).
>>>>>>> 20413f92b18afc716c9c27f890afa1c3150593a7
