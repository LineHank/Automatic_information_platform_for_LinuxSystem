from flask import Flask, render_template, request, make_response
import json
import light_calc

app = Flask(__name__)
app.debug = True


@app.route('/', methods=['POST', 'GET'])
def main():
    return render_template('test_inputs.html')


@app.route('/calc', methods=['POST'])
def calc():
    data_list = []
    data = json.loads(request.get_data(as_text=True))  # request.get_data(as_text=True) ： 获取前端POST请求传过来的 json 数据
    for key, value in data.items():
        if value == '':
            data[key] = 0
    for key, value in data.items():
        if type(value) == str and value != 'i':
            data[key] = float(value)

    for i in data['data_list']:
        new_dict = {}
        new_dict['r'] = float(i['r'])
        new_dict['d'] = float(i['d'])
        new_dict['n'] = float(i['n'])
        new_dict['n_2'] = float(i['n_2'])
        data_list.append(new_dict)
    print(data)
    print(data_list)
    try:
        result = light_calc.main(data['D'], data['q'], data['ls'], data['Lz'], data['Uz'], data['l'], data['u'],
                                 data['y'],
                                 data['P'], data['h1'], data_list)
        resp = make_response(result)
        resp.headers['Content-Type'] = 'text/json'
        return result
    except Exception as e:
        print(e)
        return '{"status":"500"}'


if __name__ == '__main__':
    app.run()