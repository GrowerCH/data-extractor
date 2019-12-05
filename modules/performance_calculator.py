from modules.module import Performance


class Config:
    def __init__(self, current):
        self.unitCurrent = current
        self.flux = 1  # 0:min 1:typ 2:max
        self.vf = 1  # 0:min 1:typ 2:max
        self.fluxFactor = 100  # %
        self.unitTc = 40  # °C


# From https://www.samsung.com/etc/designs/led/global/business/calculator/engine-calculator-control/js/calc.js
def calculate_performance(module, product, current):
    config = Config(current)

    # ORG : =IF(AND($G$7>0,$E$16>0,$H$16>0,$F$17>0,$I$17>0,D20>0),IF(E20>0,(((E20-$E$11)*BC7+1)*$AZ$7*BB7)*$I$18,((($E$11-$E$11)*BC7+1)*$AZ$7*BB7)*$I$18),"")
    E20 = to_float(config.unitTc)
    E11 = to_float(module["SortingTc"])
    D20 = to_float(config.unitCurrent)
    AF7 = to_float(module["ParallelNumber"])
    # AY7 = D20/$AF$7
    AY7 = to_float(D20) / to_float(AF7)
    CT7 = to_float(product["FluxEquationTs"][0])
    CU7 = to_float(product["FluxEquationTs"][1])
    CV7 = to_float(product["FluxEquationTs"][2])
    # BC7 = $CT$7*AY7^2+$CU$7*AY7+$CV$7
    BC7 = to_float(CT7) * (to_float(AY7) * to_float(AY7)) + to_float(CU7) * to_float(AY7) + to_float(CV7)
    # AZ7 = =VLOOKUP(BK7,Database!$AB:$BT,BA7,FALSE)
    AZ7 = to_float(product["FluxValues"][config.flux])
    CQ7 = to_float(product["FluxEquationCs"][0])
    CR7 = to_float(product["FluxEquationCs"][1])
    CS7 = to_float(product["FluxEquationCs"][2])
    # BB7 =$CQ$7*AY7^2+$CR$7*AY7+$CS$7
    BB7 = to_float(CQ7) * (to_float(AY7) * to_float(AY7)) + to_float(CR7) * to_float(AY7) + to_float(CS7)
    I18 = to_float(config.fluxFactor) / to_float(100)

    # (((E20-$E$11)*BC7+1)*$AZ$7*BB7)*$I$18
    flux = (((to_float(E20) - to_float(E11)) * to_float(BC7) + to_float(1)) * to_float(AZ7) * to_float(BB7)) * to_float(
        I18)

    # ORG : =IF(AND($G$7>0,$E$16>0,$H$16>0,$F$17>0,$I$17>0,D20>0),IF(E20>0,(E20-$E$11)*BG7*AV7+$BD$7*BF7,($E$11-$E$11)*BG7+$BD$7*BF7),"")
    CZ7 = to_float(product["VoltageEquationTs"][0])
    DA7 = to_float(product["VoltageEquationTs"][1])
    DB7 = to_float(product["VoltageEquationTs"][2])
    # BG7 = $CZ$7*AY7^2+$DA$7*AY7+$DB$7
    BG7 = to_float(CZ7) * (to_float(AY7) * to_float(AY7)) + to_float(DA7) * to_float(AY7) + to_float(DB7)
    BD7 = to_float(product["VoltageValues"][config.vf])
    CW7 = to_float(product["VoltageEquationCs"][0])
    CX7 = to_float(product["VoltageEquationCs"][1])
    CY7 = to_float(product["VoltageEquationCs"][2])
    # BF7 =$CW$7*AY7^2+$CX$7*AY7+$CY$7
    BF7 = to_float(CW7) * (to_float(AY7) * to_float(AY7)) + to_float(CX7) * to_float(AY7) + to_float(CY7)
    AV7 = to_float(module["seriesNumber"])

    # (E20-$E$11)*BG7*AV7+$BD$7*BF7
    vf = (to_float(E20) - to_float(E11)) * to_float(BG7) * to_float(AV7) + to_float(BD7) * to_float(BF7)

    return Performance(current, vf, flux)


def to_float(string):
    if not string:
        string = "0"
    return float(string)
