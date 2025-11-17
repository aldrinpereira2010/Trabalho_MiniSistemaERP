from tabulate import tabulate  # Biblioteca tabulate para formatar a lista
import locale  # Biblioteca locale para formatar valores monetários no padrão brasileiro,
# com pontos de milhar e vírgula decimal, garantindo que os valores sejam exibidos corretamente
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')  # Formato brasileiro
from datetime import datetime  # Para registrar datas e horários das movimentações
import matplotlib.pyplot as plt # Biblioteca matplotlib para criação dos gráficos de visualização de dados
import matplotlib.dates as mdates # Para manipulação de datas nos gráficos


# Lista vazia onde serão armazenados os produtos
estoque = []

# Lista onde serão registradas todas as entradas e saídas para gerar relatórios
movimentacoes = []

# Dicionário para armazenar os custos fixos do estoque
custos_fixos = {
    "capital": 0,
    "armazenagem": 0,
    "obsolescencia": 0,
    "seguro": 0
}

# Taxas usadas no cálculo do custo de manutenção (valores podem ser ajustados depois)
taxa_armazenagem = 0.03        
taxa_capital = 0.02            
taxa_obsolescencia = 0.01      
taxa_seguro = 0.015           

# Função que exibe a tabela de produtos cadastrados formatada pelo tabulate
def lista_de_produtos(lista):
    if not lista:
        print("(Nenhum produto cadastrado.)")
        return

    tabela = []
    for produto in lista:
        item = produto.copy()
        # Uso do método copy() para criar uma cópia independente do dicionário original,
        # evitando que alterações no item afetem os dados reais da lista de produtos
        item["Valor Unit."] = locale.currency(item["Valor Unit."], grouping=True)  # locale.currency() para formatar valores como moeda, adicionando R$
        item["Total"] = locale.currency(item["Total"], grouping=True)  # grouping=True adiciona separadores de milhar
        tabela.append(item)

    print(tabulate(tabela, headers="keys", tablefmt="grid"))


# Função de cadastro dos produtos
def cadastrar_produto(lista):
    print("\n-----CADASTRO DE PRODUTOS-----")

    # Loop while que retorna para o input de digitar o código caso o usuário já tenha digitado o mesmo código anteriormente
    while True:
        codigo_item = input("Digite o código do item: ").upper()  # Método upper() para deixar o código todo em letras maiúsculas

        # Loop for que percorre pelos itens da lista para verificar se o código inserido já foi digitado anteriormente
        if any(produto["Código"] == codigo_item for produto in lista):
            # Uso do método any() para verificar em toda a lista se algum item já possui o código digitado, retornando True caso exista
            print("Este código já foi cadastrado! Tente novamente.\n")
        else:
            break

    nome = input("Digite o nome do produto: ").title()  # Método title() para deixar a primeira letra da palavra maiúscula

    categoria = input("\nDigite a categoria do produto: ").title()

    qtd_inicial = int(input("\nDigite a quantidade incial em estoque do produto: "))

    valor_unit = float(input("\nDigite o valor unitário do produto: "))
    valor_total = valor_unit * qtd_inicial

    # Verifica se o estoque está baixo (abaixo de 5) ou ok
    if qtd_inicial < 5:
        status = "!ESTOQUE BAIXO!"
    else:
        status = "Estoque OK"

    print("\nProduto cadastrado com sucesso!")

    # Dicionário que armazena os itens de cada produto e envia para a lista de estoque com o método append()
    produto = {
        "Código": codigo_item,
        "Nome": nome,
        "Categoria": categoria,
        "Quantidade": qtd_inicial,
        "Valor Unit.": valor_unit,
        "Total": valor_total,
        "Status": status
    }

    lista.append(produto)

    print("\n-----LISTA DE PRODUTOS ATUALIZADA-----")
    # Chamada da função lista_de_produtos para exibir os produtos cadastrados até o momento
    lista_de_produtos(lista)


