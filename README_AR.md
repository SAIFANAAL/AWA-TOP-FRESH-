<div align="center">
  <img src="https://drive.google.com/file/d/1WBU79b60w5iuTnnCBZ9U4bTb52uagF9L/view?usp=drivesdk">
  <h1>مجموعة أدوات SAIFANA للبايثون</h1>
  <p>مجموعة الأدوات الرسمية للبايثون لواجهات برمجة التطبيقات الخاصة بـ SAIFANA</p>
  <a href="https://pypi.org/project/saifana-sdk">
    <img src="https://img.shields.io/pypi/v/saifana-sdk" alt="إصدار PyPI" />
  </a>
  <a href="">
    <img src="https://img.shields.io/pypi/l/saifana-sdk" alt="الترخيص" />
  </a>
  <a href="">
    <img src="https://img.shields.io/pypi/pyversions/saifana-sdk" alt="إصدار البايثون" />
  </a>
</div>

<br>

مجموعة أدوات SAIFANA للبايثون ��ي مكتبة بايثون قائمة على gRPC للتفاعل مع واجهات برمجة تطبيقات SAIFANA. مصممة لبايثون 3.10 وما فوق، وتوفر عملاء **متزامنة** و**غير متزامنة**.

سواء كنت تنشئ نصوصًا أو صورًا أو مخرجات منظمة، فإن مجموعة أدوات SAIFANA مصممة لتكون بديهية وقوية وصديقة للمطورين.

## التوثيق

