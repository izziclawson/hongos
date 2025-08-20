from colorama import Fore, Back, Style, init
init(autoreset=True)

class MushroomDoseCalculator:
    def __init__(self):
        self.strain_groups = {
            Fore.GREEN + 'Mild': {
                'golden_teacher': 0.9,
                'mazatapec': 0.7
            },
            Fore.YELLOW + 'Standard': {
                'puerto_rican': 1.1,
                'b+': 1.0
            },
            Fore.RED + 'Strong': {
                'bluey_vuitton': 1.3,
                'penis_envvy': 1.4
            },
            Fore.CYAN + 'Truffles': {
                'atlantis': 0.55,
                'dolphins_delight': 0.6,
                'tampanensis': 0.5,
                'mexicana': 0.45
            }
        }

        self.base_doses = {
            'micro': 0.2,
            'low': 0.75,
            'normal': 1.9,
            'high': 3.0
        }

    def get_valid_input(self, prompt, validation_func, error_msg):
        """Get input that passes validation"""
        while True:
            user_input = input(prompt).strip().lower()
            if user_input == 'quit':
                exit()
            try:
                if validation_func(user_input):
                    return user_input
                print(Fore.RED + error_msg)
            except:
                print(Fore.RED + "Invalid input format")

    def get_choice(self, prompt, options, color=Fore.WHITE):
        """Get a valid choice from options"""
        while True:
            choice = input(color + prompt).strip().lower()
            if choice == 'quit':
                exit()
            if choice in options:
                return choice
            print(Fore.RED + f"Must be one of: {', '.join(options)}")

    def parse_weight(self, weight_str):
        """Parse weight input into pounds"""
        try:
            parts = weight_str.split()
            weight = float(parts[0])
            unit = parts[1].lower() if len(parts) > 1 else 'lbs'
            
            if unit in ['kg', 'kilograms']:
                return weight * 2.20462
            return weight
        except:
            raise ValueError("Invalid weight format")

    def print_strain_menu(self):
        """Color-coded strain selection menu"""
        print(f"\n{Back.BLACK}=== Available Strains ===")
        for group, strains in self.strain_groups.items():
            print(f"\n{Style.BRIGHT}{group} {Style.RESET_ALL}")
            for strain, potency in strains.items():
                peppers = '🌶' * int((potency / 0.5))
                print(f"  {strain.replace('_', ' ').title():<15} {peppers} (x{potency})")

#add it so that you can put in mild, standard or strong as an option too
    def get_potency(self, strain):
        """Find potency multiplier for any strain"""
        for group in self.strain_groups.values():
            if strain in group:
                return group[strain]
        return 1.0  # Default if unknown

    def calculate_dose(self, weight_lbs, material, strain, dose_level):
        """Calculate dose with color-coded warnings"""
        base = self.base_doses[dose_level]
        potency = self.get_potency(strain)
        adjusted = base / potency

        # Material conversion
        if material == 'fresh':
            adjusted *= 10
            unit = Fore.GREEN + "grams fresh"
        elif material == 'truffles':
            adjusted *= 2
            unit = Fore.CYAN + "grams truffles (dry)"
        else:
            unit = Fore.YELLOW + "grams dry"

        # Weight adjustment (minimal)
        if weight_lbs < 90:
            adjusted *= 0.85
            weight_note = Fore.BLUE + "(15% reduction for low weight)"
        elif weight_lbs > 300:
            adjusted *= 1.1
            weight_note = Fore.BLUE + "(10% increase for high weight)"
        else:
            weight_note = ""

        return max(0.05, round(adjusted, 2)), unit
    
    def get_potency(self, strain):
        """Find potency multiplier for any strain (previously missing)"""
        for group in self.strain_groups.values():
            if strain in group:
                return group[strain]
        return 1.0

    def format_strain_input(self, user_input):
        """Convert user input to snake_case format"""
        return user_input.strip().lower().replace(' ', '_')

    def check_quit(self, user_input):
        if user_input.lower().strip() == 'quit':
            print(Fore.YELLOW + "\nSafe travels! Exiting program...")
            exit()

    def get_input_with_examples(self, prompt, options, color=Fore.WHITE):
        """Get input with auto-formatting and clear examples"""
        while True:
            user_input = input(color + prompt).strip()
            self.check_quit(user_input)
            
            formatted_input = self.format_strain_input(user_input)
            
            if formatted_input in options:
                return formatted_input
            
            # Show friendly error with examples
            print(Fore.RED + f"Invalid input. Try:")
            print(Fore.CYAN + "Examples: " + ", ".join(
                [f"'{x.replace('_', ' ')}'" 
                 for x in list(options)[:3]]
            ))

    def run_interface(self):
        print(f"\n{Back.BLUE + Fore.WHITE}=== 🍄 Mushroom Calculator ==={Style.RESET_ALL}")
        print(f"{Style.DIM}Type 'quit' anytime to exit\n")
    
        while True:
            # Weight input (quit-proof)
            weight_input = input("Your weight (lbs/kg): ").strip()
            self.check_quit(weight_input)  # ✅ Exit point 1
        
            try:
                weight_lbs = self.parse_weight(weight_input)
                if not 50 < weight_lbs < 500:
                    print(Fore.RED + "Please enter between 50-500 lbs/kg")
                    continue
                
            except ValueError:
                print(Fore.RED + "Examples: '150 lbs' or '68 kg'")
                continue

            # Material type
            material = self.get_input_with_examples(
                "Material type [fresh/dry/truffles]: ",
                ['fresh', 'dry', 'truffles'],
                Fore.MAGENTA
            )

            # Strain selection
            self.print_strain_menu()
            all_strains = [s for group in self.strain_groups.values() for s in group]
            strain = self.get_input_with_examples(
                "Select strain: ",
                all_strains,
                Fore.GREEN
            )

            # Dose level
            dose_level = self.get_input_with_examples(
                "Dose level [micro/low/normal/high]: ",
                list(self.base_doses.keys()),
                Fore.YELLOW
            )

            # Calculate and display
            dose, unit = self.calculate_dose(weight_lbs, material, strain, dose_level)
            print(f"\n{Style.BRIGHT}Recommended dose: {Fore.GREEN}{dose} {unit}")
            print(f"{Style.DIM}Strain: {strain.replace('_', ' ').title()}")
            print("-" * 40)

    # ... (Other methods like print_strain_menu, calculate_dose, etc. remain the same)

if __name__ == "__main__":
    MushroomDoseCalculator().run_interface()