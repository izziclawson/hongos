"""
Mushroom dose calculation logic
Handles different mushroom types, strains, and dosage levels
"""

# Strain potency database (psilocybin content estimates in mg per gram dried weight)
STRAIN_POTENCIES = {
    # Popular strains with known potencies
    'golden teacher': 6.0,
    'b+': 5.5,
    'penis envy': 11.0,
    'albino penis envy': 12.0,
    'liberty cap': 8.0,
    'blue meanie': 9.0,
    'mazatapec': 5.0,
    'cambodian': 7.0,
    'thai': 6.5,
    'ecuador': 6.0,
    'mexican': 5.5,
    'hawaiian': 7.5,
    'treasure coast': 6.5,
    'amazon': 6.0,
    'albino a+': 8.0,
    'trinity': 10.0,
    'tidal wave': 10.5,
    'ghost': 7.5,
    'jedi mind fuck': 8.5,
    'white rabbit': 9.0,
    'rusty whyte': 7.0,
    'great white monster': 8.5,
    'albino louisiana': 7.5,
    'alcabenzi': 6.5,
    'costa rican': 6.0,
    'puerto rican': 7.0,
    'orissa india': 7.0,
    'pink buffalo': 6.5,
    'redboy': 7.5,
    'syzygy': 9.5,
    'pf classic': 5.5,
    'golden mammoth': 7.0,
    'south african transkei': 8.0,
    'mckennaii': 8.5,
    'natal super strength': 9.5,
    'enigma': 12.5
}

# General potency categories
POTENCY_CATEGORIES = {
    'mild': 5.0,      # Low potency strains
    'standard': 7.0,  # Average potency strains  
    'strong': 10.0    # High potency strains
}

# Dose levels in grams (dried weight) - based on your specifications
DOSE_LEVELS = {
    'micro': 0.3,    # 0.1-0.5 grams dried (using middle value)
    'low': 1.0,      # 0.5-1.5 grams dried (using middle value) 
    'normal': 2.5,   # 2-3 grams dried (using middle value)
    'high': 4.25     # 3.5-5 grams dried (using middle value)
}

# Conversion factors
FRESH_TO_DRIED_RATIO = 10  # Fresh mushrooms are ~90% water
TRUFFLE_POTENCY_FACTOR = 0.3  # Truffles are generally 30% as potent as dried mushrooms


def normalize_strain_name(strain_name):
    """
    Normalize strain name for lookup
    Handles spaces, capitalization, and common variations
    """
    if not strain_name:
        return None
    
    # Convert to lowercase and strip whitespace
    normalized = strain_name.lower().strip()
    
    # Handle common abbreviations and variations
    variations = {
        'pe': 'penis envy',
        'ape': 'albino penis envy',
        'gt': 'golden teacher',
        'jmf': 'jedi mind fuck',
        'tat': 'south african transkei',
        'gwm': 'great white monster',
        'nss': 'natal super strength'
    }
    
    if normalized in variations:
        return variations[normalized]
    
    return normalized


def get_strain_potency(strain_input):
    """
    Get potency value for a given strain or potency category
    Returns potency in mg psilocybin per gram dried weight
    """
    if not strain_input:
        return POTENCY_CATEGORIES['standard']
    
    strain_lower = strain_input.lower().strip()
    
    # Check if it's a potency category
    if strain_lower in POTENCY_CATEGORIES:
        return POTENCY_CATEGORIES[strain_lower]
    
    # Check if it's a specific strain
    normalized_strain = normalize_strain_name(strain_input)
    if normalized_strain and normalized_strain in STRAIN_POTENCIES:
        return STRAIN_POTENCIES[normalized_strain]
    
    # Default to standard potency if strain not found
    return POTENCY_CATEGORIES['standard']


def get_weight_factor(weight_kg):
    """
    Calculate weight adjustment factor with bell curve
    115-250kg: no adjustment (factor = 1.0)
    Below 115kg: gradually decrease to 0.8 at 80kg and below
    Above 250kg: gradually increase to 1.3 at 400kg and above
    """
    if 115 <= weight_kg <= 250:
        return 1.0
    elif weight_kg < 115:
        # Linear decrease from 1.0 at 115kg to 0.8 at 80kg
        if weight_kg <= 80:
            return 0.8
        return 0.8 + (weight_kg - 80) * (1.0 - 0.8) / (115 - 80)
    else:  # weight_kg > 250
        # Linear increase from 1.0 at 250kg to 1.3 at 400kg
        if weight_kg >= 400:
            return 1.3
        return 1.0 + (weight_kg - 250) * (1.3 - 1.0) / (400 - 250)


def calculate_dose(mushroom_type, dose_level, strain_input, weight_kg):
    """
    Calculate mushroom dose based on parameters
    
    Args:
        mushroom_type: 'fresh', 'dried', or 'truffles'
        dose_level: 'micro', 'low', 'normal', or 'high'
        strain_input: strain name or potency category
        weight_kg: user body weight in kilograms
    
    Returns:
        dict with dose information
    """
    # Get base dose in grams dried
    base_dose_dried = DOSE_LEVELS[dose_level]
    
    # Apply weight adjustment with bell curve
    weight_factor = get_weight_factor(weight_kg)
    adjusted_dose_dried = base_dose_dried * weight_factor
    
    # Get strain potency category for display
    strain_potency_value = get_strain_potency(strain_input)
    if strain_potency_value <= 6.0:
        potency_category = 'mild'
    elif strain_potency_value >= 9.0:
        potency_category = 'strong'
    else:
        potency_category = 'standard'
    
    # Apply potency adjustment
    potency_factor = strain_potency_value / POTENCY_CATEGORIES['standard']  # 7.0 is standard
    final_dose_dried = adjusted_dose_dried * potency_factor
    
    # Convert based on mushroom type
    if mushroom_type == 'fresh':
        final_weight = final_dose_dried * FRESH_TO_DRIED_RATIO
        weight_unit = 'grams fresh'
    elif mushroom_type == 'dried':
        final_weight = final_dose_dried
        weight_unit = 'grams dried'
    elif mushroom_type == 'truffles':
        # Truffles are less potent and measured fresh
        final_weight = (final_dose_dried / TRUFFLE_POTENCY_FACTOR) * FRESH_TO_DRIED_RATIO
        weight_unit = 'grams fresh truffles'
    else:
        raise ValueError(f"Unknown mushroom type: {mushroom_type}")
    
    # Determine if strain was found in database
    normalized_strain = normalize_strain_name(strain_input)
    strain_found = normalized_strain and normalized_strain in STRAIN_POTENCIES
    
    return {
        'dose_grams': round(final_weight, 2),
        'weight_unit': weight_unit,
        'potency_category': potency_category,
        'strain_found': strain_found,
        'normalized_strain': normalized_strain or strain_input,
        'weight_factor': round(weight_factor, 2)
    }


def get_available_strains():
    """
    Get list of all available strains in the database
    """
    return sorted(STRAIN_POTENCIES.keys())


def get_dose_description(dose_level):
    """
    Get description for each dose level
    """
    descriptions = {
        'micro': 'Sub-perceptual dose for enhanced mood and focus',
        'low': 'Light effects, mild euphoria, enhanced creativity',
        'normal': 'Moderate psychedelic effects, visual enhancement',
        'high': 'Strong psychedelic experience, intense visuals'
    }
    return descriptions.get(dose_level, '')


def pounds_to_kg(pounds):
    """Convert pounds to kilograms"""
    return pounds * 0.453592


def kg_to_pounds(kg):
    """Convert kilograms to pounds"""
    return kg * 2.20462
