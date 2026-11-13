
from datetime import datetime
from os import name

clientes = []
contador_faturas = 1

def calcular_bonus(valor):
    if valor > 100000:
        return valor * 0.10
    return 0
def identificar_prioridade(genero, idade, gravida, deficiencia):
    motivos = []
    if genero == "F" and gravida == "S":
        motivos.append("Mulher gravida")
    if idade >= 60:
        motivos.append("Pessoa idosa")
    if deficiencia == "S":
        motivos.append("Pessoa com deficiencia")
    return motivos

def ler_inteiro(mensagem, minimo=0):
    while True:
        try:
            valor = int(input(mensagem))
            if valor < minimo:
                print("Valor invalido. Tente novamente.")
            else:
                return valor
        except ValueError:
            print("Introduza um numero inteiro valido.")
def ler_decimal(mensagem, minimo=0):
    while True:
        try:
            valor = float(input(mensagem).replace(",", "."))
            if valor < minimo:
                print("Valor invalido. Tente novamente.")
            else:
                return valor
        except ValueError:
            print("Introduza um valor numerico valido.")
def ler_opcao(mensagem, opcoes):
    while True:
        valor = input(mensagem).strip().upper()
        if valor in opcoes:
            return valor
        print("Opcao invalida. Escolha:", ", ".join(opcoes))

def registar_cliente():
    global contador_faturas
    print("\n========== REGISTO DE CLIENTE ==========")
    nome = input("Nome completo: ").strip()
    while not nome:
        print("O nome nao pode ficar vazio.")
        nome = input("Nome completo: ").strip()
    genero = ler_opcao("Genero (M/F): ", ["M", "F"])
    idade = ler_inteiro("Idade: ", 0)
    valor_compras = ler_decimal(
        "Valor total das compras (Kz): ", 0
    )
    if genero == "F":
        gravida = ler_opcao(
            "A cliente esta gravida? (S/N): ", ["S", "N"]
        )
    else:
        gravida = "N"
    deficiencia = ler_opcao(
        "Possui alguma deficiencia? (S/N): ", ["S", "N"]
    )
    bonus = calcular_bonus(valor_compras)
    valor_final = valor_compras - bonus
    motivos = identificar_prioridade(
        genero, idade, gravida, deficiencia
    )
    cliente = {
        "fatura": contador_faturas,
        "nome": nome,
        "genero": genero,
        "idade": idade,
        "valor_compras": valor_compras,
        "bonus": bonus,
        "valor_final": valor_final,
        "motivos": motivos,
        "prioritario": len(motivos) > 0,
        "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "atendido": False
    }
    clientes.append(cliente)
    contador_faturas += 1
    print("\nCliente registado com sucesso!")
    emitir_fatura(cliente)

def emitir_fatura(cliente):
    print("\n" + "=" * 55)
    print("                  FATURA")
    print("=" * 55)
    print("Numero da fatura:", cliente["fatura"])
    print("Data:", cliente["data"])
    print("Cliente:", cliente["nome"])
    print("Genero:", cliente["genero"])
    print("Idade:", cliente["idade"])
    print("-" * 55)
    print("Valor das compras: %.2f Kz" %
          cliente["valor_compras"])
    print("Bonus comercial: %.2f Kz" %
          cliente["bonus"])
    print("TOTAL A PAGAR: %.2f Kz" %
          cliente["valor_final"])
    print("-" * 55)
    if cliente["prioritario"]:
        print("ATENDIMENTO: PRIORITARIO")
        print("Motivos:")
        for motivo in cliente["motivos"]:
            print("-", motivo)
    else:
        print("ATENDIMENTO: NORMAL")
    print("=" * 55)
    print("Obrigado pela preferencia!")

def organizar_fila():
    fila = [c for c in clientes if not c["atendido"]]
    fila.sort(key=lambda c: not c["prioritario"])
    return fila

def mostrar_fila():
    fila = organizar_fila()
    print("\n========== FILA DE ATENDIMENTO ==========")
    if not fila:
        print("Nao existem clientes na fila.")
        return
    for posicao, cliente in enumerate(fila, start=1):
        estado = (
            "PRIORITARIO"
            if cliente["prioritario"]
            else "NORMAL"
        )
        print("\nPosicao:", posicao)
        print("Cliente:", cliente["nome"])
        print("Atendimento:", estado)
        if cliente["motivos"]:
            print("Motivos:", ", ".join(cliente["motivos"]))

def realizar_atendimento():
    fila = organizar_fila()
    print("\n========== ATENDIMENTO ==========")
    if not fila:
        print("Nao existem clientes para atender.")
        return
    cliente = fila[0]
    print("Proximo cliente:", cliente["nome"])
    confirmar = ler_opcao(
        "Confirmar atendimento? (S/N): ", ["S", "N"]
    )
    if confirmar == "S":
        cliente["atendido"] = True
        print("Atendimento realizado com sucesso!")
    else:
        print("Atendimento nao realizado.")

def relatorio_vendas():
    print("\n========== RELATORIO DE VENDAS ==========")
    if not clientes:
        print("Ainda nao existem vendas registadas.")
        return
    total_vendas = sum(
        c["valor_compras"] for c in clientes
    )
    total_bonus = sum(
        c["bonus"] for c in clientes
    )
    total_receber = sum(
        c["valor_final"] for c in clientes
    )
    prioritarios = sum(
        1 for c in clientes if c["prioritario"]
    )
    normais = len(clientes) - prioritarios
    atendidos = sum(
        1 for c in clientes if c["atendido"]
    )
    print("Total de clientes:", len(clientes))
    print("Total de compras: %.2f Kz" % total_vendas)
    print("Total de bonus: %.2f Kz" % total_bonus)
    print("Total a receber: %.2f Kz" % total_receber)
    print("Clientes prioritarios:", prioritarios)
    print("Clientes normais:", normais)
    print("Clientes atendidos:", atendidos)
    print("Clientes por atender:", len(clientes) - atendidos)
    print("=" * 55)

def menu_principal():
    while True:
        print("\n" + "=" * 55)
        print("       SISTEMA DE FATURACAO")
        print("       LOJA DE PRODUTOS ALIMENTARES")
        print("=" * 55)
        print("1 - Registar cliente e compra")
        print("2 - Mostrar fila de atendimento")
        print("3 - Realizar atendimento")
        print("4 - Consultar relatorio de vendas")
        print("5 - Consultar todas as faturas")
        print("0 - Sair do sistema")
        opcao = input("\nEscolha uma opcao: ").strip()
        if opcao == "1":
            registar_cliente()
        elif opcao == "2":
            mostrar_fila()
        elif opcao == "3":
            realizar_atendimento()
        elif opcao == "4":
            relatorio_vendas()
        elif opcao == "5":
            if not clientes:
                print("Nao existem faturas registadas.")
            else:
                for cliente in clientes:
                    emitir_fatura(cliente)
        elif opcao == "0":
            print("\nSistema encerrado.")
            print("Obrigado por utilizar o programa!")
            break
        else:
            print("Opcao invalida. Tente novamente.")

if __name__ == "__main__":
    menu_principal()