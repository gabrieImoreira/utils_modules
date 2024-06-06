# 26/05/2024 AFL Semanal ['TER,', 'SEX']
import datetime, traceback, calendar
from workalendar.america import BrazilSaoPauloCity
from datetime import timedelta


def obter_dia_util_baseado_na_semana_e_dia(data_base_dt: datetime, semana: int, dia_semana: str, ultimo_dia_mes: int) -> str:
    """
    Retorna a data correspondente ao dia da semana específico na semana dada, a partir de uma data base.
    Se a data for um feriado, retorna o próximo dia útil. Exemplo de entrada: 3 QUA -> 3ª quarta-feira do mês., essa função calcula isso

    :param data_base: Data base no formato 'dd/mm/yyyy'
    :param semana: Número da semana (1 a 4)
    :param dia_semana: Dia da semana ('SEG', 'TER', 'QUA', 'QUI', 'SEX')
    :return: Data no formato 'dd/mm/yyyy'
    """
    # Mapear os dias da semana para números
    dias_semana = {'SEG': 0, 'TER': 1, 'QUA': 2, 'QUI': 3, 'SEX': 4}

    # Verificar se os parâmetros são válidos
    if semana < 1 or semana > 4:
        raise ValueError("Número da semana deve ser entre 1 e 4")
    if dia_semana not in dias_semana:
        raise ValueError("Dia da semana deve ser um de 'SEG', 'TER', 'QUA', 'QUI', 'SEX'")

    cal = BrazilSaoPauloCity()
    for i in range(2):
        # Calcular o primeiro dia da semana base
        list_days = []
        primeiro_dia_mes = data_base_dt.replace(day=1)
        for day in range(ultimo_dia_mes):
            if primeiro_dia_mes.weekday() == dias_semana[dia_semana]:
                list_days.append(primeiro_dia_mes)
            primeiro_dia_mes += timedelta(days=1)

        contador = 1
        dia_desejado = list_days[semana - 1]
        if not cal.is_working_day(dia_desejado):
            dia_desejado = cal.add_working_days(dia_desejado, 1)       
        # Verificar se a data desejada é menor ou igual à data base, se não for, avançar para o próximo mês
        if datetime.datetime.combine(dia_desejado, datetime.datetime.min.time()) > data_base_dt: #datetime.datetime.combine(data_base_dt, datetime.datetime.min.time()):
            break
        else:
            data_base_dt = data_base_dt.replace(day=1) + timedelta(days=31)
            data_base_dt = data_base_dt.replace(day=1)
            # break
    if isinstance(dia_desejado, datetime.date) and not isinstance(dia_desejado, datetime.datetime):
        dia_desejado = datetime.datetime.combine(dia_desejado, datetime.datetime.min.time())    
    return dia_desejado


def obter_dia_util(month: int, year: int, work_day: int):
    """
    Função que retorna o dia útil de acordo com o mês e ano informado

    :param mes: Mês
    :param ano: Ano
    :param dia_util: Dia útil
    :return: Dia útil
    """
    # Criar uma instância do calendário do Brasil
    cal = BrazilSaoPauloCity()
    start_date = datetime.date(year, month, 1)

    working_day_count = 0
    current_date = start_date

    while working_day_count < work_day:
        if cal.is_working_day(current_date):
            working_day_count += 1
        current_date += timedelta(days=1)

    # O loop adiciona um dia a mais, então subtrai um dia do resultado final
    date_work_day = current_date - timedelta(days=1)
    return date_work_day

class Frequencia:
    def __init__(self, sigla, frequencia, data):
        self.sigla = sigla
        self.frequencia = frequencia
        self.data = data

