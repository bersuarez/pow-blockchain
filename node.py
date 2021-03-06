from flask import Flask,jsonify, request, send_from_directory
from flask_cors import CORS

from wallet import Wallet
from blockchain import Blockchain
#only clients (webpages) running on the same server can acces the server

#create server
app = Flask(__name__)#telling it the context on which to run
CORS(app)

@app.route('/',methods=['GET'])#its and endpoint.. (path, methods which shoul reach that route)
#when i reach a GET requerst reaches just our our IP in port and slash nothin, the funcition should be executed and wrpa the reutn in http response
def get_node_ui():
    return send_from_directory('ui','node.html')

@app.route('/network',methods=['GET'])#its and endpoint.. (path, methods which shoul reach that route)
#when i reach a GET requerst reaches just our our IP in port and slash nothin, the funcition should be executed and wrpa the reutn in http response
def get_network_ui():
    return send_from_directory('ui','network.html')

@app.route('/wallet',methods=['POST'])
def create_keys():
    wallet.create_keys()
    wallet.save_keys()
    if wallet.save_keys():
        global blockchain
        blockchain=Blockchain(wallet.public_key, port)
        response={
            'public_key':wallet.public_key,
            'private_key':wallet.private_key,
            'funds':blockchain.get_balance()
        }
        return jsonify(response),201
    else:
        response={
            'message':'saving the keys failed'
        }
        return jsonify(response),500

@app.route('/wallet',methods=['GET'])
def load_keys():
    if wallet.load_keys():
        global blockchain
        blockchain=Blockchain(wallet.public_key, port)
        response={
            'public_key':wallet.public_key,
            'private_key':wallet.private_key,
            'funds':blockchain.get_balance()
        }
        return jsonify(response),201
    else:
        response={
            'message':'loading the keys failed'
        }
        return jsonify(response),500

@app.route('/balance',methods=['GET'])
def get_balance():
    balance=blockchain.get_balance()
    if balance !=None:
        response={
            'message':'Fetched balance succesful',
            'funds':balance
        }
        return jsonify(response),200
    else: 
        response={
            'message':'Loading balance failes',
            'wallet_set_up':wallet.public_key!=None
        }
        return jsonify(response),500

@app.route('/broadcast-transaction', methods=['POST'])
def broadcast_transaction():
    values = request.get_json()
    if not values:
        response ={'message': 'No data found'}
        return jsonify(response), 400
    required = ['sender', 'recipient','amount','signature'] #require json to contain these fields
    if not all(key in values for key in required):
        response ={'message': 'some data is missing'}
        return jsonify(response), 400
    success = blockchain.add_transaction(values['recipient'],values['sender'], values['signature'], values['amount'], is_receiving=True)
    if success:
        response={
            'message':'succesfully added transacitioon',
            'transaction':{
                'sender':values['sender'],
                'recipient':values['recipient'],
                'amount':values['amount'],
                'signature':values['signature']
            },
        }
        return jsonify(response),201
    else:response={
        'message':'Creating a transaction failed'}
    return jsonify(response),500

@app.route('/broadcast-block', methods=['POST'])
def broadacst_block():
    values = request.get_json()
    if not values:
        response ={'message': 'No data found'}
        return jsonify(response), 400
    if 'block' not in values:
        response ={'message': 'Block is missing'}
        return jsonify(response), 400
    block = values['block']
    if block['index'] == blockchain.chain[-1].index +1: #check if incoming block corresponds to one after the last local's blockchain block
        if blockchain.add_block(block):
            response = {'message': 'Block added'}
            return jsonify(response), 201
        else:
            response = {'message': 'Block seems invalid'}
            return jsonify(response), 409
    elif block['index'] > blockchain.chain[-1].index:
        response = {'message': 'Blockchain seems to differ from local blockchain'} #tell the incoming node that their blockchain is out of date
        blockchain.resolve_conflicts = True
        return jsonify (response), 200 #its error with our blockchain, not theirs
    else: 
        response = {'message': 'Blockchain seems to be shorters, block not added'} #tell the incoming node that their blockchain is out of date
        return jsonify (response), 409



