"""
Streamlit web interface for mushroom dose calculator
Provides user-friendly interface for calculating appropriate mushroom doses
"""

import streamlit as st
from shroomies import (
    calculate_dose, 
    get_available_strains, 
    get_dose_description,
    pounds_to_kg,
    POTENCY_CATEGORIES
)

# Language translations
TRANSLATIONS = {
    'en': {
        'title': '🍄 Shroomies Dose Calculator',
        'description': 'Calculate appropriate mushroom doses based on your body weight, desired experience level, and strain potency. This calculator provides educational estimates only.',
        'disclaimer_title': '⚠️ Important Disclaimer',
        'disclaimer_text': '''**This calculator is for educational purposes only.**

- Always start with lower doses, especially with new strains
- Set and setting are crucial for safe experiences
- Never drive or operate machinery
- Consult healthcare providers if you have medical conditions
- Psilocybin mushrooms are controlled substances in many jurisdictions
- Individual sensitivity varies greatly''',
        'dose_calc': '📝 Dose Calculation',
        'mushroom_type': 'Mushroom Type',
        'mushroom_type_help': 'Select the form of mushrooms you have',
        'experience_level': 'Desired Experience Level',
        'experience_help': 'Choose your desired intensity level',
        'weight_unit': 'Weight Unit',
        'weight_kg': 'Your Weight (kg)',
        'weight_lbs': 'Your Weight (lbs)',
        'weight_help_kg': 'Enter your body weight in kilograms',
        'weight_help_lbs': 'Enter your body weight in pounds',
        'strain_selection': '🧬 Strain Selection',
        'strain_method': 'How would you like to specify the strain?',
        'general_potency': 'General Potency Level',
        'specific_strain': 'Specific Strain Name',
        'strain_method_help': 'Choose whether to use general potency categories or specify an exact strain',
        'potency_level': 'Potency Level',
        'potency_help': 'Select general potency category if you don\'t know the specific strain',
        'strain_name': 'Strain Name',
        'strain_placeholder': 'e.g., Golden Teacher, Penis Envy, B+',
        'strain_help': 'Enter the specific strain name (spaces are handled automatically)',
        'show_strains': 'Show Available Strains',
        'available_strains': '📋 Available Strains in Database',
        'hide_strains': 'Hide Strains',
        'calculate_btn': '🧮 Calculate Dose',
        'results_title': '📊 Calculation Results',
        'recommended_dose': 'Recommended Dose',
        'target_psilocybin': 'Target Psilocybin',
        'your_weight': 'Your Weight',
        'strain_potency': 'Strain Potency',
        'experience_level_metric': 'Experience Level',
        'strain_found': '✅ Strain **{strain}** found in database',
        'strain_not_found': '⚠️ Strain **{strain}** not found in database. Using standard potency estimate.',
        'additional_guidance': '💡 Additional Guidance',
        'guidance_text': '''**For {dose_level} dose with {mushroom_type} {strain_input}:**

- **Start time**: Effects typically begin 20-60 minutes after consumption
- **Duration**: {duration}
- **Setting**: Ensure you're in a safe, comfortable environment
- **Integration**: Consider keeping a journal of your experience

**Safety reminders:**
- Start with a lower dose if you're inexperienced
- Have a trusted person available if needed
- Stay hydrated and have light snacks available
- Avoid mixing with other substances*

*Note: Some combinations may be beneficial when done mindfully and with proper research.''',
        'footer': '🍄 Shroomies Calculator | For educational purposes only<br>Always research thoroughly and prioritize safety',
        'enter_strain': 'Please enter a strain name or select a potency level.',
        'calc_error': 'Error calculating dose: {error}',
        'language': 'Language / Idioma'
    },
    'es': {
        'title': '🍄 Calculadora de Dosis Shroomies',
        'description': 'Calcula dosis apropiadas de hongos basándose en tu peso corporal, nivel de experiencia deseado y potencia de la cepa. Esta calculadora proporciona estimados educativos únicamente.',
        'disclaimer_title': '⚠️ Descargo de Responsabilidad Importante',
        'disclaimer_text': '''**Esta calculadora es solo para fines educativos.**

- Siempre comienza con dosis menores, especialmente con cepas nuevas
- El entorno y mentalidad son cruciales para experiencias seguras
- Nunca manejes o operes maquinaria
- Consulta proveedores de salud si tienes condiciones médicas
- Los hongos psilocibinos son sustancias controladas en muchas jurisdicciones
- La sensibilidad individual varía enormemente''',
        'dose_calc': '📝 Cálculo de Dosis',
        'mushroom_type': 'Tipo de Hongo',
        'mushroom_type_help': 'Selecciona la forma de hongos que tienes',
        'experience_level': 'Nivel de Experiencia Deseado',
        'experience_help': 'Elige tu nivel de intensidad deseado',
        'weight_unit': 'Unidad de Peso',
        'weight_kg': 'Tu Peso (kg)',
        'weight_lbs': 'Tu Peso (lbs)',
        'weight_help_kg': 'Ingresa tu peso corporal en kilogramos',
        'weight_help_lbs': 'Ingresa tu peso corporal en libras',
        'strain_selection': '🧬 Selección de Cepa',
        'strain_method': '¿Cómo te gustaría especificar la cepa?',
        'general_potency': 'Nivel de Potencia General',
        'specific_strain': 'Nombre de Cepa Específica',
        'strain_method_help': 'Elige si usar categorías generales de potencia o especificar una cepa exacta',
        'potency_level': 'Nivel de Potencia',
        'potency_help': 'Selecciona categoría general de potencia si no conoces la cepa específica',
        'strain_name': 'Nombre de Cepa',
        'strain_placeholder': 'ej., Golden Teacher, Penis Envy, B+',
        'strain_help': 'Ingresa el nombre específico de la cepa (espacios se manejan automáticamente)',
        'show_strains': 'Mostrar Cepas Disponibles',
        'available_strains': '📋 Cepas Disponibles en Base de Datos',
        'hide_strains': 'Ocultar Cepas',
        'calculate_btn': '🧮 Calcular Dosis',
        'results_title': '📊 Resultados del Cálculo',
        'recommended_dose': 'Dosis Recomendada',
        'target_psilocybin': 'Psilocibina Objetivo',
        'your_weight': 'Tu Peso',
        'strain_potency': 'Potencia de Cepa',
        'experience_level_metric': 'Nivel de Experiencia',
        'strain_found': '✅ Cepa **{strain}** encontrada en base de datos',
        'strain_not_found': '⚠️ Cepa **{strain}** no encontrada en base de datos. Usando estimado de potencia estándar.',
        'additional_guidance': '💡 Guía Adicional',
        'guidance_text': '''**Para dosis {dose_level} con {mushroom_type} {strain_input}:**

- **Tiempo de inicio**: Los efectos típicamente comienzan 20-60 minutos después del consumo
- **Duración**: {duration}
- **Entorno**: Asegúrate de estar en un ambiente seguro y cómodo
- **Integración**: Considera mantener un diario de tu experiencia

**Recordatorios de seguridad:**
- Comienza con una dosis menor si eres inexperto
- Ten una persona de confianza disponible si es necesario
- Mantente hidratado y ten bocadillos ligeros disponibles
- Evita mezclar con otras sustancias*

*Nota: Algunas combinaciones pueden ser beneficiosas cuando se hacen conscientemente y con investigación apropiada.''',
        'footer': '🍄 Calculadora Shroomies | Solo para fines educativos<br>Siempre investiga a fondo y prioriza la seguridad',
        'enter_strain': 'Por favor ingresa un nombre de cepa o selecciona un nivel de potencia.',
        'calc_error': 'Error calculando dosis: {error}',
        'language': 'Language / Idioma'
    }
}

