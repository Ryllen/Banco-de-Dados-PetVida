import pyodbc
from db import transacao


def criar_tutor(nome, cpf, email=None, telefone=None):
    if len(cpf) != 11 or not cpf.isdigit():
        raise ValueError("CPF deve possuir 11 números")

    try:
        with transacao() as cursor:
            cursor.execute(
                """
                INSERT INTO dbo.tutor (nome, cpf, email, telefone)
                OUTPUT INSERTED.id_tutor
                VALUES (?, ?, ?, ?)
            """,
                nome,
                cpf,
                email,
                telefone,
            )
            return cursor.fetchone()[0]
    except pyodbc.IntegrityError:
        raise ValueError("CPF já cadastrado ou inválido")


def buscar_tutor(id_tutor):
    with transacao() as cursor:
        cursor.execute(
            """
            SELECT *
            FROM dbo.tutor
            WHERE id_tutor = ?
        """,
            id_tutor,
        )
        return cursor.fetchone()


def listar_tutores(filtro_nome=None):
    with transacao() as cursor:
        if filtro_nome:
            cursor.execute(
                """
                SELECT *
                FROM dbo.tutor
                WHERE nome LIKE ?
                ORDER BY nome
            """,
                "%" + filtro_nome + "%",
            )

        else:
            cursor.execute("""
                SELECT *
                FROM dbo.tutor
                ORDER BY nome
            """)

        return cursor.fetchall()


def atualizar_tutor(id_tutor, **campos):

    campos_permitidos = ["nome", "email", "telefone"]

    if not campos:
        raise ValueError("Nenhum campo informado")

    for campo in campos:
        if campo not in campos_permitidos:
            raise ValueError("Campo não permitido: " + campo)

    partes = []
    valores = []

    for campo, valor in campos.items():
        partes.append(f"{campo} = ?")
        valores.append(valor)

    valores.append(id_tutor)

    sql = f"""
        UPDATE dbo.tutor
        SET {", ".join(partes)}
        WHERE id_tutor = ?
    """

    with transacao() as cursor:
        cursor.execute(sql, *valores)

        if cursor.rowcount == 0:
            raise ValueError("Tutor não encontrado")


def excluir_tutor(id_tutor):

    try:
        with transacao() as cursor:

            cursor.execute(
                """
                DELETE FROM dbo.tutor
                WHERE id_tutor = ?
            """,
                id_tutor,
            )

            if cursor.rowcount == 0:
                raise ValueError("Tutor não encontrado")

    except pyodbc.IntegrityError:
        raise ValueError("Não é possível excluir um tutor que possui pets")


def criar_pet(id_tutor, nome, especie, raca=None, data_nascimento=None, peso_kg=None):

    try:
        with transacao() as cursor:

            cursor.execute(
                """
                INSERT INTO dbo.pet
                (
                    id_tutor,
                    nome,
                    especie,
                    raca,
                    data_nascimento,
                    peso_kg
                )
                OUTPUT INSERTED.id_pet
                VALUES (?, ?, ?, ?, ?, ?)
            """,
                id_tutor,
                nome,
                especie,
                raca,
                data_nascimento,
                peso_kg,
            )

            return cursor.fetchone()[0]

    except pyodbc.IntegrityError:
        raise ValueError("Não foi possível cadastrar o pet")


def atualizar_peso_pet(id_pet, peso_kg):

    try:
        with transacao() as cursor:

            cursor.execute(
                """
                UPDATE dbo.pet
                SET peso_kg = ?
                WHERE id_pet = ?
            """,
                peso_kg,
                id_pet,
            )

            if cursor.rowcount == 0:
                raise ValueError("Pet não encontrado")

    except pyodbc.IntegrityError:
        raise ValueError("Peso inválido")


def transferir_pet(id_pet, novo_id_tutor):

    try:
        with transacao() as cursor:

            cursor.execute(
                """
                UPDATE dbo.pet
                SET id_tutor = ?
                WHERE id_pet = ?
            """,
                novo_id_tutor,
                id_pet,
            )

            if cursor.rowcount == 0:
                raise ValueError("Pet não encontrado")

    except pyodbc.IntegrityError:
        raise ValueError("Tutor de destino inválido")


def excluir_pet(id_pet):

    try:
        with transacao() as cursor:

            cursor.execute(
                """
                DELETE FROM dbo.pet
                WHERE id_pet = ?
            """,
                id_pet,
            )

            if cursor.rowcount == 0:
                raise ValueError("Pet não encontrado")

    except pyodbc.IntegrityError:
        raise ValueError("Não é possível excluir um pet que possui consultas")


def listar_pets_do_tutor(id_tutor):

    with transacao() as cursor:

        cursor.execute(
            """
            SELECT *
            FROM dbo.pet
            WHERE id_tutor = ?
            ORDER BY nome
        """,
            id_tutor,
        )

        return cursor.fetchall()


def buscar_pet_com_tutor(id_pet):

    with transacao() as cursor:

        cursor.execute(
            """
            SELECT
                p.*,
                t.nome AS nome_tutor,
                t.cpf AS cpf_tutor
            FROM dbo.pet p
            INNER JOIN dbo.tutor t
                ON p.id_tutor = t.id_tutor
            WHERE p.id_pet = ?
        """,
            id_pet,
        )

        return cursor.fetchone()


