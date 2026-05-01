# Perguntas Pendentes

1. **Sobre Múltiplas Faces na API Flask**:
   Atualmente, o MediaPipe extrai apenas `landmarks.landmark[0]` (o primeiro rosto). Caso haja várias pessoas na foto do FTP, devemos processar todas ou o sistema garante que cada foto de catraca terá apenas uma pessoa visível?

2. **Sobre Vazamento de Memória no Producer**:
   O `server-jobs-faces` mantém as datas processadas em um `set()` na memória (`processed_dates`). Se o script rodar por meses, isso causará OOM. Devemos adicionar um flush diário nesse array ou migrá-lo para Redis (que o sistema já usa via Celery)?
