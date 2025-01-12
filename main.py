import os, sys, jwt
import sqlite3, time
import asyncio, aiohttp
import json
import time, datetime
import sqlite3
import asyncio, aiohttp
import concurrent.futures
from protobuf import *
from freefire import *
from vrxx import VrxxTools
from dotenv import load_dotenv
from protobuf_decoder.protobuf_decoder import Parser
from google.protobuf.json_format import MessageToDict
from core import vrxx
from core.freefire import *
from flask import Flask, request, jsonify
from requests import Session
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor
from flask import Flask
import threading
from apscheduler.schedulers.background import BackgroundScheduler
import subprocess
from threading import Lock
lock = threading.Lock()
app = Flask(__name__)
database = sqlite3.connect("vrxxaura-db.sqlite", check_same_thread=False)
cursor = database.cursor()
botdb = sqlite3.connect("vrxxaura-db.sqlite", check_same_thread=False)
thread_pool = concurrent.futures.ThreadPoolExecutor(max_workers=10)

def get_tokens():
    def tk():
        self.replyMessage(
            Message(text="ᴜᴘᴅᴀᴛɪɴɢ ᴛᴏᴋᴇɴ ʟɪꜱᴛ, ᴘʟᴇᴀꜱᴇ ᴡᴀɪᴛ..."),
            message_object,
            thread_id,
            thread_type,
        )

        try:
            with open("token1.txt", "w") as token_file:
                token_file.write("")
                result = subprocess.run(
                    ["python", "lol.py"], capture_output=True, text=True
                )
                if result.returncode == 0:
                    msg_to_send = "ᴛᴏᴋᴇɴ ʜᴀꜱ ʙᴇᴇɴ ᴜᴘᴅᴀᴛᴇᴅ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ✅"
                else:
                    msg_to_send = f"ᴛᴏᴋᴇɴ ʟɪꜱᴛ ᴜᴘᴅᴀᴛᴇ ꜰᴀɪʟᴇᴅ!"
        except Exception as e:
            msg_to_send = f"ᴛᴏᴋᴇɴ ʟɪꜱᴛ ᴜᴘᴅᴀᴛᴇ ꜰᴀɪʟᴇᴅ! ᴇʀʀᴏʀ: {str(e)}"

        self.replyMessage(Message(text=msg_to_send), message_object, thread_id, thread_type)

    thread = threading.Thread(target=tk)  # Fixed the threading call
    thread.start()

def updatetk():
    def token():
        try:
            with open("token1.txt", "w") as token_file:
                token_file.write("")
            result = subprocess.run(
                ["python", "lol.py"], capture_output=True, text=True
            )
            if result.returncode == 0:
                msg_to_send = "ᴛᴏᴋᴇɴ ʜᴀꜱ ʙᴇᴇɴ ᴜᴘᴅᴀᴛᴇᴅ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ✅"
            else:
                msg_to_send = "ᴛᴏᴋᴇɴ ᴄᴏᴜʟᴅ ɴᴏᴛ ʙᴇ ᴜᴘᴅᴀᴛᴇᴅ, ᴘʟᴇᴀꜱᴇ ᴄʜᴇᴄᴋ ʟᴏʟ.py ɪɴᴘᴜᴛ!"
        except Exception as e:
            msg_to_send = f"ᴛᴏᴋᴇɴ ʟɪꜱᴛ ᴜᴘᴅᴀᴛᴇ ꜰᴀɪʟᴇᴅ! ᴇʀʀᴏʀ: {str(e)}"
    thread = threading.Thread(target=token)
    thread.start()


def update_tokens(num_token=0):
    try:
        cursor = botdb.cursor()
        cursor.execute("SELECT uid, password, jwt_token FROM accounts")
        accounts = cursor.fetchall()
        accounts = [(uid, pwd, token) for uid, pwd, token in accounts]
        
        tokens_list = TokenRetriever(accounts)
        tokens_list = tokens_list[:num_token] if num_token else tokens_list
        for uid, token in tokens_list:
            cursor.execute("UPDATE accounts SET jwt_token = ? WHERE uid = ?", (token, str(uid)))
        
        cursor.close()
        botdb.commit()

    except Exception as e:
        print(f"[!] Can't Update Token List! {e}")
def update_tokens_periodically():
    num_token = int(request.args.get('num_token', 0))
    thread = threading.Thread(target=updatetk())
    thread.start()
scheduler = BackgroundScheduler()
scheduler.add_job(update_tokens_periodically, 'interval', hours=1)
scheduler.start()
@app.route('/', methods=['GET'])
def main():
    response = {
        "main": "☑",
        "message": "Api Free Fire, Lấy Key Vui Lòng Liên Hệ Admin (Telegram: @TmrVirus)",
        "api": {
            "Likes ☑": "https://virusteam4.xlanznet.site/likes?key=[KEY]&uid=[UID]",
            "Visit ☑": "https://virusteam4.xlanznet.site/visit?key=[KEY]&uid=[UID]&sl=[SỐ LƯỢNG]",
            "Spam Friend ☑": "https://virusteam4.xlanznet.site/spamkb?key=[KEY]&uid=[UID]",
            "Check Info ☑": "https://virusteam4.xlanznet.site/info?uid=[UID]",
        },
            "Version": "BETA",
            "Copyright": "Lê Quốc Việt - Tmr Virus"
    }
    return app.response_class(
        response=json.dumps(response, ensure_ascii=False, indent=2),
        mimetype='application/json'
    ), 200
