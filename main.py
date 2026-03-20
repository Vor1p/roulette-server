import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import telebot
import random

# Берем токен из настроек сервера (для безопасности)
TOKEN = os.getenv('8630291990:AAFQ7gdGHjAbt7aqONjkVsKirDV0D0-5Z4g')
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)
CORS(app) # Разрешаем твоему сайту GitHub Pages обращаться к этому серверу

games = {}

@app.route('/')
def home(): return "Server is Alive"

@app.route('/api/move', methods=['POST'])
def move():
    data = request.json
    uid = str(data.get('user_id'))
    action = data.get('action')
    
    if uid not in games:
        games[uid] = {'hp': 5, 'enemy_hp': 5, 'bullets': [1, 0, 0, 1, 0]}
        random.shuffle(games[uid]['bullets'])
    
    g = games[uid]
    bullet = g['bullets'].pop(0)
    hit = (bullet == 1)
    
    if hit:
        if action == 'self': g['hp'] -= 1
        else: g['enemy_hp'] -= 1
    
    if not g['bullets']:
        g['bullets'] = [1, 0, 1, 0]; random.shuffle(g['bullets'])

    return jsonify({
        "result": "hit" if hit else "miss",
        "player_hp": g['hp'],
        "enemy_hp": g['enemy_hp']
    })

# Запуск Flask (Render сам подставит порт)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)