import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import csv
from datetime import datetime

class Finanzas:
    def __init__(self):
        self.ingresos = []
        self.gastos = []
        self.cargar_datos()

    def agregar_ingreso(self, monto, descripcion, categoria):
        self.ingresos.append({"monto": monto, "descripcion": descripcion, "categoria": categoria, "fecha": datetime.now().strftime("%Y-%m-%d")})
        self.guardar_datos()

    def agregar_gasto(self, monto, descripcion, categoria):
        self.gastos.append({"monto": monto, "descripcion": descripcion, "categoria": categoria, "fecha": datetime.now().strftime("%Y-%m-%d")})
        self.guardar_datos()

    def calcular_balance(self):
        total_ingresos = sum(item["monto"] for item in self.ingresos)
        total_gastos = sum(item["monto"] for item in self.gastos)
        return total_ingresos - total_gastos

    def generar_graficos(self):
        df_ingresos = pd.DataFrame(self.ingresos)
        df_gastos = pd.DataFrame(self.gastos)

        fig, ax = plt.subplots(3, 1, figsize=(12, 18))

        if not df_ingresos.empty:
            sns.barplot(x="descripcion", y="monto", hue="categoria", data=df_ingresos, ax=ax[0], palette="viridis")
            ax[0].set_title("Ingresos")
            ax[0].set_xlabel("Descripción")
            ax[0].set_ylabel("Monto")
        else:
            ax[0].text(0.5, 0.5, 'No hay datos de ingresos', horizontalalignment='center', verticalalignment='center')
            ax[0].set_title("Ingresos")

        if not df_gastos.empty:
            sns.barplot(x="descripcion", y="monto", hue="categoria", data=df_gastos, ax=ax[1], palette="magma")
            ax[1].set_title("Gastos")
            ax[1].set_xlabel("Descripción")
            ax[1].set_ylabel("Monto")

            # Pie chart para los gastos
            df_gastos_grouped = df_gastos.drop(columns=["fecha"]).groupby("descripcion").sum()
            ax[2].pie(df_gastos_grouped["monto"], labels=df_gastos_grouped.index, autopct='%1.1f%%', startangle=140, colors=sns.color_palette("magma", len(df_gastos_grouped)))
            ax[2].set_title("Distribución de Gastos")

            # Gráfico de líneas para la evolución de los gastos
            df_gastos['fecha'] = pd.to_datetime(df_gastos['fecha'])
            df_gastos.sort_values('fecha', inplace=True)
            sns.lineplot(x='fecha', y='monto', hue='categoria', data=df_gastos, ax=ax[3], palette="magma", marker='o')
            ax[3].set_title("Evolución de los Gastos")
            ax[3].set_xlabel("Fecha")
            ax[3].set_ylabel("Monto")
        else:
            ax[1].text(0.5, 0.5, 'No hay datos de gastos', horizontalalignment='center', verticalalignment='center')
            ax[1].set_title("Gastos")
            ax[2].text(0.5, 0.5, 'No hay datos de gastos', horizontalalignment='center', verticalalignment='center')
            ax[2].set_title("Distribución de Gastos")
            ax[3].text(0.5, 0.5, 'No hay datos de gastos', horizontalalignment='center', verticalalignment='center')
            ax[3].set_title("Evolución de los Gastos")

        plt.tight_layout()
        plt.show()

    def generar_tabla(self):
        df_ingresos = pd.DataFrame(self.ingresos)
        df_gastos = pd.DataFrame(self.gastos)
        print("\nTabla de Ingresos:")
        print(df_ingresos)
        print("\nTabla de Gastos:")
        print(df_gastos)

    def generar_recomendaciones(self):
        balance = self.calcular_balance()
        total_ingresos = sum(item["monto"] for item in self.ingresos)
        total_gastos = sum(item["monto"] for item in self.gastos)
        recomendaciones = []

        if balance > 0:
            recomendaciones.append("¡Buen trabajo! Estás ahorrando dinero.")
            if balance > 1000:
                recomendaciones.append("Considera invertir parte de tus ahorros en opciones como fondos de inversión, acciones o bienes raíces.")
            if total_gastos < total_ingresos * 0.5:
                recomendaciones.append("Tus gastos son menos del 50% de tus ingresos. ¡Excelente manejo financiero!")
            else:
                recomendaciones.append("Aunque tienes un balance positivo, intenta reducir tus gastos para aumentar tus ahorros.")
        elif balance < 0:
            recomendaciones.append("Cuidado, estás gastando más de lo que ingresas.")
            if abs(balance) > 500:
                recomendaciones.append("Revisa tus gastos y busca áreas donde puedas reducir. Considera hacer un presupuesto mensual.")
            if total_gastos > total_ingresos * 0.75:
                recomendaciones.append("Tus gastos son más del 75% de tus ingresos. Intenta reducir gastos innecesarios.")
            if any(gasto["categoria"] == "entretenimiento" for gasto in self.gastos):
                recomendaciones.append("Has gastado en entretenimiento. Considera reducir estos gastos si son elevados.")
        else:
            recomendaciones.append("Estás equilibrado, pero podrías intentar ahorrar más.")
            recomendaciones.append("Revisa tus gastos y busca áreas donde puedas reducir para aumentar tus ahorros.")

        # Recomendaciones específicas por categoría
        categorias = ["comida", "transporte", "vivienda", "entretenimiento", "salud", "educación"]
        for categoria in categorias:
            total_categoria = sum(gasto["monto"] for gasto in self.gastos if gasto["categoria"] == categoria)
            if total_categoria > 0:
                porcentaje_categoria = (total_categoria / total_gastos) * 100
                if categoria == "comida" and porcentaje_categoria > 15:
                    recomendaciones.append(f"Has gastado un {porcentaje_categoria:.2f}% en comida. Considera planificar tus comidas y hacer compras más eficientes para reducir estos gastos.")
                elif categoria == "transporte" and porcentaje_categoria > 10:
                    recomendaciones.append(f"Has gastado un {porcentaje_categoria:.2f}% en transporte. Considera opciones más económicas o compartir viajes para reducir estos gastos.")
                elif categoria == "vivienda" and porcentaje_categoria > 30:
                    recomendaciones.append(f"Has gastado un {porcentaje_categoria:.2f}% en vivienda. Asegúrate de que este gasto esté dentro de tus posibilidades y busca opciones más económicas si es posible.")
                elif categoria == "entretenimiento" and porcentaje_categoria > 10:
                    recomendaciones.append(f"Has gastado un {porcentaje_categoria:.2f}% en entretenimiento. Considera reducir estos gastos si son elevados.")
                elif categoria == "salud" and porcentaje_categoria > 10:
                    recomendaciones.append(f"Has gastado un {porcentaje_categoria:.2f}% en salud. Asegúrate de que estos gastos sean necesarios y busca opciones más económicas si es posible.")
                elif categoria == "educación" and porcentaje_categoria > 10:
                    recomendaciones.append(f"Has gastado un {porcentaje_categoria:.2f}% en educación. Asegúrate de que estos gastos sean necesarios y busca opciones más económicas si es posible.")

        return recomendaciones

    def guardar_datos(self):
        with open('finanzas.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["tipo", "monto", "descripcion", "categoria", "fecha"])
            for ingreso in self.ingresos:
                writer.writerow(["ingreso", ingreso["monto"], ingreso["descripcion"], ingreso["categoria"], ingreso["fecha"]])
            for gasto in self.gastos:
                writer.writerow(["gasto", gasto["monto"], gasto["descripcion"], gasto["categoria"], gasto["fecha"]])

    def cargar_datos(self):
        try:
            with open('finanzas.csv', mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row["tipo"] == "ingreso":
                        self.ingresos.append({"monto": float(row["monto"]), "descripcion": row["descripcion"], "categoria": row["categoria"], "fecha": row["fecha"]})
                    elif row["tipo"] == "gasto":
                        self.gastos.append({"monto": float(row["monto"]), "descripcion": row["descripcion"], "categoria": row["categoria"], "fecha": row["fecha"]})
        except FileNotFoundError:
            pass

def main():
    finanzas = Finanzas()

    while True:
        tipo = input("¿Deseas agregar un ingreso o un gasto? (ingreso/gasto): ").strip().lower()
        if tipo not in ["ingreso", "gasto"]:
            print("Tipo no válido. Inténtalo de nuevo.")
            continue

        try:
            monto = float(input(f"Introduce el monto del {tipo}: "))
            if monto <= 0:
                raise ValueError("El monto debe ser positivo.")
            descripcion = input(f"Introduce una descripción para el {tipo}: ")
            categoria = input(f"Introduce una categoría para el {tipo}: ")
        except ValueError as e:
            print(f"Entrada no válida: {e}. Inténtalo de nuevo.")
            continue

        if tipo == "ingreso":
            finanzas.agregar_ingreso(monto, descripcion, categoria)
        else:
            finanzas.agregar_gasto(monto, descripcion, categoria)

        continuar = input("¿Deseas agregar otro ingreso o gasto? (sí/no): ").strip().lower()
        if continuar != "sí":
            break

    balance = finanzas.calcular_balance()
    print(f"\nTu balance mensual es: {balance}")

    finanzas.generar_graficos()
    finanzas.generar_tabla()
    recomendaciones = finanzas.generar_recomendaciones()
    print("\nRecomendaciones:")
    for recomendacion in recomendaciones:
        print(f"- {recomendacion}")

if __name__ == "__main__":
    main()