@app.route('/update/token', methods=['GET'])
def update_token_route():
    try:
        num_token = int(request.args.get('num_token', 0))
        thread = threading.Thread(target=updatetk())
        thread.start()
        response = {
            "status": "☑",
            "vsteam": "Update Tokens ☑"
        }
        return app.response_class(
            response=json.dumps(response, ensure_ascii=False, indent=2),
            mimetype='application/json'
        ), 200
    except Exception as e:
        response = {
            "status": "☒",
            "vsteam": "Update Tokens ☒"
        }
        return app.response_class(
            response=json.dumps(response, ensure_ascii=False, indent=2),
            mimetype='application/json'
        ), 500
@app.route('/visit', methods=['GET'])
def visit():
    try:
        key = request.args.get('key')
        uid = request.args.get('uid')
        number_visits = request.args.get('sl')

        if not key or not uid or not number_visits:
            response = {
                "status": "☒",
                "vsteam": "Missing Parameters! Provide Both /likes?key=[KEY]&uid=[UID]&sl=[SỐ LƯỢNG]"
            }
            return app.response_class(
                response=json.dumps(response, ensure_ascii=False, indent=2),
                mimetype='application/json'
            ), 400
        if os.path.exists('key.json'):
            with open('key.json', 'r') as f:
                keys = json.load(f)
        else:
            keys = {}
        if key not in keys:
            response = {
                "status": "☒",
                "vsteam": "Vui Lòng Nhập Đúng Key. Mua Key Liên Hệ Admin",
                "Contact": "Telegram: @TmrVirus"
            }
            return app.response_class(
                response=json.dumps(response, ensure_ascii=False, indent=2),
                mimetype='application/json'
            ), 403
        expiry_date = datetime.datetime.strptime(keys[key]["expiry_date"], '%Y-%m-%d %H:%M:%S')
        if expiry_date < datetime.datetime.now():
            response = {
                "status": "☒",
                "vsteam": "Key Expired! Please Contact Admin To Renew.",
                "Contact": "Telegram: @TmrVirus"
            }
            return app.response_class(
                response=json.dumps(response, ensure_ascii=False, indent=2),
                mimetype='application/json'
            ), 403
        if not uid.isdigit() or len(uid) < 8:
            response = {
                "status": "☒",
                "vsteam": "Invalid UID! The UID Should Be An 8 To 11 Digit Integer."
            }
            return app.response_class(
                response=json.dumps(response, ensure_ascii=False, indent=2),
                mimetype='application/json'
            ), 400
    
        if not number_visits.isdigit():
            response = {
                "status": "☒",
                "vsteam": "Number Of Visits Should Be An Integer."
            }
            return app.response_class(
                response=json.dumps(response, ensure_ascii=False, indent=2),
                mimetype='application/json'
            ), 400
    
        number_visits = int(number_visits)
        if number_visits < 50 or number_visits > 10000:
            response = {
                "status": "☒",
                "vsteam": "The Number Of Visits Must Be Between 50 And 10000."
            }
            return app.response_class(
                response=json.dumps(response, ensure_ascii=False, indent=2),
                mimetype='application/json'
            ), 400
        
        file_path = "token1.txt"
        try:
            with open(file_path, "r") as f:
                tokens = [line.strip().split()[-1] for line in f.readlines() if line.strip()]
        except FileNotFoundError:
            content = "ᴛʜᴇ ᴛᴏᴋᴇɴꜱ.ᴛxᴛ ꜰɪʟᴇ ᴡᴀꜱ ɴᴏᴛ ꜰᴏᴜɴᴅ! ᴘʟᴇᴀꜱᴇ ᴄʀᴇᴀᴛᴇ ᴛʜᴇ ꜰɪʟᴇ ᴀɴᴅ ᴀᴅᴅ ᴠᴀʟɪᴅ ᴛᴏᴋᴇɴꜱ."
            response = {
                "status": "☒",
                "vsteam": content
            }
            return app.response_class(
                response=json.dumps(response, ensure_ascii=False, indent=2),
                mimetype='application/json'
            ), 404
        acc_info = GetPlayerPersonalShow(uid, tokens[0])
        if not acc_info:
            response = {
                "status": "☒",
                "vsteam": "UID Incorrect Please Check Again."
            }
            return app.response_class(
                response=json.dumps(response, ensure_ascii=False, indent=2),
                mimetype='application/json'
            ), 404
        acc_info = Parser().parse(acc_info.hex())
        acc_info = VrxxTools().parsed_results_to_dict(acc_info)
        acc_name = acc_info[1][3]
        acc_region = acc_info[1][5]
        success_count = 0
        error_count = 0
        counter_lock = Lock()

        def send_visit(token):
            try:
                result = GetPlayerPersonalShow(uid, token)
                if result:
                    nonlocal success_count
                    with counter_lock:
                        success_count += 1
                return True
            except Exception as e:
                nonlocal error_count
                with counter_lock:
                    error_count += 1
                return False
        
        start = time.time()
        max_workers = min(1000, number_visits)
        try:
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                token_list = [tokens[i % len(tokens)] for i in range(number_visits)]
                list(executor.map(send_visit, token_list))
        except Exception as e:
            response = {
                "status": "☒",
                "vsteam": f"Please Try Again Later"
            }
            return app.response_class(
                response=json.dumps(response, ensure_ascii=False, indent=2),
                mimetype='application/json'
            ), 500
        
        end = time.time()
        duration = end - start
        visits_per_second = number_visits / duration if duration > 0 else 0
        response = {
            "status": "☑",
            "vsteam": {
                      "Name": acc_name,
                      "UID": uid,
                      "Successful": success_count,
                      "Failed": error_count,
                      "Time": f"{duration:.2f}s",
                      "Speed": f"{visits_per_second:.1f} visits/s"
            }
            
        }
        return app.response_class(
            response=json.dumps(response, ensure_ascii=False, indent=2),
            mimetype='application/json'
        ), 200

    except Exception as e:
        response = {
            "status": "☒",
            "vsteam": f"An error occurred: {str(e)}"
        }
        return app.response_class(
            response=json.dumps(response, ensure_ascii=False, indent=2),
            mimetype='application/json'
        ), 500
