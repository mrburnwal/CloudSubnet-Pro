from flask import Flask, render_template, request, jsonify
from logic.calculator import calculate_cidr_details
from logic.splitter import split_parent_network
from logic.validator import validate_overlapping_subnets
from logic.planner import plan_aws_vpc
from logic.terraform import generate_terraform_code

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/calculate-cidr', methods=['POST'])
def calculate_cidr():
    data = request.json
    cidr = data.get('cidr')
    try:
        result = calculate_cidr_details(cidr)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/split-subnet', methods=['POST'])
def split_subnet():
    data = request.json
    parent = data.get('parent')
    child_mask = data.get('child_mask')
    num_subnets = data.get('num_subnets')
    try:
        result = split_parent_network(parent, child_mask, num_subnets)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/validate-overlap', methods=['POST'])
def validate_overlap():
    data = request.json
    cidrs = data.get('cidrs', [])
    try:
        result = validate_overlapping_subnets(cidrs)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/aws-planner', methods=['POST'])
def aws_planner():
    data = request.json
    parent_cidr = data.get('parent_cidr')
    config = {
        'azs': data.get('azs', 2),
        'public': data.get('public', 1),
        'private': data.get('private', 1),
        'database': data.get('database', 1)
    }
    try:
        result = plan_aws_vpc(parent_cidr, config)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/generate-terraform', methods=['POST'])
def generate_terraform():
    data = request.json
    vpc_config = data.get('vpc_config')
    try:
        result = generate_terraform_code(vpc_config)
        return jsonify({'terraform': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5001)
