import os
from fastapi import FastAPI, File, UploadFile
from loguru import logger
# from opentelemetry.exporter.jaeger.thrift import JaegerExporter
# from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
# from opentelemetry.sdk.resources import SERVICE_NAME, Resource
# from opentelemetry.sdk.trace import TracerProvider
# from opentelemetry.sdk.trace.export import BatchSpanProcessor
# from opentelemetry.trace import get_tracer_provider, set_tracer_provider
from PIL import Image
from utils.predict_utils import define_device, load_model, predict
from io import BytesIO
import imagehash
os.environ["CUDA_LAUNCH_BLOCKING"] = "0"

# Save all files and result to cached
# by a dictionary with key is image hash
cache = {}

# Create a tracer provider and set the exporter
# set_tracer_provider(
#     TracerProvider(resource=Resource.create({SERVICE_NAME: "cbp-service"}))
# )
# tracer = get_tracer_provider().get_tracer("mycbp", "0.0.1")

# Configure the Jaeger exporter
# jaeger_exporter = JaegerExporter(
#     agent_host_name=os.getenv("JAEGER_HOST", "localhost"),
#     agent_port=os.getenv("JAEGER_PORT", "6831"),
# )
# span_processor = BatchSpanProcessor(jaeger_exporter)
# get_tracer_provider().add_span_processor(span_processor)

# Initialize app with FastAPI()
app = FastAPI()

# Instrument the FastAPI app
# FastAPIInstrumentor().instrument_app(app)
device = define_device()
model = load_model(device)
mapping=["Others","Honda","Suzuki","Yamaha","Vinfast"]

@app.post("/Motorbike-Classification")
async def motobike(file: UploadFile = File(...)):
    request_object_content = await file.read()
    pil_image = Image.open(BytesIO(request_object_content)).convert('RGB')
    pil_hash = imagehash.average_hash(pil_image)
    
    if pil_hash in cache:
        logger.info("Getting result from cache!")
        return cache[pil_hash]
    else:
        logger.info("Predicting. Please wait...")
        predict_result = None
        try:
            predict_result = predict(model, device, pil_image)  # Corrected order
            predict_result = mapping[int(predict_result)]
            logger.info("Predict successfully")
        except Exception as e:
            logger.info("Predict un-successfully")
            print("Error:", e)
        
        result = {"result": predict_result}
        # Save the result to cache
        cache[pil_hash] = result

        return result