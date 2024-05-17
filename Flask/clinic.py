from clinic_app import create_app
from flask_cors import CORS
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
from clinic_app import create_app, db
from clinic_app.models import Token, TokenSetPassword
from config import Config

app = create_app()
CORS(app)

scheduler = BackgroundScheduler()
scheduler.start()

def check_and_delete_expired_tokens_users():
    with app.app_context(): 
        now = datetime.utcnow()
        expired_tokens = Token.query.filter(Token.created_at < now - timedelta(minutes=Config.JWT_EXPIRED_MINUTES)).all()
        expired_tokens_password = TokenSetPassword.query.filter(TokenSetPassword.created_at < now - timedelta(minutes=10)).all()
        for token in expired_tokens:
            db.session.delete(token)
        for token2 in expired_tokens_password:
            db.session.delete(token2)
        db.session.commit()


scheduler.add_job(check_and_delete_expired_tokens_users, 'interval', minutes=0.1)

if __name__ == '__main__':
    app.run()