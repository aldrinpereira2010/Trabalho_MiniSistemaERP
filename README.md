# Trabalho Mini Sistema ERP de Controle de Estoque em Python

## Descrição
  Este projeto implementa um sistema básico de controle de estoque em Python. Ele permite cadastrar produtos, registrar entradas e saídas de estoque, gerar relatórios gerenciais e criar dashboards gráficos para análise visual dos dados. O sistema foi concebido para uso em ambientes que necessitam de monitoramento simples e eficiente de inventário.

## Funcionalidades
- Cadastro de produtos com código, nome, categoria, quantidade inicial e valor unitário.
- Registro de entradas e saídas de estoque com controle de data.
- Listagem dos produtos em estoque formatada para fácil visualização.
- Remoção de produtos por nome ou código.
- Cálculo de indicadores gerenciais como Custo das Mercadorias Vendidas (`CMV`), estoque médio, giro de estoque, custo total de manutenção e tempo médio de reposição.
- Cálculo e exibição do estoque de segurança baseado na demanda média diária.
- Dashboard visual com gráficos de estoque, participação percentual, valor total e Curva ABC, utilizando Matplotlib.
- Menu interativo para navegar entre as opções do sistema.

## Tecnologias Utilizadas
- Python 3.x
- Bibliotecas: `tabulate`, `locale`, `datetime`, `matplotlib`

## Como Usar

### Pré-requisitos
- Ter Python 3 instalado no sistema.
- Instalar as dependências necessárias:
```
pip install tabulate matplotlib
```

### Executando o Projeto
1. Copie ou baixe este repositório.
2. Execute o script principal em seu terminal:
```
python MiniSistemaErp.py
```
3. Use o menu interativo para realizar operações de controle de estoque.

## Estrutura do Código
- `estoque`: lista que armazena os produtos cadastrados em formato de dicionários.
- `movimentacoes`: lista que armazena todas as entradas e saídas para geração dos relatórios.
- `custos_fixos` e taxas para cálculo de custo de manutenção.
- Funções: 
  - `cadastrar_produto` para adicionar produtos.
  - `remover_produto` para excluir produtos.
  - `entrada_saida` para registrar movimentações no estoque.
  - `lista_de_produtos` para exibir os produtos de forma organizada.
  - `relatorio_gerencial` para gerar análises e indicadores do estoque.
  - `dashboard_estoque` para mostrar gráficos visuais.
  - `menu` que controla a interação do usuário com o sistema.

## Exemplos de Uso
Ao executar o programa, você pode:

- Cadastrar um novo produto informando código, nome, categoria, quantidade e valor unitário.
- Registrar uma entrada ou saída em estoque especificando o código do produto e a quantidade.
- Visualizar o estoque atual formatado.
- Gerar relatórios que mostram a performance do estoque.
- Visualizar gráficos para análise rápida.

## Detalhes Técnicos
- O sistema formata automaticamente valores monetários no padrão brasileiro (R$, com vírgula decimal e ponto como separador de milhar).
- Utiliza o módulo `locale` para garantir essa formatação.
- Os dados de movimentações armazenam as datas das entradas e saídas para cálculo do tempo médio de reposição.
- A Curva ABC é calculada com base no valor total em estoque, ajudando a identificar produtos mais valiosos para o negócio.
- Os gráficos são gerados pela biblioteca Matplotlib, mostrando diferentes perspectivas do estoque visualmente.



