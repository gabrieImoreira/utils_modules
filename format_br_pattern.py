def formatar_numero(numero):
    """Formata número para padrão brasileiro. Saída no padrão 1.000,00

    Args:
        numero (_type_): número de entrada

    Returns:
        str: número tratado
    """
    numero = str(numero).replace(",", ".").replace(" ", "")
    if "." in numero:
        casa_decimal_anterior = numero.split('.')[-1]
        if len(casa_decimal_anterior) == 1:
            casa_decimal = casa_decimal_anterior + "0"
        elif len(casa_decimal_anterior) == 2:
            casa_decimal = casa_decimal_anterior
        else:
            return 0
        numero = numero.replace(f".{casa_decimal_anterior}", f",{casa_decimal}")
    else:
        numero+= ",00"
    
    list_numero_tmp = numero.split(",")
    numero_tmp = list_numero_tmp[0].replace(".", "")
    numero_tmp = numero_tmp.replace(".", "")
    if len(numero_tmp) <= 3:
        return numero
    else:
        for i in range(len(numero_tmp)-3, 0, -3):
            numero_tmp = numero_tmp[:i] + "." + numero_tmp[i:]
    numero = numero_tmp + "," + list_numero_tmp[1]
    return numero

if __name__ == "__main__":
   numeros = ["10.415.69", "381.98", "968.102.124,69", "9012.1", 575.12, 575, 1000.00, 1000, 1, '1.9000,00', 1, '111112019.0129,00', 90192.09]

    for numero in numeros:
        numero_formatado = formatar_numero(numero)
        print(numero_formatado)
