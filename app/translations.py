# EncarScraper/app/translations.py
from datetime import datetime
import json
import logging
import os
from typing import Dict
from .config import DATA_DIR

logger = logging.getLogger(__name__)

BRAND_TRANSLATIONS = {
    # ===== KOREAN BRANDS =====
    "현대": "Hyundai",
    "기아": "Kia",
    "기아자동차": "Kia Motors",
    "르노코리아": "Renault Korea",
    "르노삼성": "Renault Samsung",
    "삼성": "Samsung Motors",
    "쌍용": "SsangYong",
    "쌍용자동차": "SsangYong Motor",
    "제네시스": "Genesis",
    "한국GM": "GM Korea",
    "대우": "Daewoo",
    "쉐보레": "Chevrolet",
    "GM": "General Motors",
    
    # ===== JAPANESE BRANDS =====
    "도요타": "Toyota",
    "토요타": "Toyota",
    "토타": "Toyota",  # Common misinput
    "렉서스": "Lexus",
    "닛산": "Nissan",
    "인피니티": "Infiniti",
    "혼다": "Honda",
    "아큐라": "Acura",
    "마쯔다": "Mazda",
    "마즈다": "Mazda",
    "스바루": "Subaru",
    "미쓰비시": "Mitsubishi",
    "미쯔비시": "Mitsubishi",
    "스즈키": "Suzuki",
    "다이하쓰": "Daihatsu",
    "이스즈": "Isuzu",
    
    # ===== GERMAN BRANDS =====
    "벤츠": "Mercedes-Benz",
    "메르세데스": "Mercedes",
    "메르세데스벤츠": "Mercedes-Benz",
    "BMW": "BMW",
    "비엠더블유": "BMW",
    "아우디": "Audi",
    "폭스바겐": "Volkswagen",
    "VW": "Volkswagen",
    "포르쉐": "Porsche",
    "포르셰": "Porsche",
    "오펠": "Opel",
    "마이바흐": "Maybach",
    "스마트": "Smart",
    "만": "MAN",
    "미니": "Mini",
    
    # ===== AMERICAN BRANDS =====
    "포드": "Ford",
    "링컨": "Lincoln",
    "테슬라": "Tesla",
    "캐딜락": "Cadillac",
    "캐딜락": "Cadillac",
    "시보레": "Chevrolet",
    "GMC": "GMC",
    "지프": "Jeep",
    "크라이슬러": "Chrysler",
    "닷지": "Dodge",
    "램": "RAM",
    "허머": "Hummer",
    "벅": "Buick",
    "올즈모빌": "Oldsmobile",
    "폰티악": "Pontiac",
    "새턴": "Saturn",
    
    # ===== EUROPEAN BRANDS =====
    # French
    "푸조": "Peugeot",
    "시트로엥": "Citroën",
    "시트로엔": "Citroën",
    "르노": "Renault",
    "DS": "DS Automobiles",
    "부가티": "Bugatti",
    "알핀": "Alpine",
    
    # British
    "랜드로버": "Land Rover",
    "재규어": "Jaguar",
    "로버": "Rover",
    "MG": "MG",
    "애스턴마틴": "Aston Martin",
    "벤틀리": "Bentley",
    "롤스로이스": "Rolls-Royce",
    "로터스": "Lotus",
    "TVR": "TVR",
    "맥라렌": "McLaren",
    
    # Italian
    "피아트": "Fiat",
    "알파로메오": "Alfa Romeo",
    "마세라티": "Maserati",
    "페라리": "Ferrari",
    "람보르기니": "Lamborghini",
    "란치아": "Lancia",
    "파가니": "Pagani",
    
    # Swedish
    "볼보": "Volvo",
    "사브": "Saab",
    "코닉세그": "Koenigsegg",
    
    # Dutch
    "스파이커": "Spyker",
    
    # Czech
    "스코다": "Škoda",
    
    # ===== ASIAN BRANDS =====
    # Chinese
    "BYD": "BYD",
    "지리": "Geely",
    "체리": "Chery",
    "그레이트월": "Great Wall",
    "창안": "Changan",
    "바이크": "BAIC",
    "닥": "Dongfeng",
    "홍치": "Hongqi",
    "니오": "NIO",
    "XPENG": "XPeng",
    "리보": "Li Auto",
    "웨이": "WEY",
    "링크앤코": "Lynk & Co",
    
    # Indian
    "타타": "Tata",
    "마힌드라": "Mahindra",
    
    # Malaysian
    "프로톤": "Proton",
    
    # ===== OTHER/SPECIALTY =====
    "코벳": "Corvette",
    "마스다": "Mazda",
    "델로리안": "DeLorean",
    "피스커": "Fisker",
    "리비안": "Rivian",
    "루시드": "Lucid",
    "폴스타": "Polestar",
    "카니발": "Carnival",  # Common Kia model mistaken as brand
    
    # ===== COMMON MISSPELLINGS/ALTERNATIVES =====
    "벤쯔": "Mercedes-Benz",
    "포쉐": "Porsche",
    "포르쉐": "Porsche",
    "아우디": "Audi",
    "아우띠": "Audi",
    "폭바": "Volkswagen",
    "기아자동차": "Kia",
    "현대자동차": "Hyundai",
    
    # ===== COMMON CATEGORIES =====
    "수입차": "Imported Car",
    "국산차": "Domestic Car",
    "외제차": "Foreign Car",
    "고급차": "Luxury Car",
    "중고차": "Used Car",
    "전기차": "Electric Vehicle",
    "하이브리드": "Hybrid",
    "기타": "Other",
    "미분류": "Unclassified",
    "쉐보레(GM대우)": "Chevrolet (GM Daewoo)",
    "르노코리아(삼성)": "Renault Korea (Samsung)",
    "KG모빌리티(쌍용)": "KG Mobility (Ssangyong)",
}

TRANSMISSION_TRANSLATIONS = {
    "오토": "Automatik",
    "수동": "Manual",
    "자동": "Automatik",
    "CVT": "CVT",
    "DCT": "DCT",
    "AT": "Automatik",
    "MT": "Manual",
}

FUEL_TRANSLATIONS = {
    "가솔린": "Benzinë",
    "디젤": "Dizel",
    "하이브리드": "Hibrid",
    "전기": "Elektrik",
    "LPG": "LPG",
    "CNG": "CNG",
    "가스": "gas",
    "플러그인 Hybrid": "Plugin Hybrid",
}

