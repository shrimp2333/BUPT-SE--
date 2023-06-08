from flask import Flask, jsonify
from flask_cors import CORS
from flask import request

app = Flask(__name__)
CORS(app)


@app.route('/a/login', methods=['POST'])
def login():
    dic = {"code": 200, "msg": "登录成功", "token": "sdadasda"}
    return jsonify(dic), 200


@app.route('/admin/user/list', methods=['GET'])
def user1():
    data1 = {
        "user_id": "0",
        "username": "string",
        "password": "string",
        "email": "string",
        "license_plate": "string",
        "battery_capacity": 0,
        "car_type": "老头乐",
        "created_at": "string",
        "updated_at": "string"
    }
    list1 = []
    for i in range(130):
        data2 = data1.copy()
        list1.append(data1)
        data2["user_id"] = str(i + 1)
        data1 = data2
    dic = {"code": 200, "msg": "111", "data": list1}
    return jsonify(dic), 200


@app.route('/admin/user/detail', methods=['GET'])
def user2():
    data1 = {
        "log": [
            {
                "detail_id": 0,
                "status": 1,
                "generate_time": 0,
                "charging_pile_id": 0,
                "user_id": 0,
                "charging_power": 0,
                "charging_duration": 0,
                "start_time": 0,
                "end_time": 0,
                "charging_fee": 0,
                "service_fee": 0,
                "total_fee": 0,
                "charging_type": 0
            },
            {
                "detail_id": 1,
                "status": 1,
                "generate_time": 0,
                "charging_pile_id": 0,
                "user_id": 0,
                "charging_power": 0,
                "charging_duration": 0,
                "start_time": 0,
                "end_time": 0,
                "charging_fee": 0,
                "service_fee": 0,
                "total_fee": 0,
                "charging_type": 0
            }
        ],
        "user_info": {
            "user_id": "string",
            "username": "string",
            "password": "string",
            "email": "string",
            "license_plate": "string",
            "battery_capacity": 0,
            "car_type": "string",
            "created_at": "string",
            "updated_at": "string"
        }
    }
    dic = {"code": 200, "msg": "111", "data": data1}
    return jsonify(dic), 200


@app.route('/admin/user/modify', methods=['POST'])
def user3():
    data = request.get_json()
    user_id = data.get('user_id')
    field = data.get('field')
    value = data.get('value')
    print(user_id)
    print(field)
    print(value)
    dic = {"code": 200, "msg": "修改成功"}
    return jsonify(dic), 200


@app.route('/admin/charge/detail', methods=['GET'])
def pile1():
    d1 = {
        "code": 200,
        "msg": "string",
        "data": {
            "charging_pile_info": {
                "charging_pile_id": 6,
                "charging_type": 5,
                "status": 4,
                "charging_fee": 3,
                "charging_duration": 2,
                "charging_power": 1
            },
            "log": [
                {
                    "charging_pile_id": 0,
                    "total_charging_times": 100,
                    "total_charging_duration": 60,
                    "date": 1621448793.1234567,
                    "total_charging_power": 100,
                    "charging_fee": 0,
                    "service_fee": 0,
                    "total_fee": 3100
                },
                {
                    "charging_pile_id": 0,
                    "total_charging_times": 600,
                    "total_charging_duration": 30,
                    "date": 1621448793.1234567,
                    "total_charging_power": 1000,
                    "charging_fee": 0,
                    "service_fee": 0,
                    "total_fee": 1200
                },
                {
                    "charging_pile_id": 0,
                    "total_charging_times": 150,
                    "total_charging_duration": 60,
                    "date": 1621448793.1234567,
                    "total_charging_power": 9000,
                    "charging_fee": 0,
                    "service_fee": 0,
                    "total_fee": 1600
                }
            ],
            "car_list": [
                {
                    "battery_capacity": "string",
                    "request_power": "string",
                    "user_id": "string",
                    "waiting_time": "string"
                },
                {
                    "battery_capacity": "string",
                    "request_power": "string",
                    "user_id": "string",
                    "waiting_time": "string"
                }
            ]
        }
    }
    return jsonify(d1), 200


@app.route('/admin/charge/list', methods=['GET'])
def pile2():
    d1 = {
        "charging_pile_id": 0,
        "charging_type": "快充",
        "status": 2
    }
    data1 = []
    for i in range(6):
        data2 = d1.copy()
        data1.append(d1)
        data2["charging_pile_id"] += 1
        d1 = data2
    dic = {"code": 200, "msg": "修改成功", "data": data1}
    return jsonify(dic), 200


@app.route('/admin/charge/status', methods=['POST'])
def pile3():
    data = request
    print(data)

    dic = {"code": 200, "msg": "修改成功"}
    return jsonify(dic), 200


@app.route('/admin/statistics', methods=['GET'])
def log():
    data = {
        "log": [
            {
                "date": 2621448793.1234567,
                "total_charging_power": 10,
                "total_charging_times": 20,
                "total_charging_duration": 30,
                "charging_fee": 11,
                "service_fee": 12,
                "total_fee": 40
            },
            {
                "date": 1621448793.1234567,
                "total_charging_power": 90,
                "total_charging_times": 80,
                "total_charging_duration": 70,
                "charging_fee": 0,
                "service_fee": 0,
                "total_fee": 60
            }
        ],
        "data_last_day": {
            "total_charging_power": 10000,
            "total_charging_power_change": 0.3,
            "total_charging_times": 4400,
            "total_charging_times_change": -0.2,
            "total_charging_duration": 666660.01,
            "total_charging_duration_change": 0.5,
            "total_fee": 2000000,
            "total_fee_change": -0.8,

            "fast_charging_rate": 0.3,
            "slow_charging_rate": 0.7,

            "charging_pile_rate": [
                {
                    "charging_pile_id": 0,
                    "charging_type": 0,
                    "rate": 0.3
                },
                {
                    "charging_pile_id": 1,
                    "charging_type": 0,
                    "rate": 0.3
                },
                {
                    "charging_pile_id": 2,
                    "charging_type": 1,
                    "rate": 0.4
                }
            ],
        },
        "charging_pile_queue": [
            {
                "charging_pile_id": 1,
                "user_id_1": "♂",
                "user_id_2": "yes_sir"
            },
            {
                "charging_pile_id": 2,
                "user_id_1": "♂",
                "user_id_2": "yes_sir"
            },
            {
                "charging_pile_id": 3,
                "user_id_1": "♂",
                "user_id_2": "yes_sir"
            },
            {
                "charging_pile_id": 4,
                "user_id_1": "♂",
                "user_id_2": "yes_sir"
            },
            {
                "charging_pile_id": 5,
                "user_id_1": "♂",
                "user_id_2": "yes_sir"
            },
            {
                "charging_pile_id": 6,
                "user_id_1": "♂",
                "user_id_2": "yes_sir"
            },
            {
                "charging_pile_id": 7,
                "user_id_1": "♂",
                "user_id_2": "yes_sir"
            },
            {
                "charging_pile_id": 8,
                "user_id_1": "♂",
                "user_id_2": "yes_sir"
            }
        ],
        "waiting_area_queue": [
            "1", "2", "3", "4", "5", "6"
        ]

    }
    dic = {"code": 200, "msg": "1111", "data": data}
    return jsonify(dic), 200


if __name__ == '__main__':
    app.run(debug=True)
