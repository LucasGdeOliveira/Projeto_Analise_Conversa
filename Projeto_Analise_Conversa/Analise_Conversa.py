import pandas as pd
import matplotlib.pyplot as plt

# Função para leitura e processamento do arquivo de conversa
def carregar_arquivo_conversa(arquivo):
    # Leitura do arquivo
    with open(arquivo, 'r', encoding='utf-8') as f:
        conteudo = f.readlines()
    
    # Variáveis para armazenar os dados
    dados = []
    
    # Loop para processar linha por linha e extrair data, hora, remetente e mensagem
    for linha in conteudo:
        try:
            # Divide a linha entre data e conteúdo
            data_hora, restante = linha.split('] ', 1)
            data, hora = data_hora.replace('[', '').split(', ')
            # Divide o restante entre remetente e mensagem
            remetente, mensagem = restante.split(': ', 1)
            dados.append([data, hora, remetente.strip(), mensagem.strip()])
        except ValueError:
            continue
    
    # Criação do DataFrame
    df = pd.DataFrame(dados, columns=['data', 'hora', 'remetente', 'mensagem'])
    return df

# Função para exibir o resumo das conversas
def resumo_conversas(df):
    resumo = df['remetente'].value_counts().sort_values(ascending=False)
    print(resumo)
    return resumo

# Função para exibir o histórico de um remetente específico
def historico_remetente(df, remetente):
    filtro = df[df['remetente'] == remetente]
    print(filtro[['data', 'hora', 'mensagem']])
    return filtro

# Função para exibir histograma de conversas por dia de um remetente
def grafico_histograma_remetente(df, remetente):
    filtro = df[df['remetente'] == remetente]
    contagem_por_dia = filtro['data'].value_counts().sort_index()
    ax = contagem_por_dia.plot(kind='bar', figsize=(10, 6), title=f'Histograma de conversas por dia - {remetente}')
    plt.xlabel('Data')
    plt.ylabel('Quantidade de mensagens')
    ax.legend([remetente])  # Ajusta a legenda com o nome do remetente
    plt.show()

# Função para exibir gráfico de pizza com percentual de mensagens por remetente
def grafico_pizza_remetentes(df):
    resumo = df['remetente'].value_counts()
    resumo = resumo[resumo > 0]  # Remover possíveis valores nulos
    resumo_top_15 = resumo.nlargest(15)  # Seleciona os 15 remetentes com mais mensagens
    resumo_top_15.plot(kind='pie', autopct=lambda p: f'{p:.1f}%' if p >= 3 else '', figsize=(8, 8), title='Percentual de Mensagens por Remetente (Top 15)')
    plt.ylabel('')  # Remove o label do eixo y
    plt.legend(resumo_top_15.index, loc='center left', bbox_to_anchor=(1, 0.5))  # Ajusta a legenda para o lado direito
    plt.show()

# Função para exibir gráfico de linhas com o histórico de mensagens ao longo do tempo
def grafico_linhas_remetentes(df, remetente):
    df['data'] = pd.to_datetime(df['data'], format='%d/%m/%Y', errors='coerce')
    contagem_diaria = df.groupby(['data', 'remetente']).size().unstack(fill_value=0)
    contagem_diaria[remetente].plot(kind='line', figsize=(12, 6), title='Quantidade de Mensagens ao longo do tempo')
    plt.xlabel('Data')
    plt.ylabel('Quantidade de mensagens')
    plt.legend(title='Remetente', labels=[remetente])  # Adiciona título à legenda
    plt.show()

# Leitura e criação do DataFrame a partir do arquivo
df_conversa = carregar_arquivo_conversa('_chat.txt')

# Apresentação do DataFrame completo
print(df_conversa)

# Menu para selecionar a análise desejada
remetente_escolhido = None

while True:
    print("\nEscolha uma opção de análise:")
    print("1. Resumo das conversas")
    print("2. Histórico do remetente")
    print("3. Gráfico do histórico do remetente (Histograma)")
    print("4. Gráfico de pizza (Percentual de mensagens por remetente)")
    print("5. Gráfico de linhas (Mensagens ao longo do tempo)")
    print("0. Sair")
    
    opcao = input("Digite o número da opção: ")
    
    if opcao == '1':
        resumo_conversas(df_conversa)
    elif opcao == '2':
        remetente_escolhido = input("Digite o nome do remetente: ")
        historico_remetente(df_conversa, remetente_escolhido)
    elif opcao == '3':
        if remetente_escolhido is None:
            print("Você precisa selecionar um remetente primeiro.")
        else:
            grafico_histograma_remetente(df_conversa, remetente_escolhido)
    elif opcao == '4':
        grafico_pizza_remetentes(df_conversa)
    elif opcao == '5':
        if remetente_escolhido is None:
            print("Você precisa selecionar um remetente primeiro.")
        else:
            grafico_linhas_remetentes(df_conversa, remetente_escolhido)
    elif opcao == '0':
        break
    else:
        print("Opção inválida. Tente novamente.")