@app.route('/india/visit', methods=['GET'])
def visit():
    try:
        key = request.args.get('key')
        uid = request.args.get('uid')
        number_visits = request.args.get('sl')

        if not key or not uid or not number_visits:
            response = {
                "status": "☒",
                "vsteam": "Missing Parameters! Provide Both /likes?key=[KEY]&uid=[UID]&sl=[SỐ LƯỢNG]"
            }
            return app.response_class(
                response=json.dumps(response, ensure_ascii=False, indent=2),
                mimetype='application/json'
            ), 400
        if os.path.exists('key.json'):
            with open('key.json', 'r') as f:
                keys = json.load(f)
        else:
            keys = {}
        if key not in keys:
            response = {
                "status": "☒",
                "vsteam": "Vui Lòng Nhập Đúng Key. Mua Key Liên Hệ Admin",
                "Contact": "Telegram: @TmrVirus"
            }
            return app.response_class(
                response=json.dumps(response, ensure_ascii=False, indent=2),
                mimetype='application/json'
            ), 403
        expiry_date = datetime.datetime.strptime(keys[key]["expiry_date"], '%Y-%m-%d %H:%M:%S')
        if expiry_date < datetime.datetime.now():
            response = {
                "status": "☒",
                "vsteam": "Key Expired! Please Contact Admin To Renew.",
                "Contact": "Telegram: @TmrVirus"
            }
            return app.response_class(
                response=json.dumps(response, ensure_ascii=False, indent=2),
                mimetype='application/json'
            ), 403
        if not uid.isdigit() or len(uid) < 8:
            response = {
                "status": "☒",
                "vsteam": "Invalid UID! The UID Should Be An 8 To 11 Digit Integer."
            }
            return app.response_class(
                response=json.dumps(response, ensure_ascii=False, indent=2),
                mimetype='application/json'
            ), 400
    
        if not number_visits.isdigit():
            response = {
                "status": "☒",
                "vsteam": "Number Of Visits Should Be An Integer."
            }
            return app.response_class(
                response=json.dumps(response, ensure_ascii=False, indent=2),
                mimetype='application/json'
            ), 400
    
        number_visits = int(number_visits)
        if number_visits < 50 or number_visits > 10000:
            response = {
                "status": "☒",
                "vsteam": "The Number Of Visits Must Be Between 50 And 10000."
            }
            return app.response_class(
                response=json.dumps(response, ensure_ascii=False, indent=2),
                mimetype='application/json'
            ), 400
        
        file_path = "india.txt"
        try:
            with open(file_path, "r") as f:
                tokens = [line.strip().split()[-1] for line in f.readlines() if line.strip()]
        except FileNotFoundError:
            content = "ᴛʜᴇ ᴛᴏᴋᴇɴꜱ.ᴛxᴛ ꜰɪʟᴇ ᴡᴀꜱ ɴᴏᴛ ꜰᴏᴜɴᴅ! ᴘʟᴇᴀꜱᴇ ᴄʀᴇᴀᴛᴇ ᴛʜᴇ ꜰɪʟᴇ ᴀɴᴅ ᴀᴅᴅ ᴠᴀʟɪᴅ ᴛᴏᴋᴇɴꜱ."
            response = {
                "status": "☒",
                "vsteam": content
            }
            return app.response_class(
                response=json.dumps(response, ensure_ascii=False, indent=2),
                mimetype='application/json'
            ), 404
        acc_info = GetPlayerPersonalShow(uid, tokens[0])
        if not acc_info:
            response = {
                "status": "☒",
                "vsteam": "UID Incorrect Please Check Again."
            }
            return app.response_class(
                response=json.dumps(response, ensure_ascii=False, indent=2),
                mimetype='application/json'
            ), 404
        acc_info = Parser().parse(acc_info.hex())
        acc_info = VrxxTools().parsed_results_to_dict(acc_info)
        acc_name = acc_info[1][3]
        acc_region = acc_info[1][5]
        success_count = 0
        error_count = 0
        counter_lock = Lock()

        def send_visit(token):
            try:
                result = GetPlayerPersonalShow(uid, token)
                if result:
                    nonlocal success_count
                    with counter_lock:
                        success_count += 1
                return True
            except Exception as e:
                nonlocal error_count
                with counter_lock:
                    error_count += 1
                return False
        
        start = time.time()
        max_workers = min(1000, number_visits)
        try:
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                token_list = [tokens[i % len(tokens)] for i in range(number_visits)]
                list(executor.map(send_visit, token_list))
        except Exception as e:
            response = {
                "status": "☒",
                "vsteam": f"Please Try Again Later"
            }
            return app.response_class(
                response=json.dumps(response, ensure_ascii=False, indent=2),
                mimetype='application/json'
            ), 500
        
        end = time.time()
        duration = end - start
        visits_per_second = number_visits / duration if duration > 0 else 0
        response = {
            "status": "☑",
            "vsteam": {
                      "Name": acc_name,
                      "UID": uid,
                      "Successful": success_count,
                      "Failed": error_count,
                      "Time": f"{duration:.2f}s",
                      "Speed": f"{visits_per_second:.1f} visits/s"
            }
            
        }
        return app.response_class(
            response=json.dumps(response, ensure_ascii=False, indent=2),
            mimetype='application/json'
        ), 200

    except Exception as e:
        response = {
            "status": "☒",
            "vsteam": f"An error occurred: {str(e)}"
        }
        return app.response_class(
            response=json.dumps(response, ensure_ascii=False, indent=2),
            mimetype='application/json'
        ), 500