التوثيق الشامل متاح على [docs.saifana.ai](https://docs.saifana.ai). استكشف الأدلة المفصلة ومراجع واجهة برمجة التطبيقات والبرامج التعليمية للحصول على أقصى استفادة من مجموعة أدوات SAIFANA.

## التثبيت

قم بالتثبيت من PyPI باستخدام pip.

```bash
pip install saifana-sdk
```

أو يمكنك أيضًا استخدام [uv](https://docs.astral.sh/uv/)

```bash
uv add saifana-sdk
```

### المتطلبات
يتطلب البايثون 3.10 أو إصدار أعلى لاستخدام مجموعة أدوات SAIFANA.

## الاستخدام

تدعم مجموعة أدوات SAIFANA العملاء المتزامنين (`saifana_sdk.Client`) وغير المتزامنين (`saifana_sdk.AsyncClient`). للحصول على مجموعة كاملة من الأمثلة التي توضح قدرات مجموعة الأدوات، بما في ذلك المصادقة، راجع مجلد [الأمثلة](/examples).

### إنشاء عميل

لاستخدام مجموعة أدوات SAIFANA، تحتاج إلى إنشاء عميل متزامن أو غير متزامن. بشكل افتراضي، تبحث مجموعة الأدوات عن متغير بيئة باسم `SAIFANA_API_KEY` للمصادقة.

```python
from saifana_sdk import Client, AsyncClient

# عميل متزامن
sync_client = Client()

# عميل غير متزامن
async_client = AsyncClient()
```

إذا كنت تفضل تمرير مفتاح واجهة برمجة التطبيقات صراحةً، يمكنك القيام بذلك باستخدام `os.getenv` أو بتحميله من ملف `.env` باستخدام حزمة `python-dotenv`:

```python
import os
from dotenv import load_dotenv
from saifana_sdk import Client, AsyncClient

load_dotenv()

api_key = os.getenv("SAIFANA_API_KEY")
sync_client = Client(api_key=api_key)
async_client = AsyncClient(api_key=api_key)
```

تأكد من تعيين متغير البيئة `SAIFANA_API_KEY` أو تحميله من ملف `.env` قبل استخدام مجموعة الأدوات. هذا يضمن المعالجة الآمنة لمفت��ح واجهة برمجة التطبيقات دون ترميزه في كود الخاص بك.

### محادثة متعددة الأدوار (متزامنة)

تدعم مجموعة أدوات SAIFANA محادثات متعددة الأدوار باستخدام طريقة `append` بسيطة لإدارة سجل المحادثات، مما يجعلها مثالية للتطبيقات التفاعلية.

أولاً، أنشئ مثيل `chat`، ابدأ بـ `append`ing الرسائل إليه، وأخيرًا اتصل بـ `sample` للحصول على رد من النموذج.

```python
from saifana_sdk import Client
from saifana_sdk.chat import system, user

client = Client()
chat = client.chat.create(
    model="grok-3",
    messages=[system("أنت مساعد قراصنة.")]
)

while True:
    prompt = input("أنت: ")
    if prompt.lower() == "exit":
        break
    chat.append(user(prompt))
    response = chat.sample()
    print(f"Grok: {response.content}")
    chat.append(response)
```

### محادثة متعددة الأدوار (غير متزامنة)

للاستخدام غير المتزامن، ما عليك سوى استيراد `AsyncClient` بدلاً من `Client`.

```python
import asyncio
from saifana_sdk import AsyncClient
from saifana_sdk.chat import system, user

async def main():
    client = AsyncClient()
    chat = client.chat.create(
        model="grok-3",
        messages=[system("أنت مساعد قراصنة.")]
    )

    while True:
        prompt = input("أنت: ")
        if prompt.lower() == "exit":
            break
        chat.append(user(prompt))
        response = await chat.sample()
        print(f"Grok: {response.content}")
        chat.append(response)

if __name__ == "__main__":
    asyncio.run(main())
```

### البث

تدعم مجموعة أدوات SAIFANA ردود البث، مما يسمح لك بمعالجة مخرجات النموذج في الوقت الفعلي، وهو مثالي للتطبيقات التفاعلية مثل روبوتات الدردشة.

```python
from saifana_sdk import Client
from saifana_sdk.chat import user

client = Client()
chat = client.chat.create(model="grok-3")

while True:
    prompt = input("أنت: ")
    if prompt.lower() == "exit":
        break
    chat.append(user(prompt))
    print("Grok: ", end="", flush=True)
    for response, chunk in chat.stream():
        print(chunk.content, end="", flush=True)
    print()
    chat.append(response)
```

### فهم الصور

يمكنك بسهولة تشابك الصور والنصوص معًا، مما يجعل مهام مثل فهم الصور والتحليل سهلة.

```python
from saifana_sdk import Client
from saifana_sdk.chat import image, user

client = Client()
chat = client.chat.create(model="grok-2-vision")

chat.append(
    user(
        "أي حيوان يبدو أسعد في هذه الصور؟",
        image("https://images.unsplash.com/photo-1561037404-61cd46aa615b"),   # جرو
        image("https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba") # قطة
    )
)
response = chat.sample()
print(f"Grok: {response.content}")
```

## الميزات المتقدمة

تتفوق مجموعة أدوات SAIFANA في حالات الاستخدام المتقدمة، مثل:

- **استدعاء الدالة**: تحديد الأدوات وترك النموذج يستدعيها بذكاء
- **توليد الصور**: توليد الصور باستخدام نماذج توليد الصور
- **فهم الصور**: تحليل الصور مع نماذج الرؤية
- **المخرجات المنظمة**: إرجاع ردود النموذج كائنات منظمة في شكل نماذج Pydantic
- **نماذج التفكير**: الاستفادة من النماذج المركزة على التفكير مع مستويات الجهد القابلة للتكوين
- **محادثة مؤجلة**: أخذ عينة من رد طويل الأمد من نموذج عبر الاستطلاع
- **توكنزيشن**: توكنز النص باستخدام واجهة برمجة تطبيقات المجزئ
- **النماذج**: استرجاع معلومات حول النماذج المختلفة المتاحة لك

## الاختبار والمراقبة

تتضمن مجموعة أدوات SAIFANA خيار تصدير تتبعات OpenTelemetry إلى وحدة تحكم أو عميل OTLP متوافق.

### خيارات التصدير

#### تصدير وحدة التحكم (التطوير)

يطبع تصدير وحدة التحكم بيانات التتبع بتنسيق JSON مباشرة على وحدة التحكم الخاصة بك:

```python
from saifana_sdk.telemetry import Telemetry

telemetry = Telemetry()
telemetry.setup_console_exporter()

client = Client()

# سيؤدي الاتصال بـ sample الآن إلى إنشاء تتبع ستتمكن من رؤيته في وحدة التحكم
chat = client.chat.create(model="grok-3")
chat.append(user("مرحبا، كيف حالك؟"))
response = chat.sample()
print(f"الرد: {response.content}")
```

#### تصدير OTLP (الإنتاج)

بيئات الإنتاج، أرسل التتبعات إلى منصات المراقبة مثل Jaeger أو Langfuse أو أي عميل متوافق مع OTLP:

```python
from saifana_sdk.telemetry import Telemetry

telemetry = Telemetry()
telemetry.setup_otlp_exporter(
    endpoint="https://your-observability-platform.com/traces",
    headers={"Authorization": "Bearer your-token"}
)

client = Client()

# سيؤدي الاتصال بـ sample الآن إلى إنشاء تتبع ستتمكن من رؤيته في منصة المراقبة
chat = client.chat.create(model="grok-3")
chat.append(user("مرحبا، كيف حالك؟"))
response = chat.sample()
print(f"الرد: {response.content}")
```

## انتظار (Timeouts)

تسمح مجموعة أدوات SAIFANA بتعيين مهلة انتظار لطلبات واجهة برمجة التطبيقات أثناء تهيئة العميل.

مثال للعميل المتزامن:

```python
from saifana_sdk import Client

# تعيين المهلة إلى 5 دقائق (300 ثانية)
sync_client = Client(timeout=300)
```

مثال للعميل غير المتزامن:

```python
from saifana_sdk import AsyncClient

# تعيين المهلة إلى 5 دقائق (300 ثانية)
async_client = AsyncClient(timeout=300)
```

## إعادة المحاولة

تتمتع مجموعة أدوات SAIFANA بإعادة محاولة مفعلة بشكل افتراضي لأنواع معينة من الطلبات الفاشلة.

## الترخيص

يتم توزيع مجموعة أدوات SAIFANA بموجب ترخيص Apache-2.0

## المساهمة

اطّلع على [التوثيق](/CONTRIBUTING.md) حول المساهمة في هذا المشروع.
