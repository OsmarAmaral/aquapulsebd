import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt

# Configuração da conexão com o banco de dados MySQL
db_config = {
    'host': 'localhost',       
    'user': 'root',    
    'password': '',   
    'database': 'AquaPulse'    
}

# Conexão com o banco
conn = mysql.connector.connect(**db_config)

def estados_usuario():
    try:
        # Consulta SQL para agrupar os usuários por estado
        query = """
        SELECT estado_usuario, COUNT(*) as total
        FROM tbUsuarios
        GROUP BY estado_usuario
        ORDER BY total DESC;
        """
        
        # Executar a query e carregar os dados manualmente em um DataFrame
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()  # Recuperar os resultados

        # Criar o DataFrame manualmente
        df = pd.DataFrame(rows, columns=['estado_usuario', 'total'])
        cursor.close()

        # Remover valores nulos da coluna 'estado_usuario'
        df = df[df['estado_usuario'].notna()]

        # Verificar se o DataFrame está vazio após a remoção de nulos
        if df.empty:
            print("Nenhum dado válido retornado para o gráfico.")
            return

        # Preparar o gráfico de barras horizontais
        plt.figure(figsize=(10, 8))
        plt.barh(df['estado_usuario'], df['total'], color='skyblue')
        plt.title('Distribuição de Usuários por Estado')
        plt.xlabel('Número de Usuários')
        plt.ylabel('Estado')
        plt.gca().invert_yaxis()  # Inverter o eixo Y para mostrar o maior valor no topo
        plt.tight_layout()

        # Exibir o gráfico
        plt.show()

    except mysql.connector.Error as e:
        print(f"Erro ao executar a consulta no banco de dados: {e}")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

# Executar a função para gerar o gráfico
estados_usuario()


def avaliacoes_usuario():
    # Consulta SQL para contar os valores de ava_usuario
    query = """
    SELECT ava_usuario, COUNT(*) as total
    FROM tbUsuarios
    GROUP BY ava_usuario;
    """
    
    # Executar a query e carregar os dados manualmente em um DataFrame
    cursor = conn.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()  # Recuperar os resultados
    
    # Criar o DataFrame manualmente
    df = pd.DataFrame(rows, columns=['ava_usuario', 'total'])
    cursor.close()

    # Substituir `NaN` por "Desconhecido" e verificar os dados
    df['ava_usuario'] = df['ava_usuario'].fillna('Desconhecido')
    print(df)

    # Preparar os dados para o gráfico de pizza
    labels = df['ava_usuario'].replace({1.0: 'positivo', 0.0: 'negativo', 'Desconhecido': 'desconhecido'}).tolist()
    sizes = df['total']
    colors = ['#4CAF50', '#FF5733', '#FFC300']  # Cores personalizadas para cada categoria
    
    # Remover categorias muito pequenas (opcional)
    df = df[df['total'] > 5]  # Excluir categorias com menos de 5 ocorrências
    labels = df['ava_usuario'].tolist()
    sizes = df['total']

    # Criar o gráfico de pizza
    plt.figure(figsize=(8, 8))
    plt.pie(
        sizes, 
        labels=labels, 
        autopct='%1.1f%%', 
        startangle=90, 
        colors=colors[:len(labels)]  # Ajustar cores para o número de categorias
    )
    plt.title('Distribuição de Avaliações de Usuários')
    plt.axis('equal')  # Garantir que o gráfico seja um círculo perfeito
    plt.show()

def receita_pedidos():
    try:
        # Consulta SQL para agrupar receitas por data
        query = """
        SELECT data_pedido, SUM(total_pedido) as receita
        FROM tbPedidos
        GROUP BY data_pedido
        ORDER BY data_pedido;
        """
        
        # Executar a query e carregar os dados em um DataFrame
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        df = pd.DataFrame(rows, columns=['data_pedido', 'receita'])
        cursor.close()

        # Garantir que as datas estejam em formato datetime
        df['data_pedido'] = pd.to_datetime(df['data_pedido'])

        # Criar o gráfico de linha
        plt.figure(figsize=(10, 6))
        plt.plot(df['data_pedido'], df['receita'], marker='o', color='blue')
        plt.title('Receita Total por Data')
        plt.xlabel('Data do Pedido')
        plt.ylabel('Receita Total (R$)')
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    except mysql.connector.Error as e:
        print(f"Erro ao executar a consulta no banco de dados: {e}")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

def status_pedidos():
    try:
        # Consulta SQL para agrupar status por data
        query = """
        SELECT data_pedido, COUNT(CASE WHEN status_pedido = 'concluído' THEN 1 END) as concluido,
               COUNT(CASE WHEN status_pedido = 'pendente' THEN 1 END) as pendente,
               COUNT(CASE WHEN status_pedido = 'cancelado' THEN 1 END) as cancelado
        FROM tbPedidos
        GROUP BY data_pedido
        ORDER BY data_pedido;
        """
        
        # Executar a query e carregar os dados em um DataFrame
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        df = pd.DataFrame(rows, columns=['data_pedido', 'concluido', 'pendente', 'cancelado'])
        cursor.close()

        # Garantir que as datas estejam em formato datetime
        df['data_pedido'] = pd.to_datetime(df['data_pedido'])

        # Criar o gráfico de linhas para status de pedidos
        plt.figure(figsize=(10, 6))
        plt.plot(df['data_pedido'], df['concluido'], label='Concluído', marker='o', color='green')
        plt.plot(df['data_pedido'], df['pendente'], label='Pendente', marker='o', color='orange')
        plt.plot(df['data_pedido'], df['cancelado'], label='Cancelado', marker='o', color='red')
        plt.title('Status dos Pedidos por Data')
        plt.xlabel('Data do Pedido')
        plt.ylabel('Número de Pedidos')
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    except mysql.connector.Error as e:
        print(f"Erro ao executar a consulta no banco de dados: {e}")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

# Executar a função para gerar o gráfico
receita_pedidos()
status_pedidos()

# Fechar a conexão após a execução
conn.close()
