import logging

from flask import Flask, request
from flask import jsonify

from app.error import Error
from calculators.park_calculator import ParkCalculator
from calculators.pay_calculator import PayCalculator
from calculators.pray_calculator import PrayCalculator
from models.user_input import UserInput
from operators.waze_operator import WazeOperator

app = Flask(__name__)

waze_operator = WazeOperator()
pray_calculator = PrayCalculator()
pay_calculator = PayCalculator()
park_calculator = ParkCalculator()

@app.route("/routes_options", methods=["POST"])
def routes_options():
    payload_json = request.get_json()
    user_input = UserInput(
        payload_json["source_lon"],
        payload_json["source_lat"],
        payload_json["target_lon"],
        payload_json["target_lat"]
    )

    try:
        print("user_input={}".format(user_input))
        pray_result = pray_calculator.calculate(user_input)
        pay_result = pay_calculator.calculate(user_input)
        park_result = park_calculator.calculate(user_input)
        return ({
                   'pray_result': pray_result,
                   'pay_result': pay_result,
                   'park_result': park_result,
                },
                200)
    except Error as error:
        logging.exception(error)
        return jsonify(error), error.status_code
    except Exception as error:
        logging.exception(error)
        return {'message': 'Internal Server Error'}, 500