COLOR_TRANSLATIONS = {
    # Basic Colors
    "흰색": "E Bardhë",
    "백색": "E Bardhë",
    "화이트": "E Bardhë",
    "검정색": "E Zezë",
    "검은색": "E Zezë",
    "블랙": "E Zezë",
    "회색": "Gri",
    "그레이": "Gri",
    "은색": "Argjend",
    "실버": "Argjend",
    "은색메탈": "Argjend metalik",
    "금색": "E Artë",
    "골드": "E Artë",
    "빨간색": "E Kuqe",
    "레드": "E Kuqe",
    "파란색": "E Kaltër",
    "블루": "E Kaltër",
    "초록색": "E Gjelbër",
    "그린": "E Gjelbër",
    "노란색": "E Verdhë",
    "옐로우": "E Verdhë",
    "주황색": "Portokalli",
    "오렌지": "Portokalli",
    "갈색": "Kafe",
    "브라운": "Kafe",
    "베이지": "Bezhë",
    "핑크": "Rozë",
    "분홍색": "Rozë",
    "보라색": "Vjollcë",
    "퍼플": "Vjollcë",
    "청색": "Blu e errët",
    "하늘색": "Blu qielli",
    "남색": "Blu navy",
    "진회색": "Gri i errët",
    "밝은회색": "Gri i hapur",

    # Metalic / Pearl variants
    "진주색": "Ngjyrë perle",
    "펄": "Ngjyrë perle",
    "메탈릭": "Metalik",
    "메탈": "Metalik",

    # Specific common car colors (English-Korean mapped to Albanian)
    "Black": "E Zezë",
    "White": "E Bardhë",
    "Silver": "Argjend",
    "Gray": "Gri",
    "Blue": "E Kaltër",
    "Red": "E Kuqe",
    "Green": "E Gjelbër",
    "Yellow": "E Verdhë",
    "Beige": "Bezhë",
    "Brown": "Kafe",
    "Orange": "Portokalli",
    "Pink": "Rozë",
    "Purple": "Vjollcë",
    "Gold": "E Artë",

    # Additional descriptive colors (Korean)
    "에메랄드그린": "E Gjelbër smerald",
    "다크블루": "Blu e errët",
    "라이트블루": "Blu e hapur",
    "스카이블루": "Blu qielli",
    "버건디": "Burgundi",
    "브론즈": "Bronz",
    "카키": "Kaki",
    "카멜": "Kamël",
    "올리브": "Olive",
    "로즈골드": "Rozë e artë",

    # Color with expressions (some colors come with hex, just ignore or keep color name)
    # You can parse these or ignore hex codes for Excel
    "ColorExpression": "",  # Placeholder, usually hex like "#ffffff"

    # Special entries
    "투톤": "Dy ngjyra",
    "기타": "Tjetër",
    "쥐색": "Gri",
    "녹색": "Green",
}

SEAT_COLOR_TRANSLATIONS = {
    "검정색 계열": "E Zezë",
    "베이지색 계열": "Bezhë",
    "회색 계열": "Gri",
    "갈색 계열": "Kafe",
    "빨강 계열": "E Kuqe",
    "쥐색": "Grip",
    "빨간색 계열": "Red",
    "흰색 계열": "White",
    "주황색 계열": "Orange",
}

BADGE_TRANSLATIONS = {
    # Common trims and keywords
    "스포츠": "Sport",
    "리미티드": "Limited",
    "프리미엄": "Premium",
    "럭셔리": "Luxury",
    "프레스티지": "Prestige",
    "익스클루시브": "Exclusive",
    "GT": "GT",
    "RS": "RS",
    "SE": "SE",
    "SEL": "SEL",
    "XLE": "XLE",
    "LX": "LX",
    "EX": "EX",
    "EX-L": "EX-L",
    "TDI": "TDI",
    "TFSI": "TFSI",
    "TRD": "TRD",
    "하이브리드": "Hybrid",
    "플러그인 하이브리드": "Plug-in Hybrid",
    "전기차": "Electric",
    "터보": "Turbo",
    "슈퍼차저": "Supercharged",
    "에코부스트": "EcoBoost",
    "다이내믹": "Dynamic",
    "블랙 에디션": "Black Edition",
    "화이트 에디션": "White Edition",
    "GT라인": "GT Line",
    "RS라인": "RS Line",
    "S라인": "S Line",
    "럭스": "LUX",
    "플래티넘": "Platinum",
    "다이아몬드": "Diamond",
    "어드벤처": "Adventure",
    "트레일호크": "Trailhawk",
    "데날리": "Denali",
    "스페셜 에디션": "Special Edition",
    "베이스": "Base",
    "플러스": "Plus",
    "투어링": "Touring",
    "스포트백": "Sportback",
    "컴피티션": "Competition",
    "레드라인": "Redline",
    "GTI": "GTI",
    "GTS": "GTS",
    "N라인": "N Line",
    "타이탄": "Titan",
    "골드 에디션": "Gold Edition",
    "실버 에디션": "Silver Edition",
    "어반": "Urban",
    "컴포트": "Comfort",
    "다이나믹 플러스": "Dynamic Plus",
    "스포츠 플러스": "Sport Plus",
    "GT 퍼포먼스": "GT Performance",
    "퍼포먼스": "Performance",
    "익스큐티브": "Executive",
    "시그니처": "Signature",
    "얼티메이트": "Ultimate",
    "레거시": "Legacy",
    "아웃백": "Outback",
    "플래티넘 SE": "Platinum SE",
    "XSE": "XSE",
    "XLT": "XLT",
    "ST": "ST",
    "SRT": "SRT",
    "SXT": "SXT",
    "SLE": "SLE",
    "SLT": "SLT",
    "ZR1": "ZR1",
    "GT350": "GT350",
    "GT500": "GT500",
    "Z28": "Z28",
    "타입R": "Type R",
    "STI": "STI",
    "WRX": "WRX",
    "M 스포츠": "M Sport",
    "R-디자인": "R-Design",
    "X-라인": "X-Line",
    "에코": "Eco",
    
    # Numeric trims and suffixes
    "3000": "3000",
    "2000": "2000",
    "1500": "1500",
    "2500": "2500",
    "3500": "3500",
    "500": "500",
    
    # Engine types and fuel
    "디젤": "Diesel",
    "가솔린": "Gasoline",
    "전기": "Electric",
    "수소": "Hydrogen",
    "LPG": "LPG",
    "하이브리드": "Hybrid",
    
    # Transmission types
    "오토": "Automatic",
    "수동": "Manual",
    "CVT": "CVT",
    "듀얼 클러치": "Dual Clutch",
    
    # Special features and packages
    "4륜 구동": "4WD",
    "AWD": "AWD",
    "스마트": "Smart",
    "투어링": "Touring",
    "어드밴스드": "Advanced",
    "익스트림": "Extreme",
    "스탠다드": "Standard",
    "플래티넘": "Platinum",
    "골드": "Gold",
    "실버": "Silver",
    "브론즈": "Bronze",
    "럭셔리 패키지": "Luxury Package",
    "스포츠 패키지": "Sport Package",
    "테크 패키지": "Tech Package",
    "프리미엄 패키지": "Premium Package",
    
    # Colors (for badge context sometimes)
    "블랙": "Black",
    "화이트": "White",
    "실버": "Silver",
    "레드": "Red",
    "블루": "Blue",
    "그린": "Green",
    "그레이": "Gray",
    "브라운": "Brown",
    "옐로우": "Yellow",
    "골드": "Gold",
    "오렌지": "Orange",
    
    # Others
    "에디션": "Edition",
    "GTX": "GTX",
    "S": "S",
    "SE": "SE",
    "SEL": "SEL",
    "Limited": "Limited",
    "EX-L": "EX-L",
    "Touring": "Touring",
    "Sport": "Sport",
    "LX": "LX",
    
    # Repeat variants and synonyms for coverage
    "스포트": "Sport",
    "리밋": "Limited",
    "프리미엄 에디션": "Premium Edition",
    "럭셔리 에디션": "Luxury Edition",
    "하이브리드 에디션": "Hybrid Edition",
    "전기 에디션": "Electric Edition",
    "터보 에디션": "Turbo Edition",
    "GT 에디션": "GT Edition",
    "RS 에디션": "RS Edition",
    
    # Add more as you find from data or specific brands
    "9인승 프레스티지": "9 -seater prestige",
    "1.6 모던": "1.6 Modern",
    "2.5 XLE 프리미엄 하이브리드": "2.5 XLE Premium Hybrid",
    "AMG CLS53 4MATIC+": "AMG CLS53 4MATIC+",
    "2.5 하이브리드 2WD": "2.5 Hybrid 2WD",
    "롱레인지": "Long Range",
    "xDrive M40i": "XDRIVE M40I",
    "1.6 터보 스포츠": "1.6 Turbo Sports",
    "가솔린 2.5 터보 AWD": "Gasoline 2.5 Turbo AWD",
    "GLE450 4MATIC": "GLE450 4MATIC",
    "45 TDI 콰트로 프리미엄": "45 TDI Quattro Premium",
    "HIGH": "High",
    "1.4 퍼펙트 블랙": "1.4 Perfect Black",
    "LPLI 2.0 LPe 장애인용": "LPLI 2.0 LPE for the disabled",
    "디젤 2.0 2WD": "Diesel 2.0 2WD",
    "디젤 2.2 4WD": "Diesel 2.2 4WD",
    "가솔린 3.5 터보 AWD": "Gasoline 3.5 Turbo AWD",
    "2.0 LPe RE 2WD": "2.0 LPE Re 2WD",
    "롱 레인지": "Long range",
    "45 TFSI 콰트로": "45 TFSI Quattro",
    "어스": "earth",
    "220i M 스포츠": "220i M Sports",
    "1.6 GDI 스마트": "1.6 GDI Smart",
    "디젤 2.2 2WD": "Diesel 2.2 2WD",
    "3.0 LPi 모던 (렌터카)": "3.0 LPI Modern (Rent -A -Car)",
    "xDrive 30e M 스포츠": "XDRIVE 30e M Sports",
    "3.8 GDI AWD": "3.8 GDI AWD",
    "e-AWD": "e-awd",
    "3.3": "3.3",
    "기본형": "Basic type",
    "가솔린 9인승 시그니처": "Gasoline 9 -seater signature",
    "가솔린 9인승 노블레스": "Gasoline 9 -seater Noblesse",
    "2.0 N": "2.0 n",
    "3.0 LPI 럭셔리 (렌터카)": "3.0 LPI luxury (car rental)",
}