# Função de remoção dos produtos
def remover_produto(lista):
    print("\n----- OPÇÕES DE PRODUTOS PARA EXCLUSÃO -----")
    lista_de_produtos(lista)

    pesquisa_produto = input("\nDeseja pesquisar um produto por NOME ou ID para exclusão? ").upper()

    if pesquisa_produto == "NOME":
        nome_pesquisa = input("\nDigite o nome do produto que deseja excluir: ").title()

        for produto in lista:
            if produto["Nome"] == nome_pesquisa:
                lista.remove(produto)
                print(f"\nProduto '{produto['Nome']}' removido com sucesso!\n")
                break
        else:
            print("\nProduto não encontrado! Verifique o nome digitado.\n")

    elif pesquisa_produto == "ID":
        id_pesquisa = input("\nDigite o código do produto que deseja excluir: ").upper()

        for produto in lista:
            if produto["Código"] == id_pesquisa:
                lista.remove(produto)
                print(f"\nProduto '{produto['Nome']}' removido com sucesso!\n")
                break
        else:
            print("\nProduto não encontrado! Verifique o código digitado.\n")

    else:
        print("Opção inválida. Digite 'NOME' ou 'ID'.")

    print("\n----- LISTA ATUALIZADA -----")
    lista_de_produtos(lista)


def ler_data():
    data_str = input("Digite a data da movimentação (DD/MM/AAAA) ou deixe vazio para hoje: ")

    if data_str.strip() == "":
        # Se o usuário não digitar nada pega a data atual
        return datetime.now()

    try:
        return datetime.strptime(data_str, "%d/%m/%Y")
    except:
        print("Data inválida! Usando a data de hoje.")
        return datetime.now()


# Função de entrada e saída dos produtos
def entrada_saida(lista):
    print("\n-----ENTRADA/SAÍDA DE ESTOQUE-----")
    if not lista:
        print("O estoque está vazio.")
    else:
        lista_de_produtos(lista)

        opcao = input("\nDigite o código do produto que deseja alterar: ").upper()

        # Procura o produto na lista
        for produto in lista:
            if produto["Código"] == opcao:

                entra_sai = int(input("\nVocê deseja registrar:\n1 - Entrada\n2 - Saída\nOpção: "))

                if entra_sai == 1:  # Entrada
                    print("\n-----ENTRADA DE ESTOQUE-----")
                    entrada = int(input("Digite a quantidade da entrada: "))
                    if entrada <= 0:
                        print("Digite uma quantidade válida maior que zero.")
                        continue
                        
                    data = ler_data()

                    produto["Quantidade"] += entrada
                    produto["Total"] = produto["Quantidade"] * produto["Valor Unit."]
                    produto["Status"] = "!ESTOQUE BAIXO!" if produto["Quantidade"] < 5 else "Estoque OK"

                    print(f"\nEntrada registrada! Nova quantidade de {produto['Nome']}: {produto['Quantidade']}")

                    movimentacoes.append({
                        "codigo": produto["Código"],
                        "nome": produto["Nome"],
                        "tipo": "entrada",
                        "quantidade": entrada,
                        "data_recebimento": data
                    })


                if entra_sai == 2:  # Saída
                    print("\n-----SAÍDA DE ESTOQUE-----")
                    saida = int(input("Digite a quantidade de saída: "))
                    if saida <= 0:
                        print("Digite uma quantidade válida maior que zero.")
                        continue
                    elif saida > produto["Quantidade"]:
                        print("O valor de saída não pode ser maior que a quantidade em estoque.")
                        continue

                    data = ler_data()

                    produto["Quantidade"] -= saida
                    produto["Total"] = produto["Quantidade"] * produto["Valor Unit."]
                    produto["Status"] = "!ESTOQUE BAIXO!" if produto["Quantidade"] < 5 else "Estoque OK"

                    print(f"\nSaída registrada! Nova quantidade de {produto['Nome']}: {produto['Quantidade']}")

                    movimentacoes.append({
                        "codigo": produto["Código"],
                        "nome": produto["Nome"],
                        "tipo": "saida",
                        "quantidade": saida,
                        "data_pedido": data
                    })

                else:
                    print("Opção inválida.")
                break
        else:
            print("\nProduto não encontrado! Verifique o código digitado.")

        print("\n-----ESTOQUE ATUALIZADO-----")
        lista_de_produtos(lista)


