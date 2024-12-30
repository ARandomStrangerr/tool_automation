import pandas as pd;

alternativeName = {
        "and Wellness Inc, Ar": "Arisami Health & Wellness (Neeta Sai)",
        "Law, Leonard": "Olubode (Bode) Fagamiye - Leonard Law",
        "Eagleton, Lisa": "Pet Playland Pet Care Services (Lisa Eagleton)",
        "Prestige Cleaning Se": "Prestige Cleaning Services (Shayla Adams)",
        "Ruiz, Mary": "Mary Ruiz (TEAM, BTLC)",
        "Trading Incorporated": "Mamba Wyn Trading Incorporated",
        "Trading Inc., DTH": "DTH Trading Inc.",
        "Inc., Teradrive": "Teradrive Inc.",
        "Woewoda, James Carl": "James Carl Woewoda (Woewoda Communications)",
        "Inc, TC Thermenex": "TC Thermenex Inc (Darcy Hart)",
        "Accounting Solutions": "Francis Valim (iRefund Tax & Accounting Solutions Inc.)",
        "Corporation, Pacific": "Pacificana Development Corporation",
        "Roofing Ltd, Whonnoc": "Whonnock Roofing Ltd.",
        "Drainage and Sewer I": "ASAP Excavating Drainage & Sewer Inc.",
        "Electric Ltd, Wire-M": "Wire-Man Electric (Harmandeep Randhawa)",
        "Rodrigues Sierra, Ma": "Marisel Rodrigues Sierra (Mazaro Business Services Inc).",
        "Supplies Ltd, Top EV": "Top EV Charger Supplies Ltd. (formerly Shine Building Supply Inc.)",
        "Homes and Renos Inc.": "Sash Prestige Homes and Renos",
        "Inc., Portaone": "PortaOne, Inc.",
        "Laroco, Ryzanne-Char": "TC Virtual Solutions (Ryzanne-Charmaine Laroco)",
        "Multimedia Inc, Vrae": "Vraeyda Multimedia Inc. (Lis Goryniuk-Ratajczak)",
        "Graphics Ltd, Longev": "Longevity Graphics Ltd (Lindsay Viscount)",
        "Corporation, Fateh L": "Fateh Law Corporation (Navrantan Fateh)",
        "Ltd, 1371137 B.C.": "Rivers and Valley Home Support Services (1371137 BC Ltd - Trixie Gonzales)",
        "Industries Ltd, Arma": "Jacqueline Doering (Armarium Industries Ltd.)",
        "Inc, TeraDrive": "Teradrive Inc.",
        "Industries Ltd, Kono": "KONOL Industries Ltd (Haniel Guerrero)",
        "Mechanical Inc, Nova": "Navid Nejad (Novagreen Mechanical Inc.)",
        "Santos, Willian Brit": "EveryStep Immigration (Willian Brito Santos and Gregory Silva)",
        "Salmon Society, Wate": "Watershed Watch Salmon Society (Dawn Roumieu & Meghan Rooney)",
        "Holdings Ltd, AMS Bi": "ASM Birk Holdings Ltd (ComForCare Home Care)",
        "Plumbing Services In": "Fraser Valley Plumbing Services dba Mr. Rooter Plumbing (Denee VanDiermen)",
        "Health Co Ltd, Micro": "Ryzanne Laroco (dba Micro Mvmt & Health Co. Ltd. - Formerly Micro Massage & Wellness)",
        "Health Co. Ltd., Mic": "Ryzanne Laroco (dba Micro Mvmt & Health Co. Ltd.)",
        "Chen, Shunmin": "So-Chen & Associates Inc (Shunmin (Mischa) Chen)",
        "Corporation, Classic": "Classic Packaging",
        "Counseling, Embody": "Embody Counselling",
        "Melville, Dale": "Dale Melville Law Corporation",
        "PREC, Pedro Gomes": "Pedro Gomes PREC (Personal Real Estate Corporation)",
        "Corp, No Fear Counse": "No Fear Counselling",
        "Investment Inc., Mat": "Matthew Millions Investment Inc.",
        "Immigration, Fair Fi": "Fair Field Immigration",
        "Associates, Olfat": "Olfat & Associates",
        "Tuhkala, Mary": "Mary Tuhkala (Play Therapy with Mary)",
        "Wellness Ltd, Juno": "Juno Wellness Ltd (Robin King)",
        "Counselling, Elnaz B": "Juno Wellness Ltd (Robin King)",
        "West, Frederick": "West Counselling & Associates (Frederick West)",
        "Sleep, Advanced": "Advanced Sleep",
        "Mechanical Ltd, JJA": "JJA Mechanical Ltd.",
        "Physiotherapy Ltd, H": "Pratik Vyas Physiotherapist Corporation",
        "Tansley, Kelly": "Kelly Tansley RMT",
        "Satir Institute, of": "Satir Institute of the Pacific",
        "Shepherd, Carrie": "Carrie Shepherd (dba Aligned Massage Therapy)",
        "Solutions, Golden Be": "Golden Beans Accounting Solutions",
        "Associates Ltd, D.J.": "D.J. Reznick & Associates Ltd.",
        "Routledge, Kimberley": "Dr. Kimberly Routledge",
        "Mental Health, Conne": "Connectivity Mental Health Counselling",
        "Learning, Haland": "Haland Learning",
        "John, Deepa": "SFXCloud Inc. (Deepa John - SFX Cloud Solutions)",
        "Inc, Venovis": "Venovis Inc.",
        "Hale, Jessica": "Jessica Hale RMT",
        "LLP, Affirm": "Affirm LLP Chartered Professional Accountants (Juliane Johansen)",
}

caft_file_dict = {}

account_master_dict = {}

caft_file= pd.read_excel("./CAFT file.xlsx");
account_master_file = pd.read_excel("./Accounting Master Rent Checklist.xlsx", sheet_name="Dec 2024");

# indexing CAFT file
for index, row in caft_file.iterrows():
    if caft_file.loc[index, "Payor/Payee Name"] in caft_file_dict:
        caft_file_dict[caft_file.loc[index, "Payor/Payee Name"]] += float(caft_file.loc[index, "Amount"]);
    else:
        caft_file_dict[caft_file.loc[index, "Payor/Payee Name"]] = float(caft_file.loc[index, "Amount"]);

# indexing Account Master file
for index, row in account_master_file.iterrows():
    if account_master_file.loc[index, "TENANT"] in account_master_dict:
        account_master_dict[account_master_file.loc[index, "TENANT"]] += float(account_master_file.loc[index, "TOTAL"]);
    else:
        if float(account_master_file.loc[index, "TOTAL"] == 0.0):
            continue;
        account_master_dict[account_master_file.loc[index, "TENANT"]] = float(account_master_file.loc[index, "TOTAL"]);

caftIndex = list(caft_file_dict.keys());
accountMasterIndex = list(account_master_dict.keys());

# compare 2 dictionaries
for index in caft_file_dict:
    if index in alternativeName:
        if abs(caft_file_dict[index] - account_master_dict[alternativeName[index]]) > 0.009: #due to numerical error
            print(index, " **** ", alternativeName[index], " **** ", caft_file_dict[index] - account_master_dict[alternativeName[index]]);
        try:
            caftIndex.remove(index);
            accountMasterIndex.remove(alternativeName[index]);
        except Exception:
            print("");
    else:
        print("'",index, "' is appeared in domain - codomain map");

print("CAFT file leftover: ", caftIndex);
print("Account Master file leftover: ", accountMasterIndex);
