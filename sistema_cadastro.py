import os
import datetime
import json
import time # Para personalizar a saída

# ----------------------------------------------------------------------
# VARIÁVEIS DE CONFIGURAÇÃO
# ----------------------------------------------------------------------
ARQUIVO_DADOS = 'dados/cadastros.txt'
ARQUIVO_LOG = 'log.txt'

# ----------------------------------------------------------------------
# FUNÇÕES DE APOIO (Log e Arquivo)
# ----------------------------------------------------------------------

def registrar_log(acao):
    """Registra a ação do usuário com data e hora no log.txt."""
    data_hora = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    mensagem = f"[{data_hora}] - Ação: {acao}\n"
    
    try:
        # Abre o arquivo em modo 'a' (append) para adicionar ao final
        with open(ARQUIVO_LOG, 'a', encoding='utf-8') as f:
            f.write(mensagem)
    except IOError:
        print("[ERRO FATAL] Não foi possível escrever no arquivo de log.")

def carregar_dados():
    """Lê os dados do arquivo e retorna a lista de alunos."""
    dados_alunos = []
    
    try:
        # Garante que a pasta 'dados' exista
        if not os.path.exists('dados'):
            os.makedirs('dados')
            
        with open(ARQUIVO_DADOS, 'r', encoding='utf-8') as f:
            for linha in f:
                # Transforma a linha (string) em um dicionário Python
                dados_alunos.append(json.loads(linha.strip())) 
        
        registrar_log(f"Dados carregados com sucesso. Total: {len(dados_alunos)}")
        
    except FileNotFoundError:
        # Caso o arquivo não exista (primeira execução)
        registrar_log("Arquivo de dados inexistente. Lista inicializada vazia.")
        pass 
        
    except Exception as e:
        print(f"\n[ERRO] Falha ao ler o arquivo de dados: {e}")
        registrar_log(f"ERRO ao ler dados: {e}")
        
    return dados_alunos

def salvar_dados(alunos):
    """Salva a lista atualizada de alunos no arquivo."""
    try:
        # Abre o arquivo em modo 'w' (write) para sobrescrever com dados novos
        with open(ARQUIVO_DADOS, 'w', encoding='utf-8') as f:
            for aluno in alunos:
                # Transforma o dicionário em string (JSON) para salvar
                f.write(json.dumps(aluno) + '\n')
        
        registrar_log(f"Dados salvos com sucesso. Total: {len(alunos)}")
        return True
    except Exception as e:
        print(f"\n[ERRO] Não foi possível salvar os dados no arquivo: {e}")
        registrar_log(f"ERRO ao salvar dados: {e}")
        return False

# Inicializa a lista principal de alunos com os dados do arquivo
LISTA_ALUNOS = carregar_dados()

# ----------------------------------------------------------------------
# FUNÇÕES DE CRUD (Cadastro, Listar, Editar, Excluir)
# ----------------------------------------------------------------------

def cadastrar_aluno():
    """Funcionalidade 1: Cadastra um novo aluno."""
    registrar_log("Início do cadastro de aluno")
    
    while True:
        try:
            # Entrada e Validação do Nome e Curso
            nome = input("   Nome completo: ").strip()
            if not nome:
                raise ValueError("O nome não pode ser vazio.")
            
            curso = input("   Curso: ").strip()
            if not curso:
                raise ValueError("O curso não pode ser vazio.")

            # Entrada e Tratamento de Erro para Média Final (TRY/EXCEPT)
            media_final = float(input("   Média Final (0.0 a 10.0): "))
            if not (0 <= media_final <= 10):
                raise ValueError("A média deve ser um número entre 0 e 10.")
            
            break 
        except ValueError as e:
            # Captura erros de digitação (letras em vez de número, fora do intervalo)
            print(f"\n\033[91m[ERRO de Validação]\033[0m: {e}. Tente novamente.") # Cor Vermelha
            registrar_log(f"Erro de validação no cadastro: {e}")
        except Exception as e:
            print(f"\n\033[91m[ERRO INESPERADO]\033[0m: {e}")
            registrar_log(f"Erro inesperado no cadastro: {e}")
            return 

    # Cria o novo registro (Dicionário)
    novo_aluno = {
        # Gera um RA simples e sequencial
        "RA": len(LISTA_ALUNOS) + 1 if LISTA_ALUNOS else 1, 
        "Nome": nome,
        "Curso": curso,
        "Media_Final": media_final
    }

    # Adiciona à lista em memória e salva no arquivo
    LISTA_ALUNOS.append(novo_aluno)
    salvar_dados(LISTA_ALUNOS)
    
    print(f"\n\033[92m[SUCESSO]\033[0m Cadastro do aluno '{nome}' realizado! RA: {novo_aluno['RA']}\n") # Cor Verde
    registrar_log(f"Cadastro de aluno realizado: {nome} (RA: {novo_aluno['RA']})")