@app.route('/spamkb', methods=['GET'])
def spamkb():
    try:
        key = request.args.get('key')
        uid = request.args.get('uid')

        if not key or not uid:
            response = {
                "status": "☒",
                "vsteam": "Missing Parameters! Provide Both /spamkb?key=[KEY]&uid=[UID]"
            }
            return app.response_class(
                response=json.dumps(response, ensure_ascii=False, indent=2),
                mimetype='application/json'
            ), 400
        if os.path.exists('key.json'):
            with open('key.json', 'r') as f:
                keys = json.load(f)
        else:
            keys = {}
        if key not in keys:
            response = {
                "status": "☒",
                "vsteam": "Vui Lòng Nhập Đúng Key. Mua Key Liên Hệ Admin",
                "Contact": "Telegram: @TmrVirus"
            }
            return app.response_class(
                response=json.dumps(response, ensure_ascii=False, indent=2),
                mimetype='application/json'
            ), 403
        expiry_date = datetime.datetime.strptime(keys[key]["expiry_date"], '%Y-%m-%d %H:%M:%S')
        if expiry_date < datetime.datetime.now():
            response = {
                "status": "☒",
                "vsteam": "Key Expired! Please Contact Admin To Renew.",
                "Contact": "Telegram: @TmrVirus"
            }
            return app.response_class(
                response=json.dumps(response, ensure_ascii=False, indent=2),
                mimetype='application/json'
            ), 403
        if not uid or not uid.isdigit() or len(uid) < 8 or len(uid) > 12:
            response = {
                "status": "☒",
                "vsteam": "Invalid UID! The UID Should Be An Integer Between 8 To 12 Digits."
            }
            return app.response_class(
                response=json.dumps(response, ensure_ascii=False, indent=2),
                mimetype='application/json'
            ), 400
        file_path = "token1.txt"
        try:
            with open(file_path, "r") as f:
                tokens = [line.strip().split()[-1] for line in f.readlines() if line.strip()]
        except FileNotFoundError:
            content = "ᴛʜᴇ ᴛᴏᴋᴇɴꜱ.ᴛxᴛ ꜰɪʟᴇ ᴡᴀꜱ ɴᴏᴛ ꜰᴏᴜɴᴅ! ᴘʟᴇᴀꜱᴇ ᴄʀᴇᴀᴛᴇ ᴛʜᴇ ꜰɪʟᴇ ᴀɴᴅ ᴀᴅᴅ ᴠᴀʟɪᴅ ᴛᴏᴋᴇɴꜱ."
            response = {
                "status": "☒",
                "vsteam": content
            }
            return app.response_class(
                response=json.dumps(response, ensure_ascii=False, indent=2),
                mimetype='application/json'
            ), 404
        if not tokens:
            response = {
                "status": "☒",
                "vsteam": "No Valid Tokens Found. Please Check The Token Retrieval Process."
            }
            return app.response_class(
                response=json.dumps(response, ensure_ascii=False, indent=2),
                mimetype='application/json'
            ), 500
        acc_info = GetPlayerPersonalShow(uid, tokens[0])
        acc_info = Parser().parse(acc_info.hex())
        acc_info = VrxxTools().parsed_results_to_dict(acc_info)
        acc_name = acc_info[1][3]
        visit_script_path = os.path.join(os.getcwd(), "fr.py")
        process = subprocess.Popen(["python", visit_script_path, str(uid), "101"])

        print(f"✨ Successfully sent kb to UID: {uid} | Name: {acc_name}")
        response = {
            "status": "☑",
            "vsteam": f"Successfully Sent 100 Make Friend To UID: {uid} | {acc_name}"
        }
        return app.response_class(
            response=json.dumps(response, ensure_ascii=False, indent=2),
            mimetype='application/json'
        ), 200
    except Exception as e:
        print(f"Error in /visit: {e}")
        response = {
            "status": "☒",
            "vsteam": f"Failed Please Try Again!"
        }
        return app.response_class(
            response=json.dumps(response, ensure_ascii=False, indent=2),
            mimetype='application/json'
        ), 500


