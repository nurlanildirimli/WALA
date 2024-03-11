from flask import Flask, jsonify,render_template, request 
from flask_cors import CORS
import textcomp as tx
import imagetext as it
import vicramcalc as vc
import whitespace as ws
import imagecalc as im

app = Flask(__name__) 

cors = CORS(app) 

@app.route('/') 
def hello(): 
    return render_template('popup.html') 
  
@app.route("/scan", methods=['GET'])
def Scan():
   result = {
       "Visual Complexity": 0,
       "Distinguishablity": 0,
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
   
   if visualcomp == "true":
       result["Visual Complexity"]=vc.vicramcalc1("example_role",url)
   else:
       result["Visual Complexity"]="NA"
   if distin == "true":
       result["Distinguishablity"]=ws.vicramcalc("example_role",url)
   else:
       result["Distinguishablity"]="NA"
   if text_image == "true":
       result["Text Image Ratio"]=it.calculate_image_text_ratio(url)
   else:
       result["Text Image Ratio"]="NA"
   if textc == "true":
       result["Text Complexity"]=tx.text_complexity(url)
   else:
       result["Text Complexity"]="NA"
   if image == "true":
       pass
       result["Image Complexity"]="0.60"
   else:
       result["Image Complexity"]="NA"

   #return jsonify({'message': f'Data received: {result}'})
   return jsonify(result)
   '''res = ""
   data = request.get_json()

   result1=data
   print(tx.text_complexity(result1[0]))
   data.extend(tx.text_complexity(result1[0]))
   #data = jsonify(data)
   print(result1)
   for x in result1:
       res += str(x) + ";"
   abc="aaaaa"
   data1 = {
        "message" : res,
        "id" : "11",
    }
   return jsonify(res)'''

   
if __name__ == '__main__': 
    app.run(debug=True) 


    # get methods as shown in cng 445