import repositorio as repo
from db import testar_conexao


def main():
    while True:
        print("\n====PETVIDA====")
        print("1 - Testar conexão")
        print("2 - Listar tutores")
        print("3 - Buscar tutor")
        print("4-  Cadastrar tutor")
        print("5 - Excluir tutor")
        print("6 - Listar pets de um tutor")
        print("7 - Buscar pet com tutor")
        print("8 - Total de uma consulta")
        print("9 - Histórico de um pet")
        print("0 - Sair")

        opcao = input("\nEscolha uma opção: ")
        try:
            if opcao == "1":
                resultado = testar_conexao()
                print("\nConexão realizada com sucesso")
                print("Servidor:", resultado.servidor)
                print("Banco:", resultado.banco)
                print("Versão:", resultado.versao)

            elif opcao == "2":
                tutores = repo.listar_tutores()
                if tutores:
                    print("\nTUTORES:")
                    for tutor in tutores:
                        print(tutor)
                else:
                    print("Nenhum tutor encontrado.")

            elif opcao == "3":
                id_tutor = int(input("Digite o ID do tutor: "))
                tutor = repo.buscar_tutor(id_tutor)

                if tutor:
                    print("\nTutor encontrado:")
                    print(tutor)
                else:
                    print("Tutor não encontrado")

            elif opcao == "4":
                nome = input("Nome:")
                cpf = input("CPF(somente números): ")
                email = input("Email:")
                telefone = input("Telefone:")

                id_tutor = repo.criar_tutor(nome, cpf, email, telefone)
                print("\nTutor cadastrado com sucesso")
                print("Id do novo tutor", id_tutor)

            elif opcao == "5":
                id_tutor = int(input("Digite o ID do tutor:"))
                repo.excluir_tutor(id_tutor)
                print("Tutor excluído com sucesso")

            elif opcao == "6":
                id_tutor = int(input("Digite o id do tutor:"))
                pets = repo.listar_pets_do_tutor(id_tutor)

                if pets:
                    print("\nPETS DO TUTOR")
                    for pet in pets:
                        print(pet)
                else:
                    print("Esse tutor não possui pets")

            elif opcao == "7":
                id_pet = int(input("Digite o id do pet:"))
                pet = repo.buscar_pet_com_tutor(id_pet)

                if pet:
                    print("\nPET E TUTOR")
                    print(pet)
                else:
                    print("Pet não encontrado")

            elif opcao == "8":
                id_consulta = int(input("Digite o id da consulta:"))
                total = repo.total_da_consulta(id_consulta)
                print("\nTotal da consulta : R$", total)

            elif opcao == "9":
                id_pet = int(input("Digite o id do pet:"))
                historico = repo.historico_do_pet(id_pet)

                if historico:
                    print("\nHISTORICO DO PET")

                    for consulta in historico:
                        print("\nConsulta:", consulta.id_consulta)
                        print("Data:", consulta.data_hora)
                        print("Status:", consulta.status)
                        print("Pet:", consulta.pet)
                        print("Tutor:", consulta.tutor)
                        print("Veterinário:", consulta.veterinario)
                        print("Quantidade de itens:", consulta.qtd_itens)
                        print("Valor total: R$", consulta.valor_total)
                else:
                    print("Esse pet não possui consultas")

            elif opcao == "0":
                print("Programa encerrado")
                break

            else:
                print("Opção inválida.Tente novamente")

        except ValueError as erro:
            print("\nErro:", erro)


if __name__ == "__main__":
    main()
