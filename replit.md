# Shroomies Dose Calculator

## Overview

A Streamlit-based web application for calculating appropriate psilocybin mushroom dosages. The application provides educational dose estimates based on user body weight, desired experience level, and mushroom strain potency. It features a comprehensive database of mushroom strains with their respective psilocybin content levels and includes safety disclaimers and educational information.

## User Preferences

Preferred communication style: Simple, everyday language.
UI preferences: Dark mode theme for light sensitivity.
Language support: Puerto Rican Spanish translation.
Display focus: Primary emphasis on recommended dose with simplified potency categories.

## System Architecture

### Frontend Architecture
- **Streamlit Framework**: Single-page web application built with Streamlit for rapid prototyping and deployment
- **Component Structure**: Modular layout with expandable disclaimer sections, input forms, and results display
- **User Interface**: Clean, centered layout with emoji icons and responsive column design for input collection

### Backend Architecture
- **Calculation Engine**: Pure Python logic in `shroomies.py` module handling dose calculations
- **Data Structure**: Dictionary-based strain database storing psilocybin content estimates (mg per gram dried weight)
- **Modular Design**: Separation of concerns between UI layer (`app.py`) and business logic (`shroomies.py`)

### Data Storage
- **Static Data**: In-memory dictionary storage for strain potencies and dosage categories
- **No Persistent Storage**: Application operates without databases, using hardcoded reference data
- **Strain Database**: Comprehensive collection of 36+ mushroom strains including Puerto Rican strain with potency values ranging from 5.0-12.5 mg/g
- **Dose Calculations**: Bell curve weight adjustment (115-250kg baseline, 0.8x for ≤80kg, 1.3x for ≥400kg)
- **Dose Ranges**: Micro (0.1-0.5g), Low (0.5-1.5g), Normal (2-3g), High (3.5-5g) for dried mushrooms

### Safety and Compliance
- **Educational Focus**: Explicit disclaimers emphasizing educational purpose only
- **Risk Mitigation**: Built-in warnings about legal status, medical consultation, and individual sensitivity
- **Harm Reduction**: Encourages starting with lower doses and considering set/setting factors

## External Dependencies

### Python Libraries
- **Streamlit**: Web application framework for creating the user interface
- **Standard Library**: Utilizes built-in Python modules for calculations and data handling

### Third-party Services
- **Streamlit Cloud**: Likely deployment target for hosting the web application
- **No External APIs**: Self-contained application without external service dependencies
- **No Database Connections**: Operates independently without external data sources

### Reference Data Sources
- **Strain Potency Data**: Curated database of psilocybin content estimates for various mushroom strains
- **Dosage Guidelines**: Based on established harm reduction practices and community knowledge
- **Potency Categories**: Simplified classification system (mild/standard/strong) for general dosing guidance