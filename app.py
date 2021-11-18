import uvicorn
from fastapi import FastAPI, Request
from predict_nghia import *
from colabcode import ColabCode
from gg_search import GoogleSearch
from relevance_ranking import rel_ranking
import time
import numpy as np
import gg_search_norank
from pyngrok import ngrok
import json
from starlette.responses import RedirectResponse
import os
app = FastAPI()


predictor = Predictor()
gg_search = GoogleSearch.getInstance()
URL_FOLDER = '/content/drive/MyDrive/Web_Nghia/url'
@app.get("/")
async def index():
  active_tunnels = ngrok.get_tunnels()

  public_url = {"url": active_tunnels[0].public_url}
  with open(os.path.join(URL_FOLDER, "url.json"), "w") as bf:
    json.dump(public_url, bf)
  return RedirectResponse(url = "http://localhost:8501")
  # return "Get OK"


@app.post("/closedomain")
async def submit(request: Request):
    form_data = await request.json()
    # print('form_data',form_data)
    questions = str(form_data['question'])
    # print(questions)
    contexts = str(form_data['context'])
    # print(contexts)
    model = str(form_data['model'])

    QA_input = {
  'question': questions,
  'context': contexts
    }
    # if model == 'hieu-close':
    #   res = predictor.getPredictions1(QA_input,1)
    # elif model == 'binh-close':
    #   res = predictor.getPredictions2(QA_input,1)
    # elif model == 'hieu-open':
    #   res = predictor.getPredictions1(QA_input,2)
    # elif model == 'binh-open':
    #   res = predictor.getPredictions2(QA_input,2)
    # if model == 'hieu-close':
    res = predictor.getPredictions1(QA_input,1)
    # elif model == 'binh-open':
    #   res = predictor.getPredictions2(QA_input,2)
    print(res)
    return res

@app.post("/opendomain")
async def submit(request: Request):
    form_data = await request.json()
    # print('form_data',form_data)
    questions = str(form_data['question'])
    print(questions)
    print(type(questions))
    model = str(form_data['model'])
    token_query = gg_search_norank.tokenize(questions)[0]
    keywords = gg_search_norank.keywords_extraction(token_query)
    li, urls = gg_search_norank.reurl_li(questions, keywords)
    b = gg_search_norank.reb(li)
    ques = []
    cont = []
    for i,item_b in enumerate(b):
      contexts_ = item_b.replace('_',' ')
      if contexts_:
        ques.append(questions)
        cont.append(contexts_)

    # ques = np.array(ques, dtype="object")
    # cont = np.array(cont, dtype="object")

    QA_input = {
    'question': ques,
    'context': cont
    }

    print(type(QA_input['question']))
    print(type(QA_input['context']))
    print(QA_input)
    # if model == 'hieu-close':
    #   res = predictor.getPredictions1(QA_input,1)
    # elif model == 'binh-close':
    #   res = predictor.getPredictions2(QA_input,1)
    # elif model == 'hieu-open':
    #   res = predictor.getPredictions1(QA_input,2)
    # elif model == 'binh-open':
    #   res = predictor.getPredictions2(QA_input,2)
    # res = []
    # if model == 'binh-close':
    #   res = predictor.getPredictions2(QA_input,1)
    # elif model == 'binh-open':
    #   res = predictor.getPredictions2(QA_input,2)
    res = predictor.getPredictions1(QA_input,3)
    print(res)
    result = {}
    maxs = 0
    for item in range(len(res)-1):
      if res[item]['score']>maxs:
        maxs = res[item]['score']
        result['answer'] = res[item]['answer']
        result['score'] = res[item]['score']
    result['total_time']=res[-1]['total_time']
    return result

@app.post("/opendomainranking")
async def submit(request: Request):
    form_data = await request.json()
    # print('form_data',form_data)
    questions = str(form_data['question'])
    # print(questions)
    # contexts = str(form_data['context'])
    # print(contexts)
    # start = time.time()
    links, documents = gg_search.search(questions)
    # print("link, document:", time.time()-start)
    # start = time.time()
    contexts = rel_ranking(questions,documents)
    # print("ranking:", time.time()-start)
    contexts = contexts[:40]
    print(contexts)
    examples = {"question": [], "context": []}
    for i in range(len(contexts)):
        examples["question"].append(questions)
        examples["context"].append(contexts[i])
    QA_input = examples
    print(examples)
    res = predictor.getPredictions1(QA_input,3)

    # answers = [[contexts[i], res[i][0],res[i][1]] for i in range(0,len(res)-1)]
    # answers = [a for a in answers if a[1] != '']
    # answers.sort(key = lambda x : x[2],reverse=True)

    # print("Final result: ")
    # print("Passage: ", answers[0][0])
    # print("Answer : ", answers[0][1])
    # print("Score  : ", answers[0][2])


    print(res)
    result = {}
    maxs = 0
    for item in range(len(res)-1):
      if res[item]['score']>maxs:
        maxs = res[item]['score']
        result['answer'] = res[item]['answer']
        result['score'] = res[item]['score']
    result['total_time']=res[-1]['total_time']
    return result


if __name__ == "__main__": 
    # uvicorn.run(app,port=8084, debug=True)
    server = ColabCode(port=5001, code=False)
    server.run_app(app=app)
    # app.run_server(mode='external')
