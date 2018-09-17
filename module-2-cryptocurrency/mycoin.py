#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 17 18:42:26 2018

@author: bhaveshdave
"""
import datetime
import hashlib
import json
import requests

from uuid import uuid4
from urllib.parse import urlparse
from flask import Flask, jsonify, request

# Part 1 - Building a Blockchain
class Blockchain:
    
    def __init__(self):
        self.chain = []
        self.transactions = []
        self.create_block(proof = 1 , previous_hash = "0")
        self.nodes = set()
    
    def create_block(self, proof, previous_hash):
        block = {'index': len(self.chain) + 1,
                 'timestamp': str(datetime.datetime.now()),
                 'proof': proof,
                 'previous_hash': previous_hash,
                 'transactions': self.transactions}
        self.transactions = []
        self.chain.append(block)
        return block
    
    def get_previous_block(self):
        return self.chain[-1]
    
    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        while not check_proof:
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof
    
    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    
    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            previous_block = block
            block_index +=1 
        return True
    
    def add_transaction(self, sender, receiver, amount):
        self.transactions.append({
                'sender': sender,
                'receiver': receiver,
                'amount': amount})
        return self.chain[-1]['index'] + 1
    
    def add_node(self, address):
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)
    
    def replace_chain(self):
        network = self.nodes
        longest_chain = None
        max_length = len(self.chain)
        for node in network:
            response = requests.get('http://{0}{1}'.format(node, '/get_chain'))
            if response.status_code == 200:
                res = json.loads(response)
                length = res['length']
                chain = res['chain']
                if length > max_length and self.is_chain_valid(chain):
                    max_length = length
                    longest_chain = chain
        if longest_chain:
            self.chain = longest_chain
            return True
        return False
            
        
# Part 2 - Mining our Blockchain blocks

# Creating a web app
app = Flask(__name__)

# Creating a blockchain
blockchain = Blockchain()

# Mining a block
@app.route('/mine_block', methods=['GET'])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(proof, previous_hash)
    return jsonify({'message': 'Block mined', 
                       'index': block['index'],
                       'timestamp': block['timestamp'],
                       'proof': block['proof'],
                       'previous_hash': block['previous_hash']}), 200


# Getting full blockchain
@app.route('/get_chain', methods=['GET'])
def get_chain():
    return jsonify({'chain' : blockchain.chain,
                    'length' : len(blockchain.chain)}), 200
            
# Chevk if chain valid
@app.route('/is_valid', methods=['GET'])
def is_valid():
    return jsonify({'valid': blockchain.is_chain_valid(blockchain.chain)}), 200

# Running the app
app.run('0.0.0.0', 5000)

# Part 3 - Decentralizing the Blockchain

