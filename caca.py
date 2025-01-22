argent = 167

investi = argent

def argent_investi(cash):
    cash /= 10
    temp = round(cash)
    if temp % 5:
        temp += (5 - temp) % 5
    
    return temp

for i in range(int(12 * 2.5)):
    ajout = min(argent_investi(argent), 50)
    argent += ajout
    investi += ajout

    if i > 8 and i < 14:
        argent += 750
        investi += 750

    if i % 12 == 5:
        argent += 750
        investi += 750

    argent *= 1.03


print(argent)
print(investi)
