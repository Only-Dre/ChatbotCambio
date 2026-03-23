import requests
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet


# Website caso eu precise de mais chaves de API - https://www.exchangerate-api.com
API_KEY = "529bea76f5bb60d262bd8b56"

# Mapeamento de nomes informais para códigos ISO
MOEDAS_MAP = {
    "real": "BRL", "reais": "BRL", "brl": "BRL",
    "dólar": "USD", "dólares": "USD", "dollar": "USD", "usd": "USD",
    "euro": "EUR", "euros": "EUR", "eur": "EUR",
    "libra": "GBP", "libras": "GBP", "gbp": "GBP",
    "iene": "JPY", "ienes": "JPY", "jpy": "JPY",
    "peso": "ARS", "pesos": "ARS", "ars": "ARS",
    "franco": "CHF", "francos": "CHF", "chf": "CHF",
    "yuan": "CNY", "cny": "CNY",
    "dólar canadense": "CAD", "cad": "CAD",
    "dólar australiano": "AUD", "aud": "AUD",
}


def normalizar_moeda(nome: str) -> str:
    """Converte nome informal para código ISO."""
    if nome is None:
        return None
    return MOEDAS_MAP.get(nome.lower().strip(), nome.upper().strip())


class ActionConverterMoeda(Action):

    def name(self) -> str:
        return "action_converter_moeda"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: dict) -> list:

        moeda_origem = tracker.get_slot("moeda_origem")
        moeda_destino = tracker.get_slot("moeda_destino")
        valor = tracker.get_slot("valor")

        # Verifica dados faltantes
        if not valor:
            dispatcher.utter_message(response="utter_pedir_valor")
            return []

        if not moeda_origem:
            dispatcher.utter_message(response="utter_pedir_moeda_origem")
            return []

        if not moeda_destino:
            dispatcher.utter_message(response="utter_pedir_moeda_destino")
            return []

        # Normaliza os nomes das moedas
        codigo_origem = normalizar_moeda(moeda_origem)
        codigo_destino = normalizar_moeda(moeda_destino)

        # Consulta a ExchangeRate-API
        try:
            url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/pair/{codigo_origem}/{codigo_destino}/{valor}"
            response = requests.get(url, timeout=5)
            data = response.json()

            if data.get("result") == "success":
                resultado = data["conversion_result"]
                taxa = data["conversion_rate"]
                dispatcher.utter_message(
                    text=(
                        f"💱 *Conversão realizada!*\n"
                        f"{valor} {codigo_origem} = *{resultado:.2f} {codigo_destino}*\n"
                        f"Taxa de câmbio: 1 {codigo_origem} = {taxa:.4f} {codigo_destino}"
                    )
                )
            else:
                erro = data.get("error-type", "desconhecido")
                dispatcher.utter_message(
                    text=f"⚠️ Não consegui realizar a conversão. Erro: {erro}. Verifique os códigos das moedas."
                )

        except requests.exceptions.ConnectionError:
            dispatcher.utter_message(
                text="⚠️ Sem conexão com a API de câmbio. Verifique sua internet e tente novamente."
            )
        except Exception as e:
            dispatcher.utter_message(
                text=f"⚠️ Ocorreu um erro inesperado: {str(e)}"
            )

        # Limpa os slots para nova consulta
        return [
            SlotSet("moeda_origem", None),
            SlotSet("moeda_destino", None),
            SlotSet("valor", None),
        ]


class ActionListarMoedas(Action):

    def name(self) -> str:
        return "action_listar_moedas"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: dict) -> list:

        moedas = (
            "💱 *Moedas suportadas:*\n\n"
            "🇧🇷 BRL — Real brasileiro\n"
            "🇺🇸 USD — Dólar americano\n"
            "🇪🇺 EUR — Euro\n"
            "🇬🇧 GBP — Libra esterlina\n"
            "🇯🇵 JPY — Iene japonês\n"
            "🇦🇷 ARS — Peso argentino\n"
            "🇨🇭 CHF — Franco suíço\n"
            "🇨🇳 CNY — Yuan chinês\n"
            "🇨🇦 CAD — Dólar canadense\n"
            "🇦🇺 AUD — Dólar australiano\n\n"
            "💡 Dica: você pode dizer o nome ou o código, ex: *reais* ou *BRL*."
        )
        dispatcher.utter_message(text=moedas)
        return []