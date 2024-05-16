import sqlite3

def criar_tabela():
    conn = sqlite3.connect('santander_data.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS clientes (
                      id INTEGER PRIMARY KEY,
                      nome TEXT,
                      telefone TEXT,
                      idade INTEGER,
                      score INTEGER,
                      saldo INT)''')
    conn.commit()
    conn.close()

def cadastrar_cliente():
    print("\nCadastro de Cliente\n")
    nome = input("Nome: ")
    telefone = input("Telefone: ")
    idade = int(input("Idade: "))
    score = int(input("Score: "))
    saldo = float(input("Saldo inicial: "))

    conn = sqlite3.connect('santander_data.db')
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO clientes (nome, telefone, idade, score, saldo) VALUES (?, ?, ?, ?, ?)''',
                   (nome, telefone, idade, score, saldo))
    conn.commit()
    conn.close()
    print("Cliente cadastrado com sucesso!")

def mostrar_saldo():
    print("\nConsulta de Saldo\n")
    nome_cliente = input("Digite o nome do cliente: ")

    conn = sqlite3.connect('santander_data.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT saldo FROM clientes WHERE nome = ?''', (nome_cliente,))
    resultado = cursor.fetchone()
    conn.close()

    if resultado:
        saldo = resultado[0]
        print(f"O saldo do cliente {nome_cliente} é: R$ {saldo:.2f}\n")
    else:
        print("Cliente não encontrado.")


def saque():
    print("\nRealizar Saque\n")
    nome_cliente = input("Digite o nome do cliente: ")
    valor_saque = float(input("Digite o valor do saque: "))

    conn = sqlite3.connect('santander_data.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT saldo, score FROM clientes WHERE nome = ?''', (nome_cliente,))
    resultado = cursor.fetchone()

    if resultado:
        saldo, score = resultado
        if saldo >= valor_saque:
            novo_saldo = saldo - valor_saque
            cursor.execute('''UPDATE clientes SET saldo = ? WHERE nome = ?''', (novo_saldo, nome_cliente))
            conn.commit()
            print(f"Saque de R$ {valor_saque:.2f} realizado com sucesso. Novo saldo: R$ {novo_saldo:.2f}\n")
        else:
            opcao = input("Saldo insuficiente para o saque. Deseja aceitar um empréstimo baseado em seu score? (sim/não): ")
            if opcao.lower() == 'sim':
                if score < 100:
                    print("Seu score é muito baixo para solicitar um empréstimo.")
                elif 100 <= score <= 300:
                    print("Você tem a opção de um empréstimo de R$ 5,000. Seu score será zerado.")
                    if input("Deseja continuar? (sim/não): ").lower() == 'sim':
                        novo_saldo = saldo + 5000
                        cursor.execute('''UPDATE clientes SET saldo = ?, score = 0 WHERE nome = ?''', (novo_saldo, nome_cliente))
                        conn.commit()
                        if novo_saldo >= valor_saque:
                            novo_saldo -= valor_saque
                            cursor.execute('''UPDATE clientes SET saldo = ? WHERE nome = ?''', (novo_saldo, nome_cliente))
                            conn.commit()
                            print(f"Saque de R$ {valor_saque:.2f} realizado com sucesso. Novo saldo: R$ {novo_saldo:.2f}\n")
                        else:
                            print(f"O saldo ainda é insuficiente para o saque. Saldo atual: R$ {novo_saldo:.2f}")
                elif 300 < score <= 700:
                    print("Você tem a opção de um empréstimo de R$ 10,000. Seu score será diminuído para 299.")
                    if input("Deseja continuar? (sim/não): ").lower() == 'sim':
                        novo_saldo = saldo + 10000
                        cursor.execute('''UPDATE clientes SET saldo = ?, score = 299 WHERE nome = ?''', (novo_saldo, nome_cliente))
                        conn.commit()
                        if novo_saldo >= valor_saque:
                            novo_saldo -= valor_saque
                            cursor.execute('''UPDATE clientes SET saldo = ? WHERE nome = ?''', (novo_saldo, nome_cliente))
                            conn.commit()
                            print(f"Saque de R$ {valor_saque:.2f} realizado com sucesso. Novo saldo: R$ {novo_saldo:.2f}\n")
                        else:
                            print(f"O saldo ainda é insuficiente para o saque. Saldo atual: R$ {novo_saldo:.2f}")
                elif 700 < score <= 1000:
                    print("Você tem a opção de um empréstimo de R$ 15,000. Seu score será diminuído para 699.")
                    if input("Deseja continuar? (sim/não): ").lower() == 'sim':
                        novo_saldo = saldo + 15000
                        cursor.execute('''UPDATE clientes SET saldo = ?, score = 699 WHERE nome = ?''', (novo_saldo, nome_cliente))
                        conn.commit()
                        if novo_saldo >= valor_saque:
                            novo_saldo -= valor_saque
                            cursor.execute('''UPDATE clientes SET saldo = ? WHERE nome = ?''', (novo_saldo, nome_cliente))
                            conn.commit()
                            print(f"Saque de R$ {valor_saque:.2f} realizado com sucesso. Novo saldo: R$ {novo_saldo:.2f}\n")
                        else:
                            print(f"O saldo ainda é insuficiente para o saque. Saldo atual: R$ {novo_saldo:.2f}")
            else:
                print("Operação de saque cancelada.")
    else:
        print("Cliente não encontrado.")

    conn.close()

def deposito():
    print("\nRealizar Depósito\n")
    nome_cliente = input("Digite o nome do cliente: ")
    valor_deposito = float(input("Digite o valor do depósito: "))

    conn = sqlite3.connect('santander_data.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT saldo FROM clientes WHERE nome = ?''', (nome_cliente,))
    resultado = cursor.fetchone()

    if resultado:
        saldo = resultado[0]
        novo_saldo = saldo + valor_deposito
        cursor.execute('''UPDATE clientes SET saldo = ? WHERE nome = ?''', (novo_saldo, nome_cliente))
        conn.commit()
        print(f"Depósito de R$ {valor_deposito:.2f} realizado com sucesso. Novo saldo: R$ {novo_saldo:.2f}\n")
    else:
        print("Cliente não encontrado.")

    conn.close()


def menu():
    while True:
        print("|******************************|")
        print("| Bem-vindo ao Banco Santander |")
        print("|-1 - Cadastro de Clientes-----|")
        print("|-2 - Consultar Saldo----------|")
        print("|-3 - Realizar Saque-----------|")
        print("|-4 - Depositar----------------|")
        print("|-5 - Sair---------------------|")
        print("|******************************|")

        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            cadastrar_cliente()
        elif opcao == '2':
            mostrar_saldo()
        elif opcao == '3':
            saque()
        elif opcao == '4':
            deposito()
        elif opcao == '5':
            print("Saindo do Sistema")
            break
        else:
            print("Opção inválida. Por favor, escolha uma opção válida.")

if __name__ == "__main__":
    criar_tabela()
    menu()
