# 8N8NIN0NsN0N0NoNoNINyNoNoNhN-NIN-NINONhNhN8N-Ns
# k8.y-Oh0N2IZsog.5-07861,+4%329
def decipher(ciphertext, password):
    length = int(len(password)/2)

    psw_dict = {}
    for i in range(length):
        psw_dict[password[i]] = password[length + i]

    text_list = list(ciphertext)
    result = []
    for text in text_list:
        text and result.append(psw_dict[text])


    result_str = "".join(result)
    return result_str

# decipher('8N8NIN0NsN0N0NoNoNINyNoNoNhN-NIN-NINONhNhN8N-Ns', 'k8.y-Oh0N2IZsog.5-07861,+4%329')
