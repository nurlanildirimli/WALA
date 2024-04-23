from flask import Flask, jsonify,render_template, request 
from flask_cors import CORS
import threading
import textcomp as tx
import imagetext as it
import vicramcalc as vc
import whitespace as ws
import imagecalc as im
import imagemain as imm
import crawler as cw
import requests

app = Flask(__name__) 

cors = CORS(app) 

@app.route('/') 
def hello(): 
    return render_template('popup.html') 
  
@app.route("/scan", methods=['GET'])
def Scan():
   result = {
       "Visual Complexity": 0,
       "Distinguishability": 0,
       "Text Image Ratio": 0,
       "Text Complexity": 0,
       "Image Complexity": 0,
   }
   url = request.args.get('data1')
   visualcomp = request.args.get('data2')
   distin = request.args.get('data3')
   text_image = request.args.get('data4')
   textc = request.args.get('data5')
   image = request.args.get('data6')
   
   print("DATAA",url,visualcomp,distin,text_image,textc,image)

   inner_urls=cw.crawler(url)
   inner_urls.insert(0,url)

   def calculate_visual_complexity(url, vis, index):
        out = vc.vicramcalc1("example_role",url)
        vis.append(out)
        if index == 1:
            result["Visual Complexity"]= out
            
   def calculate_distinguishability(url, dist, index):
        out = ws.vicramcalc("example_role",url)
        dist.append(out)
        if index == 1:
            result["Distinguishablity"]=out
            
   def calculate_text_image_ratio(response, te_im, index):
        out = it.calculate_image_text_ratio(response)
        te_im.append(out)
        if index == 1:
            result["Text Image Ratio"]= out
            
   def calculate_text_complexity(response, tex, index):
        out = tx.text_complexity(response)
        tex.append(out)
        if index == 1:
            result["Text Complexity"]= out
            
   def calculate_image_complexity(url, response, ima, index):   
        out = im.calculate_image(response,url)
        ima.append(out)
        if index == 1:
            result["Image Complexity"]= out
            
   index = 0
   vis = []
   dist = []
   te_im = []
   tex = []
   ima = []
   urls = []
   threads = []
   for inner_url in inner_urls:  
        index = index + 1
        if text_image == "true" or textc == "true" or image == "true":
            response = requests.get(inner_url)
        if visualcomp == "true":
            threads.append(threading.Thread(target=calculate_visual_complexity,args=(inner_url,vis,index)))
        if distin == "true":
            threads.append(threading.Thread(target=calculate_distinguishability,args=(inner_url,dist,index)))
        if text_image == "true":
            threads.append(threading.Thread(target=calculate_text_image_ratio,args=(response,te_im,index)))
        if textc == "true":
            threads.append(threading.Thread(target=calculate_text_complexity,args=(response,tex,index)))
        if image == "true":
            threads.append(threading.Thread(target=calculate_image_complexity,args=(inner_url,response,ima,index)))
   
   if visualcomp == "false":
        result["Visual Complexity"]="NA"
   if distin == "false":
        result["Distinguishability"]="NA"
   if text_image == "false":
        result["Text Image Ratio"]="NA"
   if textc == "false":
        result["Text Complexity"]="NA"
   if image == "false":
        result["Image Complexity"]="NA"

    # Start Threads
   for thread in threads:
        thread.start()

    # Wait Threads
   for thread in threads:
        thread.join()
   print(vis,dist,te_im,tex,ima)

   #return jsonify({'message': f'Data received: {result}'})
   return jsonify(result)

   
if __name__ == '__main__': 
    app.run(debug=True) 
    
    # get methods as shown in CNG 445
