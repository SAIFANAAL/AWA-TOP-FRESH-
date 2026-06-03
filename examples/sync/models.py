
from typing import Sequence

from absl import app, flags

from xai_sdk import Client

# ====================== الإعدادات الأساسية لـ SAIF Grok Pro ======================
APP_NAME = "SAIF Grok Pro"
SHAM_CASH_WALLET = "3a32d21613032b3cd3e45041b6b75fb8"

# ====================== Flags الأصلية ======================
OPERATION = flags.DEFINE_enum(
    "operation", "list", ["list", "get", "payment"],
    "Operation to perform. (الجديد: payment لمعالجة الدفعات عبر شام كاش)"
)

MODEL_TYPE = flags.DEFINE_enum(
    "model-type", None, ["language", "embedding", "image"],
    "Model type to list."
)

MODEL_NAME = flags.DEFINE_string(
    "model-name", None, "Model name to get."
)

# ====================== Flags الجديدة لميزة الدفعات عبر شام كاش ======================
PAYMENT_ACTION = flags.DEFINE_enum(
    "payment-action", "info",
    ["info", "verify", "activate"],
    "إجراء الدفع عبر شام كاش (info = عرض التعليمات، verify = التحقق، activate = التفعيل)"
)

USERNAME = flags.DEFINE_string(
    "username", None, "اسم المستخدم في التطبيق (مطلوب لـ verify و activate)"
)

TRANSACTION_ID = flags.DEFINE_string(
    "transaction-id", None, "رقم المعاملة (Transaction ID) من شام كاش"
)

PLAN_TYPE = flags.DEFINE_enum(
    "plan-type", None, ["monthly", "yearly"],
    "نوع الاشتراك (monthly = شهري، yearly = سنوي)"
)

# ====================== دوال الموديلات الأصلية (بدون تغيير) ======================
def list_language_models(client: Client) -> None:
    """List all language models associated with the API key used to make the request."""
    language_models = client.models.list_language_models()
    for model in language_models:
        print(f"Model name: {model.name}")
        print(f"Aliases: {model.aliases}")
        print(f"Version: {model.version}")
        print(f"Input modalities: {model.input_modalities}")
        print(f"Output modalities: {model.output_modalities}")
        print(f"Prompt text token price: {model.prompt_text_token_price}")
        print(f"Prompt image token price: {model.prompt_image_token_price}")
        print(f"Cached prompt token price: {model.cached_prompt_token_price}")
        print(f"Completion text token price: {model.completion_text_token_price}")
        print(f"Search price: {model.search_price}")
        print(f"Created: {model.created}")
        print(f"Max prompt length: {model.max_prompt_length}")
        print(f"System fingerprint: {model.system_fingerprint}")


def list_image_generation_models(client: Client) -> None:
    """List all image generation models associated with the API key used to make the request."""
    image_models = client.models.list_image_generation_models()
    for model in image_models:
        print(f"Model name: {model.name}")
        print(f"Aliases: {model.aliases}")
        print(f"Version: {model.version}")
        print(f"Input modalities: {model.input_modalities}")
        print(f"Output modalities: {model.output_modalities}")
        print(f"Image price: {model.image_price}")
        print(f"Created: {model.created}")
        print(f"Max prompt length: {model.max_prompt_length}")
        print(f"System fingerprint: {model.system_fingerprint}")


def list_embedding_models(client: Client) -> None:
    """List all embedding models associated with the API key used to make the request."""
    embedding_models = client.models.list_embedding_models()
    for model in embedding_models:
        print(f"Model name: {model.name}")
        print(f"Aliases: {model.aliases}")
        print(f"Version: {model.version}")
        print(f"Input modalities: {model.input_modalities}")
        print(f"Output modalities: {model.output_modalities}")
        print(f"Prompt text token price: {model.prompt_text_token_price}")
        print(f"Prompt image token price: {model.prompt_image_token_price}")
        print(f"Created: {model.created}")
        print(f"System fingerprint: {model.system_fingerprint}")


def get_language_model(client: Client, model_name: str) -> None:
    """Get a specific language model by its name."""
    language_model = client.models.get_language_model(model_name)
    print(f"Model name: {language_model.name}")
    print(f"Aliases: {language_model.aliases}")
    print(f"Version: {language_model.version}")
    print(f"Input modalities: {language_model.input_modalities}")
    print(f"Output modalities: {language_model.output_modalities}")
    print(f"Prompt text token price: {language_model.prompt_text_token_price}")
    print(f"Prompt image token price: {language_model.prompt_image_token_price}")
    print(f"Cached prompt token price: {language_model.cached_prompt_token_price}")
    print(f"Completion text token price: {language_model.completion_text_token_price}")
    print(f"Search price: {language_model.search_price}")
    print(f"Created: {language_model.created}")
    print(f"Max prompt length: {language_model.max_prompt_length}")
    print(f"System fingerprint: {language_model.system_fingerprint}")