# Função de relatório gerencial
def relatorio_gerencial(lista, movimentacoes):
    print("\n----- RELATÓRIO GERENCIAL -----")

    # 1. Calcular CMV (Custo das Mercadorias Vendidas)
    CMV = 0
    for mov in movimentacoes:
        if mov["tipo"] == "saida":
            # buscar o valor unitário do produto correspondente
            for produto in lista:
                if produto["Código"] == mov["codigo"]:
                    CMV += mov["quantidade"] * produto["Valor Unit."]
                    break

    # 2. Calcular Estoque Médio
    estoque_inicial = 0
    estoque_final = 0
    for produto in lista:
        codigo = produto["Código"]
        estoque_final += produto["Quantidade"]

        entradas = sum(mov["quantidade"] for mov in movimentacoes 
                       if mov["codigo"] == codigo and mov["tipo"] == "entrada")
        saidas  = sum(mov["quantidade"] for mov in movimentacoes 
                      if mov["codigo"] == codigo and mov["tipo"] == "saida")
        estoque_inicial += produto["Quantidade"] + saidas - entradas

    estoque_medio = (estoque_inicial + estoque_final) / 2 if len(lista) > 0 else 0

    # 3. Calcular Giro de Estoque
    giro_estoque = CMV / estoque_medio if estoque_medio > 0 else 0

    # 4. Exibir resultados de giro de estoque
    print("\n>>> Giro de Estoque:")
    print(f"CMV total: R$ {CMV:.2f}")
    print(f"Estoque médio: {estoque_medio:.2f}")
    print(f"Giro de estoque: {giro_estoque:.2f} vezes no período")

    # 5. Calcular custo de manutenção do estoque
    custo_total_manutencao = 0
    for produto in lista:
        custo_produto = produto["Total"] * (taxa_capital + taxa_armazenagem + taxa_obsolescencia + taxa_seguro)
        custo_total_manutencao += custo_produto
    print(f"Custo total de manutenção do estoque: R$ {custo_total_manutencao:.2f}")

    # 6. Calcular tempo médio de reposição
    print("\n>>> Tempo médio de reposição por produto:")
    tempo_medio_reposicao = {}  # para usar no cálculo do estoque de segurança
    for produto in lista:
        tempos = []
        for mov_entrada in movimentacoes:
            if mov_entrada["tipo"] == "entrada" and mov_entrada["codigo"] == produto["Código"]:
                # buscar a saída correspondente (pedido)
                for mov_saida in movimentacoes:
                    if mov_saida["tipo"] == "saida" and mov_saida["codigo"] == produto["Código"]:
                        dias = (mov_entrada["data_recebimento"] - mov_saida["data_pedido"]).days
                        tempos.append(dias)
                        break
        if tempos:
            tempo_medio = sum(tempos) / len(tempos)
            tempo_medio_reposicao[produto["Código"]] = tempo_medio
            print(f"{produto['Nome']}: {tempo_medio:.1f} dias")
        else:
            tempo_medio_reposicao[produto["Código"]] = 0
            print(f"{produto['Nome']}: Sem reposição registrada")

    # 7. Calcular estoque de segurança
    print("\n>>> Estoque de segurança por produto:")
    for produto in lista:
        # calcular demanda média diária baseada nas saídas registradas
        saidas = [mov["quantidade"] for mov in movimentacoes if mov["tipo"] == "saida" and mov["codigo"] == produto["Código"]]
        demanda_media_diaria = sum(saidas) / len(saidas) if saidas else 1 
        tempo_reposicao = tempo_medio_reposicao.get(produto["Código"], 1)  
        estoque_seguranca = round(demanda_media_diaria * tempo_reposicao)
        print(f"{produto['Nome']}: {estoque_seguranca} unidades")

    print("\n--------------------------------")