def agendar_consulta(id_pet, id_vet, data_hora, motivo, procedimentos):

    try:
        with transacao() as cursor:

            cursor.execute(
                """
                INSERT INTO dbo.consulta
                (
                    id_pet,
                    id_veterinario,
                    data_hora,
                    motivo
                )
                OUTPUT INSERTED.id_consulta
                VALUES (?, ?, ?, ?)
            """,
                id_pet,
                id_vet,
                data_hora,
                motivo,
            )

            id_consulta = cursor.fetchone()[0]

            for id_procedimento, quantidade in procedimentos:

                cursor.execute(
                    """
                    SELECT preco_base
                    FROM dbo.procedimento
                    WHERE id_procedimento = ?
                """,
                    id_procedimento,
                )

                procedimento = cursor.fetchone()

                if procedimento is None:
                    raise ValueError("Procedimento não encontrado")

                cursor.execute(
                    """
                    INSERT INTO dbo.consulta_procedimento
                    (
                        id_consulta,
                        id_procedimento,
                        quantidade,
                        valor_cobrado
                    )
                    VALUES (?, ?, ?, ?)
                """,
                    id_consulta,
                    id_procedimento,
                    quantidade,
                    procedimento.preco_base,
                )

            return id_consulta

    except pyodbc.IntegrityError:
        raise ValueError("Não foi possível agendar a consulta")


def adicionar_procedimento(id_consulta, id_procedimento, quantidade=1):

    try:
        with transacao() as cursor:

            cursor.execute(
                """
                SELECT status
                FROM dbo.consulta
                WHERE id_consulta = ?
            """,
                id_consulta,
            )

            consulta = cursor.fetchone()

            if consulta is None:
                raise ValueError("Consulta não encontrada")

            if consulta.status == "CANCELADA":
                raise ValueError("Consulta cancelada não pode ser alterada")

            cursor.execute(
                """
                SELECT preco_base
                FROM dbo.procedimento
                WHERE id_procedimento = ?
            """,
                id_procedimento,
            )

            procedimento = cursor.fetchone()

            if procedimento is None:
                raise ValueError("Procedimento não encontrado")

            cursor.execute(
                """
                INSERT INTO dbo.consulta_procedimento
                (
                    id_consulta,
                    id_procedimento,
                    quantidade,
                    valor_cobrado
                )
                VALUES (?, ?, ?, ?)
            """,
                id_consulta,
                id_procedimento,
                quantidade,
                procedimento.preco_base,
            )

    except pyodbc.IntegrityError:
        raise ValueError("Procedimento repetido ou quantidade inválida")


def remover_procedimento(id_consulta, id_procedimento):

    with transacao() as cursor:

        cursor.execute(
            """
            SELECT status
            FROM dbo.consulta
            WHERE id_consulta = ?
        """,
            id_consulta,
        )

        consulta = cursor.fetchone()

        if consulta is None:
            raise ValueError("Consulta não encontrada")

        if consulta.status == "CANCELADA":
            raise ValueError("Consulta cancelada não pode ser alterada")

        cursor.execute(
            """
            DELETE FROM dbo.consulta_procedimento
            WHERE id_consulta = ?
            AND id_procedimento = ?
        """,
            id_consulta,
            id_procedimento,
        )

        if cursor.rowcount == 0:
            raise ValueError("Procedimento não encontrado na consulta")


def listar_procedimentos_da_consulta(id_consulta):

    with transacao() as cursor:

        cursor.execute(
            """
            SELECT
                p.id_procedimento,
                p.descricao,
                cp.quantidade,
                cp.valor_cobrado
            FROM dbo.consulta_procedimento cp
            INNER JOIN dbo.procedimento p
                ON cp.id_procedimento =
                   p.id_procedimento
            WHERE cp.id_consulta = ?
        """,
            id_consulta,
        )

        return cursor.fetchall()


def listar_consultas_por_procedimento(id_procedimento):

    with transacao() as cursor:

        cursor.execute(
            """
            SELECT
                c.id_consulta,
                c.data_hora,
                c.status,
                c.motivo
            FROM dbo.consulta_procedimento cp
            INNER JOIN dbo.consulta c
                ON cp.id_consulta =
                   c.id_consulta
            WHERE cp.id_procedimento = ?
            ORDER BY c.data_hora
        """,
            id_procedimento,
        )

        return cursor.fetchall()


def total_da_consulta(id_consulta):

    with transacao() as cursor:

        cursor.execute(
            """
            SELECT
                COALESCE(
                    SUM(
                        quantidade * valor_cobrado
                    ),
                    0
                ) AS total
            FROM dbo.consulta_procedimento
            WHERE id_consulta = ?
        """,
            id_consulta,
        )

        return cursor.fetchone().total


def atualizar_status_consulta(id_consulta, novo_status):

    status_permitidos = ["AGENDADA", "REALIZADA", "CANCELADA"]

    if novo_status not in status_permitidos:
        raise ValueError("Status inválido")

    with transacao() as cursor:

        cursor.execute(
            """
            UPDATE dbo.consulta
            SET status = ?
            WHERE id_consulta = ?
        """,
            novo_status,
            id_consulta,
        )

        if cursor.rowcount == 0:
            raise ValueError("Consulta não encontrada")


def excluir_consulta(id_consulta):

    with transacao() as cursor:

        cursor.execute(
            """
            DELETE FROM dbo.consulta
            WHERE id_consulta = ?
        """,
            id_consulta,
        )

        if cursor.rowcount == 0:
            raise ValueError("Consulta não encontrada")


def historico_do_pet(id_pet):

    with transacao() as cursor:

        cursor.execute(
            """
            SELECT
                v.id_consulta,
                v.data_hora,
                v.status,
                v.pet,
                v.tutor,
                v.veterinario,
                v.qtd_itens,
                v.valor_total
            FROM dbo.vw_resumo_consulta v
            INNER JOIN dbo.consulta c
                ON c.id_consulta = v.id_consulta
            WHERE c.id_pet = ?
            ORDER BY v.data_hora DESC
        """,
            id_pet,
        )

        return cursor.fetchall()