@app.route('/transaction',methods=['POST'])
def add_transaction():
    if wallet.public_key==None:
        response={
            'message':'No wallet setup'
        }
        return jsonify(response),400
    values=request.get_json()
    if not values:
        response={
            'message':'no data found'
        }
        return jsonify(response),400
    required_fields=['recipient','amount']
    if not all(field in values for field in required_fields):
        response={
            'message':'required message missing'
        }
        return jsonify(response),400
    recipient=values['recipient']
    amount=values['amount']
    signature=wallet.sign_transaction(wallet.public_key, recipient,amount)
    success=blockchain.add_transaction(recipient,wallet.public_key,signature,amount)
    if success:
        response={
            'message':'succesfully added transacitioon',
            'transaction':{
                'sender':wallet.public_key,
                'recipient':recipient,
                'amount':amount,
                'signature':signature
            },
            'funds':blockchain.get_balance()
        }
        return jsonify(response),201
    else:response={
        'message':'Creating a transaction failed'}
    return jsonify(response),500

@app.route('/mine',methods=['POST'])
def mine():
    if blockchain.resolve_conflicts:
        response = {'message': 'Resolve conflicts first, block not added'}
        return jsonify(response), 409
    block=blockchain.mine_block()
    if block !=None:
        dict_block=block.__dict__.copy()
        dict_block ['transactions']=[tx.__dict__ for tx in dict_block['transactions']]
        response={
            'message':'Block added succesfully',
            'block':dict_block,
            'funds':blockchain.get_balance()
        }
        return jsonify(response),201
    else:
        response={
            'message':'Ading block failed',
            'wallet_set_up':wallet.public_key!=None
        }
        return jsonify(response),500

@app.route('/resolve-conflicts', methods=['POST'])
def resolve_conflicts():
    replaced = blockchain.resolve()
    if replaced:
        response = {'message': 'Chain was replaced'}
    else:
        response = {'message': 'Local chain kept'}
    return jsonify(response), 200

@app.route('/transactions',methods=['GET'])
def get_open_transaction():
    transactions=blockchain.get_open_transactions()
    dict_transactions=[tx.__dict__ for tx in transactions]
    return jsonify(dict_transactions),200

@app.route('/chain',methods=['GET'])
def get_chain():
    chain_snapshot=blockchain.chain
    dict_chain=[block.__dict__.copy() for block in chain_snapshot]
    for dict_block in dict_chain:
        dict_block['transactions']=[tx.__dict__ for tx in dict_block['transactions']]
    return jsonify(dict_chain),200#http status code(was it was succesful or not)
    
@app.route('/node', methods=['POST'])
def add_node():
    values = request.get_json()
    if not values:
        respose = {
            'message' : 'No data attached'
        }
        return jsonify(response), 400
    if 'node' not in values: #value is dict, "in" checks for existencie of keys
        respose = {
            'message' : 'No node data attached'
        }
        return jsonify(response), 400
    node = values['node']
    blockchain.add_peer_node(node)
    response={
    'message' : 'Node added succesfully',
    'all_nodes': blockchain.get_peer_nodes()
    }
    return jsonify(response), 201

@app.route('/node/<node_url>', methods=['DELETE'])
def remove_node(node_url):
    if node_url == '' or node_url == None:
        response = {
            'message': 'No node found'
        }
        return jsonify(response), 400
    blockchain.remove_peer_node(node_url)
    response = {
        'message': 'Node removed',
        'all_nodes': blockchain.get_peer_nodes()
    }
    return jsonify(response), 200

@app.route('/nodes', methods=['GET'])
def get_nodes():
    nodes = blockchain.get_peer_nodes()
    response = {
        'all_nodes': nodes
    }
    return jsonify(response), 200



if __name__ =='__main__':#only start if directly executing it
#start the server
    app.debug=True
    from argparse import ArgumentParser
    parser= ArgumentParser()
    parser.add_argument('-p', '--port', type=int, default=5000) #allows us to parse arguments we pass along with our Python filename command
    args = parser.parse_args()
    port = args.port
    wallet=Wallet(port)
    blockchain=Blockchain(wallet.public_key, port)
    app.run(host='0.0.0.0',port=port) #IP on which to run and port which we want to lsiten