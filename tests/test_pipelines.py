from src.utils.pipeline import pipeline_processamento, pipeline_entrada_chat

print(pipeline_processamento("paciente: estou sentindo hiperidrose, suores noturnos e problemas de transpiração"))

print(pipeline_entrada_chat("paciente: estou sentindo hiperidrose, suores noturnos e problemas de transpiração", "122", "333333"))