def obter_condicao_pagamento(sigla,data):
    """
    Função que retorna a condição de pagamento de acordo com a sigla e data informada
    :param sigla: Sigla
    :param data: Data
    :return: Condição de pagamento
    """
    try:
        de_para_dias = {
            'SEG': 0,
            'TER': 1,
            'QUA': 2,
            'QUI': 3,
            'SEX': 4,
            'SAB': 5,
            'DOM': 6
        }
        data_obj = datetime.datetime.strptime(data, "%d/%m/%Y")
        # retorno_frequencia = conciliation_bd.recuperar_frequencia_pagamento(sigla)
        retorno_frequencia = (True, Frequencia('AFL', 'Mensal', [10, 'DU']))

        if retorno_frequencia[0] == True:
            obj_frequencia = retorno_frequencia[1]

            if obj_frequencia.frequencia == "Semanal":
                # alterando dias da semana para número
                dias_numericos = [de_para_dias[dia] for dia in obj_frequencia.data]
                dias_numericos.sort()
                
                # obtendo dia da semana
                dia_obtido = data_obj.weekday()
                # obtendo dia do pagamento
                for dia_pagamento in dias_numericos:
                    if dia_pagamento > dia_obtido:
                        dia_result = dia_pagamento - dia_obtido
                        break
                else:
                    dia_result = 7 - dia_obtido + dias_numericos[0]
                
                return str(dia_result) + " DD"

            elif obj_frequencia.frequencia == "Quinzenal":
                # Ajustando dia final do mês, se o dia for 30 ou 31, para o último dia do mês
                for i, value in enumerate(obj_frequencia.data):
                    if value == 31 or value == 30:
                       obj_frequencia.data[i] = calendar.monthrange(data_obj.year, data_obj.month)[1]

                dia_obtido = data_obj.day
                dias_numericos = obj_frequencia.data
                dias_numericos.sort()

                for dia_pagamento in dias_numericos:
                    if dia_pagamento > dia_obtido:
                        # if dia_pagamento == obj_frequencia.data[-1]:
                        #     print('entrou', dia_pagamento)
                        dia_result = dia_pagamento - dia_obtido
                        break
                
                return str(dia_result) + " DD"

            elif obj_frequencia.frequencia == "Mensal":
                # Se a data de pagamento for um dia específico do mês
                if len(obj_frequencia.data) == 1:
                    # obtendo último dia do mês
                    ultimo_dia_mes = calendar.monthrange(data_obj.year, data_obj.month)[1]

                    dia_pagamento = obj_frequencia.data[0]
                    if dia_pagamento > data_obj.day:
                        dia_result = abs(dia_pagamento - data_obj.day)
                        return str(dia_result) + " DD"
                    elif dia_pagamento == data_obj.day:
                        return str(ultimo_dia_mes) + " DD"
                    else:
                        # Calcular o próximo dia de pagamento no próximo mês
                        proximo_mes = data_obj.month + 1 if data_obj.month < 12 else 1
                        proximo_ano = data_obj.year if data_obj.month < 12 else data_obj.year + 1
                        ultimo_dia_proximo_mes = calendar.monthrange(proximo_ano, proximo_mes)[1]
                        
                        if dia_pagamento > ultimo_dia_proximo_mes:
                            dia_pagamento = ultimo_dia_proximo_mes
                        
                        proxima_data_pagamento = datetime.date(proximo_ano, proximo_mes, dia_pagamento)
                        dia_result = (proxima_data_pagamento - data_obj.date()).days
                        return str(dia_result) + " DD"
                elif len(obj_frequencia.data) == 2 and obj_frequencia.data[1] == "DU":
                    # obtendo dia útil do mês
                    dia_pagamento = obter_dia_util(data_obj.month, data_obj.year, obj_frequencia.data[0]).day

                    # obtendo último dia do mês
                    ultimo_dia_mes = calendar.monthrange(data_obj.year, data_obj.month)[1]
                    
                    if dia_pagamento > data_obj.day:
                        dia_result = abs(dia_pagamento - data_obj.day)
                        return str(dia_result) + " DD"
                    else:
                        # Calcular o próximo dia útil no próximo mês
                        proximo_mes = data_obj.month + 1 if data_obj.month < 12 else 1
                        proximo_ano = data_obj.year if data_obj.month < 12 else data_obj.year + 1
                        proximo_dia_util = obter_dia_util(proximo_mes, proximo_ano, obj_frequencia.data[0])
                        dia_result = proximo_dia_util.day + ultimo_dia_mes - data_obj.day
                    
                        return str(dia_result) + " DD"
                elif len(obj_frequencia.data) == 2 and obj_frequencia.data[1] in ['SEG', 'TER', 'QUA', 'QUI', 'SEX']:
                    
                    # obtendo último dia do mês
                    ultimo_dia_mes = calendar.monthrange(data_obj.year, data_obj.month)[1]

                    # Essa função retorna o próximo dia útil baseado na semana e dia da semana, por exemplo: 3 QUA -> 3ª quarta-feira do mês
                    # Se a data for um feriado, retorna o próximo dia útil
                    # Se a data requerida já tiver passado, retorna a próxima data requerida do próximo mês
                    dia_pagamento = obter_dia_util_baseado_na_semana_e_dia(data_obj, obj_frequencia.data[0], obj_frequencia.data[1], ultimo_dia_mes)
                    dia_result = abs(dia_pagamento - data_obj)
                    return str(dia_result.days) + " DD"
            return None
        else:
            return None
    except:
        print(traceback.format_exc())
        return None


# desenvolver para pegar 1 quarta util do mes
print('21/04/2024', obter_condicao_pagamento('AFL','21/04/2024'))
print('\n\n')
print('21/11/2024', obter_condicao_pagamento('AFL','21/11/2024'))
print('\n\n')
print('03/06/2024', obter_condicao_pagamento('AFL','03/06/2024'))
print('\n\n')
print('04/07/2024', obter_condicao_pagamento('AFL','24/07/2024'))
print('\n\n')

print('05/07/2024', obter_condicao_pagamento('AFL','05/07/2024'))
print('\n\n')
print('06/08/2024', obter_condicao_pagamento('AFL','06/08/2024'))
print('\n\n')
print('14/09/2024', obter_condicao_pagamento('AFL','14/09/2024'))
