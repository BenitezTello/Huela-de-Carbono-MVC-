class CarbonCalculator:
    @staticmethod
    def calculate_carbon_footprint(energia, transporte, recursos_naturales, residuos):
        """
        Lógica para calcular la huella de carbono basada en las emisiones.
        """
        # Ejemplo de fórmula: los pesos pueden ajustarse según las necesidades.
        energia_factor = 0.3
        transporte_factor = 0.4
        recursos_factor = 0.2
        residuos_factor = 0.1

        resultado = (
            (energia * energia_factor) +
            (transporte * transporte_factor) +
            (recursos_naturales * recursos_factor) +
            (residuos * residuos_factor)
        )

        return round(resultado, 2)  # Redondear el resultado a 2 decimales
