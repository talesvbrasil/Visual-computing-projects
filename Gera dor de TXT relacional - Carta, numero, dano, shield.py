# estrutura da variavel carta
class Cards:
    def __init__(self, cardnumber, name, damage, shield):
        self.cardnumber = cardnumber
        self.name = name
        # self.energy = energy
        self.damage = damage
        self.shield = shield
        # self.effect = effect
        # self.cardimagedirectory = cardimagedirectory


Cartas = []

for i in range(0, 132):
    Nome = input("Enter a name for card number {}: ".format(i))
    Cartas.append(Cards(i, Nome, 0, 0))


for cartinhas in Cartas:
    print("Carta numero:{} Nome:{}".format(cartinhas.cardnumber, cartinhas.name))
    Cartas.damage = input("Digite o Damage desta carta: ".format(i))
    Cartas.shield = input("Digite o Shield desta carta: ".format(i))


textfile = open("relacaocardnumb.txt", "w")
for element in Cartas:
    textfile.write(
        str(element.cardnumber)
        + " - "
        + str(element.name)
        + " - "
        + str(element.damage)
        + " - "
        + str(element.shield)
        + "\n"
    )


textfile.close()