def listar_alunos():
    """Funcionalidade 2: Lista todos os alunos cadastrados."""
    registrar_log("Visualização da lista de alunos")
    
    if not LISTA_ALUNOS:
        print("\n\033[93m[INFO]\033[0m Nenhum aluno cadastrado.\n") # Cor Amarela
        return

    # Título Personalizado com Cor
    print("\n\033[94m" + "="*70) # Cor Azul
    print(f"LISTA DE ALUNOS CADASTRADOS (Total de registros: {len(LISTA_ALUNOS)})") 
    print("="*70 + "\033[0m")
    
    # Loop 'for' para percorrer cada aluno na lista
    for aluno in LISTA_ALUNOS:
        print(f"RA: {aluno['RA']} | Nome: {aluno['Nome']:<25} | Curso: {aluno['Curso']:<20} | Média Final: {aluno['Media_Final']:.2f}")

    print("="*70 + "\n")

def editar_aluno():
    """Funcionalidade 3: Edita a média final de um aluno."""
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
    
    # Percorre a lista ('for') para encontrar o aluno pelo RA
    for i, aluno in enumerate(LISTA_ALUNOS):
        if aluno['RA'] == ra_editar:
            aluno_encontrado = aluno
            indice = i
            break
            
    if aluno_encontrado:
        print(f"\nAluno encontrado: {aluno_encontrado['Nome']} | Média atual: {aluno_encontrado['Media_Final']:.2f}")
        
        while True:
            try:
                nova_media = float(input("Digite a NOVA Média Final (0 a 10): "))
                if not (0 <= nova_media <= 10):
                    raise ValueError("A média deve ser um número entre 0 e 10.")
                
                # Atualiza a média na lista em memória
                LISTA_ALUNOS[indice]['Media_Final'] = nova_media
                
                # Salva a lista atualizada no arquivo
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

def excluir_aluno():
    """Funcionalidade 4: Remove um aluno pelo RA."""
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
    
    # Percorre a lista ('for') para encontrar o aluno
    for i, aluno in enumerate(LISTA_ALUNOS):
        if aluno['RA'] == ra_excluir:
            # Remove o aluno da lista (pop)
            aluno_removido = LISTA_ALUNOS.pop(i)
            break
            
    if aluno_removido:
        # Salva a lista atualizada no arquivo
        salvar_dados(LISTA_ALUNOS)
        print(f"\n\033[92m[SUCESSO]\033[0m Aluno '{aluno_removido['Nome']}' (RA {ra_excluir}) excluído com sucesso.\n")
        registrar_log(f"Aluno excluído: {aluno_removido['Nome']} (RA {ra_excluir})")
    else:
        print(f"\n\033[93m[INFO]\033[0m Aluno com RA {ra_excluir} não encontrado.\n")
        registrar_log(f"Tentativa de exclusão de RA não encontrado: {ra_excluir}")

# ----------------------------------------------------------------------
# FUNÇÃO PRINCIPAL (Menu)
# ----------------------------------------------------------------------

def menu_principal():
    """Exibe o menu e controla a execução do sistema com um loop while."""
    
    registrar_log("Sistema iniciado")
    
    # Loop 'while True' para manter o programa rodando até o usuário escolher Sair
    while True:
        # Título Personalizado
        print("\n" + "="*40)
        print("\033[96mSISTEMA DE CADASTRO DE ALUNOS\033[0m") # Cor Ciano
        print("="*40)
        
        # O sistema deve apresentar um menu principal
        print(" [1] Cadastrar Novo Aluno") 
        print(" [2] Listar Todos os Alunos") 
        print(" [3] Editar Média Final") 
        print(" [4] Excluir Aluno") 
        print(" [5] Sair do Sistema") 
        print("="*40)
        
        opcao = input("Escolha uma opção (1-5): ")
        
        # Estruturas de condição (if, elif, else) para tratar as opções
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
            print("\n\033[95mObrigado por usar o sistema! Encerrando...\033[0m") # Cor Magenta
            time.sleep(1) # Pausa antes de fechar
            break # Encerra o loop e o programa
        else:
            print("\n\033[91m[ERRO]\033[0m Opção inválida. Digite um número de 1 a 5.\n")
            registrar_log("Opção de menu inválida")


# Inicia a execução do programa
if __name__ == "__main__":
    menu_principal()