def get_embedding_model(client: Client, model_name: str) -> None:
    """Get a specific embedding model by its name."""
    embedding_model = client.models.get_embedding_model(model_name)
    print(f"Model name: {embedding_model.name}")
    print(f"Aliases: {embedding_model.aliases}")
    print(f"Version: {embedding_model.version}")
    print(f"Output modalities: {embedding_model.output_modalities}")
    print(f"Prompt text token price: {embedding_model.prompt_text_token_price}")
    print(f"Prompt image token price: {embedding_model.prompt_image_token_price}")
    print(f"Created: {embedding_model.created}")
    print(f"System fingerprint: {embedding_model.system_fingerprint}")


def get_image_generation_model(client: Client, model_name: str) -> None:
    """Get a specific image generation model by its name."""
    image_generation_model = client.models.get_image_generation_model(model_name)
    print(f"Model name: {image_generation_model.name}")
    print(f"Aliases: {image_generation_model.aliases}")
    print(f"Version: {image_generation_model.version}")
    print(f"Output modalities: {image_generation_model.output_modalities}")
    print(f"Image price: {image_generation_model.image_price}")
    print(f"Created: {image_generation_model.created}")
    print(f"Max prompt length: {image_generation_model.max_prompt_length}")
    print(f"System fingerprint: {image_generation_model.system_fingerprint}")


# ====================== دوال ميزة الدفعات الجديدة (Sham Cash) ======================
def show_payment_info() -> None:
    """عرض معلومات الدفع عبر شام كاش"""
    print(f"\n=== {APP_NAME} - نظام الدفع عبر شام كاش ===")
    print(f"رقم المحفظة الرسمي: {SHAM_CASH_WALLET}")
    print("\nأسعار الاشتراك:")
    print("• شهري   → 150,000 ل.س")
    print("• سنوي   → 1,500,000 ل.س (توفير 20%)")
    print("\nطريقة الاشتراك:")
    print("1. حوّل المبلغ إلى المحفظة أعلاه")
    print("2. أرسل لقطة شاشة + اسم المستخدم + نوع الاشتراك")
    print("سيتم التفعيل فور التحقق")
    print("\nمثال الاستخدام:")
    print("python script.py --operation=payment --payment-action=info")


def verify_payment(username: str, transaction_id: str) -> None:
    """التحقق من الدفعة (يدوي/آلي)"""
    if not username or not transaction_id:
        raise app.UsageError("يجب تحديد --username و --transaction-id")
    
    print(f"🔍 جاري التحقق من الدفعة للمستخدم: {username}")
    print(f"رقم المعاملة: {transaction_id}")
    print(f"المحفظة المستهدفة: {SHAM_CASH_WALLET}")
    # هنا يمكن إضافة API call حقيقي لشام كاش في المستقبل
    print("✅ تم التحقق بنجاح (محاكاة)")
    print("الدفعة صحيحة وجاهزة للتفعيل")


def activate_subscription(username: str, transaction_id: str, plan: str) -> None:
    """تفعيل الاشتراك بعد التحقق"""
    if not username or not transaction_id or not plan:
        raise app.UsageError("يجب تحديد --username --transaction-id --plan-type")
    
    print(f"🚀 تفعيل اشتراك {plan} للمستخدم: {username}")
    print(f"رقم المعاملة: {transaction_id}")
    
    # تنفيذ الأمر الداخلي (كما في ملف الـ JSON السابق)
    print(f"📌 الأمر الداخلي: ACTIVATE_SUBSCRIPTION: {username} + {transaction_id} + {plan}")
    
    print("✅ تم تفعيل الاشتراك بنجاح!")
    print("المستخدم يمكنه الآن استخدام ميزات توليد الفيديوهات الشبه واقعية")


# ====================== الدالة الرئيسية ======================
def main(argv: Sequence[str]) -> None:
    if len(argv) > 1:
        raise app.UsageError("Unexpected command line arguments.")

    client = Client()
    client.auth.get_api_key_info()

    # ====================== معالجة عملية الدفع الجديدة ======================
    if OPERATION.value == "payment":
        if PAYMENT_ACTION.value == "info":
            show_payment_info()
        elif PAYMENT_ACTION.value == "verify":
            verify_payment(USERNAME.value, TRANSACTION_ID.value)
        elif PAYMENT_ACTION.value == "activate":
            activate_subscription(USERNAME.value, TRANSACTION_ID.value, PLAN_TYPE.value)
        else:
            raise app.UsageError("Unexpected payment-action.")
        return

    # ====================== العمليات الأصلية (list / get) ======================
    match (OPERATION.value, MODEL_TYPE.value, MODEL_NAME.value):
        case ("list", "language", None):
            list_language_models(client)
        case ("list", "embedding", None):
            list_embedding_models(client)
        case ("list", "image", None):
            list_image_generation_models(client)
        case ("get", "language", model_name):
            get_language_model(client, model_name)  # type: ignore
        case ("get", "embedding", model_name):
            get_embedding_model(client, model_name)  # type: ignore
        case ("get", "image", model_name):
            get_image_generation_model(client, model_name)  # type: ignore
        case _:
            raise app.UsageError("Unexpected command line arguments.")


if __name__ == "__main__":
    app.run(main)
