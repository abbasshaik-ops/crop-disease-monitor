## utils/remedies.py

DISEASE_REMEDIES = {
    # --- TOMATO ---
    "Tomato_Early_Blight": {
        "crop": "Tomato",
        "disease_name": "Early Blight (Alternaria solani)",
        "severity": "Moderate to High",
        "chemical_medicine": "Mancozeb 75 WP (2 g/L) or Chlorothalonil foliar spray.",
        "organic_remedy": "Copper oxychloride spray or Neem oil (5 ml/L) with Trichoderma viride soil enrichment.",
        "prevention": "Stake plants for airflow, avoid overhead watering, and rotate crops for 2-3 years."
    },
    "Tomato_Late_Blight": {
        "crop": "Tomato",
        "disease_name": "Late Blight (Phytophthora infestans)",
        "severity": "Critical",
        "chemical_medicine": "Metalaxyl + Mancozeb (2.5 g/L) or Cymoxanil + Mancozeb at first symptom appearance.",
        "organic_remedy": "Bordeaux mixture (1%) or copper-based bio-fungicide.",
        "prevention": "Destroy infected plant debris immediately, ensure wide plant spacing, and plant certified disease-free seedlings."
    },

    # --- BRINJAL ---
    "brinjal_healthy_leaf": {
        "crop": "Brinjal (Eggplant)",
        "disease_name": "Healthy Leaf (No Disease Detected)",
        "severity": "None",
        "chemical_medicine": "No chemical treatment required.",
        "organic_remedy": "Continue balanced vermicompost application and regular watering.",
        "prevention": "Monitor undersides of leaves weekly for early pest activity."
    },
    "brinjal_insect_pest_disease": {
        "crop": "Brinjal (Eggplant)",
        "disease_name": "Insect Pest Infestation (Shoot/Fruit Borer & Leaf Feeders)",
        "severity": "High",
        "chemical_medicine": "Emamectin benzoate 5 SG (0.4 g/L) or Spinosad 45 SC (0.3 ml/L).",
        "organic_remedy": "Azadirachtin (Neem oil 1500 ppm at 3-5 ml/L) and Bacillus thuringiensis (Bt) spray.",
        "prevention": "Install pheromone traps (5/acre) and clip off damaged shoots early."
    },
    "brinjal_leaf_spot_disease": {
        "crop": "Brinjal (Eggplant)",
        "disease_name": "Cercospora / Alternaria Leaf Spot",
        "severity": "Moderate",
        "chemical_medicine": "Carbendazim 50 WP (1 g/L) or Mancozeb 75 WP (2 g/L).",
        "organic_remedy": "Pseudomonas fluorescens foliar spray (10 g/L) and removal of lower infected leaves.",
        "prevention": "Avoid waterlogging and practice crop rotation with non-solanaceous crops."
    },
    "brinjal_mosaic_virus": {
        "crop": "Brinjal (Eggplant)",
        "disease_name": "Brinjal Mosaic Virus",
        "severity": "High",
        "chemical_medicine": "No direct cure; spray Imidacloprid 17.8 SL (0.5 ml/L) to control aphid/whitefly vectors.",
        "organic_remedy": "Neem oil (5 ml/L) + yellow sticky traps to reduce insect vector population.",
        "prevention": "Uproot and burn infected plants immediately; sanitize pruning tools."
    },
    "brinjal_small_leaf": {
        "crop": "Brinjal (Eggplant)",
        "disease_name": "Little Leaf of Brinjal (Phytoplasma)",
        "severity": "High",
        "chemical_medicine": "Dimethoate 30 EC (1.5 ml/L) or Thiamethoxam to control leafhopper vectors.",
        "organic_remedy": "Neem seed kernel extract (5%) and removal of weed hosts around field bunds.",
        "prevention": "Rogue out infected plants early and use resistant varieties."
    },
    "brinjal_white_mold": {
        "crop": "Brinjal (Eggplant)",
        "disease_name": "White Mold / Sclerotinia Rot (Sclerotinia sclerotiorum)",
        "severity": "High",
        "chemical_medicine": "Carbendazim 50 WP (1 g/L) or Thiophanate-methyl foliar and stem base drench.",
        "organic_remedy": "Soil application of Trichoderma harzianum enriched compost.",
        "prevention": "Improve air circulation, reduce dense canopy humidity, and deep-plow after harvest."
    },
    "brinjal_wilt_disease": {
        "crop": "Brinjal (Eggplant)",
        "disease_name": "Bacterial / Fusarium Wilt",
        "severity": "Critical",
        "chemical_medicine": "Copper oxychloride (3 g/L) soil drenching around root zone.",
        "organic_remedy": "Bio-priming seedlings with Pseudomonas fluorescens and Trichoderma viride.",
        "prevention": "Ensure well-drained raised beds and avoid planting in wilt-history plots."
    },

    # --- GROUNDNUT ---
    "groundnut_earlyleafspot": {
        "crop": "Groundnut",
        "disease_name": "Early Leaf Spot / Tikka (Cercospora arachidicola)",
        "severity": "Moderate",
        "chemical_medicine": "Carbendazim 50 WP (1 g/L) or Mancozeb 75 WP (2 g/L) starting 30 days after sowing.",
        "organic_remedy": "Neem leaf extract (5%) or Trichoderma viride seed treatment.",
        "prevention": "Deep bury crop residues after harvest and rotate with cereals."
    },
    "groundnut_healthy": {
        "crop": "Groundnut",
        "disease_name": "Healthy Leaf (No Disease Detected)",
        "severity": "None",
        "chemical_medicine": "No chemical treatment required.",
        "organic_remedy": "Apply gypsum (200 kg/acre) at flowering stage for healthy pod development.",
        "prevention": "Maintain weed-free rows and proper soil moisture."
    },
    "groundnut_lateleafspot": {
        "crop": "Groundnut",
        "disease_name": "Late Leaf Spot (Phaeoisariopsis personata)",
        "severity": "High",
        "chemical_medicine": "Chlorothalonil 75 WP (2 g/L) or Hexaconazole 5 EC (1 ml/L).",
        "organic_remedy": "Pseudomonas fluorescens foliar spray and botanical extracts.",
        "prevention": "Remove volunteer groundnut plants and use resistant varieties."
    },
    "groundnut_nutritiondeficiency": {
        "crop": "Groundnut",
        "disease_name": "Nutrient Deficiency (Iron / Nitrogen / Magnesium Chlorosis)",
        "severity": "Low to Moderate",
        "chemical_medicine": "Foliar spray of 0.5% Ferrous Sulphate + 0.1% Citric Acid (for iron chlorosis) or 19:19:19 NPK (5 g/L).",
        "organic_remedy": "Apply enriched farmyard manure, Rhizobium biofertilizer, and humic acid.",
        "prevention": "Conduct soil pH testing before sowing and apply balanced micronutrients."
    },
    "groundnut_rust": {
        "crop": "Groundnut",
        "disease_name": "Groundnut Rust (Puccinia arachidis)",
        "severity": "High",
        "chemical_medicine": "Hexaconazole 5 EC (1 ml/L) or Mancozeb 75 WP (2 g/L).",
        "organic_remedy": "Wettable sulphur (2 g/L) or Neem oil spray at early pustule stage.",
        "prevention": "Avoid continuous groundnut cropping and destroy crop debris."
    },

    # --- MANGO ---
    "mango Anthracnose": {
        "crop": "Mango",
        "disease_name": "Mango Anthracnose (Colletotrichum gloeosporioides)",
        "severity": "High",
        "chemical_medicine": "Carbendazim 50 WP (1 g/L) or Propiconazole 25 EC (1 ml/L) during flowering and fruit set.",
        "organic_remedy": "Copper oxychloride spray (3 g/L); post-harvest hot water dip at 52°C for 10 mins.",
        "prevention": "Prune dead twigs and overcrowded branches to allow sunlight penetration."
    },
    "mango Bacterial Canker": {
        "crop": "Mango",
        "disease_name": "Bacterial Canker (Xanthomonas citri pv. mangiferaeindicae)",
        "severity": "High",
        "chemical_medicine": "Streptocycline (0.3 g/L) + Copper oxychloride (3 g/L) at 15-day intervals.",
        "organic_remedy": "Bordeaux mixture (1%) spray after pruning affected twigs.",
        "prevention": "Use windbreaks in orchards and sanitize pruning shears between trees."
    },
    "mango Cutting Weevil": {
        "crop": "Mango",
        "disease_name": "Mango Leaf-Cutting Weevil (Deporaus marginatus)",
        "severity": "Moderate",
        "chemical_medicine": "Lambda-cyhalothrin 5 EC (1 ml/L) or Quinalphos 25 EC (2 ml/L) during new flush.",
        "organic_remedy": "Azadirachtin (Neem oil 5 ml/L) sprayed on tender new leaf flushes.",
        "prevention": "Collect and destroy fallen cut leaves containing weevil eggs/larvae."
    },
    "mango Die Back": {
        "crop": "Mango",
        "disease_name": "Mango Die Back (Lasiodiplodia theobromae)",
        "severity": "Critical",
        "chemical_medicine": "Prune 10 cm below dried tissue and spray Carbendazim (1 g/L) or Thiophanate-methyl.",
        "organic_remedy": "Apply Bordeaux paste on cut branch ends.",
        "prevention": "Maintain orchard irrigation during dry spells and avoid root injury."
    },
    "mango Gall Midge": {
        "crop": "Mango",
        "disease_name": "Mango Leaf Gall Midge (Procontarinia matteiana)",
        "severity": "Moderate",
        "chemical_medicine": "Dimethoate 30 EC (1.5 ml/L) or Thiamethoxam 25 WG (0.3 g/L) at bud burst.",
        "organic_remedy": "Neem oil (5 ml/L) and raking soil under the canopy to expose pupae.",
        "prevention": "Prune heavily galled leaves and maintain clean orchard floor."
    },
    "mango Healthy": {
        "crop": "Mango",
        "disease_name": "Healthy Leaf (No Disease Detected)",
        "severity": "None",
        "chemical_medicine": "No chemical treatment required.",
        "organic_remedy": "Apply organic compost around drip line after monsoon.",
        "prevention": "Regular canopy pruning and annual orchard sanitation."
    },
    "mango Powdery Mildew": {
        "crop": "Mango",
        "disease_name": "Powdery Mildew (Oidium mangiferae)",
        "severity": "High",
        "chemical_medicine": "Wettable Sulphur (2 g/L) or Hexaconazole 5 EC (1 ml/L) at panicle emergence.",
        "organic_remedy": "Potassium bicarbonate spray or diluted milk/whey foliar spray in early stages.",
        "prevention": "Prune dense inner branches to improve air movement through the tree."
    },
    "mango Sooty Mould": {
        "crop": "Mango",
        "disease_name": "Sooty Mould (Capnodium mangiferae)",
        "severity": "Low to Moderate",
        "chemical_medicine": "Control sap-sucking hoppers/scales first using Imidacloprid (0.5 ml/L), then spray Wettable Sulphur (2 g/L).",
        "organic_remedy": "Starch solution (2% boiled maida/starch) spray—flakes off the black fungal coating as it dries.",
        "prevention": "Manage mango hoppers and mealybugs early to stop honeydew secretion."
    },

    # --- RICE (PADDY) ---
    "rice_healthy": {
        "crop": "Rice (Paddy)",
        "disease_name": "Healthy Leaf (No Disease Detected)",
        "severity": "None",
        "chemical_medicine": "No chemical treatment required.",
        "organic_remedy": "Maintain shallow water level (2-5 cm) and split nitrogen application.",
        "prevention": "Periodic field bund cleaning and balanced potassium nutrition."
    },
    "rice_sheath_blight": {
        "crop": "Rice (Paddy)",
        "disease_name": "Rice Sheath Blight (Rhizoctonia solani)",
        "severity": "High",
        "chemical_medicine": "Hexaconazole 5 EC (2 ml/L) or Validamycin 3 L (2 ml/L) directed at plant base.",
        "organic_remedy": "Pseudomonas fluorescens (10 g/L) foliar/sheath spray and Trichoderma soil application.",
        "prevention": "Avoid excess nitrogen fertilizer, use wider hill spacing, and drain excess water."
    },

    # --- SUGARCANE ---
    "sugarcane_healthy": {
        "crop": "Sugarcane",
        "disease_name": "Healthy Leaf (No Disease Detected)",
        "severity": "None",
        "chemical_medicine": "No chemical treatment required.",
        "organic_remedy": "Trash mulching between rows to conserve soil moisture.",
        "prevention": "Proper earthing up and balanced NPK fertilization."
    },
    "sugarcane_mosiac": {
        "crop": "Sugarcane",
        "disease_name": "Sugarcane Mosaic Virus (SCMV)",
        "severity": "High",
        "chemical_medicine": "No direct viral cure; control aphid vectors with Imidacloprid 17.8 SL (0.5 ml/L).",
        "organic_remedy": "Neem oil (5 ml/L) and rogueing out infected clumps early.",
        "prevention": "Plant virus-free tissue-cultured seed setts and eliminate grassy weeds."
    },
    "sugarcane_reddot": {
        "crop": "Sugarcane",
        "disease_name": "Red Rot / Red Leaf Spot (Colletotrichum falcatum)",
        "severity": "Critical",
        "chemical_medicine": "Dip seed setts in Carbendazim 50 WP (1 g/L) for 15 minutes before planting.",
        "organic_remedy": "Bio-priming setts with Pseudomonas fluorescens and Trichoderma viride.",
        "prevention": "Uproot affected clumps immediately, avoid ratooning diseased fields, and improve drainage."
    },
    "sugarcane_rust": {
        "crop": "Sugarcane",
        "disease_name": "Sugarcane Rust (Puccinia melanocephala)",
        "severity": "Moderate to High",
        "chemical_medicine": "Mancozeb 75 WP (2 g/L) or Propiconazole 25 EC (1 ml/L).",
        "organic_remedy": "Remove heavily rusted lower leaves and apply sulphur-based fungicide.",
        "prevention": "Avoid excessive late nitrogen doses and plant rust-resistant varieties."
    },
    "sugarcane_yellow": {
        "crop": "Sugarcane",
        "disease_name": "Sugarcane Yellow Leaf Disease (SCYLV)",
        "severity": "High",
        "chemical_medicine": "Control sugarcane aphid vectors using Thiamethoxam 25 WG (0.3 g/L).",
        "organic_remedy": "Neem oil spray and foliar micronutrient boost (iron + zinc) to support vigor.",
        "prevention": "Use disease-free seed cane and hot-water/aerated-steam sett treatment."
    }
}

def get_remedy(class_label: str) -> dict:
    return DISEASE_REMEDIES.get(
        class_label,
        {
            "crop": "Regional Crop",
            "disease_name": class_label.replace("_", " "),
            "severity": "Consult Local Agronomist",
            "chemical_medicine": "Recommended local agricultural extension fungicide/bactericide.",
            "organic_remedy": "Neem-based formulation (3-5 ml/L).",
            "prevention": "Isolate affected crops and maintain field sanitation."
        }
    )