MODEL_GROUP_TRANSLATIONS = {

 # ===== KOREAN BRANDS =====

    # Kia - Compact & Sedans
    "모닝": "Morning / Picanto",
    "레이": "Ray",
    "K1": "K1",
    "K2": "K2 / Pegas",
    "K3": "K3 / Forte / Cerato",
    "쎄라토": "Cerato",
    "K4": "K4",
    "K5": "K5 / Optima",
    "K7": "K7 / Cadenza",
    "K8": "K8",
    "K9": "K9 / K900 / Quoris",
    "로체": "Lotze",
    "오피러스": "Opirus / Amanti",
    "프라이드": "Pride / Rio",
    "아벨라": "Avella",
    "세피아": "Sephia",
    "엔터프라이즈": "Enterprise",
    "포텐샤": "Potentia",
    "캐피탈": "Capital",

    # Kia - SUV & Crossovers
    "셀토스": "Seltos",
    "스토닉": "Stonic",
    "니로": "Niro",
    "스포티지": "Sportage",
    "쏘렌토": "Sorento",
    "모하비": "Mohave / Borrego",
    "레토나": "Retona",

    # Kia - MPV & Vans
    "카니발": "Carnival / Sedona",
    "베스타": "Vesta",
    "봉고": "Bongo",
    "타우너": "Towner",
    "프레지오": "Pregio",
    "베스타 밴": "Vesta Van",
    "카스타": "Carstar",

    # Kia - Electric / Hybrid
    "쏘울": "Soul",
    "쏘울 EV": "Soul EV",
    "EV6": "EV6",
    "EV9": "EV9",
    "니로 EV": "Niro EV",
    "니로 플러스": "Niro Plus",
    "레이 EV": "Ray EV",

    # Kia - Commercial
    "그랜드버드": "Granbird",


    # Genesis - Sedans & SUVs
    "G70": "G70",
    "G80": "G80",
    "G90": "G90",
    "EQ900": "EQ900 (pre-facelift G90)",
    "GV60": "GV60",
    "GV70": "GV70",
    "GV80": "GV80",


    # SsangYong / KG Mobility
    "티볼리": "Tivoli",
    "티볼리 에어": "Tivoli Air",
    "코란도": "Korando",
    "코란도 투리스모": "Korando Turismo",
    "렉스턴": "Rexton",
    "렉스턴 스포츠": "Rexton Sports",
    "렉스턴 스포츠 칸": "Rexton Sports Khan",
    "무쏘": "Musso",
    "무쏘 스포츠": "Musso Sports",
    "카이런": "Kyron",
    "액티언": "Actyon",
    "액티언 스포츠": "Actyon Sports",
    "로디우스": "Rodius / Stavic",
    "체어맨": "Chairman",
    "체어맨 H": "Chairman H",
    "체어맨 W": "Chairman W",


    # Renault Samsung
    "SM3": "SM3",
    "SM3 ZE": "SM3 ZE",
    "SM5": "SM5",
    "SM6": "SM6",
    "SM7": "SM7",
    "QM3": "QM3 / Captur",
    "QM5": "QM5 / Koleos",
    "QM6": "QM6 / Koleos",
    "르노 캡처": "Renault Captur",
    "르노 조에": "Renault Zoe",
    "르노 마스터": "Renault Master",
    "르노 트위지": "Renault Twizy",
    "르노 클리오": "Renault Clio",
    "르노 메간": "Renault Megane",

    # Daewoo (historical, now GM Korea)
    "라노스": "Lanos",
    "누비라": "Nubira",
    "레간자": "Leganza",
    "마티즈": "Matiz",
    "티코": "Tico",
    "스페로": "Espero",
    "프린스": "Prince",
    "로얄 살롱": "Royal Salon",
    "르망": "LeMans",
    "에스페로": "Espero",
    "브로엄": "Brougham",
    "알페로": "Alpheon",

    # GM Korea (Chevrolet now)
    "스파크": "Spark / Matiz Creative",
    "아베오": "Aveo",
    "크루즈": "Cruze",
    "말리부": "Malibu",
    "임팔라": "Impala",
    "올란도": "Orlando",
    "트랙스": "Trax",
    "이쿼녹스": "Equinox",
    "트래버스": "Traverse",
    "볼트 EV": "Bolt EV",
    "볼트 EUV": "Bolt EUV",
    "카마로": "Camaro",
    "콜로라도": "Colorado",
    "타호": "Tahoe",
    "트레일블레이저": "Trailblazer",
    "캡티바": "Captiva",
    "윈스톰": "Winstorm",
    "레조": "Rezzo",
    "젠트라": "Gentra",

    # ===== JAPANESE BRANDS =====

    # Toyota
    "프리우스": "Prius",
    "프리우스 C": "Prius C / Aqua",
    "프리우스 V": "Prius V / Alpha",
    "아발론": "Avalon",
    "캠리": "Camry",
    "코롤라": "Corolla",
    "코롤라 스포츠": "Corolla Sport",
    "코롤라 크로스": "Corolla Cross",
    "야리스": "Yaris / Vitz",
    "아리스 크로스": "Yaris Cross",
    "CHR": "C-HR",
    "RAV4": "RAV4",
    "하리어": "Harrier",
    "벤자": "Venza",
    "하이랜더": "Highlander",
    "포춘너": "Fortuner",
    "랜드크루저": "Land Cruiser",
    "랜드크루저 프라도": "Land Cruiser Prado",
    "4러너": "4Runner",
    "세쿼이아": "Sequoia",
    "시에나": "Sienna",
    "알파드": "Alphard",
    "벨파이어": "Vellfire",
    "노아": "Noah",
    "복시": "Voxy",
    "에스티마": "Estima / Previa",
    "이노바": "Innova",
    "타운에이스": "TownAce",
    "그랜비아": "Granvia",
    "하이에이스": "HiAce",
    "다이나": "Dyna",
    "타코마": "Tacoma",
    "툰드라": "Tundra",
    "86": "86 / GT86",
    "GR86": "GR86",
    "수프라": "Supra",
    "미라이": "Mirai",

    # Honda
    "시빅": "Civic",
    "시빅 타입 R": "Civic Type R",
    "어코드": "Accord",
    "인사이트": "Insight",
    "레전드": "Legend",
    "피트": "Fit / Jazz",
    "그레이스": "Grace",
    "시티": "City",
    "프리드": "Freed",
    "HR-V": "HR-V / Vezel",
    "CR-V": "CR-V",
    "ZR-V": "ZR-V",
    "파일럿": "Pilot",
    "패스포트": "Passport",
    "오딧세이": "Odyssey",
    "스텝왜건": "Stepwgn",
    "크로스투어": "Crosstour",
    "엘리시온": "Elysion",
    "S2000": "S2000",
    "NSX": "NSX",
    "리지라인": "Ridgeline",

    # Nissan
    "마치": "March / Micra",
    "노트": "Note",
    "큐브": "Cube",
    "센트라": "Sentra",
    "실피": "Sylphy",
    "알티마": "Altima",
    "맥시마": "Maxima",
    "티아나": "Teana",
    "블루버드": "Bluebird",
    "스카이라인": "Skyline",
    "GT-R": "GT-R / Skyline GT-R",
    "페어레이디 Z": "Fairlady Z / 350Z / 370Z / Z",
    "패스파인더": "Pathfinder",
    "로그": "Rogue / X-Trail",
    "무라노": "Murano",
    "아르마다": "Armada",
    "주크": "Juke",
    "캐시카이": "Qashqai",
    "테라노": "Terrano",
    "엑스트레일": "X-Trail",
    "프론티어": "Frontier",
    "타이탄": "Titan",
    "세레나": "Serena",
    "엘그란드": "Elgrand",
    "NV350": "NV350 Caravan",

    # Mazda
    "마즈다2": "Mazda2 / Demio",
    "마즈다3": "Mazda3 / Axela",
    "마즈다6": "Mazda6 / Atenza",
    "CX-3": "CX-3",
    "CX-30": "CX-30",
    "CX-4": "CX-4",
    "CX-5": "CX-5",
    "CX-8": "CX-8",
    "CX-9": "CX-9",
    "CX-50": "CX-50",
    "CX-60": "CX-60",
    "CX-90": "CX-90",
    "MX-5": "MX-5 / Miata / Roadster",
    "RX-7": "RX-7",
    "RX-8": "RX-8",
    "BT-50": "BT-50",

    # Subaru
    "임프레자": "Impreza",
    "레거시": "Legacy",
    "레보그": "Levorg",
    "아웃백": "Outback",
    "포레스터": "Forester",
    "크로스트렉": "Crosstrek / XV",
    "BRZ": "BRZ",
    "트리벡카": "Tribeca",
    "아세트라": "Ascent",

    # Mitsubishi
    "미라지": "Mirage",
    "콜트": "Colt",
    "랜서": "Lancer",
    "랜서 에볼루션": "Lancer Evolution",
    "아웃랜더": "Outlander",
    "아웃랜더 스포츠": "Outlander Sport / RVR / ASX",
    "이클립스 크로스": "Eclipse Cross",
    "파제로": "Pajero / Montero / Shogun",
    "파제로 스포츠": "Pajero Sport / Montero Sport",
    "델리카": "Delica",
    "트라이튼": "Triton / L200",
    "미니캡": "Minicab",

    # Suzuki
    "스위프트": "Swift",
    "발레노": "Baleno",
    "알토": "Alto",
    "웨건 R": "Wagon R",
    "셀레리오": "Celerio",
    "비타라": "Vitara",
    "그랜드 비타라": "Grand Vitara",
    "짐니": "Jimny",
    "에스프레소": "S-Presso",
    "이그니스": "Ignis",
    "에르티가": "Ertiga",
    "XL7": "XL7",
    "캐리 트럭": "Carry Truck",

# ===== GERMAN BRANDS =====

    # BMW
    "1시리즈": "1 Series",
    "2시리즈": "2 Series",
    "3시리즈": "3 Series",
    "4시리즈": "4 Series",
    "5시리즈": "5 Series",
    "6시리즈": "6 Series",
    "7시리즈": "7 Series",
    "8시리즈": "8 Series",
    "i3": "i3",
    "i4": "i4",
    "i5": "i5",
    "i7": "i7",
    "i8": "i8",
    "X1": "X1",
    "X2": "X2",
    "X3": "X3",
    "X4": "X4",
    "X5": "X5",
    "X6": "X6",
    "X7": "X7",
    "XM": "XM",
    "Z3": "Z3",
    "Z4": "Z4",
    "M2": "M2",
    "M3": "M3",
    "M4": "M4",
    "M5": "M5",
    "M6": "M6",
    "M8": "M8",
    "X5 M": "X5 M",
    "X6 M": "X6 M",
    "X3 M": "X3 M",
    "X4 M": "X4 M",

    # Mercedes-Benz
    "A클래스": "A-Class",
    "B클래스": "B-Class",
    "C클래스": "C-Class",
    "E클래스": "E-Class",
    "S클래스": "S-Class",
    "CLA": "CLA",
    "CLS": "CLS",
    "GLA": "GLA",
    "GLB": "GLB",
    "GLC": "GLC",
    "GLE": "GLE",
    "GLS": "GLS",
    "G클래스": "G-Class",
    "SLK": "SLK",
    "SLC": "SLC",
    "SL": "SL",
    "AMG GT": "AMG GT",
    "EQC": "EQC",
    "EQA": "EQA",
    "EQB": "EQB",
    "EQS": "EQS",
    "EQE": "EQE",
    "V클래스": "V-Class",
    "스프린터": "Sprinter",
    "비토": "Vito",

    # Audi
    "A1": "A1",
    "A3": "A3",
    "A4": "A4",
    "A5": "A5",
    "A6": "A6",
    "A7": "A7",
    "A8": "A8",
    "Q2": "Q2",
    "Q3": "Q3",
    "Q4": "Q4",
    "Q5": "Q5",
    "Q7": "Q7",
    "Q8": "Q8",
    "e-tron": "e-tron",
    "RS3": "RS3",
    "RS4": "RS4",
    "RS5": "RS5",
    "RS6": "RS6",
    "RS7": "RS7",
    "RS Q3": "RS Q3",
    "RS Q8": "RS Q8",
    "S3": "S3",
    "S4": "S4",
    "S5": "S5",
    "S6": "S6",
    "S7": "S7",
    "S8": "S8",
    "SQ5": "SQ5",
    "TT": "TT",
    "R8": "R8",

    # Volkswagen (VW)
    "폴로": "Polo",
    "골프": "Golf",
    "파사트": "Passat",
    "아르테온": "Arteon",
    "비틀": "Beetle",
    "투란": "Touran",
    "티구안": "Tiguan",
    "투아렉": "Touareg",
    "T-로크": "T-Roc",
    "T-크로스": "T-Cross",
    "ID.3": "ID.3",
    "ID.4": "ID.4",
    "ID.5": "ID.5",
    "ID. Buzz": "ID. Buzz",
    "샤란": "Sharan",
    "캐디": "Caddy",
    "트랜스포터": "Transporter",
    "멀티밴": "Multivan",
    "카라벨": "Caravelle",
    "아마록": "Amarok",

    # Porsche
    "카이엔": "Cayenne",
    "마칸": "Macan",
    "파나메라": "Panamera",
    "911": "911",
    "718 박스터": "718 Boxster",
    "718 카이맨": "718 Cayman",
    "타이칸": "Taycan",

    # Opel
    "코르사": "Corsa",
    "아스트라": "Astra",
    "인시그니아": "Insignia",
    "모카": "Mokka",
    "그랜드랜드": "Grandland",
    "크로슬랜드": "Crossland",
    "잠피라": "Zafira",
    "콤보": "Combo",
    "비바로": "Vivaro",

    # Smart (Mercedes-Benz)
    "포투": "ForTwo",
    "포포": "ForFour",

    # MAN, DAF, others
    "만": "MAN",
    "다프": "DAF",
    "네오플란": "Neoplan",
    
    # Others popular in Kosovo & Balkans
    "포드": "Ford",
    "포커스": "Focus",
    "몬데오": "Mondeo",
    "피에스타": "Fiesta",
    "쉐보레": "Chevrolet",
    "말리부": "Malibu",
    "크루즈": "Cruze",
    "트래버스": "Traverse",
    "지프": "Jeep",
    "랭글러": "Wrangler",
    "체로키": "Cherokee",
    "랜드로버": "Land Rover",
    "디스커버리": "Discovery",
    
    # Mini (BMW)
    "미니 쿠퍼": "Mini Cooper",
    "미니 클럽맨": "Mini Clubman",
    
# ===== FRENCH BRANDS =====

    # Renault
    "클리오": "Clio",
    "캡처": "Captur",
    "메간": "Megane",
    "라구나": "Laguna",
    "탈리스만": "Talisman",
    "세닉": "Scénic",
    "콜레오스": "Koleos",
    "카자르": "Kadjar",
    "에스파스": "Espace",
    "트위지": "Twizy",
    "조에": "Zoe",
    "아르카나": "Arkana",
    "오스트랄": "Austral",
    "에스파스 6": "Espace VI",
    
    # Renault Samsung (already partially included but recap for completeness)
    "SM3": "SM3",
    "SM5": "SM5",
    "SM6": "SM6",
    "SM7": "SM7",
    "QM3": "QM3",
    "QM5": "QM5",
    "QM6": "QM6",

    # Peugeot
    "208": "208",
    "2008": "2008",
    "308": "308",
    "3008": "3008",
    "408": "408",
    "5008": "5008",
    "508": "508",
    "607": "607",
    "RCZ": "RCZ",
    "리프터": "Rifter",
    "트래블러": "Traveller",
    "파트너": "Partner",
    "박서": "Boxer",
    "익스퍼트": "Expert",

    # Citroën
    "C1": "C1",
    "C2": "C2",
    "C3": "C3",
    "C3 에어크로스": "C3 Aircross",
    "C4": "C4",
    "C4 칵투스": "C4 Cactus",
    "C4 에어크로스": "C4 Aircross",
    "C5": "C5",
    "C5 에어크로스": "C5 Aircross",
    "C6": "C6",
    "DS3": "DS3",
    "DS4": "DS4",
    "DS5": "DS5",
    "DS7": "DS7 Crossback",
    "DS9": "DS9",
    "그랜드 C4 피카소": "Grand C4 Picasso",
    "피카소": "Picasso",
    "베를링고": "Berlingo",
    "점피": "Jumpy",
    "점퍼": "Jumper",

    # DS Automobiles (sub-brand)
    "DS3 크로스백": "DS3 Crossback",
    "DS7 크로스백": "DS7 Crossback",
    "DS9": "DS9",

# ===== ITALIAN BRANDS =====

    # Fiat
    "500": "500",
    "500C": "500C",
    "500L": "500L",
    "500X": "500X",
    "500e": "500e",
    "판다": "Panda",
    "판다 4x4": "Panda 4x4",
    "푸토": "Punto",
    "그란데 푸토": "Grande Punto",
    "푸토 이보": "Punto Evo",
    "티포": "Tipo",
    "브라보": "Bravo",
    "브라바": "Brava",
    "팔리오": "Palio",
    "알베아": "Albea",
    "우노": "Uno",
    "도블로": "Doblo",
    "쿠페 피아트": "Fiat Coupé",
    "크로마": "Croma",
    "스트라다": "Strada",
    "세이첸토": "Seicento",
    "치첸토": "Cinquecento",
    "몰티플라": "Multipla",
    "프레모": "Freemont",
    "스쿠도": "Scudo",
    "두카토": "Ducato",
    "우리스": "Ulysse",
    "이데아": "Idea",
    "템프라": "Tempra",
    "리트모": "Ritmo",
    "레가타": "Regata",

    # Alfa Romeo
    "줄리아": "Giulia",
    "줄리에타": "Giulietta",
    "스텔비오": "Stelvio",
    "미토": "MiTo",
    "브레라": "Brera",
    "159": "159",
    "156": "156",
    "147": "147",
    "GT": "GT",
    "GTV": "GTV",
    "스파이더": "Spider",
    "알페타": "Alfetta",
    "33": "33",
    "75": "75",
    "164": "164",
    "166": "166",
    "90": "90",
    "6": "6",
    "145": "145",
    "146": "146",

    # Maserati
    "기블리": "Ghibli",
    "콰트로포르테": "Quattroporte",
    "그란투리스모": "GranTurismo",
    "그란카브리오": "GranCabrio",
    "르반떼": "Levante",
    "MC20": "MC20",
    "비트루보": "Biturbo",
    "3200 GT": "3200 GT",
    "스파이더": "Spyder",
    "쿠페": "Coupé",

    # Ferrari
    "로마": "Roma",
    "포르토피노": "Portofino",
    "칼리포르니아": "California",
    "458 이탈리아": "458 Italia",
    "458 스파이더": "458 Spider",
    "488 GTB": "488 GTB",
    "488 피스타": "488 Pista",
    "F8 트리뷰토": "F8 Tributo",
    "F8 스파이더": "F8 Spider",
    "812 슈퍼패스트": "812 Superfast",
    "812 GTS": "812 GTS",
    "라페라리": "LaFerrari",
    "SF90 스트라달레": "SF90 Stradale",
    "SF90 스파이더": "SF90 Spider",
    "296 GTB": "296 GTB",
    "296 GTS": "296 GTS",
    "GTC4 루쏘": "GTC4Lusso",
    "몬자 SP1": "Monza SP1",
    "몬자 SP2": "Monza SP2",
    "엔초": "Enzo",
    "F12 베를리네타": "F12 Berlinetta",
    "599 GTB": "599 GTB",
    "612 스카글리에티": "612 Scaglietti",
    "575M": "575M Maranello",
    "550 마라넬로": "550 Maranello",
    "360 모데나": "360 Modena",
    "360 스파이더": "360 Spider",
    "F355": "F355",
    "348": "348",
    "테스타로사": "Testarossa",
    "328": "328",
    "308": "308",
    "디노": "Dino",

    # Lamborghini
    "우루스": "Urus",
    "우라칸": "Huracán",
    "우라칸 EVO": "Huracán EVO",
    "우라칸 테크니카": "Huracán Tecnica",
    "우라칸 STO": "Huracán STO",
    "아벤타도르": "Aventador",
    "아벤타도르 SVJ": "Aventador SVJ",
    "레벤톤": "Reventón",
    "무르시엘라고": "Murciélago",
    "가야르도": "Gallardo",
    "시아안": "Sian",
    "센테나리오": "Centenario",
    "디아블로": "Diablo",
    "자라마": "Jarama",
    "에스파다": "Espada",
    "우루코": "Urraco",
    "미우라": "Miura",
    "이스테오크": "Estoque",

# ===== UK BRANDS =====

    # Jaguar
    "XE": "XE",
    "XF": "XF",
    "XJ": "XJ",
    "F-타입": "F-Type",
    "E-페이스": "E-Pace",
    "I-페이스": "I-Pace",
    "F-페이스": "F-Pace",
    "X타입": "X-Type",
    "S타입": "S-Type",
    "XKR": "XKR",
    "XK": "XK",
    "XJS": "XJS",
    "XK8": "XK8",
    "XJ6": "XJ6",
    "XJ8": "XJ8",
    "XJ12": "XJ12",
    "D타입": "D-Type",
    "E타입": "E-Type",

    # Land Rover
    "디스커버리": "Discovery",
    "디스커버리 스포츠": "Discovery Sport",
    "레인지로버": "Range Rover",
    "레인지로버 스포츠": "Range Rover Sport",
    "레인지로버 이보크": "Range Rover Evoque",
    "디펜더": "Defender",
    "시리즈 I": "Series I",
    "시리즈 II": "Series II",
    "시리즈 III": "Series III",
    "레인지로버 클래식": "Range Rover Classic",
    "프리랜더": "Freelander",
    "디펜더 90": "Defender 90",
    "디펜더 110": "Defender 110",

    # MINI (BMW 그룹에 속하지만 영국 브랜드로도 봄)
    "미니 쿠퍼": "Mini Cooper",
    "미니 쿠퍼 S": "Mini Cooper S",
    "미니 클럽맨": "Mini Clubman",
    "미니 컨트리맨": "Mini Countryman",
    "미니 일렉트릭": "Mini Electric",
    "미니 JCW": "Mini JCW (John Cooper Works)",
    "미니 페이스맨": "Mini Paceman",

    # Aston Martin
    "DB11": "DB11",
    "DBS 슈퍼레제라": "DBS Superleggera",
    "밴티지": "Vantage",
    "뱅퀴시": "Vanquish",
    "라피드": "Rapide",
    "발키리": "Valkyrie",
    "DB9": "DB9",
    "DB7": "DB7",
    "V8 밴티지": "V8 Vantage",
    "V12 밴티지": "V12 Vantage",
    "Cygnet": "Cygnet",
    "V12 자가토": "V12 Zagato",

    # Rolls-Royce
    "고스트": "Ghost",
    "팬텀": "Phantom",
    "레이스": "Wraith",
    "던": "Dawn",
    "컬리넌": "Cullinan",
    "실버 섀도우": "Silver Shadow",
    "실버 스피릿": "Silver Spirit",
    "실버 레이스": "Silver Wraith",
    "실버 클라우드": "Silver Cloud",
    "콘티넨탈 GT": "Continental GT",

    # Bentley
    "콘티넨탈 GT": "Continental GT",
    "플라잉 스퍼": "Flying Spur",
    "벤테이가": "Bentayga",
    "아줄라": "Azure",
    "뮤즈": "Mulsanne",
    "알나샤": "Arnage",
    "터보 R": "Turbo R",
    "컨티넨탈 R": "Continental R",
    "컨티넨탈 T": "Continental T",
    "스피드 8": "Speed 8",

    # TVR
    "그리피스": "Griffith",
    "타스카나": "Tassie",
    "사가리": "Sagate",
    "치미라": "Chimaera",
    "타스칸": "Tascan",
    "터스카나": "Tuscan",
    "타스칸 그립": "Tuscan Grip",
    "타스칸 레이스": "Tuscan Race",

    # Lotus
    "엘리제": "Elise",
    "에보라": "Evora",
    "에스프리": "Esprit",
    "엑시지": "Exige",
    "오메가": "Omega",
    "카테라": "Catera",
    "유로파": "Europa",
    "레인": "Elan",
    "엘란": "Elan",

    # Morgan
    "플러스 4": "Plus 4",
    "플러스 8": "Plus 8",
    "애로우": "Aero",
    "로드스터": "Roadster",
    "플러스 6": "Plus 6",
    "에어로 8": "Aero 8",
    "플러스 3": "Plus 3",

# ===== USA BRANDS =====

    # Ford
    "포드 F-150": "Ford F-150",
    "포드 F-250": "Ford F-250",
    "포드 F-350": "Ford F-350",
    "포드 머스탱": "Ford Mustang",
    "포드 머스탱 셸비 GT500": "Ford Mustang Shelby GT500",
    "포드 머스탱 GT": "Ford Mustang GT",
    "포드 익스플로러": "Ford Explorer",
    "포드 에스케이프": "Ford Escape",
    "포드 에코스포츠": "Ford EcoSport",
    "포드 익스페디션": "Ford Expedition",
    "포드 브롱코": "Ford Bronco",
    "포드 브롱코 스포츠": "Ford Bronco Sport",
    "포드 레인저": "Ford Ranger",
    "포드 토러스": "Ford Taurus",
    "포드 퓨전": "Ford Fusion",
    "포드 GT": "Ford GT",
    "포드 이스케이프 하이브리드": "Ford Escape Hybrid",
    "포드 머스탱 마하-E": "Ford Mustang Mach-E",
    "포드 E-150": "Ford E-150",
    "포드 E-250": "Ford E-250",
    "포드 E-350": "Ford E-350",

    # Chevrolet
    "쉐보레 실버라도 1500": "Chevrolet Silverado 1500",
    "쉐보레 실버라도 2500HD": "Chevrolet Silverado 2500HD",
    "쉐보레 실버라도 3500HD": "Chevrolet Silverado 3500HD",
    "쉐보레 카마로": "Chevrolet Camaro",
    "쉐보레 카마로 ZL1": "Chevrolet Camaro ZL1",
    "쉐보레 말리부": "Chevrolet Malibu",
    "쉐보레 타호": "Chevrolet Tahoe",
    "쉐보레 서브어반": "Chevrolet Suburban",
    "쉐보레 콜로라도": "Chevrolet Colorado",
    "쉐보레 임팔라": "Chevrolet Impala",
    "쉐보레 크루즈": "Chevrolet Cruze",
    "쉐보레 볼트 EV": "Chevrolet Bolt EV",
    "쉐보레 트래버스": "Chevrolet Traverse",
    "쉐보레 아발란체": "Chevrolet Avalanche",
    "쉐보레 SSR": "Chevrolet SSR",

    # Dodge
    "닷지 챌린저": "Dodge Challenger",
    "닷지 챌린저 SRT 헬캣": "Dodge Challenger SRT Hellcat",
    "닷지 챌린저 데몬": "Dodge Challenger Demon",
    "닷지 차저": "Dodge Charger",
    "닷지 차저 SRT 헬캣": "Dodge Charger SRT Hellcat",
    "닷지 램 1500": "Dodge Ram 1500",
    "닷지 램 2500": "Dodge Ram 2500",
    "닷지 듀랑고": "Dodge Durango",
    "닷지 바이퍼": "Dodge Viper",
    "닷지 캘리버": "Dodge Caliber",

    # Tesla
    "모델 S": "Model S",
    "모델 S 플래드": "Model S Plaid",
    "모델 3": "Model 3",
    "모델 3 롱 레인지": "Model 3 Long Range",
    "모델 X": "Model X",
    "모델 X 플래드": "Model X Plaid",
    "모델 Y": "Model Y",
    "모델 Y 퍼포먼스": "Model Y Performance",
    "로드스터": "Roadster",
    "사이버트럭": "Cybertruck",
    "테슬라 세미": "Tesla Semi",

    # Jeep
    "지프 랭글러": "Jeep Wrangler",
    "지프 랭글러 언리미티드": "Jeep Wrangler Unlimited",
    "지프 체로키": "Jeep Cherokee",
    "지프 그랜드 체로키": "Jeep Grand Cherokee",
    "지프 컴패스": "Jeep Compass",
    "지프 레니게이드": "Jeep Renegade",
    "지프 글래디에이터": "Jeep Gladiator",

    # GMC
    "GMC 시에라 1500": "GMC Sierra 1500",
    "GMC 시에라 2500HD": "GMC Sierra 2500HD",
    "GMC 시에라 3500HD": "GMC Sierra 3500HD",
    "GMC 유콘": "GMC Yukon",
    "GMC 유콘 XL": "GMC Yukon XL",
    "GMC 아카디아": "GMC Acadia",
    "GMC 카데락": "GMC Canyon",
    "GMC 터레인": "GMC Terrain",

    # Cadillac
    "캐딜락 CTS": "Cadillac CTS",
    "캐딜락 ATS": "Cadillac ATS",
    "캐딜락 XT5": "Cadillac XT5",
    "캐딜락 에스컬레이드": "Cadillac Escalade",
    "캐딜락 CT6": "Cadillac CT6",
    "캐딜락 XT6": "Cadillac XT6",
    "캐딜락 XT4": "Cadillac XT4",

    # Buick
    "뷰익 라크로스": "Buick LaCrosse",
    "뷰익 엔클레이브": "Buick Enclave",
    "뷰익 앙코르": "Buick Encore",
    "뷰익 레갈": "Buick Regal",
    "뷰익 리갈 투어X": "Buick Regal TourX",

    # Chrysler
    "크라이슬러 300": "Chrysler 300",
    "크라이슬러 퍼시피카": "Chrysler Pacifica",
    "크라이슬러 타운 & 컨트리": "Chrysler Town & Country",

    # Ram (formerly Dodge Ram)
    "램 1500": "Ram 1500",
    "램 2500": "Ram 2500",
    "램 3500": "Ram 3500",

    # Lincoln
    "링컨 MKZ": "Lincoln MKZ",
    "링컨 네비게이터": "Lincoln Navigator",
    "링컨 에비에이터": "Lincoln Aviator",
    "링컨 컨티넨탈": "Lincoln Continental",
    "링컨 MKC": "Lincoln MKC",
    "링컨 MKX": "Lincoln MKX",

    # Hummer
    "험머 H1": "Hummer H1",
    "험머 H2": "Hummer H2",
    "험머 H3": "Hummer H3",
    "험머 EV": "Hummer EV",

    # Classic American Muscle & Other
    "포드 머스탱 클래식": "Ford Mustang Classic",
    "쉐보레 코르벳 C7": "Chevrolet Corvette C7",
    "쉐보레 코르벳 C8": "Chevrolet Corvette C8",
    "쉐보레 벨에어": "Chevrolet Bel Air",
    "닷지 챌린저 클래식": "Dodge Challenger Classic",
    "닷지 바이퍼 ACR": "Dodge Viper ACR",

    # Other Electric & Specialty
    "리비안 R1T": "Rivian R1T",
    "리비안 R1S": "Rivian R1S",
    "폴스타 2": "Polestar 2",

# ===== CHINESE BRANDS =====

    # Geely
    "지리": "Geely",
    "보이링": "Boyue / Atlas",
    "엠그래프": "Emgrand",
    "아이콘": "Icon",
    "링위": "Lingrui",
    "엑스레이": "Xray",
    "엠그랜드 GT": "Emgrand GT",

    # BYD
    "BYD 한": "Han",
    "BYD 탱크": "Tank",
    "BYD 탄탄": "Tang",
    "BYD 송": "Song",
    "BYD 아이디": "e6",
    "BYD 툰": "T3",

    # NIO
    "니오 ES6": "NIO ES6",
    "니오 ES8": "NIO ES8",
    "니오 EC6": "NIO EC6",
    "니오 ET7": "NIO ET7",

    # XPeng
    "샤오펑 P7": "XPeng P7",
    "샤오펑 G3": "XPeng G3",
    "샤오펑 G9": "XPeng G9",

    # Changan
    "창안 CS75": "Changan CS75",
    "창안 CS35": "Changan CS35",
    "창안 CS55": "Changan CS55",
    "창안 CS95": "Changan CS95",

    # Great Wall
    "하발 H6": "Haval H6",
    "하발 H9": "Haval H9",
    "하발 F7": "Haval F7",
    "하발 F5": "Haval F5",

    # SAIC Motor (MG, Roewe)
    "MG ZS": "MG ZS",
    "MG HS": "MG HS",
    "MG 5": "MG 5",
    "로위 RX5": "Roewe RX5",
    "로위 i6": "Roewe i6",

    # Other Chinese Brands
    "위저우": "Wey",
    "리링": "Lynk & Co",
    "윈펑": "Wuling Hongguang",
    "광치": "GAC Trumpchi",
    "둥펑": "Dongfeng",
    "페이튼": "Foton",

# ===== INDIAN BRANDS =====

    # Maruti Suzuki
    "스위프트": "Swift",
    "디자인": "Dzire",
    "발레노": "Baleno",
    "에르티가": "Ertiga",
    "브레자": "Brezza",
    "섬플라": "Celerio",
    "어메이즈": "Amaze",
    "징크": "Ignis",
    "어비트": "Alto",
    "알토 K10": "Alto K10",
    "어센트": "S-Presso",
    "어셰라": "XL6",
    "짐니": "Jimny",
    
    # Tata Motors
    "넥손": "Nexon",
    "하리어": "Harrier",
    "티고어": "Tigor",
    "티아고": "Tiago",
    "퓨오르자": "Punch",
    "사파리": "Safari",
    "티가오": "Tiago EV",
    "알트로즈": "Altroz",
    
    # Mahindra
    "스콜피오": "Scorpio",
    "볼레로": "Bolero",
    "투볼로": "TUV300",
    "엑스UV700": "XUV700",
    "엑스UV500": "XUV500",
    "발로로 네오": "Bolero Neo",
    "마로조네": "Marazzo",
    "쥬크": "Jeep Compass",
    
    # Hyundai India
    "크레타": "Creta",
    "베뉴": "Venue",
    "엘리트 i20": "Elite i20",
    "i20": "i20",
    "아반떼": "Verna",
    "투싼": "Tucson",
    "코나": "Kona",
    
    # Kia India
    "셀토스": "Seltos",
    "셀토스 X": "Seltos X-Line",
    "소넷": "Sonet",
    "카니발": "Carnival",
    "셀토스 헤리티지": "Seltos Heritage",
    
    # Other Indian Brands
    "레노버": "Renault Kwid",
    "퀴드": "Kwid",
    "르노 트위지": "Twizy",
    "스코다": "Skoda Octavia",
    "혼다 어메이즈": "Honda Amaze",
    "혼다 시티": "Honda City",
    "혼다 WR-V": "Honda WR-V",
    "혼다 브리오": "Honda Brio",
    "혼다 어코드": "Honda Accord",

# ===== SWEDISH BRANDS =====

    # Volvo
    "S60": "S60",
    "S90": "S90",
    "V60": "V60",
    "V90": "V90",
    "XC40": "XC40",
    "XC60": "XC60",
    "XC90": "XC90",
    "C40": "C40",
    
    # Saab (defunct but iconic)
    "9-3": "9-3",
    "9-5": "9-5",
    "900": "900",
    "9000": "9000",
    
    # Polestar (Volvo performance EV brand)
    "폴스타 1": "Polestar 1",
    "폴스타 2": "Polestar 2",
    "폴스타 3": "Polestar 3",

# ===== ELECTRIC VEHICLE BRANDS =====

    # Tesla
    "모델 S": "Model S",
    "모델 3": "Model 3",
    "모델 X": "Model X",
    "모델 Y": "Model Y",

    # Rivian
    "R1T": "R1T",
    "R1S": "R1S",

    # Lucid Motors
    "루시드 에어": "Lucid Air",

    # NIO
    "니오 ES6": "NIO ES6",
    "니오 ES8": "NIO ES8",
    "니오 EC6": "NIO EC6",
    "니오 ET7": "NIO ET7",

    # XPeng
    "샤오펑 P7": "XPeng P7",
    "샤오펑 G3": "XPeng G3",
    "샤오펑 G9": "XPeng G9",

    # Fisker
    "피스커 오션": "Fisker Ocean",

    # Bollinger
    "볼린저 B1": "Bollinger B1",
    "볼린저 B2": "Bollinger B2",

    # Lordstown Motors
    "로드스타운 엔드류": "Lordstown Endurance",

    # Faraday Future
    "파라데이 퓨처 FF 91": "Faraday Future FF 91",
    
    # Other notable EVs
    "니산 리프": "Nissan Leaf",
    "쉐보레 볼트": "Chevrolet Bolt EV",
    "BMW i3": "BMW i3",
    "BMW iX": "BMW iX",
    "아우디 e-tron": "Audi e-tron",
    "포르쉐 타이칸": "Porsche Taycan"

}