def main():
    # Page configuration
    st.set_page_config(
        page_title="Shroomies Dose Calculator",
        page_icon="🍄",
        layout="centered"
    )
    
    # Initialize session state for language
    if 'language' not in st.session_state:
        st.session_state.language = 'en'
    
    # Language selector in sidebar with globe icon
    with st.sidebar:
        language = st.selectbox(
            "🌐 Language / Idioma",
            options=['en', 'es'],
            index=0 if st.session_state.language == 'en' else 1,
            format_func=lambda x: "English" if x == 'en' else "Español (PR)"
        )
        st.session_state.language = language
    
    # Get translations for current language
    t = TRANSLATIONS[st.session_state.language]
    
    # Main title and description
    st.title(t['title'])
    st.markdown(t['description'])
    
    # Disclaimer
    with st.expander(t['disclaimer_title']):
        st.warning(t['disclaimer_text'])
    
    st.markdown("---")
    
    # Input form
    st.header(t['dose_calc'])
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Mushroom type selection
        mushroom_type = st.selectbox(
            t['mushroom_type'],
            options=['dried', 'fresh', 'truffles'],
            format_func=lambda x: x.title(),
            help=t['mushroom_type_help']
        )
        
        # Dose level selection
        dose_level = st.selectbox(
            t['experience_level'],
            options=['micro', 'low', 'normal', 'high'],
            index=1,  # Default to 'low'
            format_func=lambda x: x.title(),
            help=t['experience_help']
        )
        
        # Show dose level description
        if dose_level:
            st.info(get_dose_description(dose_level))
    
    with col2:
        # Weight input with unit selection
        weight_unit = st.selectbox(t['weight_unit'], ['kg', 'lbs'])
        
        if weight_unit == 'kg':
            weight_input = st.number_input(
                t['weight_kg'],
                min_value=20.0,
                max_value=200.0,
                value=70.0,
                step=0.5,
                help=t['weight_help_kg']
            )
            weight_kg = weight_input
        else:
            weight_input = st.number_input(
                t['weight_lbs'],
                min_value=44.0,
                max_value=440.0,
                value=154.0,
                step=1.0,
                help=t['weight_help_lbs']
            )
            weight_kg = pounds_to_kg(weight_input)
    
    st.markdown("---")
    
    # Strain input section
    st.subheader(t['strain_selection'])
    
    # Radio button for strain input method
    strain_method = st.radio(
        t['strain_method'],
        options=['general_potency', 'specific_strain'],
        format_func=lambda x: t['general_potency'] if x == 'general_potency' else t['specific_strain'],
        help=t['strain_method_help']
    )
    
    if strain_method == 'general_potency':
        # General potency selection
        potency_level = st.selectbox(
            t['potency_level'],
            options=['mild', 'standard', 'strong'],
            index=1,  # Default to 'standard'
            format_func=lambda x: x.title(),
            help=t['potency_help']
        )
        strain_input = potency_level
        
        # Simplified potency info - removed exact mg values for new users
        if st.session_state.language == 'en':
            potency_descriptions = {
                'mild': 'Lower potency strains - good for beginners',
                'standard': 'Average potency strains - most common',
                'strong': 'Higher potency strains - more experienced users'
            }
        else:
            potency_descriptions = {
                'mild': 'Cepas de menor potencia - buenas para principiantes',
                'standard': 'Cepas de potencia promedio - más comunes',
                'strong': 'Cepas de mayor potencia - usuarios más experimentados'
            }
        
        st.info(f"**{potency_level.title()}**: {potency_descriptions[potency_level]}")
        
    else:
        # Specific strain input
        col1, col2 = st.columns([3, 1])
        
        with col1:
            strain_input = st.text_input(
                t['strain_name'],
                placeholder=t['strain_placeholder'],
                help=t['strain_help']
            )
        
        with col2:
            if st.button(t['show_strains']):
                st.session_state.show_strains = True
        
        # Show available strains if requested
        if st.session_state.get('show_strains', False):
            with st.expander(t['available_strains'], expanded=True):
                strains = get_available_strains()
                
                # Display strains in columns
                num_cols = 3
                cols = st.columns(num_cols)
                
                for i, strain in enumerate(strains):
                    col_idx = i % num_cols
                    with cols[col_idx]:
                        st.write(f"• {strain.title()}")
                
                if st.button(t['hide_strains']):
                    st.session_state.show_strains = False
                    st.rerun()
    
    st.markdown("---")
    
    # Calculate button and results
    if st.button(t['calculate_btn'], type="primary"):
        if strain_input:
            try:
                # Calculate the dose
                result = calculate_dose(mushroom_type, dose_level, strain_input, weight_kg)
                
                # Display results with primary focus on dose
                st.header(t['results_title'])
                
                # Large, prominent result display
                st.markdown(f"""
                <div style='text-align: center; padding: 2rem; background-color: rgba(0, 255, 0, 0.1); border-radius: 10px; margin: 1rem 0;'>
                    <h1 style='color: #00ff00; font-size: 3rem; margin: 0;'>{result['dose_grams']} {result['weight_unit']}</h1>
                    <h2 style='color: #ffffff; margin: 0.5rem 0;'>{t['recommended_dose']}</h2>
                </div>
                """, unsafe_allow_html=True)
                
                # Small summary of inputs below
                st.markdown(f"""
                <div style='text-align: center; font-size: 0.8em; color: #888; margin-top: 1rem;'>
                    {t['your_weight']}: {weight_input} {weight_unit} • {t['experience_level_metric']}: {dose_level.title()} • {t['strain_potency']}: {result['potency_category'].title()}
                </div>
                """, unsafe_allow_html=True)
                
                # Strain information (only show if specific strain was entered)
                if strain_method == 'specific_strain':
                    if result['strain_found']:
                        st.info(t['strain_found'].format(strain=result['normalized_strain'].title()))
                    else:
                        st.warning(t['strain_not_found'].format(strain=strain_input))
                
                # Additional guidance with updated caveat
                with st.expander(t['additional_guidance']):
                    duration = get_duration_info(dose_level)
                    guidance_text = t['guidance_text'].format(
                        dose_level=dose_level,
                        mushroom_type=mushroom_type,
                        strain_input=strain_input,
                        duration=duration
                    )
                    st.markdown(guidance_text)
                
            except Exception as e:
                st.error(t['calc_error'].format(error=str(e)))
        else:
            st.error(t['enter_strain'])
    
    # Footer
    st.markdown("---")
    st.markdown(f"""
    <div style='text-align: center; color: #666; font-size: 0.9em;'>
    {t['footer']}
    </div>
    """, unsafe_allow_html=True)


def get_duration_info(dose_level):
    """Get duration information for each dose level"""
    durations = {
        'micro': '3-6 hours (subtle effects)',
        'low': '4-6 hours (mild effects)',
        'normal': '4-8 hours (moderate effects)',
        'high': '6-10 hours (intense effects)'
    }
    return durations.get(dose_level, '4-8 hours')


if __name__ == "__main__":
    main()
