labels = ["Bank account", "Trading", "Invested"]

data = ["value", "last", "rate", "incoming"]

tot_dict = dict()

for label in labels:
    tot_dict[label] = dict()
    for val in data:
        tot_dict[label][val] = 0 if val != "rate" else 1

salary = int(input("Salary:\n"))

cost = int(input("Cost of life:\n"))

tot_dict["Trading"]["rate"] = (1+float(input("Yearly trading performances:\n"))/100)**(1/12)

tot_dict["Invested"]["rate"] = (1+float(input("Yearly investing performances:\n"))/100)**(1/12)

invest = int(input("Monthly invested amount:\n"))

inv_trad = int(input("% of invested money in trading:\n"))/100

with_rate = int(input("Withdrawal rate:\n"))/100

print()

tot_dict["Bank account"]["incoming"] = salary - invest - cost
tot_dict["Trading"]["incoming"] = inv_trad * invest
tot_dict["Invested"]["incoming"] = (1 - inv_trad) * invest

tot_dict["Bank account"]["value"] = float(input("Initial bank account capital:\n"))
tot_dict["Trading"]["value"] = float(input("Initial trading capital:\n"))
tot_dict["Invested"]["value"] = float(input("Initial invested capital:\n"))

tot_dict["Bank account"]["last"] = tot_dict["Bank account"]["value"]
tot_dict["Trading"]["last"] = tot_dict["Trading"]["value"]
tot_dict["Invested"]["last"] = tot_dict["Invested"]["value"]

def tot_net():
    sum = 0
    for key in labels:
        sum += tot_dict[key]["value"]
    return sum

print()
last = tot_net()
tot = last
invested_money = tot_dict[labels[1]][data[0]]+tot_dict[labels[2]][data[0]]
taxes = 0
ans = ""

i = 0

while ans != "stop":
    for key in labels:
        tot_dict[key]["value"] += tot_dict[key]["incoming"]
    invested_money += invest

    tot = tot_net()

    print(f"{i // 12} years " if i >= 12 else "", end='')
    print(
        f"{i % 12} months - Total networth: {int(tot)}$ (+{int(tot - last)}$)\n")

    for key in labels:
        cur = tot_dict[key]
        print(f"- {key}: {int(cur[data[0]])}$ (+{int(cur[data[0]] - cur[data[1]])}$)")

    print(f"- Total invested money: {int(tot_dict[labels[1]][data[0]]+tot_dict[labels[2]][data[0]])}$ ({int(invested_money)}$+{int(tot - invested_money - tot_dict[labels[0]][data[0]])}$) --> +{int((tot - invested_money - tot_dict[labels[0]][data[0]]) / invested_money * 100)}%")

    last = tot

    for key in labels:
        cur = tot_dict[key]
        cur["last"] = cur["value"]
        cur["value"] *= cur["rate"]

    trad_prof = tot_dict["Trading"]["value"] - tot_dict["Trading"]["last"]
    inv_prof = tot_dict["Invested"]["value"] - tot_dict["Invested"]["last"]

    tot_dict["Bank account"]["value"] += (trad_prof + inv_prof) * with_rate * 0.7

    tot_dict["Trading"]["value"] -= trad_prof * with_rate
    tot_dict["Invested"]["value"] -= inv_prof * with_rate

    if with_rate != 0:
        taxes += 0.3 * with_rate * (trad_prof + inv_prof)
        print(f"Withdrawal of {int(inv_prof * with_rate * 0.7)}$ from investing account and {int(trad_prof * with_rate * 0.7)}$ from trading account. ({(trad_prof+inv_prof)*with_rate*0.7}$)\n")
    print(f"Total taxes: {int(taxes)}$")

    i += 1

    ans = input()

    while ans != "" and ans != "stop":


        if ans[:8] == "withdraw":
            if "on" in ans:
                ans = input("Percent of profits to withdraw:\n")
                with_rate = int(ans)/100
            elif "off" in ans:
                with_rate = 0
            print()

        elif ans == "transfer":
            sender = input("From:\n")
            receiver = input("To:\n")
            quantity = int(input("Quantity:\n"))

            if sender in labels and sender in labels:
                if tot_dict[sender]["value"] >= quantity:
                    tot_dict[sender]["value"] -= quantity
                    if sender != "Bank account":
                        tot_dict[receiver]["value"] += 0.7 * quantity
                        invested_money -= quantity
                        taxes += quantity * 0.3
                        print(f"Money sent\n{sender} ({int(tot_dict[sender][data[0]])}$) --(+{int(quantity*0.7)}$)--> {receiver} ({int(tot_dict[receiver][data[0]])}$)\nTaxes: {int(quantity*0.3)}$")
                    else:
                        tot_dict[receiver]["value"] += quantity
                        invested_money += quantity
                        print(f"Money sent\n{sender} ({int(tot_dict[sender][data[0]])}$) --(+{int(quantity)}$)--> {receiver} ({int(tot_dict[receiver][data[0]])}$)")
                else:
                    print(f"Not enough money ({tot_dict[sender][data[0]]}")

        else:
            print("Usage:\n -Enter: Next month\n -withdraw on/off: Automatically withdraw part of profits\n -transfer: transfer money between accounts (taxes when moving to bank account)")

        ans = input()
