from datetime import datetime, timedelta
from pickle import dump
from random import randrange
from secrets import choice, randbelow

import demo
from src.calc.log import Deposit, Payout, TradeOpen, TradeFinalized, Dividend, Itc
from src.config import rc

example_assets = {
    'TechNova Solutions': ["TechNova Solutions", "Technology", "TNVS", 0.0],
    'GlobalTech Innovations': ["GlobalTech Innovations", "Technology", "GLTCH", 0.0],
    'NebulaElectronics Corporation': ["NebulaElectronics Corporation", "Technology", "NELEC", 0.0],
    'VirtuoNet Ventures': ["VirtuoNet Ventures", "Technology", "VNET", 0.0],
    'Luminary Systems International': ["Luminary Systems International", "Technology", "LUMSY", 0.0],
    'Axis Automation Group': ["Axis Automation Group", "Technology", "AXAUT", 0.0],
    'QuantumCore Enterprises': ["QuantumCore Enterprises", "Technology Intelligence", "QNTCR", 0.0],
    'TerraRenew Corporation': ["TerraRenew Corporation", "Technology Energy", "TERRE", 0.0],
    'ApexStream Holdings': ["ApexStream Holdings", "Technology", "APEX", 0.0],
    'SynergySolutions Inc.': ["SynergySolutions Inc.", "Technology Integration", "SYNSOL", 0.0],
    'Horizon Ventures Inc.': ["Horizon Ventures Inc.", "Finance Capital", "HORIZON", 0.0],
    'Nexus Dynamics Group': ["Nexus Dynamics Group", "Finance Management", "NXDYN", 0.0],
    'Infinity Financial Solutions': ["Infinity Financial Solutions", "Finance", "INFIN", 0.0],
    'StellarSpark Industries': ["StellarSpark Industries", "Finance Banking", "STSPK", 0.0],
    'FusionTech Capital': ["FusionTech Capital", "Finance", "FUSION", 0.0],
    'Aurora Global Ventures': ["Aurora Global Ventures", "Finance Equity", "AURORA", 0.0],
    'EvolveSphere Capital': ["EvolveSphere Capital", "Finance Management", "EVOLVE", 0.0],
    'OmniWave Financials': ["OmniWave Financials", "Finance Processing", "OMWAV", 0.0],
    'Ecliptic Systems International': ["Ecliptic Systems International", "Finance", "ECLIPT", 0.0],
    'Vanguard Nexus Group': ["Vanguard Nexus Group", "Finance Funds", "VNGRD", 0.0],
    'Questify Pharmaceuticals': ["Questify Pharmaceuticals", "Healthcare", "QPHAR", 0.0],
    'MedTech Innovations': ["MedTech Innovations", "Healthcare Devices", "MEDIN", 0.0],
    'AlphaBio Corporation': ["AlphaBio Corporation", "Healthcare", "ALBIO", 0.0],
    'FutureCare Solutions': ["FutureCare Solutions", "Healthcare Informatics", "FUTCR", 0.0],
    'Celestial Health Ventures': ["Celestial Health Ventures", "Healthcare", "CELEH", 0.0],
    'QuantumGenomics Inc.': ["QuantumGenomics Inc.", "Healthcare", "QGEN", 0.0],
    'InsightHealth Analytics': ["InsightHealth Analytics", "Healthcare Analytics", "INSHL", 0.0],
    'MedRobot Dynamics Inc.': ["MedRobot Dynamics Inc.", "Healthcare Robotics", "MDRBT", 0.0],
    'Empyrean Health Solutions': ["Empyrean Health Solutions", "Healthcare Management", "EMPYR", 0.0],
    'Transcend Wellness Holdings': ["Transcend Wellness Holdings", "Healthcare", "TRANWELL", 0.0],
    'ElysianTech Retail': ["ElysianTech Retail", "E-Commerce", "ELYTECH", 0.0],
    'Genesis Luxury Ventures': ["Genesis Luxury Ventures", "Retail Goods", "GENLV", 0.0],
    'InnovateMart Group': ["InnovateMart Group", "Retail", "INNOVM", 0.0],
    'ZenithWorks International': ["ZenithWorks International", "Retail Development", "ZENWRK", 0.0],
    'PrimeLogistics Holdings': ["PrimeLogistics Holdings", "Retail", "PRIMLG", 0.0],
    'SynergyMarket Enterprises': ["SynergyMarket Enterprises", "Retail Research", "SYNMKT", 0.0],
    'ApexZenith Retail': ["ApexZenith Retail", "Retail Experience", "APXZEN", 0.0],
    'QuantumQuest Ventures': ["QuantumQuest Ventures", "Retail Marketing", "QMQUEST", 0.0],
    'NebulaForge Solutions': ["NebulaForge Solutions", "Retail Chain", "NEBFOR", 0.0],
    'VirtuosoTech Retail': ["VirtuosoTech Retail", "Retail", "VIRTCH", 0.0],
    'Luminex Motors Corporation': ["Luminex Motors Corporation", "Automotive Vehicles", "LUMX", 0.0],
    'HorizonForge Automotive': ["HorizonForge Automotive", "Automotive", "HORIZFRG", 0.0],
    'NexusDrive Innovations': ["NexusDrive Innovations", "Automotive Vehicles", "NXDRV", 0.0],
    'InfinityDrive Corporation': ["InfinityDrive Corporation", "Automotive Systems", "INFD", 0.0],
    'StellarDrive Ventures': ["StellarDrive Ventures", "Automotive Technology", "STDRV", 0.0],
    'FusionMotor Group': ["FusionMotor Group", "Automotive Cells", "FUSMOT", 0.0],
    'AuroraTech Automotive': ["AuroraTech Automotive", "Automotive Design", "AUTOTECH", 0.0],
    'EvolveSphere Mobility': ["EvolveSphere Mobility", "Automotive", "EVOLMOB", 0.0],
    'OmniNova Auto': ["OmniNova Auto", "Mobility Automotive", "OMNVA", 0.0],
    'EclipticPulse Automotive': ["EclipticPulse Automotive", "Automotive", "ECLIPAUTO", 0.0],
    'VanguardForge EdTech': ["VanguardForge EdTech", "E-Learning", "VNGDFG", 0.0],
    'QuestTech Education': ["QuestTech Education", "Education", "QSTTECH", 0.0],
    'ExcaliburSphere Learning': ["ExcaliburSphere Learning", "Education Platforms", "EXCSPL", 0.0],
    'AlphaNova Ed': ["AlphaNova Ed", "Education Education", "ALNOVA", 0.0],
    'FutureSphere EduTech': ["FutureSphere EduTech", "Education Tutoring", "FUTEDU", 0.0],
    'CelestialWorks EdTech': ["CelestialWorks EdTech", "AI in Education", "CELEDU", 0.0],
    'QuantumSphere Ed Ventures': ["QuantumSphere Ed Ventures", "Education", "QNTMED", 0.0],
    'InsightTech Ed Group': ["InsightTech Ed Group", "Education Analytics for Schools", "INSTED", 0.0],
    'EndeavorForge Ed Innovations': ["EndeavorForge Ed Innovations", "Education Support", "ENDGFI", 0.0],
    'EmpyreanPulse Education': ["EmpyreanPulse Education", "VR in Education", "EMPYEDU", 0.0],
    'SolarNova Solutions': ["SolarNova Solutions", "Energy", "SOLRNOV", 0.0],
    'WindTech Ventures': ["WindTech Ventures", "Energy", "WNDTECH", 0.0],
    'HydroGen Corporation': ["HydroGen Corporation", "Energy Power", "HYDROG", 0.0],
    'BioFuel Innovations': ["BioFuel Innovations", "Energy", "BIOFUEL", 0.0],
    'Geothermal Dynamics Inc.': ["Geothermal Dynamics Inc.", "Energy", "GEOEN", 0.0],
    'TidalWave Energy Group': ["TidalWave Energy Group", "Energy", "TIDALE", 0.0],
    'FusionSolar Holdings': ["FusionSolar Holdings", "Energy", "FUSOLS", 0.0],
    'CleanTech Solutions': ["CleanTech Solutions", "Technology", "CLEANT", 0.0],
    'RenewablePower Corp.': ["RenewablePower Corp.", "Power", "RENPW", 0.0],
    'ECOnergy Ventures': ["ECOnergy Ventures", "Eco-friendly Energy", "ECOENGY", 0.0],
    'AeroNova Technologies': ["AeroNova Technologies", "Aerospace", "AERONOV", 0.0],
    'SpaceTech Innovations': ["SpaceTech Innovations", "Aerospace", "SPTIN", 0.0],
    'AeroDynamics Corporation': ["AeroDynamics Corporation", "Aerospace", "AERODYN", 0.0],
    'AstroTech Ventures': ["AstroTech Ventures", "Aerospace", "ASTROV", 0.0],
    'OrbitalWorks International': ["OrbitalWorks International", "Aerospace", "ORBWORKS", 0.0],
    'RocketForge Solutions': ["RocketForge Solutions", "Aerospace", "RCKTFOR", 0.0],
    'Lunar Dynamics Group': ["Lunar Dynamics Group", "Aerospace", " LUNDYN", 0.0],
    'StellarFlight Enterprises': ["StellarFlight Enterprises", "Aerospace", "STFLIGHT", 0.0],
    'CosmoTech Innovations': ["CosmoTech Innovations", "Aerospace", "COSMOTEC", 0.0],
    'NebulaSpace Corporation': ["NebulaSpace Corporation", "Aerospace", "NEBUSPAC", 0.0],
    'Starlight Productions': ["Starlight Productions", "Entertainment", "STARPRO", 0.0],
    'MusicNova Entertainment': ["MusicNova Entertainment", "Entertainment", "MUSICNOV", 0.0],
    'GameTech Studios': ["GameTech Studios", "Entertainment", "GAMETEC", 0.0],
    'VirtualWorld Ventures': ["VirtualWorld Ventures", "Virtual Reality", "VRWORLD", 0.0],
    'ComicSphere Enterprises': ["ComicSphere Enterprises", "Entertainment", "COMSPH", 0.0],
    'StageCraft Innovations': ["StageCraft Innovations", "Entertainment", "STGCRFT", 0.0],
    'SportsEdge Holdings': ["SportsEdge Holdings", "Entertainment", "SPORTED", 0.0],
    'MediaFusion Corporation': ["MediaFusion Corporation", "Entertainment", "MDFUSN", 0.0],
    'ArtTech Creations': ["ArtTech Creations", "Entertainment", "ARTTECH", 0.0],
    'NoveltyWorks International': ["NoveltyWorks International", "Novelty Items", "NOVELTYW", 0.0],
    'DreamScape Resorts': ["DreamScape Resorts", "Hospitality", "DRMSRC", 0.0],
    'StellarStay Hotels': ["StellarStay Hotels", "Hospitality", "STYHOT", 0.0],
    'FoodFusion Hospitality': ["FoodFusion Hospitality", "Hospitality", "FDFUSN", 0.0],
    'AdventureWorks Travel': ["AdventureWorks Travel", "Travel Agencies", "ADVTRVL", 0.0],
    'Blissful Retreats': ["Blissful Retreats", "Hospitality", "BLISSRT", 0.0],
    'EventElevate Enterprises': ["EventElevate Enterprises", "Event Planning", "EVTELEV", 0.0],
    'SerenityStay Inns': ["SerenityStay Inns", "Hospitality", "SRNSTAY", 0.0],
    'ExoticEscape Travel Group': ["ExoticEscape Travel Group", "Luxury Travel", "EXTESC", 0.0],
    'Harmony Heights Resorts': ["Harmony Heights Resorts", "Eco Resorts", "HARMRES", 0.0],
    'TranquilTides Retreats': ["TranquilTides Retreats", "Beach Resorts", "TRQTIDE", 0.0],
}

