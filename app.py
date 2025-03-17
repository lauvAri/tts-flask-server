from flask import Flask, jsonify, request, send_file, send_from_directory, session
from flask_cors import CORS
from gradio_client import Client, file
import os
from pdf import get_pdf_page, get_pdf_pages
import doubao_vision
import tencent_cos

app = Flask(__name__)
app.secret_key = 'python-flask-secret-key'
CORS(app)

# 连接推理客户端
client = Client("http://localhost:9872/")

ref_audio_folder = os.path.join(os.getcwd(), "upload", "ref_audio")
os.makedirs(ref_audio_folder, exist_ok=True)

@app.route('/')
def start():
    return "<p>server is running</p>"

'''
获取模型
'''
@app.get('/api/change_choices')
def change_choices():
    result = client.predict(
		api_name="/change_choices"
    )
    list_data = list(result)
    return jsonify(list_data)

'''
修改GPT模型
'''
@app.get('/api/change_gpt_weights')
def change_gpt_weights():
    weights_path = request.args.get("weights_path")
    result = client.predict(
        gpt_path = weights_path,
		api_name="/change_gpt_weights"
    )
    print(result)
    return jsonify(list(result))

'''
修改SoVITS模型
'''
@app.get('/api/change_sovits_weights')
def change_sovits_weights():
    weights_path = request.args.get("weights_path")
    result = client.predict(
		sovits_path=weights_path,
		api_name="/change_sovits_weights"
    )
    print(result)
    return jsonify(list(result))

@app.post('/api/upload_ref_audio')
def upload_ref_audio():
    file = request.files.get('audio_file')
    if file:
        filepath = os.path.join(ref_audio_folder, file.filename)
        file.save(filepath)
        return jsonify({'message': '文件上传成功', 'file_path': f"{ref_audio_folder}/{file.filename}"}), 200
    else:
        # 400 Bad Request
        return jsonify({'message': '文件上传失败'}), 400

'''
生成音频文件
仅用于测试目的
'''
@app.get('/api/get_tts_wav')
def get_tts_wav():
    result = client.predict(
            ref_wav_path=file("C://Users//19871//Documents//录音//record.m4a"),
            prompt_text="",
            prompt_language="中文",
            text="请合成这段文本",
            text_language="粤语",
            how_to_cut="凑四句一切",
            top_k=15,
            top_p=1,
            temperature=1,
            ref_free=False,
            speed=1,
            if_freeze=False,
            inp_refs=None,
            api_name="/get_tts_wav"
    )
    # result是音频文件的绝对路径
    '''
    send_file发送文件
    mimetype设置文件类型
    '''
    response = send_file(result, mimetype = "audio/wav")
    # 设置响应头信息，使得浏览器知道如何处理该文件
    response.headers.set("Content-Disposition", "attachment", filename="result.wav")
    return response

'''
生成音频文件
'''
@app.post("/api/get_tts_wav")
def get_tts_wav_post():
    data = request.get_json()
    session["ref_wav_path_str"] = data.get("ref_wav_path")
    result = client.predict(
        ref_wav_path = file(data.get("ref_wav_path")),
        prompt_text = data.get("prompt_text"),
        prompt_language = data.get("prompt_language"),
        text = data.get("text"),
        text_language = data.get("text_language"),
        how_to_cut = data.get("how_to_cut"),
        top_k = data.get("top_k"),
        top_p = data.get("top_p"),
        temperature = data.get("temperature"),
        ref_free = data.get("ref_free"),
        speed = data.get("speed"),
        if_freeze = data.get("if_freeze"),
        inp_refs = None,
        api_name="/get_tts_wav"
    )
    response = send_file(result, mimetype = "audio/wav")
    # 设置响应头信息，使得浏览器知道如何处理该文件
    response.headers.set("Content-Disposition", "attachment", filename="result.wav")
    return response


'''pdf上传'''
@app.post('/api/upload_pdf')
def upload_pdf():
    if 'file' not in request.files:
        return jsonify({"error": "没有文件"}), 400
    file = request.files['file']
    if file and file.filename.endswith('.pdf'):
        filename = file.filename
        filepath = os.path.join('upload/pdf', filename)
        file.save(filepath)
        file_url = f"http://localhost:5000/api/view_pdf/{filename}"
        return jsonify({"file_url": file_url, "pdf_path":f"upload/pdf/{filename}"}), 200
    return jsonify({"error": "上传pdf失败"}), 400

'''查看pdf'''
@app.get('/api/view_pdf/<filename>')
def view_pdf(filename):
    return send_from_directory('upload/pdf', filename)

'''获取pdf页面'''
@app.get("/api/get_pdf_page")
def api_get_pdf_page():
    pdf_path = request.args.get("pdf_path")
    page_num = int(request.args.get("page_num", 1))
    flag, data = get_pdf_page(pdf_path, page_num)
    if flag:
        return jsonify(data), 200
    else:
        return jsonify({"error": data}), 400
    
'''使用豆包视觉模型 进行pdf总结摘要'''
@app.post("/api/get_summary")
def api_get_summary():
    img_data = request.get_json()["img_data"]
    choice = doubao_vision.get_vision_text(img_data)
    print(choice.message.content)
    if hasattr(choice, "message") and hasattr(choice.message, "content"):
        summary = choice.message.content
        return jsonify({"summary": summary}), 200
    else:
        return jsonify({"error": "获取摘要失败"}), 400
@app.post("/api/summary2audio")
def api_summary2audio():
    data = request.get_json()
    result = client.predict(
        ref_wav_path = file(session.get("ref_wav_path_str", "upload/ref_audio/record.m4a")),
        text = data.get("summary"),
        text_language = "多语种混合",
        inp_refs = None,
        api_name = "/get_tts_wav"
    )
    cos_resp = tencent_cos.putToTencentCOS(result)
    if cos_resp.get("status") == "success":
        key = cos_resp.get("key")
        return jsonify({
            "status": "success",
            "key": key,
            "url": f"https://tts-1326430649.cos.ap-guangzhou.myqcloud.com/{key}"
        })
    else:
        return jsonify({
            "status": "error",
            "message": cos_resp.get("message", "上传失败")
        })


@app.get("/api/get_pdf_pages")
def api_get_pdf_pages():
    pdf_path = request.args.get("pdf_path")
    data = get_pdf_pages(pdf_path)
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)