# Função de mostrar o Dashboard de Gráficos dos produtos.
def dashboard_estoque(lista):
    if not lista:
        print("Nenhum produto cadastrado para gerar dashboard.")
        return

    nomes = [p["Nome"] for p in lista]
    quantidades = [p["Quantidade"] for p in lista]
    valores_totais = [p["Total"] for p in lista]

    # Cálculo da Curva ABC
    dados_ordenados = sorted(lista, key=lambda x: x["Total"], reverse=True)

    nomes_ordenados = [p["Nome"] for p in dados_ordenados]
    valores_ordenados = [p["Total"] for p in dados_ordenados]

    total_geral = sum(valores_ordenados)

    percentuais = [(v / total_geral) * 100 for v in valores_ordenados]

    acumulado = []
    soma = 0
    for p in percentuais:
        soma += p
        acumulado.append(soma)

    # Dashboard com 4 gráficos
    plt.figure(figsize=(14, 10))

    # Gráfico 1 – Quantidade em barra
    plt.subplot(2, 2, 1)
    plt.bar(nomes, quantidades)
    plt.title("Quantidade em Estoque")
    plt.xticks(rotation=45)

    # Gráfico 2 – Pizza
    plt.subplot(2, 2, 2)
    plt.pie(quantidades, labels=nomes, autopct='%1.1f%%')
    plt.title("Participação por Quantidade")

    # Gráfico 3 – Valor total horizontal
    plt.subplot(2, 2, 3)
    plt.barh(nomes, valores_totais)
    plt.title("Valor Total em Estoque (R$)")
    plt.xlabel("Valor (R$)")

    # Gráfico 4 – Curva ABC
    plt.subplot(2, 2, 4)
    plt.plot(nomes_ordenados, acumulado, marker="o")
    plt.axhline(80, linestyle="--", color="green", label="Limite A (80%)")
    plt.axhline(95, linestyle="--", color="orange", label="Limite B (95%)")
    plt.title("Curva ABC")
    plt.xlabel("Produtos (ordenados por valor)")
    plt.ylabel("Percentual Acumulado (%)")
    plt.xticks(rotation=45)
    plt.legend()

    plt.tight_layout()
    plt.show()


# Função que armazena o menu de opções do usuário
def menu(lista):
    while True:
        opcao = int(input(
            "\nDigite a opção que deseja realizar:" 
            "\n1 - Cadastrar Produto " 
            "\n2 - Excluir Produto " 
            "\n3 - Entrada/Saída de Produto " 
            "\n4 - Listar Estoque " 
            "\n5 - Relatório Gerencial "
            "\n6 - Dashboard de Gráficos "
            "\n7 - Encerrar Programa " 
            "\nOpção: "
        ))

        if opcao == 1:
            cadastrar_produto(lista)
        elif opcao == 2:
            remover_produto(lista)
        elif opcao == 3:
            entrada_saida(lista)
        elif opcao == 4:
            lista_de_produtos(lista)
        elif opcao == 5:
            relatorio_gerencial(lista, movimentacoes)
        elif opcao == 6:
            dashboard_estoque(lista)
        elif opcao == 7:
            print("\n-----LISTA DE PRODUTOS CADASTRADOS-----")
            lista_de_produtos(lista)
            print("\nPrograma encerrado!")
            break
        else:
            print("Digite um valor válido.\n")


# Chamada da função menu que fará rodar todo o código até o usuário decidir parar o programa
menu(estoque)
