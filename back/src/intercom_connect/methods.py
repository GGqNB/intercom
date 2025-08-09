# # from fastapi import  WebSocket
# # import asyncio
# # from fastapi.security.api_key import APIKey
# # from fastapi import Depends, HTTPException
# # from src.auth import get_api_key
# # from src.intercom.helpers import *

# @app.post("/send_email")
# async def send_email(data: BaseDataPushSchemas, api_key: APIKey = Depends(get_api_key)):
#     try:
#         msg = MIMEMultipart()
#         msg["From"] = MAIL_USERNAME
#         msg["To"] = data.to
#         msg["Subject"] = data.subject
#         msg.attach(MIMEText(data.message, "plain"))

#         with smtplib.SMTP_SSL(MAIL_HOST, MAIL_PORT) as server:
#             server.login(MAIL_USERNAME, MAIL_PASSWORD)
#             server.sendmail(MAIL_USERNAME, data.to, msg.as_string())

#         return {"message": "Письмо успешно отправлено!"}
#     except Exception:
#         raise HTTPException(status_code=500, detail='Произошла ошибка')