@app.route('/info', methods=['GET'])
def info_route():
    try:
        uid = request.args.get('uid')
        if not uid:
            return "ᴜɴᴀʙʟᴇ ᴛᴏ ɢᴇᴛ ᴀᴄᴄᴏᴜɴᴛ ɪɴꜰᴏʀᴍᴀᴛɪᴏɴ ʙᴇᴄᴀᴜꜱᴇ ᴜɪᴅ ɪꜱ ᴍɪꜱꜱɪɴɢ.", 400
        if not uid.isdigit() or not (8 <= len(uid) <= 12):
            return "ɪɴᴠᴀʟɪᴅ ᴜɪᴅ! ᴛʜᴇ ᴜɪᴅ ꜱʜᴏᴜʟᴅ ʙᴇ ᴀɴ 8 ᴛᴏ 12 ᴅɪɢɪᴛ ɪɴᴛᴇɢᴇʀ.", 400
        file_path = "token1.txt"
        try:
            with open(file_path, "r") as f:
                tokens = [line.strip().split()[-1] for line in f.readlines() if line.strip()]
        except FileNotFoundError:
            content = "ᴛʜᴇ ᴛᴏᴋᴇɴꜱ.ᴛxᴛ ꜰɪʟᴇ ᴡᴀꜱ ɴᴏᴛ ꜰᴏᴜɴᴅ! ᴘʟᴇᴀꜱᴇ ᴄʀᴇᴀᴛᴇ ᴛʜᴇ ꜰɪʟᴇ ᴀɴᴅ ᴀᴅᴅ ᴠᴀʟɪᴅ ᴛᴏᴋᴇɴꜱ."
            response = {
                "status": "☒",
                "vsteam": content
            }
            return app.response_class(
                response=json.dumps(response, ensure_ascii=False, indent=2),
                mimetype='application/json'
            ), 404
        acc_info = GetPlayerPersonalShow(uid, tokens[0])
        if b"token is expired" in acc_info:
            get_tokens()
            tokens = get_tokens()
            acc_info = GetPlayerPersonalShow(uid, tokens[0])
        
        elif b"BR_ACCOUNT_NOT_FOUND" in acc_info:
            response = "ᴛʜɪꜱ ɪᴅ ɴᴏᴛ ᴇxɪꜱᴛ ɪɴ ᴛʜᴇ ɢᴀʀᴇɴᴀ ᴅᴀᴛᴀʙᴀꜱᴇ ᴏʀ ʜᴀꜱ ɴᴏᴛ ꜰᴜʟʟʏ ʀᴇɢɪꜱᴛᴇʀᴇᴅ ɪɴ ᴀ ʀᴇɢɪᴏɴ"
            return app.response_class(
                response=json.dumps(response, ensure_ascii=False, indent=2),
                mimetype='application/json'
            ), 200
        
        elif acc_info == b"\n":
            response = "ʙᴏᴛ ᴄᴜʀʀᴇɴᴛʟʏ ᴅᴏᴇꜱɴ'ᴛ ꜱᴜᴘᴘᴏʀᴛ ɪɴᴅ, ʙʀ, ʙᴅ, ᴄɪꜱ ꜱᴇʀᴠᴇʀꜱ"
            return app.response_class(
                response=json.dumps(response, ensure_ascii=False, indent=2),
                mimetype='application/json'
            ), 200
        
        response1 = f"ꜰᴇᴛᴄʜɪɴɢ ɪɴꜰᴏʀᴍᴀᴛɪᴏɴ ᴏꜰ ᴜɪᴅ `{uid}`..."
        print(response1)
        
        info_extract = account_info_pb2.Info()
        info_extract.ParseFromString(acc_info)
        info_extract = MessageToDict(info_extract)
        
        petInfo = info_extract.get("petInfo", {})
        basicInfo = info_extract.get("basicInfo", {})
        socialInfo = info_extract.get("socialInfo", {})
        profileInfo = info_extract.get("profileInfo", {})
        guildBasicInfo = info_extract.get("guildBasicInfo", {})
        leaderBasicInfo = info_extract.get("leaderBasicInfo", {})
        creditScoreInfo = info_extract.get("creditScoreInfo", {})
        
        br_points = basicInfo.get("rankingPoints", 0)
        cs_points = basicInfo.get("csRankingPoints", 0)
        br_rank = getRank(br_points, "BR")
        cs_rank = getRank(cs_points, "CS")
        
        create_at = basicInfo.get("createAt", 0)
        lastlg_at = basicInfo.get("lastLoginAt", 0)
        
        equipped_list = basicInfo.get("weaponSkinShows", [])
        weapon_id = "Not Equipped"
        animation_id = "Not Equipped"
        transform_id = "Not Equipped"
        for unknown_id in equipped_list:
            unknown_id = str(unknown_id)
            
            if unknown_id.startswith("907"):
                weapon_id = unknown_id
            
            elif unknown_id.startswith("912"):
                animation_id = unknown_id
            
            elif unknown_id.startswith("914"):
                transform_id = unknown_id
        
        itemsId = json.load( open("./core/OB46-Item-ID.json") )
        
        titleId = basicInfo.get("title", 0)
        titleName = next((item["Name"] for item in itemsId if item["Item_ID"] == str(titleId)), "Undefined")
        
        characterId = profileInfo.get("characterId", 0)
        characterName = next((item["Name"] for item in itemsId if item["Item_ID"] == str(characterId)), "Undefined")
        
        
        skills_list = profileInfo.get("equippedSkills", [])
        skills_list = [getSkillName(skill.get("skillId")) for skill in skills_list]
        skills_list = [skill for skill in skills_list if skill is not None]
        
        account_info = {
            "status": "☑",
            "account_basic_info": {
                "uid": uid,
                "name": basicInfo.get("nickname", "Undefined"),
                "level": f"{basicInfo.get('level', 0)} (exp: {basicInfo.get('exp', 0)})",
                "region": basicInfo.get("region", "Undefined"),
                "likes": basicInfo.get("likes", 0),
                "honor_score": creditScoreInfo.get("creditScore", "Undefined"),
                "equipped_title": titleName,
                "evo_access_badge": "Active" if basicInfo.get("evoAccessBadge") else "Inactive"
            },
            "account_social_info": {
                "gender": socialInfo.get("gender", "Hidden"),
                "rank_show": socialInfo.get("modePrefer", "Undefined").replace("prefermode_", ""),
                "language": socialInfo.get("language", "Undefined").replace("Language_", ""),
                "signature": socialInfo.get("signature", "Default")
            },
            "account_activity": {
                "current_bp_badges": basicInfo.get("currentBPBadges", 0),
                "br_rank": br_rank,
                "cs_rank": cs_rank,
                "last_login": formatTime(lastlg_at),
                "created_at": formatTime(create_at)
            },
            "account_overview": {
                "avatar_id": basicInfo.get("avatarId", "Default"),
                "banner_id": basicInfo.get("bannerId", "Default"),
                "pin_id": basicInfo.get("pinId", "Default"),
                "equipped_gun_id": weapon_id,
                "equipped_anim_id": animation_id,
                "transform_anim_id": transform_id,
                "equipped_character": characterName,
                "equipped_skills": skills_list if skills_list else ["No Equipped"]
            },
            "pet_details": {
                "equipped": "Yes" if petInfo and petInfo.get("isSelected") else "No",
                "pet_id": petInfo.get("id", "Undefined") if petInfo else "Undefined",
                "pet_level": petInfo.get("level", "Undefined") if petInfo else "Undefined",
                "pet_exp": petInfo.get("exp", "Undefined") if petInfo else "Undefined",
                "pet_skin_id": petInfo.get("skinId", "Undefined") if petInfo else "Undefined",
                "pet_skill_id": petInfo.get("selectedSkillId", "Undefined") if petInfo else "Undefined"
            },
            "guild_info": {
                "guild_id": guildBasicInfo.get("GuildID", "Undefined") if guildBasicInfo else "Undefined",
                "guild_name": guildBasicInfo.get("GuildName", "Undefined") if guildBasicInfo else "Undefined",
                "guild_level": guildBasicInfo.get("GuildLevel", "Undefined") if guildBasicInfo else "Undefined",
                "live_members": f"{guildBasicInfo.get('GuildMember', 0)}/{guildBasicInfo.get('GuildCapacity', 0)}" if guildBasicInfo else "0/0",
                "leader_id": guildBasicInfo.get("GuildOwner", "Undefined") if guildBasicInfo else "Undefined",
                "status": "This account is not in a guild" if not guildBasicInfo else None
            },

            "Info Admin - Group": {
                "Admin": "Tmr Virus - Rov",
                "Telegram": "@TmrVirus",
                "Group Zalo": "https://zalo.me/g/nttwey011"
            }
        }
        return app.response_class(
            response=json.dumps(account_info, ensure_ascii=False, indent=2),
            mimetype='application/json'
        ), 200
    except Exception as e:
        response = {
            "status": "☒",
            "vsteam": f"Check Info Failed. Please Try Again! {e}"
        }
        return app.response_class(
            response=json.dumps(response, ensure_ascii=False, indent=2),
            mimetype='application/json'
        ), 500
