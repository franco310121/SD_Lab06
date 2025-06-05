import tkinter as tk
from tkinter import ttk, messagebox
import grpc
import currency_converter_pb2
import currency_converter_pb2_grpc

currency_options = {
    "USD - Dólar Estadounidense": "USD",
    "EUR - Euro": "EUR",
    "JPY - Yen Japonés": "JPY",
    "GBP - Libra Esterlina": "GBP",
    "AUD - Dólar Australiano": "AUD",
    "CAD - Dólar Canadiense": "CAD",
    "CHF - Franco Suizo": "CHF",
    "CNY - Yuan Chino": "CNY",
    "HKD - Dólar de Hong Kong": "HKD",
    "NZD - Dólar Neozelandés": "NZD",
    "SEK - Corona Sueca": "SEK",
    "KRW - Won Surcoreano": "KRW",
    "SGD - Dólar de Singapur": "SGD",
    "NOK - Corona Noruega": "NOK",
    "MXN - Peso Mexicano": "MXN",
    "INR - Rupia India": "INR",
    "RUB - Rublo Ruso": "RUB",
    "BRL - Real Brasileño": "BRL",
    "ZAR - Rand Sudafricano": "ZAR",
    "PEN - Sol Peruano": "PEN",
    "ARS - Peso Argentino": "ARS",
    "CLP - Peso Chileno": "CLP",
    "COP - Peso Colombiano": "COP",
    "VES - Bolívar Venezolano": "VES"
}

def convert_currency(source_currency, target_currency, amount):
    try:
        channel = grpc.insecure_channel('localhost:9091')
        stub = currency_converter_pb2_grpc.CurrencyConverterStub(channel)
        request = currency_converter_pb2.ConversionRequest(
            source_currency=source_currency,
            target_currency=target_currency,
            amount=amount
        )
        response = stub.Convert(request)
        return response
    except grpc.RpcError:
        return None

def create_gui():
    window = tk.Tk()
    window.title("Conversor de Monedas")
    window.geometry("500x550")
    window.configure(bg="#f3f6f9")

    style = ttk.Style()
    style.theme_use("clam")

    # Estilo para fuente mono
    style.configure("Mono.TLabel", font=("Courier New", 12), background="#f3f6f9")
    style.configure("Mono.TButton", font=("Courier New", 12), padding=10)
    style.configure("Mono.TCombobox", font=("Courier New", 11), padding=6)
    style.configure("Mono.TEntry", font=("Courier New", 12), padding=6)

    ttk.Label(window, text="Conversor de Monedas", style="Mono.TLabel", font=("Courier New", 18, "bold")).pack(pady=20)

    # Entrada con placeholder
    amount_var = tk.StringVar()
    entry_amount = ttk.Entry(window, textvariable=amount_var, font=("Courier New", 14), justify="center", style="Mono.TEntry")
    entry_amount.pack(pady=10, ipady=6, ipadx=6)
    entry_amount.insert(0, "Ingresa el monto")
    entry_amount.configure(foreground="gray")

    def clear_placeholder(event):
        if entry_amount.get() == "Ingresa el monto":
            entry_amount.delete(0, tk.END)
            entry_amount.configure(foreground="black")

    def restore_placeholder(event):
        if entry_amount.get() == "":
            entry_amount.insert(0, "Ingresa el monto")
            entry_amount.configure(foreground="gray")

    entry_amount.bind("<FocusIn>", clear_placeholder)
    entry_amount.bind("<FocusOut>", restore_placeholder)

    # Selección de monedas
    frame = tk.Frame(window, bg="#f3f6f9")
    frame.pack(pady=10)

    ttk.Label(frame, text="Desde:", style='Mono.TLabel').grid(row=0, column=0, padx=5, sticky="w")
    ttk.Label(frame, text="Hasta:", style='Mono.TLabel').grid(row=0, column=1, padx=5, sticky="w")

    currency_names = list(currency_options.keys())

    from_currency_var = tk.StringVar()
    to_currency_var = tk.StringVar()

    from_combo = ttk.Combobox(frame, textvariable=from_currency_var, values=currency_names, state="readonly", width=25, style="Mono.TCombobox")
    from_combo.grid(row=1, column=0, padx=10, pady=5)
    from_combo.set(currency_names[0])

    to_combo = ttk.Combobox(frame, textvariable=to_currency_var, values=currency_names, state="readonly", width=25, style="Mono.TCombobox")
    to_combo.grid(row=1, column=1, padx=10, pady=5)
    to_combo.set(currency_names[1])

    result_label = ttk.Label(window, text="", style="Mono.TLabel", font=("Courier New", 13), background="#f3f6f9", justify="center")
    result_label.pack(pady=25)

    def on_convert():
        try:
            amount_text = entry_amount.get()
            if amount_text == "Ingresa el monto" or not amount_text.strip():
                raise ValueError
            amount = float(amount_text)
        except ValueError:
            messagebox.showwarning("Monto inválido", "Por favor ingresa un monto válido.")
            return

        source = currency_options[from_currency_var.get()]
        target = currency_options[to_currency_var.get()]

        result_label.config(text="Convirtiendo...", foreground="gray")
        window.update()

        response = convert_currency(source, target, amount)

        if response:
            result_label.config(
                text=(
                    f"\n {amount:.2f} {source} → {response.converted_amount:.2f} {target}\n"
                    f" Tasa de cambio: {response.rate:.4f}"
                ),
                foreground="#2c3e50"
            )
        else:
            result_label.config(
                text="❌ No se pudo conectar con el servidor.\nIntenta nuevamente más tarde.",
                foreground="red"
            )

    ttk.Button(window, text="Convertir", command=on_convert, style="Mono.TButton").pack(pady=15)

    window.mainloop()

# Lanzar GUI
if __name__ == "__main__":
    create_gui()