MODEL_TRANSLATIONS = {

  
    "더 뉴 QM6": "The New QM6",
    "모델 3": "Model 3",
    "Q7 (4M)": "Q7 (4M)",
    "디 올 뉴 니로 EV": "De All New Niro EV",
    "더 뉴 쏘렌토": "The New Sorento",
    "2시리즈 그란쿠페 (F44)": "2 Series Gran Coupe (F44)",
    "아반떼 AD": "Avante ad",
    "더 뉴 싼타페": "The New Santa Fe",
    "그랜저 IG": "Grandeur Ig",
    "X3 (G01)": "X3 (G01)",
    "더 뉴 K9 2세대": "The New K9 2nd generation",
    "일렉트리파이드 GV70": "Electric Fide GV70",
    "더 뉴 그랜저 IG": "The New Grandeur Ig",
    "쿠퍼 클럽맨": "Cooper Club Man",
    "카니발 4세대": "Carnival 4th generation",
    "G80 (RG3)": "G80 (RG3)",
    "아이오닉5": "Ionic 5",
    "아반떼 (CN7)": "Avante (CN7)",
    "올 뉴 K7": "All New K7",
}

DIAGNOSIS_TRANSLATIONS: Dict[str, str] = {
    # --- General Status ---
    "모든 항목 정상": "Të gjitha artikujt normalë",
    "양호": "Mirë",
    "점검필요": "Nevojitet Kontroll",
    "없음": "Asnjë",
    "있음": "Ka",
    "적정": "Mjaftueshëm",
    "부족": "Pamjaftueshëm",
    "과다": "I tepërt",
    "불량": "Me defekt / I keq",

    # --- Warranty & Diagnosis Type ---
    "보험사보증": "Garanci Sigurimi",
    "자가보증": "Vetë-garanci",
    "자기진단": "Vetë-diagnostikim",

    # --- Leaks ---
    "미세누유": "Rrjedhje e lehtë vaji",
    "누유": "Rrjedhje vaji",
    "미세누수": "Rrjedhje e lehtë uji",
    "누수": "Rrjedhje uji",
    "연료누출(LP가스포함)": "Rrjedhje karburanti (përfshirë gazin)",

    # --- Repairs & Damage ---
    "판금/용접": "Llamarinë / Saldim",
    "교환": "Ndërrim (pjesë e zëvendësuar)",
    "수리필요": "Nevojitet riparim",

    # --- Engine Components (원동기) ---
    "원동기": "Motorri",
    "작동상태(공회전)": "Gjendja e punës (në rale)",
    "실린더 커버(로커암 커버)": "Kapaku i cilindrit (kapaku i valvulave)",
    "실린더 헤드 / 개스킷": "Koka e cilindrit / Guarnicioni",
    "실린더 블록 / 오일팬": "Blloku i cilindrit / Karteri i vajit",
    "오일 유량": "Sasia e vajit",
    "워터펌프": "Pompë uji",
    "라디에이터": "Radiatori",
    "냉각수 수량": "Sasia e lëngut ftohës",
    "커먼레일": "Linja e përbashkët",

    # --- Transmission (변속기) ---
    "변속기": "Transmisioni",
    "자동변속기(A/T)": "Transmision Automatik (A/T)",
    "수동변속기(M/T)": "Transmision Manual (M/T)",
    "오일유량 및 상태": "Sasia dhe gjendja e vajit",
    "기어변속장치": "Mekanizmi i ndërrimit të marsheve",

    # --- Drivetrain (동력전달) ---
    "동력전달": "Sistemi i Transmetimit",
    "클러치 어셈블리": "Sistemi i friksionit",
    "등속조인트": "Gjysëmaksi",
    "추친축 및 베어링": "Boshti i kardanit dhe kushinetat",
    "디퍼렌셜 기어": "Diferenciali",

    # --- Steering (조향) ---
    "조향": "Sistemi i Drejtimit",
    "동력조향 작동 오일 누유": "Rrjedhje vaji në sistemin e drejtimit",
    "스티어링 펌프": "Pompa e timonit",
    "스티어링 기어(MDPS포함)": "Kutia e timonit (përfshirë MDPS)",
    "스티어링 조인트": "Nyja e timonit",
    "파워고압호스": "Tubi i presionit të lartë",
    "타이로드엔드 및 볼 조인트": "Kokat e shufrës dhe nyjet sferike",

    # --- Braking (제동) ---
    "제동": "Sistemi i Frenimit",
    "브레이크 마스터 실린더오일 누유": "Rrjedhje vaji nga cilindri kryesor i frenave",
    "브레이크 오일 누유": "Rrjedhje vaji frenash",
    "배력장치 상태": "Gjendja e servo-frenave",

    # --- Electrical (전기) ---
    "전기": "Sistemi Elektrik",
    "발전기 출력": "Kapaciteti i alternatorit",
    "시동 모터": "Motorino",
    "와이퍼 모터 기능": "Funksioni i motorit të fshirëseve",
    "실내송풍 모터": "Motori i ventilatorit të kabinës",
    "라디에이터 팬 모터": "Motori i ventilatorit të radiatorit",
    "윈도우 모터": "Motori i xhamave",

    # --- High Voltage System (고전원전기장치) ---
    "고전원전기장치": "Sistemi elektrik i tensionit të lartë",
    "충전구 절연 상태": "Gjendja e izolimit të portës së karikimit",
    "구동축전지 격리 상태": "Gjendja e izolimit të baterisë kryesore",
    "고전원전기배선 상태(접속단자, 피복, 보호기구)": "Gjendja e kabllove të tensionit të lartë",

    # --- Body Panels (외장) ---
    "후드": "Kapaku i motorit",
    "프론트 휀더(좌)": "Parafango e përparme (majtas)",
    "프론트 휀더(우)": "Parafango e përparme (djathtas)",
    "프론트 도어(좌)": "Dera e përparme (majtas)",
    "프론트 도어(우)": "Dera e përparme (djathtas)",
    "리어 도어(좌)": "Dera e pasme (majtas)",
    "리어 도어(우)": "Dera e pasme (djathtas)",
    "트렁크 리드": "Kapaku i bagazhit",
    "쿼터 패널(좌)": "Paneli anësor i pasmë (majtas)",
    "쿼터 패널(우)": "Paneli anësor i pasmë (djathtas)",
    "루프 패널": "Paneli i çatisë",
    "사이드실 패널(좌)": "Pragu anësor (majtas)",
    "사이드실 패널(우)": "Pragu anësor (djathtas)",
    "프론트 패널": "Paneli i përparmë",
    "리어 패널": "Paneli i pasmë",
    "라디에이터 서포트(볼트체결부품)": "Mbështetësja e radiatorit",
}

SALE_TYPE_TRANSLATIONS = {
    "일반": "Standard Sale",
    "일반": "Standard Sale",
    "경매": "Auction",
    "딜러": "Dealer",
    "개인": "Private",
}

DIAGNOSIS_RESULT_TRANSLATIONS = {

}

SELLER_COMMENT_TRANSLATIONS = {
    "수리필요": "Nevojitet riparim",
    "사고차": "Makina e aksidentuar",
    "정비이력": "Historia e mirëmbajtjes",
    "차량상태": "Gjendja e automjetit",
}

def save_new_translations_to_file(new_translations: dict):
    """Saves newly discovered translatable terms to a timestamped file for review."""
    
    # Filter out any empty categories
    non_empty_translations = {
        category: terms for category, terms in new_translations.items() if terms
    }
    
    if not non_empty_translations:
        return

    os.makedirs(DATA_DIR, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(DATA_DIR, f"new_translations_{timestamp}.json")
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(non_empty_translations, f, ensure_ascii=False, indent=4)
        print(f"INFO: New translations saved to {filename}")
    except Exception as e:
        print(f"ERROR: Could not save new translations: {e}")