@app.route('/taokey', methods=['GET'])
def create_key():
    try:
        admin_key = request.args.get('admin')
        new_key = request.args.get('key')
        expiry_days = request.args.get('time')

        if admin_key != "23092003":
            response = {
                "status": "☒",
                "vsteam": "?????"
            }
            return app.response_class(
                response=json.dumps(response, ensure_ascii=False, indent=2),
                mimetype='application/json'
            ), 403

        if not new_key or not expiry_days.isdigit():
            response = {
                "status": "☒",
                "vsteam": "Invalid Parameters! Provide /taokey?admin=&key=&time="
            }
            return app.response_class(
                response=json.dumps(response, ensure_ascii=False, indent=2),
                mimetype='application/json'
            ), 400
        expiry_date = (datetime.datetime.now() + datetime.timedelta(days=int(expiry_days))).strftime('%Y-%m-%d %H:%M:%S')
        if os.path.exists('key.json'):
            with open('key.json', 'r') as f:
                keys = json.load(f)
        else:
            keys = {}
        keys[new_key] = {
            "expiry_date": expiry_date,
            "created_date": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        with open('key.json', 'w') as f:
            json.dump(keys, f, ensure_ascii=False, indent=4)
        response = {
            "status": "☑",
            "vsteam": f"Key [ {new_key} ] Has Been Successfully Created!",
            "details": {
                "expiry_date": expiry_date
            }
        }
        return app.response_class(
            response=json.dumps(response, ensure_ascii=False, indent=2),
            mimetype='application/json'
        ), 200

    except Exception as e:
        response = {
            "status": "☒",
            "vsteam": f"Failure [ERROR]"
        }
        return app.response_class(
            response=json.dumps(response, ensure_ascii=False, indent=2),
            mimetype='application/json'
        ), 500
@app.route('/showkey', methods=['GET'])
def show_keys():
    try:
        admin_key = request.args.get('admin')
        with open("key.json", "r") as file:
            keys = json.load(file)
        
        if admin_key != "23092003":
            response = {
                "status": "☒",
                "vsteam": "?????"
            }
            return app.response_class(
                response=json.dumps(response, ensure_ascii=False, indent=2),
                mimetype='application/json'
            ), 403
        all_keys = {k: v for k, v in keys.items() if k != "23092003"}

        response = {
            "status": "☑",
            "vsteam": "Danh Sách Key",
            "keys": all_keys
        }
        return app.response_class(
            response=json.dumps(response, ensure_ascii=False, indent=2),
            mimetype='application/json'
        ), 200

    except Exception as e:
        response = {
            "status": "☒",
            "vsteam": f"ERROR"
        }
        return app.response_class(
            response=json.dumps(response, ensure_ascii=False, indent=2),
            mimetype='application/json'
        ), 500
@app.route('/xoakey', methods=['GET'])
def delete_key():
    try:
        admin_key = request.args.get('admin')
        key_to_delete = request.args.get('key')
        if not admin_key or not key_to_delete:
            response = {
                "status": "☒",
                "vsteam": "Missing Parameters! Provide Both"
            }
            return app.response_class(
                response=json.dumps(response, ensure_ascii=False, indent=2),
                mimetype='application/json'
            ), 400
        with open("key.json", "r") as file:
            keys = json.load(file)
        
        if admin_key != "23092003":
            response = {
                "status": "☒",
                "vsteam": "?????"
            }
            return app.response_class(
                response=json.dumps(response, ensure_ascii=False, indent=2),
                mimetype='application/json'
            ), 403
        if key_to_delete not in keys:
            response = {
                "status": "☒",
                "vsteam": f"Key [ {key_to_delete} ] Không Tồn Tại!"
            }
            return app.response_class(
                response=json.dumps(response, ensure_ascii=False, indent=2),
                mimetype='application/json'
            ), 404
        del keys[key_to_delete]
        with open("key.json", "w") as file:
            json.dump(keys, file, ensure_ascii=False, indent=2)

        response = {
            "status": "☑",
            "vsteam": f"Key [ {key_to_delete} ] Đã Được Xóa Thành Công!"
        }
        return app.response_class(
            response=json.dumps(response, ensure_ascii=False, indent=2),
            mimetype='application/json'
        ), 200

    except Exception as e:
        response = {
            "status": "☒",
            "vsteam": f"ERROR"
        }
        return app.response_class(
            response=json.dumps(response, ensure_ascii=False, indent=2),
            mimetype='application/json'
        ), 500
@app.route('/likes', methods=['GET'])
def like_with_key():
    try:
        key = request.args.get('key')
        uid = request.args.get('uid')

        if not key or not uid:
            response = {
                "status": "☒",
                "vsteam": "Missing Parameters! Provide Both /likes?key=[KEY]&uid=[UID]"
            }
            return app.response_class(
                response=json.dumps(response, ensure_ascii=False, indent=2),
                mimetype='application/json'
            ), 400
        if os.path.exists('key.json'):
            with open('key.json', 'r') as f:
                keys = json.load(f)
        else:
            keys = {}
        if key not in keys:
            response = {
                "status": "☒",
                "vsteam": "Vui Lòng Nhập Đúng Key. Mua Key Liên Hệ Admin",
                "Contact": "Telegram: @TmrVirus"
            }
            return app.response_class(
                response=json.dumps(response, ensure_ascii=False, indent=2),
                mimetype='application/json'
            ), 403
        expiry_date = datetime.datetime.strptime(keys[key]["expiry_date"], '%Y-%m-%d %H:%M:%S')
        if expiry_date < datetime.datetime.now():
            response = {
                "status": "☒",
                "vsteam": "Key Expired! Please Contact Admin To Renew.",
                "Contact": "Telegram: @TmrVirus"
            }
            return app.response_class(
                response=json.dumps(response, ensure_ascii=False, indent=2),
                mimetype='application/json'
            ), 403
        if not uid or not uid.isdigit() or len(uid) < 8 or len(uid) > 12:
            response = {
                "status": "☒",
                "vsteam": "Invalid UID! The UID should be an integer between 8 to 12 digits."
            }
            return app.response_class(
                response=json.dumps(response, ensure_ascii=False, indent=2),
                mimetype='application/json'
            ), 400

        file_path = "token1.txt"
        try:
            with open(file_path, "r") as f:
                tokens = [line.strip().split()[-1] for line in f.readlines() if line.strip()]
        except FileNotFoundError:
            content = "ᴛʜᴇ ᴛᴏᴋᴇɴꜱ.ᴛxᴛ ꜰɪʟᴇ ᴡᴀꜱ ɴᴏᴛ ꜰᴏᴜɴᴅ! ᴘʟᴇᴀꜱᴇ ᴄʀᴇᴀᴛᴇ ᴛʜᴇ ꜰɪʟᴇ ᴀɴᴅ ᴀᴅᴅ ᴠᴀʟɪᴅ ᴛᴏᴋᴇɴꜱ."
            response = {
                "status": "☒",
                "vsteam": content
            }
            return app.response_class(
                response=json.dumps(response, ensure_ascii=False, indent=2),
                mimetype='application/json'
            ), 404
        acc_info = GetPlayerPersonalShow(uid, tokens[0])

        if b"token is expired" in acc_info:
            get_tokens()
            tokens = get_tokens()
            acc_info = GetPlayerPersonalShow(uid, tokens[0])

        elif b"BR_ACCOUNT_NOT_FOUND" in acc_info:
            response = {
                "status": "☒",
                "vsteam": "This UID does not exist in the database or is not fully registered in any region."
            }
            return app.response_class(
                response=json.dumps(response, ensure_ascii=False, indent=2),
                mimetype='application/json'
            ), 404
        
        acc_info = Parser().parse(acc_info.hex())
        acc_info = VrxxTools().parsed_results_to_dict(acc_info)
        acc_name = acc_info[1][3]
        acc_region = acc_info[1][5]
        likes_before = int(acc_info[1].get(21, 0))

        response = f"Sending likes to UID: {uid}, Nickname: {acc_name}, Region: {acc_region}..."
        print(response)
        used_tokens = set()
        while tokens:
            tokens_batch = [token for token in tokens if token not in used_tokens][:101]
            if not tokens_batch:
                get_tokens()
                response = {
                    "status": "☒",
                    "vsteam": "Token has just been updated. Please try again."
                }
                return app.response_class(
                    response=json.dumps(response, ensure_ascii=False, indent=2),
                    mimetype='application/json'
                ), 500
            
            start = time.time()
            success, error = asyncio.run(LikeProfile(uid, acc_region, tokens))
            end = time.time()

            if not success and error >= 100:
                used_tokens.update(tokens_batch)
            else:
                break
        
        tts_like = f"{(end - start):.2f}"
        acc_info = GetPlayerPersonalShow(uid, tokens[0])
        acc_info = Parser().parse(acc_info.hex())
        acc_info = VrxxTools().parsed_results_to_dict(acc_info)
        likes_after = int(acc_info[1].get(21, 0))
        
        likes_increase = likes_after - likes_before
        if not likes_increase and success:
            response = {
                "status": "☄",
                "vsteam": f"Account with UID `{uid}` has reached the maximum likes for today. Please try again tomorrow."
            }
            return app.response_class(
                response=json.dumps(response, ensure_ascii=False, indent=2),
                mimetype='application/json'
            ), 200
        response = {
            "status": "☑",
            "UID Validated - API connected": {
                "UID": uid,
                "Name": acc_name,
                "Region": acc_region,
                "Time Sent": f"{tts_like} sec"
            },
            "Likes details": {
                "Likes Before CMD": likes_before,
                "Likes After CMD": likes_after,
                "Likes Given By API": likes_increase
            },
            "Info Admin - Group": {
                "Admin": "Tmr Virus - Rov",
                "Telegram": "@TmrVirus",
                "Group Zalo": "https://zalo.me/g/nttwey011"
            }
        }

        return app.response_class(
            response=json.dumps(response, ensure_ascii=False, indent=2),
            mimetype='application/json'
        ), 200

    except Exception as e:
        response = {
            "status": "☒",
            "vsteam": f"Buff Likes Failed. Please Try Again!"
        }
        return app.response_class(
            response=json.dumps(response, ensure_ascii=False, indent=2),
            mimetype='application/json'
        ), 500
def create_like_route(route_num):
    endpoint_name = f'like_with_key_route_{route_num}'  # Tạo endpoint duy nhất
    @app.route(f'/likes{route_num}', methods=['GET'], endpoint=endpoint_name)
    def like_with_key_route():
        try:
            key = request.args.get('key')
            uid = request.args.get('uid')

            if not key or not uid:
                return json_response("☒", "Missing Parameters! Provide Both /likes1?key=[KEY]&uid=[UID]", 400)

            if os.path.exists('key.json'):
                with open('key.json', 'r') as f:
                    keys = json.load(f)
            else:
                keys = {}

            if key not in keys:
                return json_response("☒", "Vui Lòng Nhập Đúng Key. Mua Key Liên Hệ Admin", 403)

            expiry_date = datetime.datetime.strptime(keys[key]["expiry_date"], '%Y-%m-%d %H:%M:%S')
            if expiry_date < datetime.datetime.now():
                return json_response("☒", "Key Expired! Please Contact Admin To Renew.", 403)

            if not uid or not uid.isdigit() or len(uid) < 8 or len(uid) > 12:
                return json_response("☒", "Invalid UID! The UID should be an integer between 8 to 12 digits.", 400)

            file_path = f"token{route_num}.txt"
            try:
                with open(file_path, "r") as f:
                    tokens = [line.strip().split()[-1] for line in f.readlines() if line.strip()]
            except FileNotFoundError:
                return json_response("☒", "ᴛʜᴇ ᴛᴏᴋᴇɴꜱ.ᴛxᴛ ꜰɪʟᴇ ᴡᴀꜱ ɴᴏᴛ ꜰᴏᴜɴᴅ! ᴘʟᴇᴀꜱᴇ ᴄʀᴇᴀᴛᴇ ᴛʜᴇ ꜰɪʟᴇ ᴀɴᴅ ᴀᴅᴅ ᴠᴀʟɪᴅ ᴛᴏᴋᴇɴꜱ.", 404)

            acc_info = GetPlayerPersonalShow(uid, tokens[0])

            if b"token is expired" in acc_info:
                get_tokens()
                tokens = get_tokens()
                acc_info = GetPlayerPersonalShow(uid, tokens[0])

            elif b"BR_ACCOUNT_NOT_FOUND" in acc_info:
                return json_response("☒", "This UID does not exist in the database or is not fully registered in any region.", 404)

            acc_info = Parser().parse(acc_info.hex())
            acc_info = VrxxTools().parsed_results_to_dict(acc_info)
            acc_name = acc_info[1][3]
            acc_region = acc_info[1][5]
            likes_before = int(acc_info[1].get(21, 0))

            response = f"Sending likes to UID: {uid}, Nickname: {acc_name}, Region: {acc_region}..."
            print(response)
            used_tokens = set()
            while tokens:
                tokens_batch = [token for token in tokens if token not in used_tokens][:101]
                if not tokens_batch:
                    get_tokens()
                    return json_response("☒", "Token has just been updated. Please try again.", 500)

                start = time.time()
                success, error = asyncio.run(LikeProfile(uid, acc_region, tokens))
                end = time.time()

                if not success and error >= 100:
                    used_tokens.update(tokens_batch)
                else:
                    break

            tts_like = f"{(end - start):.2f}"
            acc_info = GetPlayerPersonalShow(uid, tokens[0])
            acc_info = Parser().parse(acc_info.hex())
            acc_info = VrxxTools().parsed_results_to_dict(acc_info)
            likes_after = int(acc_info[1].get(21, 0))

            likes_increase = likes_after - likes_before
            if not likes_increase and success:
                return json_response("☄", f"Account with UID `{uid}` has reached the maximum likes for today. Please try again tomorrow.", 200)

            return json_response("☑", {
                "UID Validated - API connected": {
                    "UID": uid,
                    "Name": acc_name,
                    "Region": acc_region,
                    "Time Sent": f"{tts_like} sec"
                },
                "Likes details": {
                    "Likes Before CMD": likes_before,
                    "Likes After CMD": likes_after,
                    "Likes Given By API": likes_increase
                }
            }, 200)

        except Exception as e:
            return json_response("☒", f"Buff Likes Failed. Error: {str(e)}", 500)

def json_response(status, message, code):
    response = {
        "status": status,
        "vsteam": message,
        "Contact": "Telegram: @TmrVirus"
    }
    return app.response_class(
        response=json.dumps(response, ensure_ascii=False, indent=2),
        mimetype='application/json'
    ), code

for i in range(1, 8):
    create_like_route(i)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