_len_example_assets = len(example_assets)


def randint(a, b):
    c = b - a
    return randbelow(c + 1) + a


def randrate():
    i = randint(0, 40)
    if i == 36:
        return randint(50_00, 80_00) / 100_00
    if i == 12:
        return randint(80_00, 100_00) / 100_00
    if i < 16:
        return randint(106_00, 130_00) / 100_00
    if i < 28:
        return randint(109_00, 118_00) / 100_00
    return randint(103_00, 108_00) / 100_00


def randrate2():
    i = randint(0, 8)
    if i < 3:
        return randint(3_00, 8_00) / 100_00
    if i < 6:
        return randint(2_70, 3_60) / 100_00
    return randint(30, 4_90) / 100_00


def make():
    class _Money:
        cash = 0.0

    _money = _Money()

    _deposits = list()
    _payouts = list()
    _open_trades = list()
    _trade_letopen = list()
    _finalized_trades = list()
    _dividends = list()
    _itc = list()

    _traded_assets = list()

    for ex in example_assets.values():
        ex[-1] = randint(10, 200_00) / 100

    now = datetime.now()
    time = now - timedelta(365 * 10)

    def deposit():
        amount = (randint(10, 60) / 2) * 100
        _money.cash += amount
        _deposits.append(Deposit({"n": 0, "InvestAmount": amount, "InvestTime": time.strftime(rc.timeFormatTransaction)}, time, amount, now))

    def payout():
        if (x := _money.cash // 100) > 10:
            amount = (randint(1, int(x) - 9) / 5) * 100
            _money.cash -= amount
            _payouts.append(Payout({"n": 0, "TakeAmount": amount, "TakeTime": time.strftime(rc.timeFormatTransaction)}, time, amount, now))

    def trading(lo=True):
        if _open_trades and randint(0, (x := len(_open_trades)) + 12) > 11:
            trade = _open_trades.pop(randrange(0, x))
            if lo:
                if randint(0, 11) == 5:
                    _trade_letopen.append(trade)
                    return
                else:
                    trading(False)
            amount = trade.data["InvestAmount"] * randrate()
            _money.cash += amount
            _finalized_trades.append(TradeFinalized(trade.data | {"TakeAmount": amount, "TakeTime": time.strftime(rc.timeFormatTransaction)}, time, amount, now))
        elif (x := _money.cash // 100) > 5:
            amount = x * randint(50, 80) / 100
            for i in range(randint(3, 8)):
                if _traded_assets and randint(0, 3) == 3:
                    asset = choice(_traded_assets)
                else:
                    asset = example_assets[choice(list(example_assets))]
                    _traded_assets.append(asset)
                if asset[-1] < amount:
                    n = amount // asset[-1]
                    amount = asset[-1] * n
                    asset[-1] *= randrate()
                    break
            else:
                n = amount / asset[-1]
                n = round(n, 2) or n
                amount = asset[-1] * n
                asset[-1] *= randrate()
            _money.cash -= amount
            _open_trades.append(TradeOpen({"n": n, "Name": asset[0], "Symbol": asset[2], "Type": asset[1], "InvestAmount": amount, "InvestTime": time.strftime(rc.timeFormatTransaction)}, time, amount, now, False))
        else:
            deposit()

    def dividend():
        if _open_trades:
            trade = choice(_open_trades)
            amount = trade["InvestAmount"] * randrate2()
            _money.cash += amount
            _dividends.append(Dividend({"n": 0, "Name": trade["Name"], "TakeAmount": amount, "TakeTime": time.strftime(rc.timeFormatTransaction)}, time, amount, now, False))
        else:
            trading()

    def itc():
        if (x := _money.cash // 100) > 1:
            amount = x * (randint(11, 18) / 1000)
            if randint(0, 1):
                amount *= -1
            _money.cash += amount
            if randint(0, 10) > 3:
                _itc.append(Itc({"n": 0, "ITC": amount, "InvestTime": time.strftime(rc.timeFormatTransaction)}, time, amount, now, True))
            else:
                _itc.append(Itc({"n": 0, "ITC": amount, "TakeTime": time.strftime(rc.timeFormatTransaction)}, time, amount, now, False))
        else:
            deposit()

    while time < now:
        time += timedelta(seconds=randint(14400, 259200))
        if randint(0, 1):
            i = 1
        else:
            i = randint(1, 3)
        for _ in range(i):
            i = randint(0, 30)
            if i == 2:
                itc()
            elif i == 3:
                dividend()
            elif i == 7:
                payout()
            elif i == 8:
                deposit()
            else:
                trading()
            time += timedelta(seconds=randint(14400, 72000))
        time += timedelta(seconds=randint(259200, 1036800))

    data = [
        i.row_dat | {"id": n} for n, i in enumerate(_deposits + _payouts + _finalized_trades + _open_trades + _dividends + _itc + _trade_letopen)
    ]

    with open(demo.CACHE_TRADINGLOG, "wb") as f:
        dump(data, f)
