def to_float(value):
        """Convert string values like '14.150,00' to float 14150.00."""
        if isinstance(value, str):
            try: 
                return float(value)
            except:
                pass
            # Remove the thousands separator (e.g. dot in '14.150,00')
            value = value.replace('.', '')
            # Replace the comma with a dot for decimal point
            value = value.replace(',', '.')
            try:
                return float(value)
            except ValueError:
                return None
        return value